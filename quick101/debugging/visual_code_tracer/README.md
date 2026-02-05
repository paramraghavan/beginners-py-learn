# Visual Python Tracer

A visual debugging tool that traces Python function calls in real-time with a web UI. Filter by module, function, duration, and more.

![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)

## Features

- 🔍 **Real-time tracing** - See function calls as they happen
- 📦 **Module filtering** - Filter by `prepay.utils`, `myapp.*`, `*.services`
- ⚡ **Performance filtering** - Only show slow calls (>100ms)
- 🎯 **"My Code" mode** - Hide third-party libraries automatically
- ❌ **Exception tracking** - See where errors are raised
- 📂 **Click to open** - Jump to source in VS Code, Cursor, PyCharm, or Sublime
- ⏸️ **Pause/Resume** - Control tracing without stopping your code
- 🖥️ **Web UI** - Configure everything in the browser

## Installation

```bash
# Copy visual_tracer.py to your project
cp visual_tracer.py /your/project/

# Install dependency
pip install flask
```

## Quick Start

Add one line to your code:

```python
from visual_tracer import trace; trace()
```

That's it! A browser window opens with the tracer UI.

---

## Usage Options

### Option 1: Configure in UI (Recommended for exploration)

Best when you want to interactively explore and adjust filters.

**Step 1:** Start the tracer server

```bash
python visual_tracer.py
```

**Step 2:** Configure filters in the browser

Click **⚙️ Config** to open the configuration panel:

- Add module filters (e.g., `myapp.*`)
- Enable "Only my code" 
- Set minimum duration threshold
- Click **Apply**

**Step 3:** Run your code with tracing

```python
# your_script.py
from visual_tracer import trace
trace()  # Uses config from UI

# Your code here
def main():
    process_data()
    
main()
```

---

### Option 2: Configure in Code (Recommended for repeatable debugging)

Best when you know exactly what you want to trace.

```python
from visual_tracer import trace

# Basic - trace everything
trace()

# Only trace specific modules
trace(include_modules=["myapp.services", "myapp.utils"])

# Trace all submodules with wildcard
trace(include_modules=["myapp.*"])

# Exclude test modules
trace(exclude_modules=["*.tests", "*.test_*", "*.migrations"])

# Only your code (skip third-party)
trace(only_user_code=True)

# Only slow calls (great for performance debugging)
trace(min_duration_ms=100)

# Combine filters
trace(
    include_modules=["myapp.*"],
    exclude_modules=["myapp.tests.*"],
    only_user_code=True,
    min_duration_ms=10,
    track_exceptions=True
)
```

---

## Configuration Reference

### Module Filtering

```python
# Include specific modules
trace(include_modules=["myapp.api", "myapp.services"])

# Wildcard - all submodules
trace(include_modules=["myapp.*"])

# Wildcard - all utils modules anywhere
trace(include_modules=["*.utils"])

# Exclude modules
trace(exclude_modules=["*.tests", "*.migrations"])
```

### Function Filtering

```python
# Only trace functions containing these strings
trace(include=["process", "handle", "fetch"])

# Skip functions containing these strings
trace(exclude=["helper", "validate", "_internal"])
```

### Performance Filtering

```python
# Only show calls taking longer than 100ms
trace(min_duration_ms=100)

# Limit call stack depth
trace(max_depth=20)
```

### Other Options

```python
trace(
    port=5050,              # Server port (default: 5050)
    open_browser=True,      # Auto-open browser (default: True)
    keep_alive=True,        # Keep server after script ends (default: True)
    only_user_code=False,   # Skip third-party libraries (default: False)
    track_exceptions=True,  # Track raised exceptions (default: True)
    project_root=None,      # Project root path (auto-detected)
)
```

---

## UI Features

### Sidebar Filters

