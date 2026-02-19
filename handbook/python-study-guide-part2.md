## Chapter 6: Error Handling & Exceptions

### 6.1 Why Error Handling Matters

Without error handling, your program crashes the moment something goes wrong. With it, you can gracefully handle problems and keep running.

```python
# Without error handling - program crashes
user_input = "not a number"
number = int(user_input)  # ValueError: invalid literal for int()
print("This never executes")

# With error handling - program continues
try:
    number = int(user_input)
    print(f"You entered: {number}")
except ValueError:
    print("That's not a valid number!")
print("Program continues running...")
```

### 6.2 try / except / else / finally

Here's the full anatomy:

```python
def divide(a, b):
    try:
        # Code that MIGHT raise an exception
        result = a / b

    except ZeroDivisionError:
        # Handle specific exception
        print("Error: Cannot divide by zero!")
        return None

    except TypeError as e:
        # Catch the exception object to see the error message
        print(f"Error: Wrong types - {e}")
        return None

    except (ValueError, ArithmeticError) as e:
        # Catch multiple exception types
        print(f"Math error: {e}")
        return None

    except Exception as e:
        # Catch ANY exception (use as last resort)
        print(f"Unexpected error: {e}")
        return None

    else:
        # Runs ONLY if NO exception occurred
        # This is the "happy path"
        print(f"Success! {a} / {b} = {result}")
        return result

    finally:
        # ALWAYS runs, whether there was an exception or not
        # Use for cleanup (closing files, database connections, etc.)
        print("Division operation complete.")

# Test it:
divide(10, 3)     # Success! 10 / 3 = 3.333... / Division operation complete.
divide(10, 0)     # Error: Cannot divide by zero! / Division operation complete.
divide("10", 3)   # Error: Wrong types... / Division operation complete.
```

**When to use each block:**
- `try`: Code that might fail
- `except`: Handle specific errors
- `else`: Code that should run only on success (keeps try block minimal)
- `finally`: Cleanup that must always happen (closing files, connections)

### 6.3 Common Built-in Exceptions

```python
# ValueError - wrong value for the type
int("hello")              # ValueError

# TypeError - wrong type
"hello" + 42              # TypeError

# KeyError - dict key not found
d = {"a": 1}
d["b"]                    # KeyError

# IndexError - list index out of range
lst = [1, 2, 3]
lst[10]                   # IndexError

# AttributeError - object doesn't have that attribute
"hello".nonexistent()     # AttributeError

# FileNotFoundError - file doesn't exist
open("nonexistent.txt")   # FileNotFoundError

# ImportError - can't import module
import nonexistent_module  # ModuleNotFoundError (subclass of ImportError)

# ZeroDivisionError
10 / 0                    # ZeroDivisionError

# NameError - variable not defined
print(undefined_variable)  # NameError
```

### 6.4 Custom Exceptions

Create your own exceptions for your application's specific errors:

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, field, message, value=None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"Validation failed for '{field}': {message}")

class NotFoundError(Exception):
    """Raised when a resource is not found."""
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} with id '{resource_id}' not found")

class InsufficientFundsError(Exception):
    """Raised when account balance is too low."""
    pass

# Usage
def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("age", "must be an integer", age)
    if age < 0:
        raise ValidationError("age", "cannot be negative", age)
    if age > 150:
        raise ValidationError("age", f"unrealistic value: {age}", age)
    return age

def get_user(user_id):
    users = {"1": "Alice", "2": "Bob"}
    if user_id not in users:
        raise NotFoundError("User", user_id)
    return users[user_id]

# Using them:
try:
    validate_age(-5)
except ValidationError as e:
    print(f"Caught: {e}")
    print(f"  Field: {e.field}")
    print(f"  Value: {e.value}")
# Caught: Validation failed for 'age': cannot be negative
#   Field: age
#   Value: -5

try:
    get_user("999")
except NotFoundError as e:
    print(f"Caught: {e}")
    print(f"  Type: {e.resource_type}, ID: {e.resource_id}")
