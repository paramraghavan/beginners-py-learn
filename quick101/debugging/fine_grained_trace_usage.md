# 🔍 Fine-Grained Control: `sys.settrace` & `strace`

> Filter the noise. See only what matters.

---

## `sys.settrace` — Python-Level Tracing

### How It Works

`sys.settrace` fires a callback on four events per frame:

| Event       | Triggered When                       |
|-------------|--------------------------------------|
| `call`      | A function is entered                |
| `line`      | A new line is about to execute       |
| `return`    | A function is about to return        |
| `exception` | An exception is raised or propagates |

Each callback receives:

- `frame` — the current execution frame (locals, globals, filename, line number)
- `event` — one of the four above
- `arg` — return value (`return`), exception tuple (`exception`), or `None` (`call`/`line`)

---

## Filter Techniques for `sys.settrace`

### 1. Filter by File Path

Only trace functions inside **your project folder**, skipping stdlib and installed packages:

```python
import sys

MY_PATH = "/path/to/your/project"


def trace_calls(frame, event, arg):
    if event != "call":
        return
    filename = frame.f_code.co_filename
    if MY_PATH not in filename:
        return  # skip stdlib, site-packages, third-party libs
    if "<" in filename:
        return  # skip <frozen importlib>, <string>, <stdin>, etc.

    print(f"  --> {frame.f_code.co_name}()  [{filename}:{frame.f_lineno}]")
    return trace_calls


sys.settrace(trace_calls)
# your code here
sys.settrace(None)
```

---

### 2. Filter by Module Name

Allowlist only the specific modules you own:

```python
import sys

ALLOWED_MODULES = {"data_loader", "processor", "main", "utils"}


def trace_calls(frame, event, arg):
    if event != "call":
        return
    module = frame.f_globals.get("__name__", "")
    if not any(m in module for m in ALLOWED_MODULES):
        return
    print(f"  [module: {module}]  {frame.f_code.co_name}()")
    return trace_calls


sys.settrace(trace_calls)
```

**Example output:**

```
  [module: data_loader]  fetch_records()
  [module: processor]    transform()
  [module: utils]        sanitize_input()
```

---

### 3. Filter by Function Name Pattern

Only trace functions matching a naming convention using regex:

```python
import sys, re

PATTERN = re.compile(r"^(fetch|process|handle|build|run|execute)_")


def trace_calls(frame, event, arg):
    if event != "call":
        return
    name = frame.f_code.co_name
    if not PATTERN.match(name):
        return
    print(f"  --> {name}()  line {frame.f_lineno}")
    return trace_calls


sys.settrace(trace_calls)
```

**Example output:**

```
  --> fetch_records()  line 42
  --> process_batch()  line 87
  --> handle_error()   line 103
```

---

### 4. Filter by Call Depth

Stop tracing beyond N levels deep — prevents drowning in deeply nested helper calls:

```python
import sys

MAX_DEPTH = 5
_depth = [0]


def trace_calls(frame, event, arg):
    if event == "call":
        _depth[0] += 1
        if _depth[0] > MAX_DEPTH:
            return  # don't trace any deeper
        indent = "  " * _depth[0]
        print(f"{indent}--> {frame.f_code.co_name}()")
    elif event == "return":
        _depth[0] = max(0, _depth[0] - 1)
    return trace_calls


sys.settrace(trace_calls)
```

**Example output (depth-limited at 3):**

```
  --> main()
    --> run_pipeline()
      --> process_batch()
        [depth limit reached — inner helpers suppressed]
```

---

### 5. Trace Exception Events Only

Watch only `exception` events to pinpoint exactly where errors originate:

```python
import sys


def trace_exceptions(frame, event, arg):
    if event == "exception":
        exc_type, exc_value, _ = arg
        filename = frame.f_code.co_filename
        print(f"  ⚠ Exception in {frame.f_code.co_name}() "
              f"at {filename}:{frame.f_lineno}")
        print(f"     {exc_type.__name__}: {exc_value}")
    return trace_exceptions


sys.settrace(trace_exceptions)
```

**Example output:**

```
  ⚠ Exception in process_record() at /project/processor.py:56
     KeyError: 'user_id'
  ⚠ Exception in run_pipeline() at /project/main.py:34
     KeyError: 'user_id'
```

---

### 6. Capture Local Variables at a Target Function

Dump the local scope when a specific function is entered — useful when a variable is unexpectedly missing:

```python
import sys

TARGET_FN = "process_record"  # the function you want to inspect


def trace_calls(frame, event, arg):
    if event != "call":
        return
    if frame.f_code.co_name == TARGET_FN:
        print(f"\n📌 Entered {TARGET_FN}()")
        for k, v in frame.f_locals.items():
            print(f"   {k} = {v!r}")
    return trace_calls


sys.settrace(trace_calls)
```

**Example output:**

```
📌 Entered process_record()
   record_id = 1042
   mode = 'strict'
   config = {'retries': 3, 'timeout': 30}
```

---

### 7. Combine All Filters (Full Example)

Stack all gates together for maximum precision:

```python
import sys, re

MY_PATH = "/path/to/your/project"
ALLOWED_MODS = {"data_loader", "processor", "main"}
NAME_PATTERN = re.compile(r"^(fetch|process|handle|build|run)_")
MAX_DEPTH = 6
_depth = [0]


def trace_calls(frame, event, arg):
    filename = frame.f_code.co_filename
    module = frame.f_globals.get("__name__", "")
    name = frame.f_code.co_name

    if event == "call":
        # Gate 1: must be inside project folder
        if MY_PATH not in filename or "<" in filename:
            return
        # Gate 2: must be an allowed module
        if not any(m in module for m in ALLOWED_MODS):
            return
        # Gate 3: function name must match pattern
        if not NAME_PATTERN.match(name):
            return
        # Gate 4: respect max call depth
        _depth[0] += 1
        if _depth[0] > MAX_DEPTH:
            return
        indent = "  " * _depth[0]
        print(f"{indent}--> {name}()  ({filename}:{frame.f_lineno})")

    elif event == "return":
        _depth[0] = max(0, _depth[0] - 1)

    return trace_calls


sys.settrace(trace_calls)
# ... your script runs here ...
sys.settrace(None)  # always stop tracing when done
```

