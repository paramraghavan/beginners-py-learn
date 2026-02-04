## Visual Tracer - How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR PYTHON SCRIPT                        │
│  from visual_tracer import trace; trace()                       │
│  def main(): ...                                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PYTHON PROFILER HOOK                         │
│  sys.setprofile(_trace_fn)                                      │
│  Called on EVERY function call/return                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        EVENT QUEUE                               │
│  {func_name, args, timestamp, depth, filepath, lineno, ...}     │
└───────────────┬─────────────────────────────────┬───────────────┘
                │                                 │
                ▼                                 ▼
┌───────────────────────────┐     ┌───────────────────────────────┐
│     CONSOLE OUTPUT        │     │      FLASK SERVER             │
│  02:21:03 ┌─ main()       │     │  (background thread)          │
│  02:21:03   ┌─ foo()      │     │                               │
│  02:21:03   └─ foo ✓ 2ms  │     │  /stream  → SSE events        │
└───────────────────────────┘     │  /events  → all history       │
                                  │  /source  → code preview      │
                                  │  /open    → launch editor     │
                                  └───────────────┬───────────────┘
                                                  │
                                                  ▼
                                  ┌───────────────────────────────┐
                                  │         BROWSER UI            │
                                  │  - Real-time event stream     │
                                  │  - Function filter sidebar    │
                                  │  - Click to view code         │
                                  │  - Click to open in editor    │
                                  └───────────────────────────────┘
```

---

### Key Components

#### 1. **Python's Profiler Hook** (`sys.setprofile`)

Python has a built-in mechanism to intercept function calls:

```python
def _trace_fn(frame, event, arg):
    # frame = current execution frame (has locals, code, line number)
    # event = 'call' or 'return'
    # arg   = return value (for 'return' events)

    if event == 'call':
        # Function is being called
        func_name = frame.f_code.co_name
        filepath = frame.f_code.co_filename
        lineno = frame.f_lineno
        args = frame.f_locals  # function arguments

    elif event == 'return':
        # Function is returning
        return_value = arg
        elapsed_time = now - start_time


sys.setprofile(_trace_fn)  # Install the hook
```

This is called **automatically by Python** for every function call/return.

---

#### 2. **Event Queue** (Thread-Safe Communication)

```python
event_queue = queue.Queue()  # Thread-safe

# In trace function (main thread):
event_queue.put({"func": "foo", "event": "call", ...})

# In Flask server (background thread):
event = event_queue.get()  # Blocks until event available
```

This allows the tracer (running in your code) to send events to the web server (running in a separate thread).

---

#### 3. **Server-Sent Events (SSE)** (Real-Time Browser Updates)

```python
@app.route('/stream')
def stream():
    def generate():
        while True:
            event = event_queue.get()  # Wait for event
            yield f"data: {json.dumps(event)}\n\n"  # SSE format

    return Response(generate(), mimetype='text/event-stream')
```

Browser connects once and receives events as they happen:

```javascript
// Browser
var sse = new EventSource('/stream');
sse.onmessage = function(e) {
    var event = JSON.parse(e.data);
    renderEvent(event);  // Add to UI
};
```

---

#### 4. **Call Stack Tracking** (For Parent-Child Relationships)

```python
call_stack = []

if event == 'call':
    parent_id = call_stack[-1]['id'] if call_stack else 0
    call_stack.append({'id': new_id, 'start': time.now(), ...})

elif event == 'return':
    info = call_stack.pop()
    elapsed = time.now() - info['start']
```

This allows:

- Calculating **elapsed time** per function
- Building **parent-child hierarchy** (for filtering)
- Creating **indentation** in the UI

---

#### 5. **Filtering Logic** (Hide Parent = Hide Children)

```javascript
function isHidden(event) {
    // Check if this function is hidden
    if (hidden[event.func_name]) return true;
    
    // Check if ANY ancestor is hidden
    var parentId = event.parent_id;
    while (parentId) {
        var parent = calls[parentId];
        if (parent && hidden[parent.func_name]) return true;
        parentId = parent ? parent.parent_id : 0;
    }
    return false;
}
```

---

### Data Flow Timeline

```
Time    Your Code              Tracer                    Browser
────────────────────────────────────────────────────────────────────
T0      trace()         →      Start Flask server        
                               sys.setprofile(hook)      
                                                    ←    Connect to /stream
                                                    
T1      main()          →      hook('call', main)   →    Render: ┌─ main()
                               
T2        foo()         →      hook('call', foo)    →    Render:   ┌─ foo()
                               
T3        return 42     →      hook('return', 42)   →    Render:   └─ foo ✓ 2ms → 42
                               
T4      return          →      hook('return')       →    Render: └─ main ✓ 5ms

T5      script ends     →      atexit handler       →    Server keeps running
                               (keeps server alive)      (browse trace history)
```

---

### Why Each Piece Exists

| Component             | Purpose                                             |
|-----------------------|-----------------------------------------------------|
| `sys.setprofile`      | Intercept all function calls without modifying code |
| `queue.Queue`         | Thread-safe communication between tracer and server |
| Flask server          | Serve web UI and API endpoints                      |
| SSE `/stream`         | Push real-time events to browser (no polling)       |
| `/events` endpoint    | Load historical events when browser connects late   |
| `/source` endpoint    | Read source file for code preview                   |
| `/open` endpoint      | Launch editor via subprocess                        |
| `atexit` handler      | Keep server running after script ends               |
| Parent-child tracking | Enable "hide function + all its children"           |

---

### Why It's Just One Line

```python
from visual_tracer import trace;

trace()
```

This single call:

1. Starts Flask server in **background thread**
2. Installs **profiler hook** via `sys.setprofile`
3. Registers **atexit handler** to keep server alive
4. Opens **browser** automatically