```

### 6.5 Exception Handling with Logging (Production Pattern)

```python
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(data):
    """Production-grade error handling pattern."""
    try:
        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")

        # Process
        result = transform(data)
        logger.info(f"Successfully processed {len(data)} items")
        return result

    except ValueError as e:
        # Known, expected errors - log as warning
        logger.warning(f"Invalid input: {e}")
        return None

    except ConnectionError as e:
        # Transient errors - might want to retry
        logger.error(f"Connection failed: {e}")
        raise  # Re-raise so caller can decide to retry

    except Exception:
        # Unknown errors - log full traceback for debugging
        logger.error(f"Unexpected error processing data:\n{traceback.format_exc()}")
        raise  # Re-raise unknown errors (don't swallow them!)
```

### 6.6 Exception Handling Decorator (Reusable Pattern)

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Retry decorator - retries function on failure.

    Args:
        max_attempts: Maximum number of tries
        delay: Seconds between retries
        exceptions: Tuple of exception types to catch

    Usage:
        @retry(max_attempts=3, delay=2)
        def flaky_api_call():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                        print(f"  Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print(f"  All {max_attempts} attempts failed!")
            raise last_exception
        return wrapper
    return decorator

# Usage:
import random

@retry(max_attempts=3, delay=1)
def unreliable_api_call():
    """Simulates a flaky API that fails randomly."""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Server unavailable")
    return {"status": "success", "data": [1, 2, 3]}

# This will retry up to 3 times:
try:
    result = unreliable_api_call()
    print(f"Got result: {result}")
except ConnectionError:
    print("API is down, giving up.")
```

### Exercise 6.1: Build a Robust Input Validator
Write a function `get_valid_number()` that keeps asking the user for input until they enter a valid number between 1 and 100.

<details>
<summary>Solution</summary>

```python
def get_valid_number(prompt="Enter a number (1-100): "):
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 100:
                return value
            else:
                print(f"  {value} is out of range. Must be 1-100.")
        except ValueError:
            print("  That's not a valid number. Try again.")
        except KeyboardInterrupt:
            print("\n  Cancelled.")
            return None

number = get_valid_number()
if number:
    print(f"You chose: {number}")
```
</details>

---

## Chapter 7: File I/O & Serialization

### 7.1 Reading and Writing Text Files

```python
# ===== WRITING =====

# Write (creates file or OVERWRITES existing)
with open("output.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")

# Write multiple lines
lines = ["Hello\n", "World\n", "Python\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)

# Append (adds to end of file)
with open("output.txt", "a") as f:
    f.write("Appended line\n")

# ===== READING =====

# Read entire file as one string
with open("output.txt", "r") as f:
    content = f.read()
    print(content)

# Read all lines into a list
with open("output.txt", "r") as f:
    lines = f.readlines()  # Each line includes \n
    for line in lines:
        print(line.strip())  # strip() removes \n

# Read line by line (memory efficient for large files)
with open("output.txt", "r") as f:
    for line in f:  # f is an iterator - reads one line at a time
        print(line.strip())

# Read first N lines
with open("output.txt", "r") as f:
    for i, line in enumerate(f):
        if i >= 5:  # Read only first 5 lines
            break
        print(line.strip())
```

**The `with` statement** - why you should always use it:

```python
# WITHOUT with (bad - you might forget to close)
f = open("file.txt", "r")
content = f.read()
f.close()  # Easy to forget, especially if an error occurs above

# WITH with (good - auto-closes even if error occurs)
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed here, even if an exception happened
```

### 7.2 pathlib - Modern File Operations

`pathlib` is the modern, Pythonic way to work with file paths:

```python
from pathlib import Path

# Create path objects
p = Path("data/output.txt")
home = Path.home()           # /Users/username (Mac) or C:\Users\username (Win)
cwd = Path.cwd()             # Current working directory

# Path properties
print(p.name)       # "output.txt"
print(p.stem)       # "output"
print(p.suffix)     # ".txt"
print(p.parent)     # "data"
print(p.exists())   # True or False
print(p.is_file())  # True if it's a file
print(p.is_dir())   # True if it's a directory

# Create directories
Path("data/processed").mkdir(parents=True, exist_ok=True)
# parents=True: create parent dirs too
# exist_ok=True: don't error if already exists

# Read and write (simple!)
p = Path("data/output.txt")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("Hello from pathlib!")
content = p.read_text()
print(content)

# Find files
for py_file in Path(".").rglob("*.py"):       # Recursive glob
    print(py_file)

for txt_file in Path("data").glob("*.txt"):    # Non-recursive
    print(txt_file)

# Join paths (works across OS)
config_path = Path.home() / ".config" / "myapp" / "settings.json"
```

