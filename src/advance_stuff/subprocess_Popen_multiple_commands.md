# How to run  three commands sequentially using `subprocess.Popen` by chaining them or using shell operators.

Here are a few approaches:

## Method 1: Single shell command with `&&`

```python
import subprocess

# Run all commands in sequence, stopping if any fails
process = subprocess.Popen(
    "./setup_env.sh && export HADOOP_HOME=hadoop && ./script",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()
```

## Method 2: Multiple Popen calls with wait()

```python
import subprocess

# Run setup_env.sh first
p1 = subprocess.Popen("./setup_env.sh", shell=True)
p1.wait()  # Wait for completion

# Set environment variable and run script
p2 = subprocess.Popen(
    "export HADOOP_HOME=hadoop && ./script",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = p2.communicate()
```

## Method 3: Using environment parameter

```python
import subprocess
import os

# Run setup_env.sh first
p1 = subprocess.Popen("./setup_env.sh", shell=True)
p1.wait()

# Create environment with HADOOP_HOME set
env = os.environ.copy()
env['HADOOP_HOME'] = 'hadoop'

# Run script with modified environment
p2 = subprocess.Popen(
    "./script",
    shell=True,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = p2.communicate()
```

**Method 1** is probably the simplest since it runs everything in one shell session, preserving environment variables
between commands. The `&&` operator ensures each command only runs if the previous one succeeded.

# Can we use '\n' as a separator

Yes, you can use newlines to separate the commands. Here are a few ways to do it:

## Method 1: Multi-line string with shell=True

```python
import subprocess

commands = """
./setup_env.sh
export HADOOP_HOME=hadoop
./script
"""

process = subprocess.Popen(
    commands,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()
```

## Method 2: Using semicolons with newlines for readability

```python
import subprocess

commands = """
./setup_env.sh;
export HADOOP_HOME=hadoop;
./script
"""

process = subprocess.Popen(
    commands,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()
```

## Method 3: Join commands with newlines

```python
import subprocess

commands = [
    "./setup_env.sh",
    "export HADOOP_HOME=hadoop",
    "./script"
]

command_string = "\n".join(commands)

process = subprocess.Popen(
    command_string,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()
```

**Note**: When using newlines in shell commands, each line is executed sequentially, but unlike `&&`, if one command
fails, the subsequent commands will still execute. If you want to stop execution on failure, you should still use `&&`
or add `set -e` at the beginning of your command string.