The command `python -m trace --trace test_jwt.py` runs Python's built-in trace module to show **every single line of
code** that gets executed when running your script. You can instrument your Python script to trace execution without
actually running the code using several approaches.
> This is much more useful than `strace` for Python debugging because it shows the actual Python code execution flow.

# What it does:

- **Line-by-line execution tracing**: Shows each line as it's executed
- **Import tracing**: Shows what happens during module imports
- **Function call tracing**: Shows when functions are entered/exited
- **Module loading**: Shows which files are loaded and in what order

## Method 1: Using Python's Built-in `trace` Module

The simplest approach is using Python's `trace` module:

```bash
python -m trace --trace your_script.py arg1 arg2 arg3
```

This will print every line as it's executed. For cleaner output, you can:

```bash
# Only show lines from your script (not library code)
python -m trace --trace --ignore-dir=/usr/lib/python3.x your_script.py arg1 arg2

# Save output to file
python -m trace --trace your_script.py arg1 arg2 > execution_trace.txt
```

## Method 2: Custom Trace Function

Add this to the beginning of your script:

```python
import sys


def trace_calls(frame, event, arg):
    if event == 'line':
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        line = open(filename).readlines()[lineno - 1].strip()
        print(f"TRACE: {filename}:{lineno} -> {line}")
    return trace_calls


# Enable tracing
sys.settrace(trace_calls)

# Your original code follows...
```

## Method 3: Using a Wrapper Script

Create a separate wrapper script:

```python
# trace_runner.py
import sys
import runpy
import trace


def run_with_trace(script_path, args):
    # Set up sys.argv as if running the script directly
    old_argv = sys.argv
    sys.argv = [script_path] + args

    try:
        # Create tracer
        tracer = trace.Trace(count=False, trace=True)

        # Run the script with tracing
        tracer.run('exec(open("{}").read())'.format(script_path))

    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trace_runner.py script.py [args...]")
        sys.exit(1)

    script_path = sys.argv[1]
    script_args = sys.argv[2:]
    run_with_trace(script_path, script_args)
```

Run it with:

```bash
python trace_runner.py your_script.py arg1 arg2 arg3
```

## Method 4: Conditional Tracing (Recommended)

Add this at the top of your actual script:

```python
import sys
import os


def setup_tracing():
    def trace_lines(frame, event, arg):
        if event == 'line':
            # Only trace lines from your script, not libraries
            filename = frame.f_code.co_filename
            if os.path.basename(filename) == os.path.basename(__file__):
                lineno = frame.f_lineno
                try:
                    with open(filename, 'r') as f:
                        lines = f.readlines()
                        line = lines[lineno - 1].strip()
                    print(f"EXECUTING: Line {lineno}: {line}")
                except:
                    print(f"EXECUTING: Line {lineno}")
        return trace_lines

    sys.settrace(trace_lines)


# Enable tracing only when DEBUG environment variable is set
if os.getenv('DEBUG_TRACE'):
    setup_tracing()

# Your original script code continues here...
```

Then run with:

```bash
DEBUG_TRACE=1 python your_script.py arg1 arg2 arg3
```

## Method 5: Using `pdb` in Non-Interactive Mode

For more control, you can use the debugger:

```python
import pdb
import sys


class TracePdb(pdb.Pdb):
    def user_line(self, frame):
        """Called when we stop or break at this line"""
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        line = self.get_file_breaks(filename)
        print(f"TRACE: {filename}:{lineno}")
        # Don't actually stop, just continue
        self.set_continue()


# Set up tracing
tracer = TracePdb()
tracer.set_trace()
```

## Filtering Output

To make the output more useful, you might want to filter out library code:

```python
def should_trace_file(filename):
    """Only trace files in your project directory"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return filename.startswith(script_dir)


def trace_calls(frame, event, arg):
    if event == 'line' and should_trace_file(frame.f_code.co_filename):
# ... rest of trace logic
```

The **trace module approach (Method 1)** is usually the quickest for one-off debugging, while **Method 4** is best if
you want to permanently instrument your code for optional tracing.