### 7.3 JSON

JSON is the most common format for data exchange:

```python
import json

# ===== Python dict <-> JSON string =====

data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"],
    "address": {
        "city": "NYC",
        "state": "NY"
    }
}

# Python -> JSON string
json_str = json.dumps(data)
print(json_str)
# {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"], ...}

# Pretty-printed JSON
json_pretty = json.dumps(data, indent=2)
print(json_pretty)

# JSON string -> Python dict
parsed = json.loads(json_str)
print(parsed["name"])   # "Alice"
print(parsed["hobbies"][0])  # "reading"

# ===== JSON files =====

# Write to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read from file
with open("data.json", "r") as f:
    loaded = json.load(f)
```

### 7.4 CSV

```python
import csv

# ===== Writing CSV =====
with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "Grade"])   # Header
    writer.writerow(["Alice", 30, "A"])
    writer.writerow(["Bob", 25, "B"])
    writer.writerow(["Charlie", 35, "A"])

# ===== Reading CSV =====
with open("students.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)     # Read header row
    print(f"Columns: {header}")
    for row in reader:
        print(f"  {row[0]}, age {row[1]}, grade {row[2]}")

# ===== DictReader (much nicer - access by column name) =====
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['Name']}: {row['Grade']}")
```

### 7.5 YAML

```python
# pip install pyyaml
import yaml

# Read YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)  # Always use safe_load!

# Write YAML
with open("output.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False)

# Example YAML file (config.yaml):
# database:
#   host: localhost
#   port: 5432
#   name: mydb
# features:
#   - logging
#   - caching
```

### 7.6 Pickle (Python Object Serialization)

```python
import pickle

# Pickle can serialize ANY Python object
data = {
    "model_weights": [0.5, 0.3, 0.2],
    "metadata": {"version": "1.0", "created": "2024-01-15"},
    "history": [(1, 0.9), (2, 0.95), (3, 0.97)]
}

# Save
with open("model.pkl", "wb") as f:  # 'wb' = write binary
    pickle.dump(data, f)

# Load
with open("model.pkl", "rb") as f:  # 'rb' = read binary
    loaded = pickle.load(f)

print(loaded["model_weights"])  # [0.5, 0.3, 0.2]
```

> **SECURITY WARNING**: Never unpickle data from untrusted sources! Pickle can execute arbitrary code. Use JSON for data exchange between systems.

### Exercise 7.1: CSV to JSON Converter
Read a CSV file, transform the data, and write to JSON:

<details>
<summary>Solution</summary>

```python
import csv
import json

def csv_to_json(csv_path, json_path):
    records = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    with open(json_path, "w") as f:
        json.dump(records, f, indent=2)

    print(f"Converted {len(records)} records from {csv_path} to {json_path}")

csv_to_json("students.csv", "students.json")
```
</details>

---

## Chapter 8: Modules, Packages & Imports

### 8.1 What Are Modules and Packages?

| Term | What it is | Example |
|---|---|---|
| **Module** | A single `.py` file | `math.py`, `utils.py` |
| **Package** | A folder with `__init__.py` containing modules | `requests/`, `pandas/` |
| **Library** | A collection of packages (installed via pip) | `pandas`, `flask` |
| **Framework** | An opinionated library that controls the structure | `Django`, `FastAPI` |

### 8.2 Import Styles

```python
# Import the entire module
import os
print(os.path.exists("/tmp"))

# Import specific things from a module
from pathlib import Path
from collections import defaultdict, Counter

# Import with an alias (common for data science)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import everything (AVOID - clutters namespace)
# from os import *  # Don't do this in production code
```

### 8.3 Creating Your Own Package

```
myproject/
├── mypackage/
│   ├── __init__.py       # Makes this directory a package
│   ├── utils.py
│   ├── models.py
│   └── subpackage/
│       ├── __init__.py
│       └── helpers.py
├── main.py
└── tests/
    └── test_utils.py
```

```python
# mypackage/__init__.py
"""My package - does amazing things."""

# Control what gets imported with "from mypackage import *"
__all__ = ["utils", "models"]

# Convenience imports (so users can do: from mypackage import MyClass)
from .utils import useful_function
from .models import MyModel

__version__ = "1.0.0"
```

