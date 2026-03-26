# 🐛 Python Debugging on Linux
### A Practical Guide to Ditching `pdb`

---

## The Problem with `pdb`

Debugging with `pdb` is painful:
- No visual context — you're flying blind
- Setting and removing breakpoints requires typing commands
- No variable pane — you inspect one variable at a time
- Easy to lose your place in deep call stacks

There are much better tools. Here's what to use instead.

---

## 🥇 `pudb` — Best for Terminal / Linux

> **Recommended for your situation.** Full-screen TUI debugger that runs entirely in your terminal — no GUI or desktop environment needed.

### Installation

```bash
pip install pudb
```

### Usage

**Option 1 — Drop a breakpoint in your code:**
```python
import pudb; pudb.set_trace()
```

**Option 2 — Run your entire script under pudb:**
```bash
python -m pudb my_script.py
```

### Key Bindings

| Key | Action |
|-----|--------|
| `n` | Step over (next line) |
| `s` | Step into function |
| `c` | Continue to next breakpoint |
| `b` | **Toggle breakpoint on current line** |
| `t` | Run to cursor |
| `u` | Move up the call stack |
| `d` | Move down the call stack |
| `!` | Open interactive Python REPL at current frame |
| `?` | Show help |
| `q` | Quit |

> 💡 You can also **click** directly on any source line to toggle a breakpoint.

### What You See

```
┌─ Source ──────────────────────┐ ┌─ Variables ─────────┐
│  12   def load_config(path):  │ │ path = '/etc/app.cfg'│
│  13 ●     data = read(path)   │ │ data = None          │
│  14       return parse(data)  │ └─────────────────────┘
└───────────────────────────────┘ ┌─ Stack ─────────────┐
                                  │ > load_config        │
                                  │   main               │
                                  └─────────────────────┘
```

---

## 🥈 VS Code — Best for a GUI Experience

If you're running Linux with a desktop (or SSH + Remote extension), VS Code gives you click-to-set breakpoints, a full variable watch panel, and a call stack view.

### Setup

1. Install the **Python** extension by Microsoft
2. Open your `.py` file
3. Click the **gutter** (left margin beside line numbers) — a 🔴 red dot appears
4. Press **F5** to launch the debugger

### Key Shortcuts

| Shortcut | Action |
|----------|--------|
| `F5` | Start / Continue |
| `F10` | Step over |
| `F11` | Step into |
| `Shift+F11` | Step out |
| `F9` | Toggle breakpoint on current line |
| **Pause button** | **Pause a running/hanging program** ← very useful |

> 💡 The **Pause** button is invaluable for your **freezing script** — hit it mid-run and VS Code will show you exactly which line is hanging and why.

---

## 🥉 `ipdb` — Quick Drop-in Replacement

Same interface as `pdb` but with **tab-completion** and **syntax highlighting**. Minimal learning curve if you're already used to `pdb`.

### Installation

```bash
pip install ipdb
```

### Usage

```python
import ipdb; ipdb.set_trace()
```

---

## 🔍 Diagnosing Your Specific Issues

### Problem 1 — Parameters Not Pulling In Correctly

With `pudb` or VS Code, you can inspect **all locals and globals** visually the moment you hit a breakpoint — no more `print()` hunting.

**Quick approach with pudb:**
1. Set a breakpoint right after the parameters are loaded
2. Hit `b` to confirm breakpoint is set (shown as `●`)
3. Run — the Variables pane on the right shows every value instantly
4. Hit `!` to open a REPL and interactively test expressions against live data

---

### Problem 2 — Script Freezes / Hangs

The script is likely stuck on one of:
- A blocking network/socket call
- A `queue.get()` or `threading.Event.wait()` with no timeout
- An infinite loop
- A deadlock between threads

**Option A — Interrupt and inspect (quickest):**
```bash
# In a second terminal, find your script's PID:
ps aux | grep my_script.py

# Send SIGINT to force a traceback:
kill -SIGINT <pid>
```
The traceback will show the exact line where it was stuck.

**Option B — VS Code Pause button:**
While the script is hanging, click the **⏸ Pause** button in the debug toolbar. VS Code will halt execution and highlight the frozen line.

**Option C — pudb remote attach:**
```bash
# Start your script with remote debugging enabled:
python -m pudb.remote --host 127.0.0.1 --port 6900 my_script.py

# In another terminal, connect:
telnet 127.0.0.1 6900
```

**Option D — Add a signal handler (no debugger needed):**
```python
import signal, traceback

def dump_stack(sig, frame):
    print("=== STACK DUMP ===")
    traceback.print_stack(frame)

signal.signal(signal.SIGUSR1, dump_stack)
```
Then trigger it anytime with:
```bash
kill -SIGUSR1 <pid>
```

---

## ⚡ Quick Comparison

| Tool | Environment | Breakpoints | Variable Inspect | Hang Diagnosis |
|------|-------------|-------------|-----------------|----------------|
| `pudb` | Terminal only | `b` key / click | Visual pane | SIGINT + attach |
| VS Code | Desktop / SSH | Click gutter / F9 | Watch panel | Pause button ✅ |
| `ipdb` | Terminal only | Typed commands | Manual query | SIGINT |
| `pdb` | Terminal only | Typed commands | Manual query | Pain |

---

## 🚀 Recommended Workflow

```
1.  pip install pudb
2.  Add  import pudb; pudb.set_trace()  where you want to start
3.  Run your script normally
4.  Use  b  to toggle breakpoints on the fly
5.  Use  !  to open a REPL and test fixes live
6.  For hangs: open a second terminal and  kill -SIGUSR1 <pid>
```

---

*Happy debugging — may your parameters always resolve and your threads never deadlock.* 🎯