---

## `strace` — OS / Syscall-Level Tracing

### Core Flags Reference

| Flag                 | Purpose                                              |
|----------------------|------------------------------------------------------|
| `-e trace=<syscall>` | Filter to one or more specific syscalls              |
| `-e trace=file`      | All file-related syscalls (open, stat, unlink, etc.) |
| `-e trace=network`   | All network-related syscalls                         |
| `-e trace=process`   | Process lifecycle (fork, exec, exit)                 |
| `-P <path>`          | Only syscalls touching this exact path               |
| `-p <pid>`           | Attach to an already-running process                 |
| `--trace=!<syscall>` | Exclude a specific syscall                           |
| `-f`                 | Follow forked child processes and threads            |
| `-T`                 | Show time spent in each syscall                      |
| `-t`                 | Prefix each line with wall-clock timestamp           |
| `-tt`                | Prefix with microsecond-precision timestamp          |
| `-o <file>`          | Write output to a file instead of stderr             |
| `-s <n>`             | Show up to N characters of string args (default: 32) |
| `-c`                 | Print a syscall summary/count table at the end       |

---

### Show Only File Opens, Exclude System Noise

```bash
strace -e openat python your_script.py 2>&1 \
  | grep -v "/lib\|/usr\|/proc\|/dev\|/sys\|/etc\|site-packages\|\.pyc"
```

---

### Pin to a Specific File Path

```bash
strace -e openat -P /path/to/your/data/input.csv python your_script.py 2>&1
```

`-P` pins tracing to that **exact path** — zero noise from everything else.

---

### Exclude Noisy Low-Level Syscalls

```bash
# mmap, mprotect, brk, munmap are almost always irrelevant noise
strace --trace='!mmap,mprotect,brk,munmap,futex' python your_script.py 2>&1
```

---

### Trace File + Network Syscalls Together

```bash
strace -e trace=file,network python your_script.py 2>&1 \
  | grep -v "/lib\|/usr\|/proc"
```

Useful when your script reads files **and** makes outbound network calls — trace both in one run.

---

### Time Each Syscall

```bash
strace -T -e openat python your_script.py 2>&1
```

**Example output:**

```
openat(AT_FDCWD, "/project/data/input.csv", O_RDONLY) = 5 <0.000312>
openat(AT_FDCWD, "/project/config/settings.json", O_RDONLY) = 6 <0.000089>
```

The `<0.000312>` shows seconds spent in that call — useful to spot slow file reads.

---

### Get a Syscall Summary Table

```bash
strace -c python your_script.py
```

**Example output:**

```
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- -------
 45.3    0.002301          12       192           read
 30.1    0.001528           8       191           write
 15.2    0.000772          11        70           openat
  ...
```

Great for a high-level view of *what kind* of syscalls dominate before diving deeper.

---

### Attach to an Already-Running Process

```bash
# Step 1: find the PID
pgrep -f your_script.py

# Step 2: attach and filter
strace -p <PID> -e trace=file 2>&1 | grep -v "/lib\|/usr"
```

No restart needed — attach live at any point.

---

### Save Full Trace, Query Later

```bash
# Capture everything first
strace -o trace.log python your_script.py

# Then query freely without re-running
grep "input.csv" trace.log
grep -B 10 "ENOENT" trace.log          # 10 lines before a "file not found"
grep -B 5  "EACCES" trace.log          # 5 lines before a "permission denied"
grep "connect\|sendto" trace.log       # find all outbound network calls
```

---

## Quick Decision Guide

```
Need to trace...                         Use
────────────────────────────────────────────────────────────────
Your own functions only                → sys.settrace + path filter
Specific modules                       → sys.settrace + module filter
Functions matching a naming pattern    → sys.settrace + regex filter
Where exceptions originate             → sys.settrace, event='exception'
Inspect locals at a function entry     → sys.settrace + TARGET_FN dump
File opens at OS level                 → strace -e openat
One specific file path only            → strace -P /path/to/file
Slow syscalls                          → strace -T
Syscall frequency overview             → strace -c
Attach to an already-running process   → strace -p <PID>
Capture everything, query later        → strace -o trace.log + grep
Low effort, purpose-built filtering    → hunter library
```

---

## `hunter` — Cleanest Alternative

```bash
pip install hunter
```

```bash
# Trace only your module, only function calls
python -m hunter "module_startswith='your_module',kind='call'" your_script.py
```

```bash
# Show calls AND local variables at each call site
python -m hunter "module_startswith='your_module',kind='call',action=CodePrinter" your_script.py
```

```bash
# Exclude stdlib and internal modules entirely
python -m hunter \
  "not module_startswith('_'),not module_startswith('importlib'),kind='call'" \
  your_script.py
```

```bash
# Trace only when a specific variable exists in the local scope
python -m hunter "locals_contains_key='user_id',kind='call'" your_script.py
```

`hunter` supports boolean combinators (`|`, `&`, `~`) and pluggable actions — `Debugger`, `CallPrinter`, `VarsPrinter` —
for precise, readable output without boilerplate.

---

*`sys.settrace`, `strace`, and `hunter` — fine-grained tracing for Python scripts.*