```python
# mypackage/utils.py
def useful_function(x):
    return x * 2
```

```python
# main.py
from mypackage import useful_function
from mypackage.models import MyModel
```

### 8.4 `__name__` and `__main__`

Every Python file has a special variable `__name__`:
- When run directly: `__name__` is `"__main__"`
- When imported: `__name__` is the module's name

```python
# mymodule.py
def main():
    print("Running as main program")

def helper():
    print("I'm a helper function")

# This block only runs when the file is executed directly
# NOT when imported by another module
if __name__ == "__main__":
    main()
```

```python
# another_file.py
import mymodule          # Does NOT run main()
mymodule.helper()       # Can use the functions
```

### 8.5 Import Order (PEP 8)

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports (installed via pip)
import pandas as pd
import numpy as np
import requests

# 3. Local application imports
from mypackage import utils
from mypackage.models import UserModel
```

---

## Chapter 9: Python Environment, pip & Dependency Management

### 9.1 Virtual Environments: Why and How

**Why**: Without virtual environments, all projects share the same Python packages. Project A might need `requests==2.28` while Project B needs `requests==2.31`. Virtual environments isolate each project's dependencies.

```bash
# CREATE a virtual environment
python -m venv .venv

# ACTIVATE it
# Mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Your prompt changes to show (.venv):
# (.venv) $ python --version

# INSTALL packages (only affects this virtual environment)
pip install requests pandas

# DEACTIVATE when done
deactivate
```

### 9.2 pip - Python Package Manager

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.28.0

# Install a version range
pip install "requests>=2.28,<3.0"

# pip install vs python -m pip install
# IMPORTANT: Always prefer python -m pip install
# This ensures you're using the pip for YOUR Python, not some other one
python -m pip install requests

# Upgrade a package
pip install --upgrade requests

# See what's installed
pip list
pip show requests    # Detailed info about one package

# Save your project's dependencies
pip freeze > requirements.txt

# Install from requirements file (reproduce environment)
pip install -r requirements.txt

# Uninstall
pip uninstall requests
```

### 9.3 Common pip Issues & How to Fix Them

**Issue: "pip: command not found"**
```bash
# Use python -m pip instead:
python -m pip install package_name
# Or upgrade pip:
python -m pip install --upgrade pip
```

**Issue: Permission denied**
```bash
# Option 1: Use --user (installs just for your user)
pip install --user package_name

# Option 2 (RECOMMENDED): Use a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install package_name
```

**Issue: SSL certificate error (common behind corporate firewalls)**
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org package_name
```

**Issue: Wrong package installed (e.g., `jwt` vs `PyJWT`)**
```bash
# Diagnose: check what you actually have
python -c "import jwt; print(jwt.__file__); print(dir(jwt))"

# Fix: remove wrong package, install correct one
pip uninstall jwt PyJWT
pip install PyJWT
```

**Issue: Dependency conflict**
```bash
# Force reinstall one package (ignoring dependencies)
pip install --force-reinstall --no-deps package_name

# Nuclear option: reinstall everything
pip install --force-reinstall package_name
```

**Issue: "externally-managed-environment" (newer Ubuntu/macOS)**
```bash
# This means your OS protects system Python. ALWAYS use virtual envs:
python -m venv .venv
source .venv/bin/activate
pip install package_name
```

### 9.4 Pipenv (Better Dependency Management)

Pipenv combines `pip` + `virtualenv` into one tool:

```bash
# Install pipenv
pip install pipenv

# Start a new project (creates Pipfile + virtual env)
pipenv install requests

# Install dev-only packages
pipenv install pytest --dev

# Activate the virtual environment
pipenv shell

# Run a command in the virtual env (without activating)
pipenv run python script.py
pipenv run pytest tests/

# Lock dependencies for reproducible builds
pipenv lock

# Install everything from Pipfile.lock
pipenv install

# Convert existing requirements.txt to Pipfile
pipenv install -r requirements.txt

