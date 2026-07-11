# Python Packaging And Environment Debugging Field Guide

This note is for beginners and experienced engineers who hit Python environment problems such as:

- `ModuleNotFoundError: No module named ...`
- `ImportError: cannot import name ...`
- `pip install` says a package is installed, but Python cannot import it
- Python imports the wrong version of a library
- VS Code, PyCharm, terminal, and Jupyter use different environments
- local code changes are not picked up
- `requirements.txt`, `pyproject.toml`, `setup.py`, and editable installs feel confusing

The main idea: most Python environment bugs are caused by one of these mismatches:

```text
Python you are running != pip you used to install packages
Python import path != folder where your code/package lives
IDE/Jupyter interpreter != terminal interpreter
installed package copy != local source code you are editing
```

## 1. The Fast Diagnosis Checklist

Run these commands in the same terminal where the problem happens:

```bash
which python
which python3
python --version
python -m pip --version
python -m pip list
python -m site
```

Then run this small Python check:

```bash
python - <<'PY'
import sys
import site

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("\nFirst import paths:")
for path in sys.path[:10]:
    print(" -", path)
print("\nsite-packages:")
for path in site.getsitepackages():
    print(" -", path)
PY
```

If you are debugging a specific package:

```bash
python -m pip show requests
python -c "import requests; print(requests.__file__)"
```

Replace `requests` with the package you care about.

## 2. Mental Model: Python Has Two Separate Problems

Python setup problems usually involve two different systems.

### Package Installation

This is handled by `pip`:

```bash
python -m pip install pandas
```

It downloads or installs packages into the current Python environment.

### Import Resolution

This is handled by Python at runtime:

```python
import pandas
```

Python searches folders in `sys.path` until it finds a matching package or module.

The package can be installed correctly but still not import if you are running a different Python interpreter.

## 3. Always Prefer `python -m pip`

Use this:

```bash
python -m pip install package_name
```

Instead of this:

```bash
pip install package_name
```

Why? `python -m pip` means:

```text
Use pip that belongs to this exact Python interpreter.
```

On a real machine, you may have many Pythons:

```text
/usr/bin/python3
/usr/local/bin/python3
/opt/homebrew/bin/python3
~/.pyenv/shims/python
./.venv/bin/python
/opt/anaconda3/bin/python
```

If `pip` points to one Python but `python` points to another, packages get installed into the wrong place.

## 4. Virtual Environments

A virtual environment is an isolated Python environment for one project.

Create one:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Verify:

```bash
which python
python --version
python -m pip --version
```

You want paths that point inside your project:

```text
.../my_project/.venv/bin/python
.../my_project/.venv/lib/python3.x/site-packages/pip
```

Deactivate:

```bash
deactivate
```

## 5. `ModuleNotFoundError`: Common Causes

### Cause 1: Package Not Installed In This Environment

Check:

```bash
python -m pip show package_name
```

Install:

```bash
python -m pip install package_name
```

### Cause 2: You Installed With A Different pip

Bad pattern:

```bash
pip install package_name
python script.py
```

Better pattern:

```bash
python -m pip install package_name
python script.py
```

### Cause 3: You Are Running From The Wrong Folder

Example project:

```text
my_project/
  app/
    __init__.py
    main.py
  tests/
```

If you run Python from inside `app/`, imports may behave differently than when running from `my_project/`.

Prefer running commands from the project root:

```bash
cd /path/to/my_project
python -m app.main
```

### Cause 4: Missing `__init__.py`

For many beginner projects, add an empty `__init__.py` to folders you want Python to treat as packages:

```text
my_project/
  app/
    __init__.py
    main.py
    helpers.py
```

Modern Python supports namespace packages without `__init__.py`, but beginners should usually add it because it makes package intent explicit.

### Cause 5: IDE Or Notebook Uses A Different Interpreter

Terminal says package is installed, but VS Code/Jupyter says it is missing.

Check inside Python:

```python
import sys
print(sys.executable)
```

Make your IDE or notebook use the same interpreter as your terminal `.venv`.

## 6. Normal Install vs Editable Install

Suppose you have a local project:

```text
my_project/
  pyproject.toml
  my_package/
    __init__.py
    core.py
```

A normal install copies your package into `site-packages`:

```bash
python -m pip install .
```

Mental model:

```text
repo code -> copied into .venv/site-packages -> Python imports the copy
```

If you edit `my_package/core.py`, Python may still import the installed copy until you reinstall.

An editable install points the environment back to your source tree:

```bash
python -m pip install -e .
```

Mental model:

```text
repo code <- .venv/site-packages points back here -> Python imports live files
```

Use editable installs for active development:

```bash
python -m pip install -e .
```

Then changes to your source code are picked up immediately.

## 7. Optional Dependency Groups

Modern Python projects often define dependencies in `pyproject.toml`:

```toml
[project]
name = "my-project"
dependencies = [
    "requests>=2.32",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "ruff>=0.5",
]
local = [
    "pandas>=2",
]
```

Install only the base package:

```bash
python -m pip install -e .
```

Install dev tools:

```bash
python -m pip install -e ".[dev]"
```

Install multiple optional groups:

```bash
python -m pip install -e ".[dev,local]"
```

Quotes matter on zsh/macOS because square brackets can be interpreted by the shell.

## 8. `requirements.txt` vs `pyproject.toml`

### `requirements.txt`

Simple list of packages:

```text
requests>=2.32
pandas>=2.2
pytest>=8
```

Install:

