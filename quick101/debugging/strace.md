`strace` traces **system calls** made by programs.

## Basic syntax

```bash
strace [options] command [args]
```

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