# Remove virtual environment
pipenv --rm
```

---

## Chapter 10: Debugging & Profiling

This is one of the most important skills for any developer. Let's cover every technique from simple to advanced.

### 10.1 Print Debugging (The Basics)

The simplest debugging technique. Good for quick checks, but remove before committing:

```python
def calculate_total(items):
    print(f"DEBUG: items received = {items}")  # What did we get?

    total = 0
    for item in items:
        print(f"DEBUG: processing item = {item}")  # What are we processing?
        price = item["price"] * item["quantity"]
        print(f"DEBUG: price for {item['name']} = {price}")  # Intermediate result
        total += price

    print(f"DEBUG: final total = {total}")  # Final result
    return total

# Better: use f-strings with variable names
x = 42
print(f"{x = }")  # Output: x = 42  (Python 3.8+)

items = [1, 2, 3]
print(f"{len(items) = }")  # Output: len(items) = 3
```

### 10.2 pdb - Python Debugger (Step-by-Step Guide)

pdb lets you pause your program and inspect everything interactively. This is **much more powerful** than print debugging.

**How to start pdb:**

```python
# Method 1: Add breakpoint() where you want to pause (Python 3.7+)
def calculate_discount(price, discount_pct):
    breakpoint()  # Program pauses here
    discount = price * discount_pct / 100
    final_price = price - discount
    return final_price

result = calculate_discount(100, 20)
```

```python
# Method 2: Old style (works on all Python 3 versions)
import pdb

def calculate_discount(price, discount_pct):
    pdb.set_trace()  # Same effect as breakpoint()
    discount = price * discount_pct / 100
    final_price = price - discount
    return final_price
```

**When you run this, you'll see the pdb prompt:**

```
> /path/to/script.py(3)calculate_discount()
-> discount = price * discount_pct / 100
(Pdb)
```

**Now you can type commands. Here's a complete walkthrough:**

```
(Pdb) p price            # PRINT a variable's value
100
(Pdb) p discount_pct     # Print another variable
20
(Pdb) p price * discount_pct / 100    # Print ANY expression
20.0
(Pdb) pp locals()        # PRETTY-PRINT all local variables
{'discount_pct': 20, 'price': 100}

(Pdb) n                  # NEXT - execute current line, move to next
> /path/to/script.py(4)calculate_discount()
-> final_price = price - discount

(Pdb) p discount         # Now 'discount' exists
20.0

(Pdb) n                  # Execute this line too
> /path/to/script.py(5)calculate_discount()
-> return final_price

(Pdb) p final_price      # Check the result
80.0

(Pdb) c                  # CONTINUE - run until next breakpoint or end
```

**Complete pdb command reference:**

| Command | Short | What it does | Example |
|---|---|---|---|
| `print(expr)` | `p expr` | Print a value | `p my_variable` |
| `pp expr` | | Pretty-print (for dicts, lists) | `pp my_dict` |
| `next` | `n` | Execute current line, go to next | |
| `step` | `s` | Step INTO a function call | |
| `continue` | `c` | Run until next breakpoint | |
| `list` | `l` | Show code around current line | `l 1, 20` (lines 1-20) |
| `longlist` | `ll` | Show entire current function | |
| `where` | `w` | Show call stack (who called what) | |
| `up` | `u` | Go UP one level in call stack | |
| `down` | `d` | Go DOWN one level in call stack | |
| `break` | `b` | Set a breakpoint | `b 42` (line 42), `b my_func` |
| `clear` | `cl` | Remove breakpoints | `cl 1` (breakpoint #1) |
| `return` | `r` | Run until current function returns | |
| `quit` | `q` | Quit debugger | |
| `!statement` | | Execute Python statement | `!x = 42` |
| `whatis expr` | | Show type of expression | `whatis my_var` |

**Real debugging session example:**

Say you have a bug - the function returns wrong results:

```python
def find_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    average = total / len(numbers) + 1  # Bug! The +1 is wrong
    return average

# Let's debug:
def find_average(numbers):
    breakpoint()  # ADD THIS
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    average = total / len(numbers) + 1
    return average

result = find_average([10, 20, 30])
print(f"Average: {result}")  # Prints 21.0, but should be 20.0
```

```
# Run the script, pdb starts:

(Pdb) n                    # Skip past total = 0
(Pdb) n                    # Enter the for loop
(Pdb) n                    # Execute total += numbers[i]
(Pdb) p total              # Check total after first iteration
10
(Pdb) c                    # Continue (but we want to see more...)

