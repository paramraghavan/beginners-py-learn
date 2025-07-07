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
# Executes the script in a new subprocess
# Separate environment - changes don't affect the parent shell
# Environment variables set in the script are lost when the subprocess ends
p1 = subprocess.Popen("./setup_env.sh", shell=True)

# Blocks execution - your Python script pauses at this line
# Waits for completion - doesn't return until the subprocess finishes
# Returns exit code - gives you the process's return code (0 for success, non-zero for failure)
exit_code = p1.wait()

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

## Using `subprocess.check_output()` for long-running ETL processes

Using `subprocess.check_output()` for long-running ETL processes like `spark-submit` has several significant drawbacks
that make it generally not recommended:

**Problems with check_output():**

1. **No real-time output** - You won't see any logs or progress until the entire process completes, making it impossible
   to monitor long-running jobs
2. **Memory issues** - All output is buffered in memory, which can be problematic for verbose Spark jobs
3. **No timeout handling** - If your Spark job hangs, your Python process will hang indefinitely
4. **Poor error handling** - You only get error information after the process fails completely

**Better alternatives:**

```python
import subprocess
import sys


# Option 1: Real-time output with Popen
def run_spark_job_with_output(spark_command):
    process = subprocess.Popen(
        spark_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    for line in iter(process.stdout.readline, ''):
        print(line.strip())
        sys.stdout.flush()

    process.wait()
    return process.returncode


# Option 2: Using subprocess.run() with streaming
def run_spark_job_streaming(spark_command):
    result = subprocess.run(
        spark_command,
        capture_output=False,  # Let output go directly to terminal
        text=True,
        timeout=3600  # 1 hour timeout
    )
    return result.returncode
```

**For production ETL pipelines, consider:**

- **Apache Airflow** - Better orchestration, monitoring, and retry logic
- **Prefect** - Modern workflow management
- **Direct Spark APIs** - Using `pyspark` directly instead of `spark-submit`
- **Kubernetes operators** - For containerized Spark jobs

The key is having visibility into your long-running processes and proper error handling, which `check_output()` doesn't
provide.