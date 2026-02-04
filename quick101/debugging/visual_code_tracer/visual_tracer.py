"""
Visual Python Tracer
====================
Just add ONE line - server starts automatically!

    from visual_tracer import trace; trace()
"""

import sys
import os
import time
import json
import queue
import threading
import webbrowser
import subprocess
import atexit
from typing import Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass, asdict

# Shared state
event_queue = queue.Queue()
call_history = []
server_started = False
server_lock = threading.Lock()

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

class Config:
    enabled = False
    depth = 0
    call_stack = []
    call_counter = 0
    max_depth = 30
    max_arg_len = 80
    exclude = {"site-packages", "lib/python", "/usr/lib", "<frozen", 
               "flask", "werkzeug", "visual_tracer", "threading", "queue"}
    include_funcs = None  # If set, only trace these functions (substring match)
    exclude_funcs = None  # If set, skip these functions (substring match)

cfg = Config()

def _fmt_arg(v):
    try:
        s = repr(v)
        return s[:cfg.max_arg_len-3] + "..." if len(s) > cfg.max_arg_len else s
    except:
        return "<?>"

def _fmt_args(frame):
    code = frame.f_code
    names = code.co_varnames[:code.co_argcount + code.co_kwonlyargcount]
    args = []
    for n in names:
        if n in frame.f_locals and n not in ('self', 'cls'):
            args.append(f"{n}={_fmt_arg(frame.f_locals[n])}")
    return ", ".join(args[:4])

def _should_trace(path, func):
    if not path or func.startswith('_'):
        return False
    for p in cfg.exclude:
        if p in path:
            return False
    if not path.endswith('.py'):
        return False
    # Check function name filters
    if cfg.exclude_funcs:
        for pattern in cfg.exclude_funcs:
            if pattern.lower() in func.lower():
                return False
    if cfg.include_funcs:
        for pattern in cfg.include_funcs:
            if pattern.lower() in func.lower():
                return True
        return False  # include_funcs set but no match
    return True

def _trace_fn(frame, event, arg):
    if not cfg.enabled:
        return None
    
    path = frame.f_code.co_filename
    func = frame.f_code.co_name
    line = frame.f_lineno
    
    if not _should_trace(path, func):
        return _trace_fn
    
    if cfg.depth > cfg.max_depth:
        return _trace_fn
    
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    abspath = os.path.abspath(path)
    
    if event == 'call':
        cfg.depth += 1
        cfg.call_counter += 1
        cid = cfg.call_counter
        pid = cfg.call_stack[-1]['cid'] if cfg.call_stack else 0
        
        evt = TraceEvent(
            event_type='call',
            func_name=func,
            filename=os.path.basename(path),
            filepath=abspath,
            lineno=line,
            depth=cfg.depth,
            args=_fmt_args(frame),
            return_value='',
            elapsed_ms=0,
            timestamp=ts,
            call_id=cid,
            parent_id=pid
        )
        
        cfg.call_stack.append({'cid': cid, 'func': func, 'start': time.perf_counter(), 'depth': cfg.depth})
        
        d = asdict(evt)
        event_queue.put(d)
        call_history.append(d)
        
        indent = "  " * (cfg.depth - 1)
        print(f"{ts} {indent}┌─ {func}({evt.args[:50]})")
    
    elif event == 'return':
        if cfg.call_stack and cfg.call_stack[-1]['depth'] == cfg.depth:
            info = cfg.call_stack.pop()
            elapsed = (time.perf_counter() - info['start']) * 1000
            pid = cfg.call_stack[-1]['cid'] if cfg.call_stack else 0
            
            evt = TraceEvent(
                event_type='return',
                func_name=func,
                filename=os.path.basename(path),
                filepath=abspath,
                lineno=line,
                depth=cfg.depth,
                args='',
                return_value=_fmt_arg(arg) if arg is not None else '',
                elapsed_ms=round(elapsed, 2),
                timestamp=ts,
                call_id=info['cid'],
                parent_id=pid
            )
            
            d = asdict(evt)
            event_queue.put(d)
            call_history.append(d)
            
            indent = "  " * (cfg.depth - 1)
            ret = f" → {evt.return_value[:30]}" if evt.return_value and evt.return_value != 'None' else ""
            print(f"{ts} {indent}└─ {func} ✓ {elapsed:.1f}ms{ret}")
        
        cfg.depth = max(0, cfg.depth - 1)
    
    return _trace_fn