# Better approach - set a breakpoint AFTER the loop:
(Pdb) b 6                 # Set breakpoint at line 6 (the average line)
(Pdb) c                    # Continue to that breakpoint
(Pdb) p total              # Check total
60
(Pdb) p len(numbers)       # Check count
3
(Pdb) p total / len(numbers)  # What should average be?
20.0
(Pdb) p total / len(numbers) + 1  # What IS the average (with bug)?
21.0
# AHA! The + 1 is the bug!
```

**Step vs Next - the important difference:**

```python
def helper(x):
    return x * 2

def main():
    breakpoint()
    result = helper(5)  # Line we're about to execute
    print(result)
```

```
# At the breakpoint:
(Pdb) n    # NEXT: executes helper(5) completely, stops at print(result)
           # You DON'T go inside helper()

(Pdb) s    # STEP: goes INSIDE helper(5), stops at "return x * 2"
           # You CAN inspect x inside helper
```

**Post-mortem debugging** - debug AFTER a crash:

```bash
# Run with -m pdb to auto-enter debugger on crash:
python -m pdb my_script.py

# When it crashes, you're dropped into pdb at the crash site
# You can inspect all variables to understand what went wrong
```

### 10.3 Logging (Production-Grade Debugging)

Print statements get removed before deployment. Logging is permanent and configurable.

**Basic logging:**

```python
import logging

