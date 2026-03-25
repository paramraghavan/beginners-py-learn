It’s  really frustrating when a script turns into a "black box" and just sits there staring back at you. Since
`trace` was too noisy and `strace` only showed you the system-level bottleneck, you need a way to peek at the **Python
Call Stack** while the process is currently stuck. Here are some ways you can do it


## 1. The "Quick & Dirty" Way: `SIGQUIT`

If you are on Linux or macOS, you can often force a running Python process to dump its current state by hitting *
*`Ctrl + \`** (SIGQUIT) in the terminal where it's running.

However, for a truly useful stack trace, you usually need to have the `faulthandler` module enabled. If you can restart
the script once more, run it like this:

```bash
python -X faulthandler your_script.py
```

If it hangs, hit **`Ctrl + C`**. Because `faulthandler` is active, it will print the exact line of Python code that was
executing at that microsecond.

---

## 2. `py-spy` (Best option)

This is the best tool for your situation. `py-spy` is a sampling profiler that can attach to a **currently running**
Python process without restarting it or modifying the code.

* **Install it:** `pip install py-spy`
* **Top view:** Like the `top` command but for Python functions.
    ```bash
    # Replace <PID> with your script's process ID
    sudo py-spy top --pid <PID>
    ```
* **Dump the stack:** This shows you exactly where every thread is currently sitting.
    ```bash
    sudo py-spy dump --pid <PID>
    ```

## 3. The "Internal" Way: `sys._current_frames()`

If you can modify the code but don't want to add 1,000 print statements, you can register a "heartbeat" or a signal
handler that prints the stack trace when you send it a signal.

```python
import sys
import traceback
import signal


def debug_signal_handler(sig, frame):
    print("\n--- STACK TRACE ---")
    for thread_id, stack in sys._current_frames().items():
        traceback.print_stack(stack)
    print("-------------------\n")


# Register the USR1 signal
signal.signal(signal.SIGUSR1, debug_signal_handler)
```

While the script is hung, run `kill -USR1 <PID>` from another terminal, and your script will print its current line to
its own stdout.

>**`py-spy dump`** is the best bet if you can have this library installed. It’s non-intrusive, works on running processes, and handles multi-threaded scripts  beautifully.