# HTML with clean JavaScript (using data attributes instead of inline onclick)
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>Python Tracer</title>
    <style>
        *{box-sizing:border-box;margin:0;padding:0}
        body{font-family:'SF Mono',Consolas,monospace;background:#0d1117;color:#c9d1d9;font-size:13px}
        .layout{display:flex;height:100vh}
        .sidebar{width:240px;background:#161b22;border-right:1px solid #30363d;display:flex;flex-direction:column}
        .sidebar-header{padding:12px;border-bottom:1px solid #30363d;font-weight:bold;color:#58a6ff}
        .search-box{padding:10px;border-bottom:1px solid #30363d;background:#21262d}
        .search-box input{width:100%;padding:8px 12px;background:#0d1117;border:1px solid #30363d;border-radius:4px;color:#c9d1d9;font-size:12px}
        .search-box input::placeholder{color:#6e7681}
        .search-box input:focus{outline:none;border-color:#58a6ff}
        .filter-list{flex:1;overflow-y:auto;padding:8px}
        .filter-item{display:flex;align-items:center;padding:6px 8px;border-radius:4px;cursor:pointer;margin-bottom:2px;font-size:12px}
        .filter-item:hover{background:#21262d}
        .filter-item input{margin-right:8px}
        .filter-item.disabled{opacity:0.4}
        .filter-item .cnt{margin-left:auto;background:#30363d;padding:1px 6px;border-radius:8px;font-size:10px}
        .filter-btns{padding:8px;border-top:1px solid #30363d;display:flex;gap:4px}
        .filter-btns button{flex:1;padding:6px;background:#21262d;border:1px solid #30363d;color:#c9d1d9;border-radius:4px;cursor:pointer}
        .main{flex:1;display:flex;flex-direction:column}
        .header{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:#161b22;border-bottom:1px solid #30363d}
        .header h1{font-size:14px;color:#58a6ff;display:flex;align-items:center;gap:8px}
        .status{width:8px;height:8px;border-radius:50%}
        .status.on{background:#3fb950}.status.off{background:#f85149}
        .stats{display:flex;gap:10px;font-size:11px}
        .stats span{background:#21262d;padding:3px 8px;border-radius:4px}
        .ctrls{display:flex;gap:6px;align-items:center}
        .ctrls select,.ctrls button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 10px;border-radius:4px;cursor:pointer}
        .main-search{flex:1;max-width:300px;margin:0 15px}
        .main-search input{width:100%;padding:6px 12px;background:#0d1117;border:1px solid #30363d;border-radius:4px;color:#c9d1d9;font-size:12px}
        .main-search input::placeholder{color:#6e7681}
        .main-search input:focus{outline:none;border-color:#58a6ff}
        .trace-box{flex:1;overflow:auto;padding:10px}
        .line{display:flex;padding:2px 0}
        .line.hidden{display:none}
        .ts{color:#6e7681;min-width:75px;font-size:10px}
        .ind{color:#30363d;white-space:pre}
        .cm{color:#3fb950;margin-right:4px}.rm{color:#f85149;margin-right:4px}
        .fn{color:#d2a8ff;font-weight:600;cursor:pointer}
        .fn:hover{text-decoration:underline}
        .ar{color:#8b949e}.rv{color:#7ee787;margin-left:4px}
        .el{color:#f0883e;margin-left:4px;font-size:10px}
        .el.slow{color:#f85149}
        .fi{color:#6e7681;font-size:10px;margin-left:6px;cursor:pointer}
        .fi:hover{color:#58a6ff;text-decoration:underline}
        .empty{text-align:center;padding:40px;color:#6e7681}
        .empty code{display:block;background:#21262d;padding:10px;border-radius:4px;margin:10px auto;max-width:350px}
        .modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:100;justify-content:center;align-items:center}
        .modal-bg.show{display:flex}
        .modal{background:#161b22;border:1px solid #30363d;border-radius:6px;width:80%;max-width:900px;max-height:75vh;display:flex;flex-direction:column}
        .modal-hd{display:flex;justify-content:space-between;padding:10px 14px;background:#21262d;border-bottom:1px solid #30363d}
        .modal-hd h3{color:#58a6ff;font-size:12px;font-weight:normal}
        .modal-x{background:none;border:none;color:#8b949e;font-size:16px;cursor:pointer}
        .modal-body{flex:1;overflow:auto;background:#0d1117}
        .code-ln{display:flex;line-height:1.5;padding:0 10px}
        .code-ln.hl{background:#2d4a2d}.code-ln.ctx{background:#1c2128}
        .ln-num{color:#6e7681;min-width:40px;text-align:right;padding-right:10px}
        .ln-txt{white-space:pre}
        .modal-ft{display:flex;gap:6px;padding:10px 14px;background:#21262d;border-top:1px solid #30363d}
        .modal-ft button{padding:6px 12px;border-radius:4px;cursor:pointer;border:none}
        .btn-p{background:#238636;color:white}.btn-s{background:#30363d;color:#c9d1d9}
        .toast{position:fixed;bottom:16px;right:16px;background:#238636;color:white;padding:8px 14px;border-radius:4px;display:none;z-index:200}
        .toast.err{background:#da3633}.toast.show{display:block}
    </style>
</head>
<body>
<div class="layout">
    <div class="sidebar">
        <div class="sidebar-header">Functions</div>
        <div class="search-box"><input type="text" id="search" placeholder="🔍 Search functions..."></div>
        <div class="filter-list" id="flist"></div>
        <div class="filter-btns"><button id="btnAll">All</button><button id="btnNone">None</button></div>
    </div>
    <div class="main">
        <div class="header">
            <h1><span class="status" id="st"></span>Tracer</h1>
            <div class="stats"><span>Calls: <b id="nc">0</b></span><span>Visible: <b id="nv">0</b></span></div>
            <div class="main-search"><input type="text" id="mainSearch" placeholder="🔍 Filter trace..."></div>
            <div class="ctrls">
                <select id="ed"><option value="vscode">VS Code</option><option value="cursor">Cursor</option><option value="pycharm">PyCharm</option></select>
                <button id="btnClr">Clear</button>
            </div>
        </div>
        <div class="trace-box" id="traceBox">
            <div class="empty" id="empty"><h3>Waiting...</h3><code>from visual_tracer import trace; trace()</code></div>
        </div>
    </div>
</div>
<div class="modal-bg" id="mbg"><div class="modal"><div class="modal-hd"><h3 id="mt">Code</h3><button class="modal-x" id="mclose">x</button></div><div class="modal-body" id="mb"></div><div class="modal-ft"><button class="btn-p" id="obtn">Open</button><button class="btn-s" id="cbtn">Close</button></div></div></div>
<div class="toast" id="toast"></div>
<script>
var evts=[], nc=0, funcs={}, hidden={}, calls={};
var traceBox=document.getElementById('traceBox');
var flist=document.getElementById('flist');
var empty=document.getElementById('empty');
var mbg=document.getElementById('mbg');
var searchBox=document.getElementById('search');
var mainSearchBox=document.getElementById('mainSearch');
var curFile='', curLine=0, searchTerm='';

var sse=new EventSource('/stream');
sse.onopen=function(){document.getElementById('st').className='status on';};
sse.onerror=function(){document.getElementById('st').className='status off';};
sse.onmessage=function(e){handle(JSON.parse(e.data));};

function handle(e){
    evts.push(e);
    empty.style.display='none';
    if(e.event_type==='call'){
        nc++;
        calls[e.call_id]=e;
        if(!funcs[e.func_name]){funcs[e.func_name]={c:0};updFlist();}
        funcs[e.func_name].c++;
    }else{
        if(calls[e.call_id])calls[e.call_id].ret=e;
    }
    document.getElementById('nc').textContent=nc;
    render(e);
    updVis();
    updCnts();
}

function render(e){
    var d=document.createElement('div');
    d.className='line';
    d.setAttribute('data-cid',e.call_id);
    d.setAttribute('data-fn',e.func_name);
    d.setAttribute('data-pid',e.parent_id||0);
    d.setAttribute('data-fp',e.filepath);
    d.setAttribute('data-ln',e.lineno);
    if(isHid(e))d.className+=' hidden';
    
    var ind='';for(var i=1;i<e.depth;i++)ind+='|  ';
    var h='<span class="ts">'+e.timestamp+'</span><span class="ind">'+ind+'</span>';
    h+='<span class="'+(e.event_type==='call'?'cm':'rm')+'">+-</span>';
    h+='<span class="fn">'+esc(e.func_name)+'</span>';
    
    if(e.event_type==='call'){
        h+='<span class="ar">('+esc(e.args||'')+')</span>';
    }else{
        h+='<span class="ar">ok</span>';
        if(e.elapsed_ms>0)h+='<span class="el'+(e.elapsed_ms>100?' slow':'')+'">'+e.elapsed_ms+'ms</span>';
        if(e.return_value&&e.return_value!=='None')h+='<span class="rv">-&gt;'+esc(e.return_value.substr(0,40))+'</span>';
    }
    h+='<span class="fi">'+esc(e.filename)+':'+e.lineno+'</span>';
    d.innerHTML=h;
    traceBox.appendChild(d);
    d.scrollIntoView({behavior:'smooth',block:'end'});
}

function isHid(e){
    // Search filter - hide if doesn't match search term
    if(searchTerm && e.func_name.toLowerCase().indexOf(searchTerm)===-1) return true;
    // Manual filter - hide if unchecked
    if(hidden[e.func_name])return true;
    // Parent filter - hide if parent is hidden
    var p=e.parent_id;
    while(p){var x=calls[p];if(x&&hidden[x.func_name])return true;p=x?x.parent_id:0;}
    return false;
}

function updFlist(){
    flist.innerHTML='';
    var arr=[];for(var n in funcs)arr.push([n,funcs[n].c]);
    arr.sort(function(a,b){return b[1]-a[1];});
    for(var i=0;i<arr.length;i++){
        var n=arr[i][0],c=arr[i][1],h=hidden[n];
        // Skip if doesn't match search
        if(searchTerm && n.toLowerCase().indexOf(searchTerm)===-1) continue;
        var d=document.createElement('div');
        d.className='filter-item'+(h?' disabled':'');
        d.innerHTML='<input type="checkbox" data-fn="'+esc(n)+'"'+(h?'':' checked')+'><span>'+esc(n)+'</span><span class="cnt" data-f="'+esc(n)+'">'+c+'</span>';
        flist.appendChild(d);
    }
}

function updCnts(){for(var n in funcs){var e=document.querySelector('.cnt[data-f="'+n+'"]');if(e)e.textContent=funcs[n].c;}}

function applyF(){
    var lines=document.querySelectorAll('.line');
    for(var i=0;i<lines.length;i++){
        var l=lines[i];
        var e={func_name:l.getAttribute('data-fn'),parent_id:parseInt(l.getAttribute('data-pid'))||0};
        if(isHid(e))l.className='line hidden';else l.className='line';
    }
    updVis();
}

function updVis(){document.getElementById('nv').textContent=document.querySelectorAll('.line:not(.hidden)').length;}

function showC(fp,ln,fn){
    curFile=fp;curLine=ln;
    document.getElementById('mt').textContent=fn+' - '+fp.split('/').pop()+':'+ln;
    document.getElementById('mb').innerHTML='<div style="padding:15px">Loading...</div>';
    mbg.className='modal-bg show';
    fetch('/source?file='+encodeURIComponent(fp)+'&line='+ln)
        .then(function(r){return r.json();})
        .then(function(d){
            if(d.error){document.getElementById('mb').innerHTML='<div style="padding:15px;color:#f85149">'+d.error+'</div>';return;}
            var h='';
            for(var i=0;i<d.lines.length;i++){
                var l=d.lines[i];
                var cls=l.number===ln?'hl':(Math.abs(l.number-ln)<=3?'ctx':'');
                h+='<div class="code-ln '+cls+'"><span class="ln-num">'+l.number+'</span><span class="ln-txt">'+esc(l.content)+'</span></div>';
            }
            document.getElementById('mb').innerHTML=h;
            setTimeout(function(){var x=document.querySelector('.hl');if(x)x.scrollIntoView({block:'center'});},50);
        });
}

function openE(fp,ln){
    var ed=document.getElementById('ed').value;
    fetch('/open',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filepath:fp,lineno:ln,editor:ed})})
        .then(function(r){return r.json();})
        .then(function(d){showT(d.status==='ok'?'Opened':'Failed',d.status!=='ok');});
}

function showT(m,err){var t=document.getElementById('toast');t.textContent=m;t.className='toast show'+(err?' err':'');setTimeout(function(){t.className='toast';},2000);}

function esc(t){var d=document.createElement('div');d.textContent=t||'';return d.innerHTML;}

// Event listeners
document.addEventListener('click',function(e){
    var t=e.target;
    if(t.classList.contains('fn')){
        var line=t.closest('.line');
        showC(line.getAttribute('data-fp'),parseInt(line.getAttribute('data-ln')),line.getAttribute('data-fn'));
    }
    if(t.classList.contains('fi')){
        var line=t.closest('.line');
        openE(line.getAttribute('data-fp'),parseInt(line.getAttribute('data-ln')));
    }
    if(t.type==='checkbox'&&t.hasAttribute('data-fn')){
        var fn=t.getAttribute('data-fn');
        if(t.checked)delete hidden[fn];else hidden[fn]=true;
        applyF();updFlist();
    }
});

document.getElementById('btnAll').onclick=function(){hidden={};applyF();updFlist();};
document.getElementById('btnNone').onclick=function(){for(var n in funcs)hidden[n]=true;applyF();updFlist();};
searchBox.oninput=function(){searchTerm=this.value.toLowerCase();mainSearchBox.value=this.value;applyF();updFlist();};
mainSearchBox.oninput=function(){searchTerm=this.value.toLowerCase();searchBox.value=this.value;applyF();updFlist();};
document.getElementById('btnClr').onclick=function(){
    evts=[];nc=0;funcs={};hidden={};calls={};searchTerm='';
    searchBox.value='';mainSearchBox.value='';
    traceBox.querySelectorAll('.line').forEach(function(e){e.remove();});
    flist.innerHTML='';
    document.getElementById('nc').textContent='0';
    document.getElementById('nv').textContent='0';
    empty.style.display='block';
    fetch('/clear',{method:'POST'});
};
document.getElementById('mclose').onclick=function(){mbg.className='modal-bg';};
document.getElementById('cbtn').onclick=function(){mbg.className='modal-bg';};
document.getElementById('obtn').onclick=function(){openE(curFile,curLine);};
mbg.onclick=function(e){if(e.target===mbg)mbg.className='modal-bg';};
document.addEventListener('keydown',function(e){if(e.key==='Escape')mbg.className='modal-bg';});

// Load existing events
console.log('Loading events...');
fetch('/events')
    .then(function(r){return r.json();})
    .then(function(es){
        console.log('Got',es.length,'events');
        for(var i=0;i<es.length;i++)handle(es[i]);
    });
</script>
</body>
</html>"""


def _create_app():
    from flask import Flask, Response, jsonify, request
    
    app = Flask(__name__)
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    
    @app.route('/')
    def index():
        return HTML_PAGE
    
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
    def clear_events():
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
        }
        
        try:
            subprocess.Popen(cmds.get(editor, cmds['vscode']), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return jsonify({"status": "ok"})
        except:
            return jsonify({"status": "error", "error": f"{editor} not found"})
    
    return app


def _start_server(port=5050):
    global server_started
    with server_lock:
        if server_started:
            return
        server_started = True
    
    app = _create_app()
    def run():
        app.run(host='127.0.0.1', port=port, threaded=True, debug=False, use_reloader=False)
    
    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(0.8)


def _on_exit():
    stop_trace()
    if server_started and call_history:
        print(f"\n{'='*50}")
        print(f"🔍 Script done. Server running at http://localhost:5050")
        print(f"   Press Ctrl+C to exit")
        print(f"{'='*50}\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Bye")


def trace(port=5050, open_browser=True, keep_alive=True, include=None, exclude=None):
    """
    Start tracing. Just add: from visual_tracer import trace; trace()
    
    Args:
        port: Server port (default 5050)
        open_browser: Auto-open browser (default True)
        keep_alive: Keep server running after script ends (default True)
        include: Only trace functions matching these patterns (list of strings)
        exclude: Skip functions matching these patterns (list of strings)
    
    Examples:
        trace()                              # Trace all functions
        trace(include=['process', 'fetch'])  # Only trace functions containing 'process' or 'fetch'
        trace(exclude=['helper', 'util'])    # Skip functions containing 'helper' or 'util'
    """
    _start_server(port)
    
    cfg.enabled = True
    cfg.depth = 0
    cfg.call_stack = []
    cfg.call_counter = 0
    cfg.include_funcs = include
    cfg.exclude_funcs = exclude
    
    sys.setprofile(_trace_fn)
    
    if keep_alive:
        atexit.register(_on_exit)
    
    print(f"\n{'='*50}")
    print(f"🔍 TRACER ACTIVE - http://localhost:{port}")
    print(f"{'='*50}\n")
    
    if open_browser:
        try:
            webbrowser.open(f'http://localhost:{port}')
        except:
            pass


def stop_trace():
    sys.setprofile(None)
    cfg.enabled = False


if __name__ == '__main__':
    print("Start server: python visual_tracer.py")
    print("Then add to your code: from visual_tracer import trace; trace()")
    app = _create_app()
    app.run(host='0.0.0.0', port=5050, threaded=True)