# Configure logging (do this ONCE, at the top of your main script)
logging.basicConfig(
    level=logging.DEBUG,       # Show all messages DEBUG and above
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Log at different levels:
logger.debug("Detailed info for diagnosing problems")
logger.info("General operational info")
logger.warning("Something unexpected but not fatal")
logger.error("Something failed!")
logger.critical("System is unusable!")

# Output:
# 2024-03-15 14:30:00 [DEBUG] __main__: Detailed info for diagnosing problems
# 2024-03-15 14:30:00 [INFO] __main__: General operational info
# ...
```

**Log levels (from least to most severe):**

| Level | When to use | Example |
|---|---|---|
| `DEBUG` | Detailed diagnostic info | `logger.debug(f"Processing item {i}: {item}")` |
| `INFO` | General operational events | `logger.info("Server started on port 8080")` |
| `WARNING` | Something unexpected | `logger.warning("Disk space below 10%")` |
| `ERROR` | Something failed | `logger.error("Failed to connect to database")` |
| `CRITICAL` | System is unusable | `logger.critical("Out of memory!")` |

**Production logging setup** (log to file + console):

```python
import logging
import logging.handlers

def setup_logging(log_file="app.log", level=logging.INFO):
    """Set up production-grade logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture everything

    # Format
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler - show INFO and above
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler - log EVERYTHING, rotate at 10MB, keep 5 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Usage
logger = setup_logging()
logger.info("Application started")
```

### 10.4 Decorator for Logging and Timing

This is a pattern used extensively in production Python code:

```python
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_calls(func):
    """Decorator that logs function calls, return values, and execution time.

    Usage:
        @log_calls
        def my_function(x, y):
            return x + y

    When you call my_function(3, 4), it logs:
        CALL my_function(args=(3, 4), kwargs={})
        RETURN my_function -> 7 [0.0001s]
    """
    @wraps(func)  # Preserves function name and docstring
    def wrapper(*args, **kwargs):
        # Log the call
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"CALL {func.__name__}({signature})")

        # Execute and time
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.info(f"RETURN {func.__name__} -> {result!r} [{elapsed:.4f}s]")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            logger.error(f"ERROR {func.__name__} raised {type(e).__name__}: {e} [{elapsed:.4f}s]")
            raise

    return wrapper

# Usage:
@log_calls
def calculate_tax(amount, rate=0.08):
    return round(amount * rate, 2)

@log_calls
def process_order(items):
    total = sum(item["price"] for item in items)
    tax = calculate_tax(total)
    return total + tax

# When you call:
result = process_order([{"price": 10}, {"price": 20}])
# You see in the logs:
# CALL process_order([{'price': 10}, {'price': 20}])
# CALL calculate_tax(30, rate=0.08)
# RETURN calculate_tax -> 2.4 [0.0000s]
# RETURN process_order -> 32.4 [0.0001s]
```

### 10.5 Who Called Me? (Call Stack Inspection)

When debugging, it's useful to know WHO called a function:

```python
import inspect

def who_called_me():
    """Print information about the caller."""
    frame = inspect.currentframe().f_back  # Go up one level
    caller_name = frame.f_code.co_name
    caller_file = frame.f_code.co_filename
    caller_line = frame.f_lineno
    print(f"Called by: {caller_name}() at {caller_file}:{caller_line}")

def my_function():
    who_called_me()

def another_function():
    my_function()

# Run it:
another_function()
# Output: Called by: my_function() at script.py:12

# See the full call stack:
def show_call_stack():
    """Print the entire call stack."""
    print("Call stack (most recent call last):")
    for i, frame_info in enumerate(inspect.stack()):
        frame = frame_info[0]
        print(f"  {i}: {frame.f_code.co_name}() "
              f"at {frame.f_code.co_filename}:{frame.f_lineno}")
```

### 10.6 Python trace Module

The `trace` module shows every line of code as it executes:

```bash
# Trace every line executed in your script
python -m trace --trace script.py

# Example output:
#  --- modulename: script, funcname: calculate
# script.py(3):     total = 0
# script.py(4):     for i in range(len(numbers)):
# script.py(5):         total += numbers[i]
# script.py(4):     for i in range(len(numbers)):
# script.py(5):         total += numbers[i]
# ...

# Show which functions were called (less verbose)
python -m trace --listfuncs script.py

# Count how many times each line was executed
python -m trace --count script.py

# Verbose import tracing (see which modules are loaded)
python -v script.py
```

**Using trace programmatically:**

```python
import sys

def trace_calls(frame, event, arg):
    """Custom tracer that shows function calls."""
    if event == 'call':
        filename = frame.f_code.co_filename
        funcname = frame.f_code.co_name
        lineno = frame.f_lineno
        # Only trace our own code (not library code)
        if 'site-packages' not in filename:
            print(f"CALL: {funcname}() at {filename}:{lineno}")
    return trace_calls

# Enable tracing
sys.settrace(trace_calls)

# Your code here...
def hello(name):
    return f"Hello, {name}!"

result = hello("World")

# Disable tracing
sys.settrace(None)
```

### 10.7 strace / dtrace (System-Level Debugging)

When Python-level debugging isn't enough, you can trace system calls (file opens, network connections, etc.):

```bash
# Linux: see what files Python opens
strace -e trace=open,openat python script.py

# Linux: see network activity
strace -e trace=network python script.py

# macOS: use dtruss
sudo dtruss python script.py

# Useful for:
# - "Why can't Python find my module?" -> see which paths it searches
# - "Why is this script slow?" -> see unexpected disk or network I/O
# - "Permission denied errors" -> see which files it's trying to access
```

### 10.8 Visual Code Tracer (From This Repository)

This repository includes a powerful visual tracing tool that shows function calls in a web browser:

```python
# Copy visual_tracer.py from quick101/debugging/visual_code_tracer/
# Then in your code:

from visual_tracer import trace

# Basic - trace everything
trace()

# Now write your code normally:
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(result)

# A browser window opens at http://localhost:5050 showing:
# - Every function call in real-time
# - Call duration (how long each function took)
# - Call depth (how deep in the call stack)
# - Source code viewing (click to see code)
```

**Filtering (so you don't get overwhelmed):**

```python
# Only trace your code (skip third-party libraries)
trace(only_user_code=True)

# Only trace specific modules
trace(include_modules=["myapp.utils", "myapp.api"])

# Trace all modules starting with "myapp"
trace(include_modules=["myapp.*"])

# Skip test modules
trace(exclude_modules=["*.tests", "*.test_*"])

# Only show slow calls (>100ms)
trace(min_duration_ms=100)

# Combine filters
trace(
    include_modules=["myapp.*"],
    exclude_modules=["myapp.tests.*"],
    only_user_code=True,
    min_duration_ms=10
)
```

### 10.9 Profiling (Finding Performance Bottlenecks)

**cProfile** - find which functions are slow:

```python
import cProfile
import pstats

# Method 1: Profile a function call
cProfile.run('my_slow_function()')

# Method 2: Profile a block of code
profiler = cProfile.Profile()
profiler.enable()

# ... your code here ...
result = process_large_dataset(data)

profiler.disable()

# Print the top 10 slowest functions
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')  # Sort by total time
stats.print_stats(10)           # Show top 10

# Output looks like:
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.056    0.056 script.py:28(big_loop)
#    120002    0.039    0.000    0.039    0.000 script.py:33(<genexpr>)
#         2    0.016    0.008    0.055    0.028 {method 'join' of 'str'}
#
# Columns:
#   ncalls:  how many times the function was called
#   tottime: time spent IN this function (not counting sub-calls)
#   cumtime: time spent in this function INCLUDING sub-calls
```

**Command-line profiling:**

```bash
# Save profile data
python -m cProfile -o profile.pstats script.py

# Visualize with snakeviz (interactive browser UI)
pip install snakeviz
snakeviz profile.pstats

# Visualize with gprof2dot (generates an image)
pip install gprof2dot
brew install graphviz  # macOS
gprof2dot -f pstats profile.pstats | dot -Tpng -o profile.png

# Timeline profiling with viztracer
pip install viztracer
viztracer script.py
vizviewer result.json
```

**Quick timing** - measure how long something takes:

```python
from time import perf_counter

# Time a block of code
start = perf_counter()
result = sum(range(1_000_000))
elapsed = perf_counter() - start
print(f"Took {elapsed:.4f} seconds")

# In Jupyter notebooks:
# %timeit [x**2 for x in range(1000)]     # Time one expression (runs many times)
# %%time                                    # Time an entire cell (runs once)
# slow_function()
```

### 10.10 Debugging Cheat Sheet

| Situation | Tool | Command |
|---|---|---|
| Quick value check | Print | `print(f"{var = }")` |
| Step through code | pdb | `breakpoint()` then `n`, `s`, `c` |
| Inspect after crash | pdb post-mortem | `python -m pdb script.py` |
| See every line executed | trace | `python -m trace --trace script.py` |
| Find slow functions | cProfile | `python -m cProfile script.py` |
| Visual slow-function analysis | snakeviz | `snakeviz profile.pstats` |
| See system calls | strace/dtruss | `strace python script.py` |
| Visual live tracing | visual_tracer | `trace(only_user_code=True)` |
| Production debugging | logging | `logger.debug(f"x={x}")` |
| Find who called a function | inspect | `inspect.stack()` |
| Module loading issues | verbose | `python -v script.py` |

### Exercise 10.1: Debug This Function

This function has a bug. Use `breakpoint()` and pdb to find it:

```python
def calculate_average_grade(students):
    """Calculate the average grade for all students."""
    total = 0
    count = 0
    for student in students:
        if student["grade"] is not None:
            total += student["grade"]
    count += 1  # BUG: this is outside the if block!
    return total / count if count > 0 else 0

students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob", "grade": 80},
    {"name": "Charlie", "grade": None},
    {"name": "Diana", "grade": 85},
]

print(calculate_average_grade(students))  # Should be 85, but isn't!
```

<details>
<summary>Solution</summary>

The bug is that `count += 1` is outside the `if` block and outside the `for` loop. It should be inside both:

```python
def calculate_average_grade(students):
    total = 0
    count = 0
    for student in students:
        if student["grade"] is not None:
            total += student["grade"]
            count += 1  # FIXED: now inside the if block AND the for loop
    return total / count if count > 0 else 0
```

Using pdb to find the bug:
1. Add `breakpoint()` before the return
2. Check `total` (255) and `count` (1 - wrong, should be 3!)
3. Realize count is only incremented once because it's outside the loop
</details>

### Exercise 10.2: Profile and Optimize

Profile this code, find the bottleneck, and optimize it:

```python
def slow_search(data, target):
    """Find all indices where target appears."""
    indices = []
    for i in range(len(data)):
        for j in range(len(data)):  # BUG: why are we scanning the whole list again?
            if data[i] == target:
                indices.append(i)
                break
    return indices

import random
data = [random.randint(0, 100) for _ in range(10000)]
result = slow_search(data, 42)
```

<details>
<summary>Solution</summary>

```python
# Optimized: single pass O(n)
def fast_search(data, target):
    return [i for i, val in enumerate(data) if val == target]

# Or even simpler for just counting:
# count = data.count(42)
```
</details>
