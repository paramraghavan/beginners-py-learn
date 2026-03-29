`strace` traces **system calls** made by programs.

## Basic syntax

```bash
strace [options] command [args]
```

> In scenarios where the script hangs at a particular point and you don't know where run
>> strace python_script
>>> once the script hangs perform ctrl+c
> > > this should give you the stack trace.

## Common usage patterns

### 1. Trace a command

```bash
strace ls -la
strace python script.py
```

### 2. Save output to file

```bash
strace -o output.txt ls -la
strace -o trace.log python script.py
```

### 3. Follow child processes

```bash
strace -f python script.py          # Follow forks
strace -ff -o trace python script.py # Each process to separate file
```

### 4. Filter specific system calls

```bash
strace -e open,read,write ls        # Only file operations
strace -e network python script.py  # Only network calls
strace -e file python script.py     # Only file-related calls
```

### 5. Show full strings (not truncated)

```bash
strace -s 1024 python script.py     # Show up to 1024 chars
strace -s 0 python script.py        # Show full strings
```

### 6. Attach to running process

```bash
strace -p 1234                      # Attach to PID 1234
strace -p 1234 -o /tmp/trace.txt    # Save to file
```

### 7. Show timestamps

```bash
strace -t python script.py          # Time of day
strace -tt python script.py         # Microsecond precision
strace -r python script.py          # Relative timestamps
```

## Useful combinations

```bash
# Common debugging setup
strace -f -s 1024 -o /tmp/debug.txt python script.py

# Network debugging
strace -e network -f python script.py

# File access debugging
strace -e open,read,write,stat -f python script.py
```

## What you'll see

- `open("/path/file", O_RDONLY)` - Opening files
- `read(3, "data", 1024)` - Reading data
- `write(1, "output", 6)` - Writing to stdout
- `execve("/usr/bin/python", ...)` - Process execution
- `connect(3, {sa_family=AF_INET, ...})` - Network connections

**Note**: strace shows system-level calls, not Python function calls. For Python debugging, use `python -m trace` or
profiling tools instead.

## strace and stdout

strace treats almost everything written to the screen as a generic `write` system call.

To specifically find where your script is writing to **stdout** (Standard Output) or **stderr** (Standard Error), you
need to look at the **File Descriptor (fd)** associated with the write call.

### The Logic

In Linux/Unix systems, the first three file descriptors are reserved:

* **0**: stdin (Standard Input)
* **1**: **stdout** (Standard Output - where `print()` usually goes)
* **2**: **stderr** (Standard Error - where tracebacks and errors go)

### The Command

To filter your `strace` output for writes specifically to stdout and stderr, you can use the `-e write` flag and then
`grep` for the file descriptors `1` or `2` at the start of the call:

```bash
strace -e write -f python3 script.py 2>&1 | grep -E '^\[?.*write\([12],'
```

**Breakdown of this command:**

* `-e write`: Only captures the `write` system calls.
* `2>&1`: Redirects the `strace` output (which defaults to stderr) into stdout so `grep` can read it.
* `grep -E '^\[?.*write\([12],'`: This regex looks for lines starting with `write(1,` or `write(2,`. The `\[?.*` part
  accounts for process IDs that appear when using the `-f` (follow forks) flag.

---

### Alternative: Python-Specific Tracing

If you want to find the actual **line numbers** in your Python code where these prints happen (which `strace` won't show
you directly), the built-in `trace` module is often much more helpful.

Run this in your terminal:

```bash
python3 -m trace --trace script.py | grep -B 1 "print("
```

This will show you the line of code being executed immediately before or during a print statement.

### Comparison Table

| Tool               | Level       | Best For...                                         |
|:-------------------|:------------|:----------------------------------------------------|
| **strace**         | System      | Checking if data actually hit the OS kernel/buffer. |
| **trace (Python)** | Application | Finding the exact line number in your `.py` file.   |
| **ltrace**         | Library     | Seeing calls to the C-library (like `printf`).      |

