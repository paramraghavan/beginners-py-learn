# Check my python setup

- python -m site
- python -m site --user-site
- pip config list
- pip show <package>
- Check python being used by the current python console/env

```python
import sys

print(sys.executable)
```

- [env.md](env.md)
- [pipenv.md](pipenv.md)

## To list all Python installations on your PC, you can try the following methods:

- Using the command prompt or terminal:

  **On Windows:**
   ```
   where python
   ```

  **On macOS or Linux:**
   ```
   which -a python
   which -a python3
   ```
  These commands will show the paths of Python executables in your system PATH.

2. Check common installation directories:
   On Windows, look in:
    - C:\Python*
    - C:\Program Files\Python*
    - C:\Users\YourUsername\AppData\Local\Programs\Python

   On macOS or Linux, check:
    - /usr/bin/python*
    - /usr/local/bin/python*
    - /opt/homebrew/bin/python* (for Homebrew installations on macOS)

- Use the `py` launcher (Windows only):
   ```
   py -0
   ```
  This will list all Python versions registered with the py launcher.

- Check your system's package manager:

  On macOS with Homebrew:
   ```
   brew list | grep python
   ```

  On Linux (Ubuntu/Debian):
   ```
   dpkg --list | grep python
   ```

- Use a PowerShell script (Windows):

   ```powershell
   Get-ChildItem -Path C:\ -Include python.exe -File -Recurse -ErrorAction SilentlyContinue
   ```

  This will search for all `python.exe` files on your C drive.

## List/Print the dependencies for installed packages

```shell
# Method 1: Using pip show
pip show package_name
pip show package_name | grep Requires: --> direct dependencies
pip show package_name | grep Required-by: --> packages that depend on this one
# Example:
pip show requests   # Shows metadata including dependencies

# Method 2: Using pipdeptree
pip install pipdeptree
pipdeptree -p package_name  # Shows dependency tree for specific package
```

## List/Print the dependencies for not yet installed packages

```shell
# Method 1: Using pip show --no-deps
pip download package_name --no-deps
pip show --no-deps package_name.whl

# Method 2: Using yolk3k
pip install yolk3k
yolk -D package_name

# Method 3: Check PyPI website
# Visit https://pypi.org/project/package_name/

# Method 4: Using pip-tools
pip install pip-tools
pip-compile --no-annotate --no-emit-index-url <(echo "package_name")
```

> For installed packages: **pip show package_name**

> For uninstalled packages:
> Check the PyPI website or
> use pip download followed by pip show

## Custom script

- Checks if the package is installed before attempting analysis
- Option to automatically install missing packages
- Recursively install dependencies if needed
- Direct dependencies (immediately required by the package)
- All dependencies (including transitive/nested dependencies)

```shell
# analyze only
python [package_dependency_analyzer.py](package_dependency_analyzer.py) <package name>

# analyze and auto install as needed
python [package_dependency_analyzer.py](package_dependency_analyzer.py) <package name> --install
```

# Errors and how to handle

## Question

```text
I have python files in
folder1
folder2
foldern

file11.py on folder1 is import file21 from folder2
as
from folder2 import file21

getting error ModuleNotFoundError : No module named folder2 found
```

## Fix options

This is a common Python import error that occurs when trying to import modules from different directories. Let me help
you fix this issue.

There are several ways to solve this:

1. The simplest solution is to add an empty `__init__.py` file in each folder to make them Python packages:

```
.
├── folder1/
│   ├── __init__.py  (empty file)
│   └── file11.py
├── folder2/
│   ├── __init__.py  (empty file)
│   └── file21.py
└── foldern/
    └── __init__.py  (empty file)
```

2. Modify your import statement in file11.py to use relative imports:

```python
# In file11.py
from ..folder2 import file21
```

3. Add the parent directory to the Python path. You can do this by:

a) Adding this at the beginning of file11.py:

```python
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from folder2 import file21
```

b) Or setting the PYTHONPATH environment variable to include the parent directory:

```bash
# On Unix/Linux/MacOS
export PYTHONPATH="/path/to/parent/directory:$PYTHONPATH"

# On Windows
set PYTHONPATH=C:\path\to\parent\directory;%PYTHONPATH%
```

## Debug stacktrace 
strace -s 1024 > /tmp/why.txt -f python your_script.py