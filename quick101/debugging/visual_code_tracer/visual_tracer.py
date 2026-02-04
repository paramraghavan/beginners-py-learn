"""
Visual Python Tracer (with Code Navigation + Filtering)
========================================================
Real-time visualization with:
- Click to open in editor (VS Code, PyCharm, Sublime, Cursor)
- Filter functions (deselect parent = hide children too)
- Code preview modal

USAGE:
    1. Start server:  python visual_tracer.py
    2. Open browser:  http://localhost:5050
    3. Add to code:   from visual_tracer import trace; trace()
    4. Run your code and watch!
"""

import sys
import os
import time
import json
import queue
import threading
import subprocess
from typing import Optional, Set, Callable, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from flask import Flask, render_template_string, Response, jsonify, request

# ============================================================================
# EVENT QUEUE
# ============================================================================

event_queue = queue.Queue()
call_history = []
source_cache = {}

# ============================================================================
# TRACER CONFIG
# ============================================================================

@dataclass
class TraceEvent:
    event_type: str
    func_name: str
    filename: str
    filepath: str
    lineno: int
    depth: int
    args: str
    return_value: str
    elapsed_ms: float
    timestamp: str
    call_id: int
    parent_id: int


class TracerConfig:
    enabled: bool = False
    depth: int = 0
    call_stack: list = None
    call_counter: int = 0
    exclude_patterns: Set[str] = {"site-packages", "lib/python", "/usr/lib", "<frozen", "<string>", "flask", "werkzeug", "visual_tracer"}
    max_depth: int = 30
    max_arg_length: int = 100

config = TracerConfig()
config.call_stack = []

# ============================================================================
# TRACE FUNCTION
# ============================================================================

def _format_arg(value: Any) -> str:
    try:
        s = repr(value)
        if len(s) > config.max_arg_length:
            s = s[:config.max_arg_length - 3] + "..."
        return s
    except:
        return "<?>"


def _format_args(frame) -> str:
    code = frame.f_code
    arg_count = code.co_argcount + code.co_kwonlyargcount
    arg_names = code.co_varnames[:arg_count]
    local_vars = frame.f_locals
    
    args = []
    for name in arg_names:
        if name in local_vars and name not in ('self', 'cls'):
            value = _format_arg(local_vars[name])
            args.append(f"{name}={value}")
    
    return ", ".join(args[:5])


def _should_trace(filename: str, func_name: str) -> bool:
    if not filename or func_name.startswith('_'):
        return False
    for pattern in config.exclude_patterns:
        if pattern in filename:
            return False
    return filename.endswith('.py')


def _trace_calls(frame, event: str, arg: Any) -> Optional[Callable]:
    if not config.enabled:
        return None
    
    filepath = frame.f_code.co_filename
    filename = os.path.basename(filepath)
    func_name = frame.f_code.co_name
    lineno = frame.f_lineno
    
    if not _should_trace(filepath, func_name):
        return _trace_calls
    
    if config.depth > config.max_depth:
        return _trace_calls
    
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    abs_filepath = os.path.abspath(filepath)
    
    if event == 'call':
        config.depth += 1
        config.call_counter += 1
        call_id = config.call_counter
        parent_id = config.call_stack[-1]['call_id'] if config.call_stack else 0
        
        args_str = _format_args(frame)
        
        evt = TraceEvent(
            event_type='call',
            func_name=func_name,
            filename=filename,
            filepath=abs_filepath,
            lineno=lineno,
            depth=config.depth,
            args=args_str,
            return_value='',
            elapsed_ms=0,
            timestamp=timestamp,
            call_id=call_id,
            parent_id=parent_id
        )
        
        config.call_stack.append({
            'call_id': call_id,
            'name': func_name,
            'start': time.perf_counter(),
            'depth': config.depth
        })
        
        event_queue.put(asdict(evt))
        call_history.append(asdict(evt))
    
    elif event == 'return':
        if config.call_stack and config.call_stack[-1]['depth'] == config.depth:
            call_info = config.call_stack.pop()
            elapsed = (time.perf_counter() - call_info['start']) * 1000
            parent_id = config.call_stack[-1]['call_id'] if config.call_stack else 0
            ret_str = _format_arg(arg) if arg is not None else ''
            
            evt = TraceEvent(
                event_type='return',
                func_name=func_name,
                filename=filename,
                filepath=abs_filepath,
                lineno=lineno,
                depth=config.depth,
                args='',
                return_value=ret_str,
                elapsed_ms=round(elapsed, 2),
                timestamp=timestamp,
                call_id=call_info['call_id'],
                parent_id=parent_id
            )
            
            event_queue.put(asdict(evt))
            call_history.append(asdict(evt))
        
        config.depth = max(0, config.depth - 1)
    
    return _trace_calls