- **Modules tab** - Group functions by module, collapse/expand
- **Functions tab** - Flat list of all functions
- **Search** - Filter with wildcards: `myapp.*`, `*utils*`
- **All/None** - Quick select/deselect all
- **My Code** - Toggle third-party visibility

### Header Controls

- **Min ms** - Filter by minimum duration
- **Editor** - Choose VS Code, Cursor, PyCharm, or Sublime
- **⚙️ Config** - Open configuration panel
- **⏸️ Pause** - Pause/resume tracing
- **🗑 Clear** - Clear all traces

### Trace View

- Click **function name** → View source code
- Click **filename:line** → Open in editor
- 🟢 Green = function call
- 🔴 Red = function return
- 🟠 Orange/Red timing = slow calls (>100ms / >500ms)
- ❌ Red background = exception raised

---

## Examples

### Debug a Specific Feature

```python
from visual_tracer import trace

# Only trace payment processing
trace(include_modules=["myapp.payments.*", "myapp.billing.*"])

def checkout(cart):
    process_payment(cart)
    send_receipt(cart.user)
```

### Find Performance Bottlenecks

```python
from visual_tracer import trace

# Only show calls taking >50ms
trace(min_duration_ms=50, only_user_code=True)

def slow_operation():
    fetch_data()      # Will show if >50ms
    process_items()   # Will show if >50ms
```

### Debug a Django/Flask App

```python
# In your app startup or a test file
from visual_tracer import trace

trace(
    include_modules=["myapp.*"],
    exclude_modules=["myapp.migrations.*", "myapp.tests.*"],
    only_user_code=True
)

# Then make requests to your app
```

### Trace a Single Function

```python
from visual_tracer import trace

# Only trace functions with "process" in the name
trace(include=["process"])

def process_order(order):    # ✓ Traced
    validate_order(order)    # ✗ Not traced
    process_payment(order)   # ✓ Traced
```

---

## API Reference

### Functions

| Function | Description |
|----------|-------------|
| `trace(...)` | Start tracing with optional filters |
| `stop_trace()` | Stop tracing completely |
| `pause_trace()` | Pause tracing (can resume) |
| `resume_trace()` | Resume after pause |
| `start_server(port)` | Start server without tracing (for UI config) |

### trace() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `port` | int | 5050 | Server port |
| `open_browser` | bool | True | Auto-open browser |
| `keep_alive` | bool | True | Keep server after script ends |
| `include_modules` | list | None | Only trace these modules |
| `exclude_modules` | list | None | Skip these modules |
| `include` | list | None | Only trace functions matching these |
| `exclude` | list | None | Skip functions matching these |
| `only_user_code` | bool | False | Skip third-party libraries |
| `min_duration_ms` | float | 0 | Min call duration to record |
| `max_depth` | int | 30 | Max call stack depth |
| `track_exceptions` | bool | True | Track raised exceptions |
| `project_root` | str | None | Project root (auto-detected) |

---

## Tips

1. **Start broad, then narrow down** - Begin with `only_user_code=True`, then add module filters

2. **Use wildcards** - `myapp.*` is easier than listing every module

3. **Performance debugging** - Set `min_duration_ms=100` to find bottlenecks

4. **Keep the server running** - After your script ends, the UI stays up so you can explore

5. **Pause during noise** - Hit ⏸️ Pause during setup/teardown to reduce noise

6. **Click to navigate** - Click any function name to see source, click filename to open in editor

---

## Troubleshooting

### "Module not found" for flask
```bash
pip install flask
```

### Tracer shows nothing
- Check that your code is actually running
- Make sure files end in `.py`
- Try `trace(only_user_code=False)` to see all calls

### Too much output
- Add module filters: `trace(include_modules=["myapp.*"])`
- Enable "My Code" mode: `trace(only_user_code=True)`
- Increase min duration: `trace(min_duration_ms=10)`

### Editor doesn't open
- Make sure your editor is in PATH
- Try a different editor in the dropdown

---

## License

MIT
