# `subprocess.Popen` vs `subprocess.check_output`

## subprocess.Popen

- **Low-level interface** that gives you full control over the process
- **Non-blocking by default** - returns immediately while the process runs
- **Manual communication** - you handle stdin/stdout/stderr yourself
- **Custom error handling** - you check return codes and handle errors as needed
- **More flexible** for complex scenarios

```python
import subprocess

# Basic usage
process = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()  # Wait for completion
return_code = process.returncode

# Real-time output processing
process = subprocess.Popen(['ping', 'google.com'], stdout=subprocess.PIPE, text=True)
for line in process.stdout:
    print(f"Output: {line.strip()}")
```

## subprocess.check_output

- **High-level convenience function** for simple cases
- **Blocking** - waits for the process to complete before returning
- **Automatic output capture** - returns stdout directly
- **Automatic error handling** - raises `CalledProcessError` on non-zero exit codes
- **Simpler for basic use cases**

```python
import subprocess

# Basic usage
try:
    output = subprocess.check_output(['ls', '-l'], text=True)
    print(output)
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
```

## When to use each

**Use Popen when you need:**

- Real-time output processing
- Non-blocking execution
- Custom error handling
- Complex stdin/stdout interactions
- Multiple processes running simultaneously

**Use check_output when you need:**

- Simple "run command and get output" scenarios
- Automatic error handling is sufficient
- You want the result as a string/bytes immediately
- The command is expected to complete quickly

For most simple cases where you just want to run a command and get its output, `check_output` is more convenient. For
anything more complex, `Popen` gives you the control you need.