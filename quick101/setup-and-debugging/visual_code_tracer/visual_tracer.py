"""
Visual Python Tracer - Enhanced Edition
========================================
Just add ONE line - server starts automatically!

    from visual_tracer import trace; trace()

New Features:
- Filter by module path (e.g., prepay.utils, myapp.services)
- Filter by file path patterns
- Show full module paths
- Min duration filter (only show slow calls)
- Exception tracking
- Pause/resume tracing
- Project root detection ("only my code" mode)
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
import traceback
import fnmatch
from typing import Optional, Callable, Any, List, Set
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

# Shared state
event_queue = queue.Queue()
call_history = []
server_started = False
server_lock = threading.Lock()

@dataclass 
class TraceEvent:
    event_type: str
    func_name: str
    module_path: str  # Full module path like "prepay.utils"
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
    exception: str = ""  # Exception info if call raised
    is_user_code: bool = True  # True if in project, False if third-party

class Config:
    enabled = False
    paused = False  # Pause without stopping
    depth = 0
    call_stack = []
    call_counter = 0
    max_depth = 30
    max_arg_len = 100
    min_duration_ms = 0  # Only record calls taking longer than this
    
    # Paths to always exclude (standard library, site-packages, etc.)
    exclude_paths = {
        "site-packages", "lib/python", "/usr/lib", "<frozen", 
        "flask", "werkzeug", "visual_tracer", "threading", "queue",
        "importlib", "encodings", "_bootstrap"
    }
    
    # Module-based filtering (the main new feature!)
    include_modules: Optional[List[str]] = None  # e.g., ["prepay.utils", "prepay.api"]
    exclude_modules: Optional[List[str]] = None  # e.g., ["prepay.tests"]
    
    # File path pattern filtering
    include_paths: Optional[List[str]] = None  # e.g., ["*/myproject/*"]
    exclude_paths_custom: Optional[List[str]] = None  # e.g., ["*/tests/*"]
    
    # Function name filtering (existing)
    include_funcs: Optional[List[str]] = None
    exclude_funcs: Optional[List[str]] = None
    
    # Project root for "only my code" detection
    project_root: Optional[str] = None
    only_user_code: bool = False
    
    # Track exceptions
    track_exceptions: bool = True

cfg = Config()


def _detect_project_root() -> Optional[str]:
    """Try to detect project root by looking for common markers."""
    markers = ['setup.py', 'pyproject.toml', 'setup.cfg', '.git', 'requirements.txt']
    
    # Start from the caller's directory
    frame = sys._getframe(2)
    start_path = Path(frame.f_code.co_filename).parent.absolute()
    
    current = start_path
    for _ in range(10):  # Don't go more than 10 levels up
        for marker in markers:
            if (current / marker).exists():
                return str(current)
        parent = current.parent
        if parent == current:
            break
        current = parent
    
    return str(start_path)


def _filepath_to_module(filepath: str) -> str:
    """Convert a file path to a module path like 'prepay.utils'."""
    if not filepath or not filepath.endswith('.py'):
        return ''
    
    path = Path(filepath).absolute()
    
    # Try to find the module relative to sys.path
    for sp in sys.path:
        if not sp:
            continue
        try:
            sp_path = Path(sp).absolute()
            if path.is_relative_to(sp_path):
                rel_path = path.relative_to(sp_path)
                # Convert path to module: prepay/utils.py -> prepay.utils
                parts = list(rel_path.parts)
                if parts[-1].endswith('.py'):
                    parts[-1] = parts[-1][:-3]
                if parts[-1] == '__init__':
                    parts = parts[:-1]
                if parts:
                    return '.'.join(parts)
        except (ValueError, TypeError):
            continue
    
    # Fallback: try relative to project root
    if cfg.project_root:
        try:
            root_path = Path(cfg.project_root).absolute()
            if path.is_relative_to(root_path):
                rel_path = path.relative_to(root_path)
                parts = list(rel_path.parts)
                if parts[-1].endswith('.py'):
                    parts[-1] = parts[-1][:-3]
                if parts[-1] == '__init__':
                    parts = parts[:-1]
                if parts:
                    return '.'.join(parts)
        except (ValueError, TypeError):
            pass
    
    # Last resort: just use filename without .py
    return path.stem


def _is_user_code(filepath: str) -> bool:
    """Check if filepath is user code (not third-party)."""
    if not filepath:
        return False
    
    # Check common third-party locations
    third_party_markers = ['site-packages', 'dist-packages', '/lib/python', 'lib64/python']
    for marker in third_party_markers:
        if marker in filepath:
            return False
    
    # If project root is set, check if file is inside it
    if cfg.project_root:
        try:
            path = Path(filepath).absolute()
            root = Path(cfg.project_root).absolute()
            return path.is_relative_to(root)
        except (ValueError, TypeError):
            return True
    
    return True


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
    return ", ".join(args[:5])


def _match_pattern(value: str, patterns: List[str]) -> bool:
    """Check if value matches any of the patterns (supports wildcards)."""
    value_lower = value.lower()
    for pattern in patterns:
        pattern_lower = pattern.lower()
        # Support both substring match and glob patterns
        if '*' in pattern_lower or '?' in pattern_lower:
            if fnmatch.fnmatch(value_lower, pattern_lower):
                return True
        else:
            if pattern_lower in value_lower:
                return True
    return False


def _should_trace(path: str, func: str, module: str) -> bool:
    """Determine if this call should be traced based on all filters."""
    if not path:
        return False
    
    # Skip private/dunder methods (but allow __init__)
    if func.startswith('_') and not func == '__init__':
        return False
    
    # Check built-in exclusions
    for p in cfg.exclude_paths:
        if p in path:
            return False
    
    if not path.endswith('.py'):
        return False
    
    # Check "only user code" mode
    is_user = _is_user_code(path)
    if cfg.only_user_code and not is_user:
        return False
    
    # Check module filters (THE KEY NEW FEATURE)
    if cfg.exclude_modules and module:
        if _match_pattern(module, cfg.exclude_modules):
            return False
    
    if cfg.include_modules and module:
        if not _match_pattern(module, cfg.include_modules):
            return False
    
    # Check path pattern filters
    if cfg.exclude_paths_custom:
        if _match_pattern(path, cfg.exclude_paths_custom):
            return False
    
    if cfg.include_paths:
        if not _match_pattern(path, cfg.include_paths):
            return False
    
    # Check function name filters
    if cfg.exclude_funcs:
        if _match_pattern(func, cfg.exclude_funcs):
            return False
    
    if cfg.include_funcs:
        if not _match_pattern(func, cfg.include_funcs):
            return False
    
    return True


def _trace_fn(frame, event, arg):
    if not cfg.enabled or cfg.paused:
        return _trace_fn if cfg.enabled else None
    
    path = frame.f_code.co_filename
    func = frame.f_code.co_name
    line = frame.f_lineno
    module = _filepath_to_module(path)
    
    if not _should_trace(path, func, module):
        return _trace_fn
    
    if cfg.depth > cfg.max_depth:
        return _trace_fn
    
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    abspath = os.path.abspath(path)
    is_user = _is_user_code(path)
    
    if event == 'call':
        cfg.depth += 1
        cfg.call_counter += 1
        cid = cfg.call_counter
        pid = cfg.call_stack[-1]['cid'] if cfg.call_stack else 0
        
        evt = TraceEvent(
            event_type='call',
            func_name=func,
            module_path=module,
            filename=os.path.basename(path),
            filepath=abspath,
            lineno=line,
            depth=cfg.depth,
            args=_fmt_args(frame),
            return_value='',
            elapsed_ms=0,
            timestamp=ts,
            call_id=cid,
            parent_id=pid,
            is_user_code=is_user
        )
        
        cfg.call_stack.append({
            'cid': cid, 
            'func': func, 
            'module': module,
            'start': time.perf_counter(), 
            'depth': cfg.depth
        })
        
        d = asdict(evt)
        event_queue.put(d)
        call_history.append(d)
        
        indent = "  " * (cfg.depth - 1)
        mod_str = f"[{module}] " if module else ""
        print(f"{ts} {indent}┌─ {mod_str}{func}({evt.args[:50]})")
    
    elif event == 'return':
        if cfg.call_stack and cfg.call_stack[-1]['depth'] == cfg.depth:
            info = cfg.call_stack.pop()
            elapsed = (time.perf_counter() - info['start']) * 1000
            pid = cfg.call_stack[-1]['cid'] if cfg.call_stack else 0
            
            # Check min duration filter
            if cfg.min_duration_ms > 0 and elapsed < cfg.min_duration_ms:
                cfg.depth = max(0, cfg.depth - 1)
                return _trace_fn
            
            evt = TraceEvent(
                event_type='return',
                func_name=func,
                module_path=module,
                filename=os.path.basename(path),
                filepath=abspath,
                lineno=line,
                depth=cfg.depth,
                args='',
                return_value=_fmt_arg(arg) if arg is not None else '',
                elapsed_ms=round(elapsed, 2),
                timestamp=ts,
                call_id=info['cid'],
                parent_id=pid,
                is_user_code=is_user
            )
            
            d = asdict(evt)
            event_queue.put(d)
            call_history.append(d)
            
            indent = "  " * (cfg.depth - 1)
            ret = f" → {evt.return_value[:30]}" if evt.return_value and evt.return_value != 'None' else ""
            print(f"{ts} {indent}└─ {func} ✓ {elapsed:.1f}ms{ret}")
        
        cfg.depth = max(0, cfg.depth - 1)
    
    elif event == 'exception' and cfg.track_exceptions:
        exc_type, exc_value, exc_tb = arg
        if cfg.call_stack:
            info = cfg.call_stack[-1]
            evt = TraceEvent(
                event_type='exception',
                func_name=func,
                module_path=module,
                filename=os.path.basename(path),
                filepath=abspath,
                lineno=line,
                depth=cfg.depth,
                args='',
                return_value='',
                elapsed_ms=0,
                timestamp=ts,
                call_id=info['cid'],
                parent_id=cfg.call_stack[-2]['cid'] if len(cfg.call_stack) > 1 else 0,
                exception=f"{exc_type.__name__}: {exc_value}",
                is_user_code=is_user
            )
            
            d = asdict(evt)
            event_queue.put(d)
            call_history.append(d)
            
            indent = "  " * (cfg.depth - 1)
            print(f"{ts} {indent}❌ {func} raised {exc_type.__name__}: {exc_value}")
    
    return _trace_fn


HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>Python Tracer</title>
    <style>
        *{box-sizing:border-box;margin:0;padding:0}
        body{font-family:'SF Mono',Consolas,monospace;background:#0d1117;color:#c9d1d9;font-size:13px}
        .layout{display:flex;height:100vh}
        .sidebar{width:280px;background:#161b22;border-right:1px solid #30363d;display:flex;flex-direction:column}
        .sidebar-header{padding:12px;border-bottom:1px solid #30363d;font-weight:bold;color:#58a6ff;display:flex;justify-content:space-between;align-items:center}
        .sidebar-tabs{display:flex;border-bottom:1px solid #30363d}
        .sidebar-tab{flex:1;padding:8px;text-align:center;cursor:pointer;font-size:11px;border-bottom:2px solid transparent}
        .sidebar-tab:hover{background:#21262d}
        .sidebar-tab.active{border-bottom-color:#58a6ff;color:#58a6ff}
        .search-box{padding:10px;border-bottom:1px solid #30363d;background:#21262d}
        .search-box input{width:100%;padding:8px 12px;background:#0d1117;border:1px solid #30363d;border-radius:4px;color:#c9d1d9;font-size:12px}
        .search-box input::placeholder{color:#6e7681}
        .search-box input:focus{outline:none;border-color:#58a6ff}
        .filter-list{flex:1;overflow-y:auto;padding:8px}
        .filter-item{display:flex;align-items:center;padding:6px 8px;border-radius:4px;cursor:pointer;margin-bottom:2px;font-size:12px}
        .filter-item:hover{background:#21262d}
        .filter-item input{margin-right:8px;flex-shrink:0}
        .filter-item.disabled{opacity:0.4}
        .filter-item .cnt{margin-left:auto;background:#30363d;padding:1px 6px;border-radius:8px;font-size:10px;flex-shrink:0}
        .filter-item .name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}
        .filter-item.third-party .name{color:#8b949e}
        .module-group{margin-bottom:8px}
        .module-header{display:flex;align-items:center;padding:6px 8px;background:#21262d;border-radius:4px;cursor:pointer;font-size:11px;color:#7ee787}
        .module-header:hover{background:#30363d}
        .module-header .arrow{margin-right:6px;transition:transform 0.2s}
        .module-header.collapsed .arrow{transform:rotate(-90deg)}
        .module-header .mod-cnt{margin-left:auto;color:#6e7681}
        .module-children{padding-left:12px}
        .module-children.hidden{display:none}
        .filter-btns{padding:8px;border-top:1px solid #30363d;display:flex;gap:4px;flex-wrap:wrap}
        .filter-btns button{flex:1;padding:6px;background:#21262d;border:1px solid #30363d;color:#c9d1d9;border-radius:4px;cursor:pointer;font-size:11px;min-width:60px}
        .filter-btns button:hover{background:#30363d}
        .filter-btns button.active{background:#238636;border-color:#238636}
        .main{flex:1;display:flex;flex-direction:column;min-width:0}
        .header{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;gap:8px}
        .header h1{font-size:14px;color:#58a6ff;display:flex;align-items:center;gap:8px}
        .status{width:8px;height:8px;border-radius:50%}
        .status.on{background:#3fb950}.status.off{background:#f85149}.status.paused{background:#d29922}.status.config{background:#a371f7}
        .stats{display:flex;gap:10px;font-size:11px}
        .stats span{background:#21262d;padding:3px 8px;border-radius:4px}
        .ctrls{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
        .ctrls select,.ctrls button,.ctrls input{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px}
        .ctrls input[type="number"]{width:70px}
        .ctrls button.active{background:#238636;border-color:#238636}
        .ctrls button.config-btn{background:#a371f7;border-color:#a371f7}
        .main-search{flex:1;max-width:300px}
        .main-search input{width:100%;padding:6px 12px;background:#0d1117;border:1px solid #30363d;border-radius:4px;color:#c9d1d9;font-size:12px}
        .main-search input::placeholder{color:#6e7681}
        .main-search input:focus{outline:none;border-color:#58a6ff}
        .trace-box{flex:1;overflow:auto;padding:10px}
        .line{display:flex;padding:2px 0;align-items:flex-start}
        .line.hidden{display:none}
        .line.third-party{opacity:0.6}
        .line.exception{background:#3d1f1f}
        .ts{color:#6e7681;min-width:75px;font-size:10px;flex-shrink:0}
        .ind{color:#30363d;white-space:pre}
        .cm{color:#3fb950;margin-right:4px}.rm{color:#f85149;margin-right:4px}.em{color:#f0883e;margin-right:4px}
        .fn{color:#d2a8ff;font-weight:600;cursor:pointer}
        .fn:hover{text-decoration:underline}
        .mod{color:#7ee787;font-size:10px;margin-right:4px}
        .ar{color:#8b949e}.rv{color:#7ee787;margin-left:4px}
        .el{color:#f0883e;margin-left:4px;font-size:10px}
        .el.slow{color:#f85149;font-weight:bold}
        .el.very-slow{color:#f85149;font-weight:bold;background:#3d1f1f;padding:0 4px;border-radius:2px}
        .fi{color:#6e7681;font-size:10px;margin-left:6px;cursor:pointer;flex-shrink:0}
        .fi:hover{color:#58a6ff;text-decoration:underline}
        .exc{color:#f85149;margin-left:4px;font-size:11px}
        .empty{text-align:center;padding:40px;color:#6e7681}
        .empty code{display:block;background:#21262d;padding:10px;border-radius:4px;margin:10px auto;max-width:400px;font-size:11px}
        .modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:100;justify-content:center;align-items:center}
        .modal-bg.show{display:flex}
        .modal{background:#161b22;border:1px solid #30363d;border-radius:6px;width:85%;max-width:1000px;max-height:80vh;display:flex;flex-direction:column}
        .modal-hd{display:flex;justify-content:space-between;padding:10px 14px;background:#21262d;border-bottom:1px solid #30363d}
        .modal-hd h3{color:#58a6ff;font-size:12px;font-weight:normal}
        .modal-x{background:none;border:none;color:#8b949e;font-size:16px;cursor:pointer}
        .modal-body{flex:1;overflow:auto;background:#0d1117}
        .code-ln{display:flex;line-height:1.5;padding:0 10px}
        .code-ln.hl{background:#2d4a2d}.code-ln.ctx{background:#1c2128}.code-ln.exc{background:#3d1f1f}
        .ln-num{color:#6e7681;min-width:50px;text-align:right;padding-right:10px;user-select:none}
        .ln-txt{white-space:pre;overflow-x:auto}
        .modal-ft{display:flex;gap:6px;padding:10px 14px;background:#21262d;border-top:1px solid #30363d}
        .modal-ft button{padding:6px 12px;border-radius:4px;cursor:pointer;border:none}
        .btn-p{background:#238636;color:white}.btn-s{background:#30363d;color:#c9d1d9}.btn-start{background:#238636;color:white;font-size:14px;padding:10px 24px}
        .toast{position:fixed;bottom:16px;right:16px;background:#238636;color:white;padding:8px 14px;border-radius:4px;display:none;z-index:200}
        .toast.err{background:#da3633}.toast.show{display:block}
        .help-tip{font-size:10px;color:#6e7681;padding:8px;border-top:1px solid #30363d;line-height:1.4}
        .help-tip code{background:#21262d;padding:1px 4px;border-radius:2px}
        
        /* Config Panel Styles */
        .config-panel{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:150;justify-content:center;align-items:center}
        .config-panel.show{display:flex}
        .config-box{background:#161b22;border:1px solid #30363d;border-radius:8px;width:90%;max-width:600px;max-height:90vh;overflow:auto}
        .config-header{padding:16px 20px;background:#21262d;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;align-items:center}
        .config-header h2{color:#58a6ff;font-size:16px;font-weight:600;display:flex;align-items:center;gap:8px}
        .config-body{padding:20px}
        .config-section{margin-bottom:20px}
        .config-section h3{color:#c9d1d9;font-size:13px;margin-bottom:10px;display:flex;align-items:center;gap:6px}
        .config-section h3 .hint{color:#6e7681;font-weight:normal;font-size:11px}
        .config-row{display:flex;align-items:center;gap:12px;margin-bottom:12px}
        .config-row label{color:#8b949e;font-size:12px;min-width:120px}
        .config-row input[type="text"],.config-row input[type="number"],.config-row textarea{flex:1;padding:8px 12px;background:#0d1117;border:1px solid #30363d;border-radius:4px;color:#c9d1d9;font-size:12px;font-family:inherit}
        .config-row input:focus,.config-row textarea:focus{outline:none;border-color:#58a6ff}
        .config-row textarea{min-height:60px;resize:vertical}
        .config-row input[type="checkbox"]{width:18px;height:18px}
        .config-row .checkbox-label{display:flex;align-items:center;gap:8px;cursor:pointer}
        .config-row .input-hint{color:#6e7681;font-size:10px;margin-top:4px}
        .config-footer{padding:16px 20px;background:#21262d;border-top:1px solid #30363d;display:flex;justify-content:space-between;align-items:center}
        .config-footer .status-text{color:#6e7681;font-size:11px}
        .config-footer .status-text.running{color:#3fb950}
        .config-footer .status-text.stopped{color:#f85149}
        .config-actions{display:flex;gap:8px}
        .tag-input{display:flex;flex-wrap:wrap;gap:6px;padding:8px;background:#0d1117;border:1px solid #30363d;border-radius:4px;min-height:40px;cursor:text}
        .tag-input:focus-within{border-color:#58a6ff}
        .tag-input .tag{background:#238636;color:white;padding:2px 8px;border-radius:3px;font-size:11px;display:flex;align-items:center;gap:4px}
        .tag-input .tag.exclude{background:#da3633}
        .tag-input .tag .remove{cursor:pointer;opacity:0.7}
        .tag-input .tag .remove:hover{opacity:1}
        .tag-input input{border:none;background:none;color:#c9d1d9;font-size:12px;flex:1;min-width:100px;outline:none}
        .tag-input input::placeholder{color:#6e7681}
        .preset-btns{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
        .preset-btns button{padding:4px 10px;background:#21262d;border:1px solid #30363d;color:#c9d1d9;border-radius:4px;cursor:pointer;font-size:11px}
        .preset-btns button:hover{background:#30363d}
        .config-divider{height:1px;background:#30363d;margin:16px 0}
        .current-config{background:#0d1117;border:1px solid #30363d;border-radius:4px;padding:12px;margin-top:12px}
        .current-config h4{color:#7ee787;font-size:11px;margin-bottom:8px}
        .current-config pre{color:#8b949e;font-size:10px;white-space:pre-wrap;word-break:break-all}
    </style>
</head>
<body>
<div class="layout">
    <div class="sidebar">
        <div class="sidebar-header">
            <span>Filters</span>
            <span style="font-size:10px;color:#6e7681" id="filterMode">by module</span>
        </div>
        <div class="sidebar-tabs">
            <div class="sidebar-tab active" data-view="modules">Modules</div>
            <div class="sidebar-tab" data-view="functions">Functions</div>
        </div>
        <div class="search-box"><input type="text" id="search" placeholder="🔍 Filter (e.g. prepay.utils, process*)"></div>
        <div class="filter-list" id="flist"></div>
        <div class="filter-btns">
            <button id="btnAll">All</button>
            <button id="btnNone">None</button>
            <button id="btnUser" title="Only show your code">My Code</button>
        </div>
        <div class="help-tip">
            Filter examples:<br>
            <code>prepay.*</code> - all prepay modules<br>
            <code>*.utils</code> - all utils modules<br>
            <code>process</code> - functions containing "process"
        </div>
    </div>
    <div class="main">
        <div class="header">
            <h1><span class="status" id="st"></span>Tracer</h1>
            <div class="stats">
                <span>Calls: <b id="nc">0</b></span>
                <span>Visible: <b id="nv">0</b></span>
                <span>Modules: <b id="nm">0</b></span>
            </div>
            <div class="main-search"><input type="text" id="mainSearch" placeholder="🔍 Search trace..."></div>
            <div class="ctrls">
                <label style="font-size:11px">Min ms:</label>
                <input type="number" id="minMs" value="0" min="0" step="10" title="Only show calls slower than this">
                <select id="ed"><option value="vscode">VS Code</option><option value="cursor">Cursor</option><option value="pycharm">PyCharm</option><option value="sublime">Sublime</option></select>
                <button id="btnConfig" class="config-btn" title="Configure tracer">⚙️ Config</button>
                <button id="btnPause">⏸ Pause</button>
                <button id="btnClr">🗑 Clear</button>
            </div>
        </div>
        <div class="trace-box" id="traceBox">
            <div class="empty" id="empty">
                <h3>Waiting for traces...</h3>
                <p style="margin:10px 0">Click <b>⚙️ Config</b> to set up filters, then run your code with:</p>
                <code>from visual_tracer import trace; trace()</code>
            </div>
        </div>
    </div>
</div>

<!-- Config Panel -->
<div class="config-panel" id="configPanel">
    <div class="config-box">
        <div class="config-header">
            <h2>⚙️ Tracer Configuration</h2>
            <button class="modal-x" id="configClose">×</button>
        </div>
        <div class="config-body">
            <div class="config-section">
                <h3>📦 Module Filters <span class="hint">(wildcards supported: myapp.*, *.utils)</span></h3>
                <div class="config-row">
                    <label>Include modules:</label>
                    <div style="flex:1">
                        <div class="tag-input" id="includeModulesInput">
                            <input type="text" placeholder="Type module and press Enter...">
                        </div>
                        <div class="preset-btns">
                            <button data-preset="include" data-value="myapp.*">myapp.*</button>
                            <button data-preset="include" data-value="src.*">src.*</button>
                            <button data-preset="include" data-value="app.*">app.*</button>
                        </div>
                    </div>
                </div>
                <div class="config-row">
                    <label>Exclude modules:</label>
                    <div style="flex:1">
                        <div class="tag-input" id="excludeModulesInput">
                            <input type="text" placeholder="Type module and press Enter...">
                        </div>
                        <div class="preset-btns">
                            <button data-preset="exclude" data-value="*.tests">*.tests</button>
                            <button data-preset="exclude" data-value="*.test_*">*.test_*</button>
                            <button data-preset="exclude" data-value="*.migrations">*.migrations</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="config-divider"></div>
            
            <div class="config-section">
                <h3>🎯 Quick Settings</h3>
                <div class="config-row">
                    <label class="checkbox-label">
                        <input type="checkbox" id="cfgOnlyUserCode">
                        <span>Only my code</span>
                    </label>
                    <span class="hint" style="margin-left:auto">Skip third-party libraries (site-packages)</span>
                </div>
                <div class="config-row">
                    <label class="checkbox-label">
                        <input type="checkbox" id="cfgTrackExceptions" checked>
                        <span>Track exceptions</span>
                    </label>
                    <span class="hint" style="margin-left:auto">Show when functions raise errors</span>
                </div>
            </div>
            
            <div class="config-divider"></div>
            
            <div class="config-section">
                <h3>⏱️ Performance Filters</h3>
                <div class="config-row">
                    <label>Min duration (ms):</label>
                    <input type="number" id="cfgMinDuration" value="0" min="0" step="10" style="width:100px">
                    <span class="hint">Only trace calls slower than this</span>
                </div>
                <div class="config-row">
                    <label>Max depth:</label>
                    <input type="number" id="cfgMaxDepth" value="30" min="1" max="100" style="width:100px">
                    <span class="hint">Maximum call stack depth to trace</span>
                </div>
            </div>
            
            <div class="config-divider"></div>
            
            <div class="config-section">
                <h3>📝 Function Filters <span class="hint">(filter by function name)</span></h3>
                <div class="config-row">
                    <label>Include functions:</label>
                    <div style="flex:1">
                        <div class="tag-input" id="includeFuncsInput">
                            <input type="text" placeholder="e.g. process, fetch, handle...">
                        </div>
                    </div>
                </div>
                <div class="config-row">
                    <label>Exclude functions:</label>
                    <div style="flex:1">
                        <div class="tag-input" id="excludeFuncsInput">
                            <input type="text" placeholder="e.g. helper, util, _internal...">
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="current-config">
                <h4>Current Server Configuration</h4>
                <pre id="currentConfigPre">Loading...</pre>
            </div>
        </div>
        <div class="config-footer">
            <span class="status-text" id="configStatus">Tracer not started</span>
            <div class="config-actions">
                <button class="btn-s" id="btnResetConfig">Reset</button>
                <button class="btn-p" id="btnApplyConfig">Apply & Start Tracing</button>
            </div>
        </div>
    </div>
</div>

<div class="modal-bg" id="mbg">
    <div class="modal">
        <div class="modal-hd"><h3 id="mt">Code</h3><button class="modal-x" id="mclose">×</button></div>
        <div class="modal-body" id="mb"></div>
        <div class="modal-ft">
            <button class="btn-p" id="obtn">Open in Editor</button>
            <button class="btn-s" id="cbtn">Close</button>
        </div>
    </div>
</div>
<div class="toast" id="toast"></div>
<script>
var evts=[], nc=0, funcs={}, modules={}, hidden={}, hiddenMods={}, calls={};
var traceBox=document.getElementById('traceBox');
var flist=document.getElementById('flist');
var empty=document.getElementById('empty');
var mbg=document.getElementById('mbg');
var searchBox=document.getElementById('search');
var mainSearchBox=document.getElementById('mainSearch');
var minMsInput=document.getElementById('minMs');
var curFile='', curLine=0, searchTerm='', minMs=0;
var viewMode='modules'; // 'modules' or 'functions'
var onlyUserCode=false;
var isPaused=false;

var sse=new EventSource('/stream');
sse.onopen=function(){document.getElementById('st').className='status on';};
sse.onerror=function(){document.getElementById('st').className='status off';};
sse.onmessage=function(e){if(!isPaused)handle(JSON.parse(e.data));};

function handle(e){
    evts.push(e);
    empty.style.display='none';
    
    // Track by module
    var mod=e.module_path||'(unknown)';
    if(!modules[mod]){modules[mod]={c:0,funcs:{},isUser:e.is_user_code};updFlist();}
    
    if(e.event_type==='call'){
        nc++;
        calls[e.call_id]=e;
        modules[mod].c++;
        if(!modules[mod].funcs[e.func_name])modules[mod].funcs[e.func_name]=0;
        modules[mod].funcs[e.func_name]++;
        if(!funcs[e.func_name]){funcs[e.func_name]={c:0,mod:mod};}
        funcs[e.func_name].c++;
    }else if(e.event_type==='return'){
        if(calls[e.call_id])calls[e.call_id].ret=e;
    }else if(e.event_type==='exception'){
        if(calls[e.call_id])calls[e.call_id].exc=e;
    }
    
    document.getElementById('nc').textContent=nc;
    document.getElementById('nm').textContent=Object.keys(modules).length;
    render(e);
    updVis();
    updCnts();
}

function render(e){
    // Check min duration filter for return events
    if(e.event_type==='return' && minMs>0 && e.elapsed_ms<minMs)return;
    
    var d=document.createElement('div');
    d.className='line';
    if(e.event_type==='exception')d.className+=' exception';
    if(!e.is_user_code)d.className+=' third-party';
    d.setAttribute('data-cid',e.call_id);
    d.setAttribute('data-fn',e.func_name);
    d.setAttribute('data-mod',e.module_path||'');
    d.setAttribute('data-pid',e.parent_id||0);
    d.setAttribute('data-fp',e.filepath);
    d.setAttribute('data-ln',e.lineno);
    d.setAttribute('data-user',e.is_user_code?'1':'0');
    d.setAttribute('data-ms',e.elapsed_ms||0);
    if(isHid(e))d.className+=' hidden';
    
    var ind='';for(var i=1;i<e.depth;i++)ind+='│  ';
    var h='<span class="ts">'+e.timestamp+'</span><span class="ind">'+ind+'</span>';
    
    if(e.event_type==='call'){
        h+='<span class="cm">┌─</span>';
    }else if(e.event_type==='return'){
        h+='<span class="rm">└─</span>';
    }else{
        h+='<span class="em">⚠─</span>';
    }
    
    // Show module path
    if(e.module_path){
        h+='<span class="mod">['+esc(e.module_path)+']</span>';
    }
    
    h+='<span class="fn">'+esc(e.func_name)+'</span>';
    
    if(e.event_type==='call'){
        h+='<span class="ar">('+esc(e.args||'')+')</span>';
    }else if(e.event_type==='return'){
        h+='<span class="ar">✓</span>';
        if(e.elapsed_ms>0){
            var cls='el';
            if(e.elapsed_ms>500)cls+=' very-slow';
            else if(e.elapsed_ms>100)cls+=' slow';
            h+='<span class="'+cls+'">'+e.elapsed_ms.toFixed(1)+'ms</span>';
        }
        if(e.return_value&&e.return_value!=='None')h+='<span class="rv">→ '+esc(e.return_value.substr(0,50))+'</span>';
    }else if(e.event_type==='exception'){
        h+='<span class="exc">❌ '+esc(e.exception)+'</span>';
    }
    
    h+='<span class="fi">'+esc(e.filename)+':'+e.lineno+'</span>';
    d.innerHTML=h;
    traceBox.appendChild(d);
    d.scrollIntoView({behavior:'smooth',block:'end'});
}

function isHid(e){
    // Min duration filter
    if(minMs>0 && e.event_type==='return' && e.elapsed_ms<minMs)return true;
    // Search filter
    var searchTarget=(e.module_path||'')+'.'+e.func_name;
    if(searchTerm && !matchPattern(searchTarget,searchTerm) && !matchPattern(e.func_name,searchTerm))return true;
    // User code filter
    if(onlyUserCode && !e.is_user_code)return true;
    // Module filter
    if(hiddenMods[e.module_path])return true;
    // Function filter
    if(hidden[e.func_name])return true;
    // Parent filter
    var p=e.parent_id;
    while(p){var x=calls[p];if(!x)break;if(hiddenMods[x.module_path]||hidden[x.func_name])return true;p=x.parent_id;}
    return false;
}

function matchPattern(str,pattern){
    if(!str)return false;
    str=str.toLowerCase();
    pattern=pattern.toLowerCase();
    if(pattern.indexOf('*')===-1)return str.indexOf(pattern)!==-1;
    // Convert glob to regex
    var regex=pattern.replace(/[.+^${}()|[\\]\\\\]/g,'\\\\$&').replace(/\\*/g,'.*').replace(/\\?/g,'.');
    try{return new RegExp('^'+regex+'$').test(str);}catch(e){return str.indexOf(pattern.replace(/\\*/g,''))!==-1;}
}

function updFlist(){
    flist.innerHTML='';
    if(viewMode==='modules'){
        // Group by module
        var arr=[];
        for(var m in modules)arr.push([m,modules[m]]);
        arr.sort(function(a,b){return b[1].c-a[1].c;});
        
        for(var i=0;i<arr.length;i++){
            var mod=arr[i][0],info=arr[i][1];
            if(searchTerm && !matchPattern(mod,searchTerm))continue;
            if(onlyUserCode && !info.isUser)continue;
            
            var isHiddenMod=hiddenMods[mod];
            var g=document.createElement('div');
            g.className='module-group';
            
            var hdr=document.createElement('div');
            hdr.className='module-header'+(isHiddenMod?' collapsed':'');
            hdr.setAttribute('data-mod',mod);
            hdr.innerHTML='<span class="arrow">▼</span><input type="checkbox" data-mod-check="'+esc(mod)+'"'+(isHiddenMod?'':' checked')+' onclick="event.stopPropagation()"><span class="name" title="'+esc(mod)+'">'+esc(mod)+'</span><span class="mod-cnt">'+info.c+'</span>';
            g.appendChild(hdr);
            
            var children=document.createElement('div');
            children.className='module-children'+(isHiddenMod?' hidden':'');
            
            var funcsArr=[];
            for(var fn in info.funcs)funcsArr.push([fn,info.funcs[fn]]);
            funcsArr.sort(function(a,b){return b[1]-a[1];});
            
            for(var j=0;j<funcsArr.length;j++){
                var fn=funcsArr[j][0],cnt=funcsArr[j][1];
                var isHiddenFn=hidden[fn];
                var item=document.createElement('div');
                item.className='filter-item'+(isHiddenFn?' disabled':'')+(info.isUser?'':' third-party');
                item.innerHTML='<input type="checkbox" data-fn="'+esc(fn)+'"'+(isHiddenFn?'':' checked')+'><span class="name" title="'+esc(fn)+'">'+esc(fn)+'</span><span class="cnt">'+cnt+'</span>';
                children.appendChild(item);
            }
            g.appendChild(children);
            flist.appendChild(g);
        }
    }else{
        // Flat function list
        var arr=[];for(var n in funcs)arr.push([n,funcs[n].c,funcs[n].mod]);
        arr.sort(function(a,b){return b[1]-a[1];});
        for(var i=0;i<arr.length;i++){
            var n=arr[i][0],c=arr[i][1],mod=arr[i][2];
            if(searchTerm && !matchPattern(n,searchTerm) && !matchPattern(mod+'.'+n,searchTerm))continue;
            var h=hidden[n];
            var d=document.createElement('div');
            d.className='filter-item'+(h?' disabled':'');
            d.innerHTML='<input type="checkbox" data-fn="'+esc(n)+'"'+(h?'':' checked')+'><span class="name" title="'+esc(mod)+'.'+esc(n)+'">'+esc(n)+'</span><span class="cnt">'+c+'</span>';
            flist.appendChild(d);
        }
    }
}

function updCnts(){
    // Update counts in sidebar
    document.querySelectorAll('.mod-cnt').forEach(function(el){
        var mod=el.parentElement.getAttribute('data-mod');
        if(modules[mod])el.textContent=modules[mod].c;
    });
}

function applyF(){
    var lines=document.querySelectorAll('.line');
    for(var i=0;i<lines.length;i++){
        var l=lines[i];
        var e={
            func_name:l.getAttribute('data-fn'),
            module_path:l.getAttribute('data-mod'),
            parent_id:parseInt(l.getAttribute('data-pid'))||0,
            is_user_code:l.getAttribute('data-user')==='1',
            elapsed_ms:parseFloat(l.getAttribute('data-ms'))||0,
            event_type:l.classList.contains('exception')?'exception':(l.querySelector('.cm')?'call':'return')
        };
        l.className='line'+(e.event_type==='exception'?' exception':'')+(e.is_user_code?'':' third-party')+(isHid(e)?' hidden':'');
    }
    updVis();
}

function updVis(){document.getElementById('nv').textContent=document.querySelectorAll('.line:not(.hidden)').length;}

function showC(fp,ln,fn,mod){
    curFile=fp;curLine=ln;
    var title=mod?mod+'.'+fn:fn;
    document.getElementById('mt').textContent=title+' — '+fp.split('/').pop()+':'+ln;
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
        .then(function(d){showT(d.status==='ok'?'Opened in '+ed:'Failed: '+(d.error||'unknown'),d.status!=='ok');});
}

function showT(m,err){var t=document.getElementById('toast');t.textContent=m;t.className='toast show'+(err?' err':'');setTimeout(function(){t.className='toast';},2000);}

function esc(t){var d=document.createElement('div');d.textContent=t||'';return d.innerHTML;}

// Event listeners
document.addEventListener('click',function(e){
    var t=e.target;
    
    // Function name click -> show code
    if(t.classList.contains('fn')){
        var line=t.closest('.line');
        showC(line.getAttribute('data-fp'),parseInt(line.getAttribute('data-ln')),line.getAttribute('data-fn'),line.getAttribute('data-mod'));
    }
    
    // File link click -> open in editor
    if(t.classList.contains('fi')){
        var line=t.closest('.line');
        openE(line.getAttribute('data-fp'),parseInt(line.getAttribute('data-ln')));
    }
    
    // Function checkbox
    if(t.type==='checkbox'&&t.hasAttribute('data-fn')){
        var fn=t.getAttribute('data-fn');
        if(t.checked)delete hidden[fn];else hidden[fn]=true;
        applyF();updFlist();
    }
    
    // Module checkbox
    if(t.type==='checkbox'&&t.hasAttribute('data-mod-check')){
        var mod=t.getAttribute('data-mod-check');
        if(t.checked)delete hiddenMods[mod];else hiddenMods[mod]=true;
        applyF();updFlist();
    }
    
    // Module header click -> collapse/expand
    if(t.closest('.module-header')&&!t.matches('input')){
        var hdr=t.closest('.module-header');
        hdr.classList.toggle('collapsed');
        var children=hdr.nextElementSibling;
        if(children)children.classList.toggle('hidden');
    }
    
    // Sidebar tabs
    if(t.classList.contains('sidebar-tab')){
        document.querySelectorAll('.sidebar-tab').forEach(function(tab){tab.classList.remove('active');});
        t.classList.add('active');
        viewMode=t.getAttribute('data-view');
        document.getElementById('filterMode').textContent='by '+viewMode;
        updFlist();
    }
});

document.getElementById('btnAll').onclick=function(){hidden={};hiddenMods={};onlyUserCode=false;document.getElementById('btnUser').classList.remove('active');applyF();updFlist();};
document.getElementById('btnNone').onclick=function(){for(var m in modules)hiddenMods[m]=true;for(var n in funcs)hidden[n]=true;applyF();updFlist();};
document.getElementById('btnUser').onclick=function(){onlyUserCode=!onlyUserCode;this.classList.toggle('active',onlyUserCode);applyF();updFlist();};

searchBox.oninput=function(){searchTerm=this.value;mainSearchBox.value=this.value;applyF();updFlist();};
mainSearchBox.oninput=function(){searchTerm=this.value;searchBox.value=this.value;applyF();updFlist();};
minMsInput.onchange=function(){minMs=parseFloat(this.value)||0;applyF();};

document.getElementById('btnPause').onclick=function(){
    isPaused=!isPaused;
    this.textContent=isPaused?'▶ Resume':'⏸ Pause';
    this.classList.toggle('active',isPaused);
    document.getElementById('st').className='status '+(isPaused?'paused':'on');
    fetch('/pause',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({paused:isPaused})});
};

document.getElementById('btnClr').onclick=function(){
    evts=[];nc=0;funcs={};modules={};hidden={};hiddenMods={};calls={};searchTerm='';minMs=0;
    searchBox.value='';mainSearchBox.value='';minMsInput.value='0';
    traceBox.querySelectorAll('.line').forEach(function(e){e.remove();});
    flist.innerHTML='';
    document.getElementById('nc').textContent='0';
    document.getElementById('nv').textContent='0';
    document.getElementById('nm').textContent='0';
    empty.style.display='block';
    fetch('/clear',{method:'POST'});
};

document.getElementById('mclose').onclick=function(){mbg.className='modal-bg';};
document.getElementById('cbtn').onclick=function(){mbg.className='modal-bg';};
document.getElementById('obtn').onclick=function(){openE(curFile,curLine);};
mbg.onclick=function(e){if(e.target===mbg)mbg.className='modal-bg';};
document.addEventListener('keydown',function(e){if(e.key==='Escape'){mbg.className='modal-bg';configPanel.classList.remove('show');}});

// Config Panel Logic
var configPanel=document.getElementById('configPanel');
var includeModules=[], excludeModules=[], includeFuncs=[], excludeFuncs=[];

function setupTagInput(containerId, arr, isExclude) {
    var container = document.getElementById(containerId);
    var input = container.querySelector('input');
    
    function renderTags() {
        container.querySelectorAll('.tag').forEach(function(t){t.remove();});
        arr.forEach(function(tag, idx) {
            var span = document.createElement('span');
            span.className = 'tag' + (isExclude ? ' exclude' : '');
            span.innerHTML = esc(tag) + '<span class="remove" data-idx="'+idx+'">×</span>';
            container.insertBefore(span, input);
        });
    }
    
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && this.value.trim()) {
            e.preventDefault();
            arr.push(this.value.trim());
            this.value = '';
            renderTags();
        } else if (e.key === 'Backspace' && !this.value && arr.length) {
            arr.pop();
            renderTags();
        }
    });
    
    container.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove')) {
            var idx = parseInt(e.target.getAttribute('data-idx'));
            arr.splice(idx, 1);
            renderTags();
        } else {
            input.focus();
        }
    });
    
    return renderTags;
}

var renderIncludeMods = setupTagInput('includeModulesInput', includeModules, false);
var renderExcludeMods = setupTagInput('excludeModulesInput', excludeModules, true);
var renderIncludeFuncs = setupTagInput('includeFuncsInput', includeFuncs, false);
var renderExcludeFuncs = setupTagInput('excludeFuncsInput', excludeFuncs, true);

// Preset buttons
document.querySelectorAll('[data-preset]').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var type = this.getAttribute('data-preset');
        var value = this.getAttribute('data-value');
        if (type === 'include' && includeModules.indexOf(value) === -1) {
            includeModules.push(value);
            renderIncludeMods();
        } else if (type === 'exclude' && excludeModules.indexOf(value) === -1) {
            excludeModules.push(value);
            renderExcludeMods();
        }
    });
});

document.getElementById('btnConfig').onclick = function() {
    configPanel.classList.add('show');
    loadCurrentConfig();
};

document.getElementById('configClose').onclick = function() {
    configPanel.classList.remove('show');
};

configPanel.onclick = function(e) {
    if (e.target === configPanel) configPanel.classList.remove('show');
};

function loadCurrentConfig() {
    fetch('/config')
        .then(function(r){return r.json();})
        .then(function(cfg) {
            // Update UI with current config
            document.getElementById('cfgOnlyUserCode').checked = cfg.only_user_code;
            document.getElementById('cfgTrackExceptions').checked = cfg.track_exceptions;
            document.getElementById('cfgMinDuration').value = cfg.min_duration_ms;
            document.getElementById('cfgMaxDepth').value = cfg.max_depth;
            
            // Update status
            var statusEl = document.getElementById('configStatus');
            if (cfg.enabled) {
                statusEl.textContent = cfg.paused ? '⏸ Tracer paused' : '🟢 Tracer running';
                statusEl.className = 'status-text running';
            } else {
                statusEl.textContent = '⚪ Tracer not started (run your code with trace())';
                statusEl.className = 'status-text stopped';
            }
            
            // Show current config
            document.getElementById('currentConfigPre').textContent = JSON.stringify(cfg, null, 2);
        });
}

document.getElementById('btnApplyConfig').onclick = function() {
    var config = {
        include_modules: includeModules.length ? includeModules : null,
        exclude_modules: excludeModules.length ? excludeModules : null,
        include_funcs: includeFuncs.length ? includeFuncs : null,
        exclude_funcs: excludeFuncs.length ? excludeFuncs : null,
        only_user_code: document.getElementById('cfgOnlyUserCode').checked,
        track_exceptions: document.getElementById('cfgTrackExceptions').checked,
        min_duration_ms: parseFloat(document.getElementById('cfgMinDuration').value) || 0,
        max_depth: parseInt(document.getElementById('cfgMaxDepth').value) || 30
    };
    
    fetch('/config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(config)
    })
    .then(function(r){return r.json();})
    .then(function(d) {
        if (d.status === 'ok') {
            showT('Configuration applied! Run your code with trace() to start.', false);
            loadCurrentConfig();
        } else {
            showT('Failed to apply config: ' + (d.error || 'unknown'), true);
        }
    });
};

document.getElementById('btnResetConfig').onclick = function() {
    includeModules = []; excludeModules = []; includeFuncs = []; excludeFuncs = [];
    renderIncludeMods(); renderExcludeMods(); renderIncludeFuncs(); renderExcludeFuncs();
    document.getElementById('cfgOnlyUserCode').checked = false;
    document.getElementById('cfgTrackExceptions').checked = true;
    document.getElementById('cfgMinDuration').value = 0;
    document.getElementById('cfgMaxDepth').value = 30;
    
    fetch('/config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({reset: true})
    })
    .then(function(r){return r.json();})
    .then(function(d) {
        showT('Configuration reset to defaults', false);
        loadCurrentConfig();
    });
};

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
        cfg.call_counter = 0
        cfg.depth = 0
        cfg.call_stack = []
        return jsonify({"status": "ok"})
    
    @app.route('/pause', methods=['POST'])
    def pause_trace():
        data = request.json
        cfg.paused = data.get('paused', False)
        return jsonify({"status": "ok", "paused": cfg.paused})
    
    @app.route('/config', methods=['GET', 'POST'])
    def handle_config():
        if request.method == 'GET':
            return jsonify({
                "enabled": cfg.enabled,
                "paused": cfg.paused,
                "include_modules": cfg.include_modules,
                "exclude_modules": cfg.exclude_modules,
                "include_funcs": cfg.include_funcs,
                "exclude_funcs": cfg.exclude_funcs,
                "include_paths": cfg.include_paths,
                "exclude_paths": cfg.exclude_paths_custom,
                "only_user_code": cfg.only_user_code,
                "min_duration_ms": cfg.min_duration_ms,
                "max_depth": cfg.max_depth,
                "track_exceptions": cfg.track_exceptions,
                "project_root": cfg.project_root
            })
        else:
            data = request.json
            
            # Handle reset
            if data.get('reset'):
                cfg.include_modules = None
                cfg.exclude_modules = None
                cfg.include_funcs = None
                cfg.exclude_funcs = None
                cfg.include_paths = None
                cfg.exclude_paths_custom = None
                cfg.only_user_code = False
                cfg.min_duration_ms = 0
                cfg.max_depth = 30
                cfg.track_exceptions = True
                return jsonify({"status": "ok", "message": "Config reset"})
            
            # Apply new config
            if 'include_modules' in data:
                cfg.include_modules = data['include_modules']
            if 'exclude_modules' in data:
                cfg.exclude_modules = data['exclude_modules']
            if 'include_funcs' in data:
                cfg.include_funcs = data['include_funcs']
            if 'exclude_funcs' in data:
                cfg.exclude_funcs = data['exclude_funcs']
            if 'only_user_code' in data:
                cfg.only_user_code = data['only_user_code']
            if 'min_duration_ms' in data:
                cfg.min_duration_ms = data['min_duration_ms']
            if 'max_depth' in data:
                cfg.max_depth = data['max_depth']
            if 'track_exceptions' in data:
                cfg.track_exceptions = data['track_exceptions']
            
            return jsonify({"status": "ok", "message": "Config updated"})
    
    @app.route('/source')
    def get_source():
        filepath = request.args.get('file')
        lineno = int(request.args.get('line', 1))
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({"error": "File not found"})
        
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            start = max(0, lineno - 20)
            end = min(len(lines), lineno + 20)
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
            subprocess.Popen(cmds.get(editor, cmds['vscode']), 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return jsonify({"status": "ok"})
        except FileNotFoundError:
            return jsonify({"status": "error", "error": f"{editor} not found in PATH"})
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)})
    
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
        print(f"\n{'='*60}")
        print(f"🔍 Script done. Tracer UI still running at http://localhost:5050")
        print(f"   Press Ctrl+C to exit")
        print(f"{'='*60}\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Bye")


def trace(
    port: int = 5050,
    open_browser: bool = True,
    keep_alive: bool = True,
    # Module filtering (NEW!)
    include_modules: Optional[List[str]] = None,
    exclude_modules: Optional[List[str]] = None,
    # Path pattern filtering
    include_paths: Optional[List[str]] = None,
    exclude_paths: Optional[List[str]] = None,
    # Function filtering (existing)
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    # Project settings
    project_root: Optional[str] = None,
    only_user_code: bool = False,
    # Performance
    min_duration_ms: float = 0,
    max_depth: int = 30,
    track_exceptions: bool = True,
):
    """
    Start tracing. Just add: from visual_tracer import trace; trace()
    
    Args:
        port: Server port (default 5050)
        open_browser: Auto-open browser (default True)
        keep_alive: Keep server running after script ends (default True)
        
        # MODULE FILTERING (supports wildcards!)
        include_modules: Only trace these modules. Examples:
            - ["prepay.utils"] - exact module
            - ["prepay.*"] - all prepay submodules
            - ["*.utils"] - all utils modules
        exclude_modules: Skip these modules
        
        # PATH FILTERING
        include_paths: Only trace files matching these patterns
            - ["*/myproject/*"]
        exclude_paths: Skip files matching these patterns
            - ["*/tests/*", "*/migrations/*"]
        
        # FUNCTION FILTERING
        include: Only trace functions containing these strings
        exclude: Skip functions containing these strings
        
        # PROJECT SETTINGS
        project_root: Your project root (auto-detected if not set)
        only_user_code: Only trace your code, skip third-party (default False)
        
        # PERFORMANCE
        min_duration_ms: Only record calls taking longer than this (default 0)
        max_depth: Max call depth to trace (default 30)
        track_exceptions: Track exceptions (default True)
    
    Examples:
        # Basic - trace everything
        trace()
        
        # Only trace specific modules
        trace(include_modules=["prepay.utils", "prepay.api"])
        
        # Trace all modules starting with "myapp"
        trace(include_modules=["myapp.*"])
        
        # Skip test modules
        trace(exclude_modules=["*.tests", "*.test_*"])
        
        # Only your code (skip third-party)
        trace(only_user_code=True)
        
        # Only slow calls (>100ms)
        trace(min_duration_ms=100)
        
        # Combine filters
        trace(
            include_modules=["myapp.*"],
            exclude_modules=["myapp.tests.*"],
            only_user_code=True,
            min_duration_ms=10
        )
    """
    _start_server(port)
    
    # Auto-detect project root
    if project_root is None:
        cfg.project_root = _detect_project_root()
    else:
        cfg.project_root = project_root
    
    cfg.enabled = True
    cfg.paused = False
    cfg.depth = 0
    cfg.call_stack = []
    cfg.call_counter = 0
    
    # Module filters
    cfg.include_modules = include_modules
    cfg.exclude_modules = exclude_modules
    
    # Path filters
    cfg.include_paths = include_paths
    cfg.exclude_paths_custom = exclude_paths
    
    # Function filters
    cfg.include_funcs = include
    cfg.exclude_funcs = exclude
    
    # Settings
    cfg.only_user_code = only_user_code
    cfg.min_duration_ms = min_duration_ms
    cfg.max_depth = max_depth
    cfg.track_exceptions = track_exceptions
    
    sys.setprofile(_trace_fn)
    
    if keep_alive:
        atexit.register(_on_exit)
    
    # Print config summary
    print(f"\n{'='*60}")
    print(f"🔍 TRACER ACTIVE - http://localhost:{port}")
    if cfg.project_root:
        print(f"   Project root: {cfg.project_root}")
    if include_modules:
        print(f"   Include modules: {include_modules}")
    if exclude_modules:
        print(f"   Exclude modules: {exclude_modules}")
    if only_user_code:
        print(f"   Mode: Only user code (skip third-party)")
    if min_duration_ms > 0:
        print(f"   Min duration: {min_duration_ms}ms")
    print(f"{'='*60}\n")
    
    if open_browser:
        try:
            webbrowser.open(f'http://localhost:{port}')
        except:
            pass


def stop_trace():
    """Stop tracing."""
    sys.setprofile(None)
    cfg.enabled = False


def pause_trace():
    """Pause tracing (can be resumed)."""
    cfg.paused = True


def resume_trace():
    """Resume tracing after pause."""
    cfg.paused = False


def start_server(port: int = 5050, open_browser: bool = True):
    """
    Start the tracer server without enabling tracing.
    Use this to configure filters in the UI before running your code.
    
    Usage:
        1. Run: python -c "from visual_tracer import start_server; start_server()"
        2. Configure filters in the browser UI
        3. Then run your code with: trace()  (it will use UI config)
    """
    _start_server(port)
    
    print(f"\n{'='*60}")
    print(f"🔧 TRACER SERVER STARTED - http://localhost:{port}")
    print(f"   Configure filters in the browser, then run your code with:")
    print(f"   from visual_tracer import trace; trace()")
    print(f"{'='*60}\n")
    
    if open_browser:
        try:
            webbrowser.open(f'http://localhost:{port}')
        except:
            pass
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Visual Python Tracer')
    parser.add_argument('--port', '-p', type=int, default=5050, help='Server port (default: 5050)')
    parser.add_argument('--no-browser', action='store_true', help="Don't open browser automatically")
    args = parser.parse_args()
    
    print("Visual Python Tracer - Enhanced Edition")
    print("="*60)
    print("\n1. Configure filters in the browser UI")
    print("2. Then run your code with:")
    print("   from visual_tracer import trace; trace()")
    print("\nOr use programmatic filters:")
    print('   trace(include_modules=["myapp.*"])')
    print('   trace(only_user_code=True)')
    print('   trace(min_duration_ms=100)')
    print("\nStarting server...")
    print("="*60)
    
    _start_server(args.port)
    
    if not args.no_browser:
        try:
            webbrowser.open(f'http://localhost:{args.port}')
        except:
            pass
    
    print(f"\n🔧 Server running at http://localhost:{args.port}")
    print("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Bye")
