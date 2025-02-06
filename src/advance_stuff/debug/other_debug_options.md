## How to Use `strace` with Python

`strace` is a Linux utility that allows you to trace system calls and signals of a program. While `strace` itself is not
a Python tool, you can use it to analyze Python programs at the system call level.

You can run `strace` on a Python script to see what system calls it makes:

```bash
strace -o trace.log -e trace=open,read,write python3 my_script.py
```

### Explanation:

- `-o trace.log`: Saves the output to a file.
- `-e trace=open,read,write`: Filters system calls to only show file-related calls (`open`, `read`, `write`).
- `python3 my_script.py`: Runs your script under `strace`.

### Example Output:

```plaintext
open("my_script.py", O_RDONLY) = 3
read(3, "import os\nprint('Hello World')", 28) = 28
write(1, "Hello World\n", 12) = 12
```

This shows that Python opened `my_script.py`, read its content, and wrote "Hello World" to standard output.


### Another example
```bash
strace -s 1024 > /tmp/why.txt -f python your_script.py
````
Above command traces system calls made by your Python script with these key elements:

- `-s 1024`: Sets maximum string size to 1024 bytes (default is 32)
- `> /tmp/why.txt`: Redirects trace output to this file
- `-f`: Follows child processes (traces subprocess forks)
- Traces all system calls made by `python your_script.py`
  The trace output will show every system call, its arguments, and return values, useful for debugging or understanding
  program behavior at the OS level.


## Using `strace` in Python

If you want to invoke `strace` from within a Python script, you can use the `subprocess` module:

```python
import subprocess

subprocess.run(["strace", "-c", "python3", "my_script.py"])
```
This will show a summary of system calls made by `my_script.py`.

## Alternative: Python's `trace` Module

If you're looking for a Python-native way to trace function calls, you can use the built-in `trace` module:

```python
import trace

tracer = trace.Trace(trace=True, count=False)
tracer.run('print("Hello World")')
```

**This traces Python function calls rather than system calls.**