```bash
python -m pip install -r requirements.txt
```

Good for:

- simple scripts
- old projects
- deployment platforms that expect it
- quick tutorials

### `pyproject.toml`

Modern project metadata file:

```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = ["requests>=2.32"]
```

Good for:

- packages
- libraries
- editable installs
- optional dependency groups
- tool config such as pytest, ruff, mypy, black

Rule of thumb:

```text
For a real package or reusable project: use pyproject.toml
For a quick script or legacy deploy: requirements.txt is okay
```

## 9. `PYTHONPATH`: Useful But Dangerous

You can make Python search an extra folder:

```bash
export PYTHONPATH=/path/to/my_project:$PYTHONPATH
python script.py
```

This can fix imports temporarily.

But it has limits:

- it does not install dependencies
- it does not register package metadata
- it can leak into other projects
- it can hide real packaging problems
- IDEs and notebooks may not inherit it

Use `PYTHONPATH` for quick debugging only.

Prefer editable install for real projects:

```bash
python -m pip install -e .
```

## 10. `sys.path`: What Python Actually Searches

When Python sees:

```python
import my_package
```

it searches `sys.path`.

Inspect it:

```python
import sys
for path in sys.path:
    print(path)
```

Temporary hack:

```python
import sys
sys.path.insert(0, "/path/to/my_project")
```

This can help during debugging, but do not build serious projects around hardcoded `sys.path` changes.

## 11. Shadowing: When Your File Name Breaks Imports

Do not name your files after popular packages or standard library modules.

Bad:

```text
requests.py
pandas.py
json.py
typing.py
email.py
```

If you create `requests.py`, then this may import your file instead of the real package:

```python
import requests
```

Debug:

```bash
python -c "import requests; print(requests.__file__)"
```

If it points to your project file unexpectedly, rename your file.

## 12. Jupyter Notebook Problems

Jupyter often uses a different Python than your terminal.

Inside a notebook cell:

```python
import sys
print(sys.executable)
```

Install an IPython kernel for your venv:

```bash
source .venv/bin/activate
python -m pip install ipykernel
python -m ipykernel install --user --name my_project --display-name "Python (my_project)"
```

Then select that kernel in Jupyter.

## 13. VS Code And PyCharm Problems

### VS Code

Open Command Palette:

```text
Python: Select Interpreter
```

Choose:

```text
/path/to/project/.venv/bin/python
```

### PyCharm

Go to:

```text
Settings -> Project -> Python Interpreter
```

Choose the `.venv` interpreter for the project.

In both IDEs, verify inside your code:

```python
import sys
print(sys.executable)
```

## 14. Import Styles In A Project

Given:

```text
my_project/
  my_package/
    __init__.py
    main.py
    utils.py
```

Inside `main.py`, prefer absolute imports:

```python
from my_package.utils import helper
```

Or explicit relative imports when inside a package:

```python
from .utils import helper
```

Avoid relying on whatever folder you happen to run from.

Run package modules like this from the project root:

```bash
python -m my_package.main
```

## 15. Clean Rebuild Of A Broken Environment

Sometimes the fastest fix is to recreate the venv.

macOS/Linux:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

Only delete `.venv`, not your source code.

## 16. Expert Debug Commands

Show Python executable:

```bash
python -c "import sys; print(sys.executable)"
```

Show import path:

```bash
python -c "import sys; print('\n'.join(sys.path))"
```

Show where a package is imported from:

```bash
python -c "import package_name; print(package_name.__file__)"
```

Show pip version and location:

```bash
python -m pip --version
```

Show installed package metadata:

```bash
python -m pip show package_name
```

List installed packages with install locations:

```bash
python -m pip list -v
```

Trace import loading:

```bash
python -v script.py
```

Find all Python executables on macOS/Linux:

```bash
which -a python python3
```

Find Python executables on Windows:

```powershell
where python
py -0p
```

## 17. Decision Tree

### Error: `ModuleNotFoundError`

1. Are you in the right venv?

```bash
which python
python -m pip --version
```

2. Is the package installed there?

```bash
python -m pip show package_name
```

3. If it is local project code, did you install the project?

```bash
python -m pip install -e .
```

4. Are you running from the project root?

```bash
pwd
```

5. Is your IDE/Jupyter using the same interpreter?

```python
import sys
print(sys.executable)
```

### Error: Wrong Package Version

1. Check import location:

```bash
python -c "import package_name; print(package_name.__file__)"
```

2. Check installed version:

```bash
python -m pip show package_name
```

3. Reinstall in the active env:

```bash
python -m pip install --upgrade package_name
```

### Error: Local Changes Not Picked Up

Use editable install:

```bash
python -m pip install -e .
```

Then restart the Python process. Long-running servers, notebooks, and REPL sessions may need restart even with editable installs.

## 18. Best Practices

- Use one virtual environment per project.
- Use `python -m pip`, not bare `pip`.
- Use `pyproject.toml` for reusable projects.
- Use editable installs for local development.
- Do not rely on global `PYTHONPATH` for real projects.
- Do not name files after standard library modules or popular packages.
- Keep IDE and terminal interpreters aligned.
- Recreate `.venv` when the environment becomes confusing.

## 19. Tiny Healthy Project Example

```text
hello_project/
  pyproject.toml
  hello_project/
    __init__.py
    main.py
```

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "hello-project"
version = "0.1.0"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8"]
```

Install:

```bash
cd hello_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run:

```bash
python -m hello_project.main
```

If this works, your Python packaging basics are healthy.