# ============================================================================
# PUBLIC API
# ============================================================================

def trace():
    """Start tracing - add this ONE line at top of your script"""
    config.enabled = True
    config.depth = 0
    config.call_stack = []
    sys.setprofile(_trace_calls)
    print("🔍 Visual Tracer ENABLED - View at http://localhost:5050")


def stop_trace():
    sys.setprofile(None)
    config.enabled = False


# ============================================================================
# FLASK SERVER
# ============================================================================

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Python Visual Tracer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'SF Mono', 'Consolas', monospace;
            background: #0d1117;
            color: #c9d1d9;
            font-size: 13px;
        }
        
        .layout { display: flex; height: 100vh; }
        
        /* Sidebar */
        .sidebar {
            width: 260px;
            background: #161b22;
            border-right: 1px solid #30363d;
            display: flex;
            flex-direction: column;
        }
        
        .sidebar-header {
            padding: 15px;
            border-bottom: 1px solid #30363d;
            font-weight: bold;
            color: #58a6ff;
        }
        
        .filter-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }
        
        .filter-item {
            display: flex;
            align-items: center;
            padding: 8px 10px;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 4px;
        }
        
        .filter-item:hover { background: #21262d; }
        .filter-item input { margin-right: 10px; cursor: pointer; }
        .filter-item.disabled { opacity: 0.4; }
        
        .filter-item .fname {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .filter-item .count {
            margin-left: auto;
            background: #30363d;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
        }
        
        .filter-actions {
            padding: 10px;
            border-top: 1px solid #30363d;
        }
        
        .filter-actions button {
            width: 48%;
            padding: 8px;
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
        }
        
        .filter-actions button:hover { background: #30363d; }
        
        /* Main */
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background: #161b22;
            border-bottom: 1px solid #30363d;
        }
        
        .header h1 {
            font-size: 15px;
            color: #58a6ff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status { width: 8px; height: 8px; border-radius: 50%; }
        .status.connected { background: #3fb950; }
        .status.disconnected { background: #f85149; }
        
        .controls { display: flex; gap: 8px; align-items: center; }
        
        .controls select, .controls button {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            font-size: 11px;
        }
        
        .stats { display: flex; gap: 12px; font-size: 11px; color: #8b949e; }
        .stats span { background: #21262d; padding: 3px 8px; border-radius: 4px; }
        
        /* Trace */
        .trace-container { flex: 1; overflow: auto; padding: 12px; }
        
        .trace-line {
            display: flex;
            align-items: flex-start;
            padding: 2px 0;
            animation: fadeIn 0.15s ease;
        }
        
        .trace-line.hidden { display: none; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateX(-5px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .timestamp { color: #6e7681; min-width: 80px; font-size: 10px; }
        .indent { color: #30363d; white-space: pre; }
        .call-marker { color: #3fb950; margin-right: 5px; }
        .return-marker { color: #f85149; margin-right: 5px; }
        
        .func-name {
            color: #d2a8ff;
            font-weight: 600;
            cursor: pointer;
        }
        .func-name:hover { text-decoration: underline; }
        
        .args { color: #8b949e; }
        .return-value { color: #7ee787; margin-left: 5px; }
        .elapsed { color: #f0883e; margin-left: 5px; font-size: 10px; }
        .elapsed.slow { color: #f85149; font-weight: bold; }
        
        .file-info {
            color: #6e7681;
            font-size: 10px;
            margin-left: 8px;
            cursor: pointer;
        }
        .file-info:hover { color: #58a6ff; text-decoration: underline; }
        
        .empty-state { text-align: center; padding: 50px; color: #6e7681; }
        .empty-state code {
            display: block;
            background: #21262d;
            padding: 12px;
            border-radius: 6px;
            margin: 15px auto;
            max-width: 420px;
            text-align: left;
            font-size: 12px;
        }
        
        /* Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.85);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal-overlay.active { display: flex; }
        
        .modal {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            width: 85%;
            max-width: 950px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 16px;
            background: #21262d;
            border-bottom: 1px solid #30363d;
        }
        
        .modal-header h3 { color: #58a6ff; font-size: 12px; font-weight: normal; }
        
        .modal-close {
            background: none;
            border: none;
            color: #8b949e;
            font-size: 18px;
            cursor: pointer;
        }
        
        .modal-body { flex: 1; overflow: auto; background: #0d1117; }
        
        .code-line { display: flex; line-height: 1.6; padding: 0 12px; }
        .code-line.highlight { background: #2d4a2d; }
        .code-line.context { background: #1c2128; }
        
        .line-number {
            color: #6e7681;
            min-width: 45px;
            text-align: right;
            padding-right: 12px;
            user-select: none;
        }
        .line-content { white-space: pre; }
        
        .modal-actions {
            display: flex;
            gap: 8px;
            padding: 10px 16px;
            background: #21262d;
            border-top: 1px solid #30363d;
        }
        
        .modal-actions button {
            padding: 6px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            border: none;
        }
        .btn-primary { background: #238636; color: white; }
        .btn-primary:hover { background: #2ea043; }
        .btn-secondary { background: #30363d; color: #c9d1d9; }
        
        /* Toast */
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #238636;
            color: white;
            padding: 10px 16px;
            border-radius: 6px;
            display: none;
            z-index: 1001;
            font-size: 12px;
        }
        .toast.error { background: #da3633; }
        .toast.active { display: block; }
    </style>
</head>
<body>
    <div class="layout">
        <div class="sidebar">
            <div class="sidebar-header">📋 Function Filter</div>
            <div class="filter-list" id="filterList"></div>
            <div class="filter-actions">
                <button onclick="selectAll()">✓ All</button>
                <button onclick="deselectAll()">✗ None</button>
            </div>
        </div>
        
        <div class="main">
            <div class="header">
                <h1><span class="status" id="status"></span>🔍 Visual Tracer</h1>
                <div class="stats">
                    <span>Calls: <b id="callCount">0</b></span>
                    <span>Visible: <b id="visibleCount">0</b></span>
                    <span>Time: <b id="totalTime">0ms</b></span>
                </div>
                <div class="controls">
                    <select id="editorSelect">
                        <option value="vscode">VS Code</option>
                        <option value="cursor">Cursor</option>
                        <option value="pycharm">PyCharm</option>
                        <option value="sublime">Sublime</option>
                    </select>
                    <button onclick="clearTrace()">Clear</button>
                    <button onclick="exportTrace()">Export</button>
                </div>
            </div>
            
            <div class="trace-container">
                <div class="empty-state" id="emptyState">
                    <h2>Waiting for events...</h2>
                    <code>from visual_tracer import trace; trace()</code>
                    <p>💡 Click function → preview code | Click file:line → open editor</p>
                </div>
                <div id="traceView"></div>
            </div>
        </div>
    </div>
    
    <div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 id="modalTitle">Code Preview</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalBody"></div>
            <div class="modal-actions">
                <button class="btn-primary" id="openBtn">Open in Editor</button>
                <button class="btn-secondary" onclick="closeModal()">Close</button>
            </div>
        </div>
    </div>
    
    <div class="toast" id="toast"></div>

    <script>
        let events = [];
        let callCount = 0;
        let totalTime = 0;
        let funcStats = new Map();
        let hiddenFuncs = new Set();
        let callMap = new Map();
        
        const traceView = document.getElementById('traceView');
        const filterList = document.getElementById('filterList');
        const emptyState = document.getElementById('emptyState');
        const statusEl = document.getElementById('status');
        const modal = document.getElementById('modalOverlay');
        
        // SSE
        const sse = new EventSource('/stream');
        sse.onopen = () => statusEl.className = 'status connected';
        sse.onerror = () => statusEl.className = 'status disconnected';
        sse.onmessage = e => handleEvent(JSON.parse(e.data));
        
        function handleEvent(evt) {
            events.push(evt);
            emptyState.style.display = 'none';
            
            if (evt.event_type === 'call') {
                callCount++;
                callMap.set(evt.call_id, evt);
                
                if (!funcStats.has(evt.func_name)) {
                    funcStats.set(evt.func_name, { count: 0 });
                    updateFilterList();
                }
                funcStats.get(evt.func_name).count++;
            } else {
                totalTime += evt.elapsed_ms;
                const call = callMap.get(evt.call_id);
                if (call) call.returnEvt = evt;
            }
            
            document.getElementById('callCount').textContent = callCount;
            document.getElementById('totalTime').textContent = totalTime.toFixed(1) + 'ms';
            
            renderEvent(evt);
            updateVisibleCount();
            updateFilterCounts();
        }
        
        function renderEvent(evt) {
            const div = document.createElement('div');
            div.className = 'trace-line';
            div.dataset.callId = evt.call_id;
            div.dataset.func = evt.func_name;
            div.dataset.parent = evt.parent_id || 0;
            
            if (isHidden(evt)) div.classList.add('hidden');
            
            const indent = '│  '.repeat(Math.max(0, evt.depth - 1));
            const marker = evt.event_type === 'call' ? '┌─' : '└─';
            const mClass = evt.event_type === 'call' ? 'call-marker' : 'return-marker';
            
            let html = `<span class="timestamp">${evt.timestamp}</span>
                <span class="indent">${indent}</span>
                <span class="${mClass}">${marker}</span>
                <span class="func-name" onclick="showCode('${esc(evt.filepath)}',${evt.lineno},'${evt.func_name}')">${evt.func_name}</span>`;
            
            if (evt.event_type === 'call') {
                html += `<span class="args">(${esc(evt.args||'')})</span>`;
            } else {
                html += `<span class="args">✓</span>`;
                if (evt.elapsed_ms > 0) {
                    html += `<span class="elapsed${evt.elapsed_ms > 100 ? ' slow' : ''}">${evt.elapsed_ms}ms</span>`;
                }
                if (evt.return_value && evt.return_value !== 'None') {
                    html += `<span class="return-value">→ ${esc(evt.return_value)}</span>`;
                }
            }
            
            html += `<span class="file-info" onclick="openEditor('${esc(evt.filepath)}',${evt.lineno})">${evt.filename}:${evt.lineno}</span>`;
            
            div.innerHTML = html;
            traceView.appendChild(div);
            div.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
        
        function isHidden(evt) {
            if (hiddenFuncs.has(evt.func_name)) return true;
            let pid = evt.parent_id;
            while (pid) {
                const p = callMap.get(pid);
                if (p && hiddenFuncs.has(p.func_name)) return true;
                pid = p ? p.parent_id : 0;
            }
            return false;
        }
        
        function updateFilterList() {
            filterList.innerHTML = '';
            const sorted = [...funcStats.entries()].sort((a,b) => b[1].count - a[1].count);
            
            for (const [name, s] of sorted) {
                const hidden = hiddenFuncs.has(name);
                const div = document.createElement('div');
                div.className = 'filter-item' + (hidden ? ' disabled' : '');
                div.innerHTML = `<input type="checkbox" ${hidden ? '' : 'checked'} onchange="toggleFunc('${name}',this.checked)">
                    <span class="fname">${name}</span>
                    <span class="count" data-func="${name}">${s.count}</span>`;
                filterList.appendChild(div);
            }
        }
        
        function updateFilterCounts() {
            funcStats.forEach((s, name) => {
                const el = document.querySelector(`.count[data-func="${name}"]`);
                if (el) el.textContent = s.count;
            });
        }
        
        function toggleFunc(name, visible) {
            if (visible) hiddenFuncs.delete(name);
            else hiddenFuncs.add(name);
            applyFilters();
            updateFilterList();
        }
        
        function applyFilters() {
            document.querySelectorAll('.trace-line').forEach(line => {
                const id = parseInt(line.dataset.callId);
                const evt = callMap.get(id) || { func_name: line.dataset.func, parent_id: parseInt(line.dataset.parent) };
                line.classList.toggle('hidden', isHidden(evt));
            });
            updateVisibleCount();
        }
        
        function updateVisibleCount() {
            const v = document.querySelectorAll('.trace-line:not(.hidden)').length;
            document.getElementById('visibleCount').textContent = v;
        }
        
        function selectAll() { hiddenFuncs.clear(); applyFilters(); updateFilterList(); }
        function deselectAll() { funcStats.forEach((_,n) => hiddenFuncs.add(n)); applyFilters(); updateFilterList(); }
        
        // Code preview
        async function showCode(path, line, func) {
            document.getElementById('modalTitle').textContent = `${func} — ${path.split('/').pop()}:${line}`;
            document.getElementById('modalBody').innerHTML = '<div style="padding:20px;color:#8b949e">Loading...</div>';
            modal.classList.add('active');
            
            try {
                const r = await fetch(`/source?file=${encodeURIComponent(path)}&line=${line}`);
                const d = await r.json();
                
                if (d.error) {
                    document.getElementById('modalBody').innerHTML = `<div style="padding:20px;color:#f85149">${d.error}</div>`;
                    return;
                }
                
                let html = '';
                d.lines.forEach(l => {
                    const cls = l.number === line ? 'highlight' : (Math.abs(l.number - line) <= 3 ? 'context' : '');
                    html += `<div class="code-line ${cls}"><span class="line-number">${l.number}</span><span class="line-content">${esc(l.content)}</span></div>`;
                });
                document.getElementById('modalBody').innerHTML = html;
                
                setTimeout(() => {
                    const h = document.querySelector('.highlight');
                    if (h) h.scrollIntoView({ block: 'center' });
                }, 50);
            } catch(e) {
                document.getElementById('modalBody').innerHTML = '<div style="padding:20px;color:#f85149">Failed to load</div>';
            }
            
            document.getElementById('openBtn').onclick = () => openEditor(path, line);
        }
        
        function closeModal(e) {
            if (!e || e.target === modal) modal.classList.remove('active');
        }
        
        async function openEditor(path, line) {
            const editor = document.getElementById('editorSelect').value;
            try {
                const r = await fetch('/open', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filepath: path, lineno: line, editor })
                });
                const d = await r.json();
                toast(d.status === 'ok' ? `Opened in ${editor}` : (d.error || 'Failed'), d.status !== 'ok');
            } catch(e) {
                toast('Failed to open', true);
            }
        }
        
        function toast(msg, err=false) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.className = 'toast active' + (err ? ' error' : '');
            setTimeout(() => t.classList.remove('active'), 2500);
        }
        
        function clearTrace() {
            events = []; callCount = 0; totalTime = 0;
            funcStats.clear(); hiddenFuncs.clear(); callMap.clear();
            traceView.innerHTML = ''; filterList.innerHTML = '';
            document.getElementById('callCount').textContent = '0';
            document.getElementById('visibleCount').textContent = '0';
            document.getElementById('totalTime').textContent = '0ms';
            emptyState.style.display = 'block';
            fetch('/clear', { method: 'POST' });
        }
        
        function exportTrace() {
            const a = document.createElement('a');
            a.href = URL.createObjectURL(new Blob([JSON.stringify(events, null, 2)]));
            a.download = 'trace_' + new Date().toISOString().slice(0,19).replace(/:/g,'-') + '.json';
            a.click();
        }
        
        function esc(t) {
            const d = document.createElement('div');
            d.textContent = t;
            return d.innerHTML;
        }
        
        fetch('/events').then(r => r.json()).then(evts => evts.forEach(handleEvent));
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/stream')
def stream():
    def gen():
        while True:
            try:
                evt = event_queue.get(timeout=1)
                yield f"data: {json.dumps(evt)}\n\n"
            except queue.Empty:
                yield ": keepalive\n\n"
    return Response(gen(), mimetype='text/event-stream')


@app.route('/events')
def get_events():
    return jsonify(call_history)


@app.route('/clear', methods=['POST'])
def clear():
    global call_history
    call_history = []
    return jsonify({"status": "ok"})


@app.route('/source')
def get_source():
    filepath = request.args.get('file')
    lineno = int(request.args.get('line', 1))
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File not found"})
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        start = max(0, lineno - 15)
        end = min(len(lines), lineno + 15)
        
        result = [{"number": i+1, "content": lines[i].rstrip('\n')} for i in range(start, end)]
        return jsonify({"lines": result})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/open', methods=['POST'])
def open_editor():
    data = request.json
    filepath = data.get('filepath')
    lineno = data.get('lineno', 1)
    editor = data.get('editor', 'vscode')
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"status": "error", "error": "File not found"})
    
    cmds = {
        'vscode': ['code', '--goto', f'{filepath}:{lineno}'],
        'cursor': ['cursor', '--goto', f'{filepath}:{lineno}'],
        'pycharm': ['pycharm', '--line', str(lineno), filepath],
        'sublime': ['subl', f'{filepath}:{lineno}'],
    }
    
    try:
        subprocess.Popen(cmds.get(editor, cmds['vscode']), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"status": "ok"})
    except FileNotFoundError:
        return jsonify({"status": "error", "error": f"{editor} not found"})


def run_server(port=5050):
    print(f"\n🌐 Visual Tracer: http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False, use_reloader=False)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, default=5050)
    run_server(port=p.parse_args().port)
