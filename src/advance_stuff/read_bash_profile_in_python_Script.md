Yes, there are several ways to handle this. The issue is that `source setup_env.sh` sets environment variables that only
exist within that shell session, but they're not being passed to your Python script properly. setup_env.sh isa  copy of .bash_profile

Here are the best approaches:

## Option 1: Load the environment in Python directly

```python
import subprocess
import os


def load_env_from_script(script_path):
    """Load environment variables from a shell script"""
    # Run the script and capture the environment
    command = f"source {script_path} && env"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Parse the environment variables
    env_vars = {}
    for line in result.stdout.strip().split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            env_vars[key] = value

    return env_vars


# Load environment variables
env_vars = load_env_from_script('./setup_env.sh')

# Update current environment
os.environ.update(env_vars)

# Now run your script with the loaded environment
import my_script  # or exec(open('my_script.py').read())
```

## Option 2: Parse the setup script directly in Python

```python
import os
import re


def parse_env_file(file_path):
    """Parse environment variables from a shell script"""
    env_vars = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Handle export statements
            if line.startswith('export '):
                line = line[7:]  # Remove 'export '

            # Parse KEY=value
            if '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip('"\'')
                env_vars[key] = value

    return env_vars


# Load and set environment variables
env_vars = parse_env_file('./setup_env.sh')
os.environ.update(env_vars)

# Now run your script
exec(open('./my_script.py').read())
```

## Option 3: Fix the subprocess approach

```python
import subprocess

# Combine commands properly with shell=True
commands = "source setup_env.sh && python ./my_script.py"

process = subprocess.Popen(
    commands,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()

print("STDOUT:", stdout.decode())
print("STDERR:", stderr.decode())
print("Return code:", process.returncode)
```

## Option 4: Use python-dotenv (if setup_env.sh is simple)

If your `setup_env.sh` just sets environment variables:

```bash
pip install python-dotenv
```

Convert `setup_env.sh` to `.env` format:

```bash
# .env file
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your_api_key
```

Then in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # This loads .env file

# Now run your script
exec(open('./my_script.py').read())
```

## Option 5: Pass environment explicitly to subprocess

```python
import subprocess
import os


def get_env_from_script(script_path):
    """Get environment variables from sourcing a script"""
    cmd = f"source {script_path} && python -c 'import os; print(dict(os.environ))'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return eval(result.stdout.strip())


# Get the environment with setup_env.sh sourced
env_with_setup = get_env_from_script('./setup_env.sh')

# Run your script with this environment
process = subprocess.Popen(
    ['python', './my_script.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env_with_setup
)
stdout, stderr = process.communicate()
```

**Option 1 or 2 are usually the cleanest** since they keep everything in Python and make the environment loading
explicit. Choose based on whether your `setup_env.sh` is simple variable assignments or has more complex shell logic.