# How To Use `pyproject.toml` In Python Projects

`pyproject.toml` is the modern standard configuration file for Python projects. Put it at the root of your project.

```text
my_project/
  pyproject.toml
  my_package/
    __init__.py
    main.py
  tests/
```

It can describe how your project is built, what it is named, which Python versions it supports, what packages it depends on, and how tools such as pytest, ruff, black, and mypy should behave.

## 1. Why `pyproject.toml` Exists

Older Python projects often used several separate files:

```text
setup.py
setup.cfg
requirements.txt
MANIFEST.in
pytest.ini
mypy.ini
.flake8
```

That worked, but it spread project configuration across many files. `pyproject.toml` gives Python tools one standard place to look.

The important standards are:

- PEP 518: build-system requirements
- PEP 517: build backend interface
- PEP 621: project metadata such as name, version, dependencies

Beginner translation:

```text
pyproject.toml tells Python tools what your project is and how to install/build/check it.
```

## 2. Minimal `pyproject.toml`

A tiny package can start with this:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-project"
version = "0.1.0"
description = "A small Python project"
requires-python = ">=3.11"
dependencies = []
```

Important details:

- `name` is the install/distribution name, usually written with hyphens.
- Your import package folder may use underscores.
- `requires-python` tells installers which Python versions are supported.
- `dependencies` lists runtime packages your code needs.

Example:

```toml
[project]
name = "my-cool-tool"
```

Project folder:

```text
my_cool_tool/
  __init__.py
```

Install command:

```bash
python -m pip install -e .
```

Import:

```python
import my_cool_tool
```

## 3. Runtime Dependencies

Runtime dependencies are packages your application or library needs to run.

```toml
[project]
dependencies = [
    "requests>=2.32",
    "pydantic>=2.7",
]
```

Install them with your project:

```bash
python -m pip install -e .
```

This installs:

- your local project
- `requests`
- `pydantic`

## 4. Optional Dependencies

Optional dependency groups are useful for development, testing, docs, local tools, or larger feature sets.

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8",
    "ruff>=0.5",
    "mypy>=1.10",
]
docs = [
    "mkdocs>=1.6",
]
api = [
    "fastapi>=0.111",
    "uvicorn>=0.30",
]
```

Install one group:

```bash
python -m pip install -e ".[dev]"
```

Install multiple groups:

```bash
python -m pip install -e ".[dev,api]"
```

The quotes matter on macOS/zsh because square brackets can be treated as shell patterns.

## 5. Editable Install

For local development, use editable install:

```bash
python -m pip install -e .
```

Mental model:

```text
repo code <- .venv/site-packages points back here -> Python imports live files
```

This means changes to your local `.py` files are picked up without reinstalling every time.

Use editable install when:

- you are learning
- you are developing a package
- you are running tests while changing code
- you want examples to import your local source tree

## 6. Recommended Beginner Workflow

```bash
cd my_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
python -m pytest
```

Windows PowerShell:

```powershell
cd my_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
python -m pytest
```

## 7. `pyproject.toml` vs `requirements.txt`

| File | Best For | Notes |
|---|---|---|
| `pyproject.toml` | Real projects, packages, reusable code, tool config | Modern standard |
| `requirements.txt` | Simple scripts, deployment pins, old systems | Simple but less expressive |
| `requirements-dev.txt` | Legacy dev dependency lists | Optional groups are cleaner in modern projects |

You can use both, but pick one source of truth.

Good modern default:

```text
pyproject.toml = source of truth for project metadata and dependencies
requirements.txt = optional pinned export for deployment, if needed
```

## 8. Creating `requirements.txt` From `pyproject.toml`

Yes, you can create a `requirements.txt` from `pyproject.toml`. The best method depends on what kind of requirements file you want.

### Simple Manual Version

If your `pyproject.toml` has direct dependencies:

```toml
[project]
dependencies = [
    "requests>=2.32",
    "pydantic>=2.7",
]
```

Then a simple `requirements.txt` could be:

```text
requests>=2.32
pydantic>=2.7
```

This is easy to read, but it only includes direct dependencies. It does not include transitive dependencies such as packages that `requests` itself depends on.

### Better Version: Use `pip-tools`

Install `pip-tools`:

```bash
python -m pip install pip-tools
```

Generate a pinned `requirements.txt` from `pyproject.toml`:

```bash
python -m piptools compile pyproject.toml -o requirements.txt
```

This creates a locked/pinned file with exact versions:

```text
certifi==2025.7.9
charset-normalizer==3.4.2
idna==3.10
pydantic==2.11.7
requests==2.32.4
urllib3==2.5.0
```

That output includes both direct and transitive dependencies.

### Export Optional Dependency Groups

If your `pyproject.toml` has optional dependencies:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8",
    "ruff>=0.5",
]
api = [
    "fastapi>=0.111",
    "uvicorn>=0.30",
]
```

Generate a dev requirements file:

```bash
python -m piptools compile pyproject.toml --extra dev -o requirements-dev.txt
```

Generate an API requirements file:

```bash
python -m piptools compile pyproject.toml --extra api -o requirements-api.txt
```

Generate a combined requirements file:

```bash
python -m piptools compile pyproject.toml --extra dev --extra api -o requirements-dev-api.txt
```

### Using `uv` To Export Requirements

If the project uses `uv`, you can export requirements from the lock file.

Create or update the lock file:

```bash
uv lock
```

Export:

```bash
uv export --format requirements-txt -o requirements.txt
```

With extras:

```bash
uv lock --extra dev
uv export --format requirements-txt -o requirements-dev.txt
```

### Important Mental Model

Use `pyproject.toml` as the source of truth:

```text
requests>=2.32
pydantic>=2.7
```

Use `requirements.txt` as an exported install artifact:

```text
requests==2.32.4
pydantic==2.11.7
urllib3==2.5.0
```

The difference:

| File | Meaning |
|---|---|
| `pyproject.toml` | What the project needs |
| `requirements.txt` | Exact versions to install in one environment |
| `requirements-dev.txt` | Exact dev/test tool versions |
| lock file | Exact dependency solution for reproducible installs |

Rule of thumb:

```text
Edit pyproject.toml by hand.
Generate requirements.txt with tools.
Do not manually maintain both unless the project is very small.
```

### Common Mistake

Do not let `pyproject.toml` and `requirements.txt` disagree.

Bad:

```toml
# pyproject.toml
requests>=2.32
```

```text
# requirements.txt
requests==2.28.0
```

This creates confusion because one file says modern `requests` is allowed, but the other pins an older version.

If `pyproject.toml` is your source of truth, regenerate `requirements.txt` when dependencies change.

## 9. Tool Configuration

Many Python tools can be configured inside `pyproject.toml`.

### pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### ruff

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

### mypy

```toml
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

## 10. Console Scripts

You can create command-line commands from Python functions.

Project:

```text
my_project/
  pyproject.toml
  my_tool/
    __init__.py
    cli.py
```

`my_tool/cli.py`:

```python
def main() -> None:
    print("hello")
```

`pyproject.toml`:

```toml
[project.scripts]
my-tool = "my_tool.cli:main"
```

Install:

```bash
python -m pip install -e .
```

Run:

```bash
my-tool
```

This creates a command, not a standalone binary. Users still need the Python environment where the package is installed.

## 11. Package Discovery

If your package folder is simple, setuptools often finds it automatically.

```text
my_project/
  pyproject.toml
  my_package/
    __init__.py
```

For a `src/` layout:

```text
my_project/
  pyproject.toml
  src/
    my_package/
      __init__.py
```

Use:

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

The `src/` layout is common in professional packages because it catches import mistakes earlier.

## 12. Including Data Files

If your package needs data files:

```text
my_package/
  __init__.py
  data/
    config.json
```

Add:

```toml
[tool.setuptools.package-data]
my_package = ["data/*.json"]
```

Then read files using `importlib.resources`, not hardcoded relative paths:

```python
from importlib.resources import files

config_path = files("my_package").joinpath("data/config.json")
text = config_path.read_text()
```

## 13. Common Mistakes

### Mistake: package name and import name confusion

Distribution name:

```toml
name = "my-awesome-tool"
```

Import name:

```python
import my_awesome_tool
```

Hyphens are okay in package distribution names. Python imports use valid Python identifiers, usually underscores.

### Mistake: using `pip install .` during active development

Use editable mode:

```bash
python -m pip install -e .
```

### Mistake: forgetting quotes around optional dependencies

Use:

```bash
python -m pip install -e ".[dev]"
```

Not:

```bash
python -m pip install -e .[dev]
```

The unquoted version may fail in zsh.

### Mistake: relying on `PYTHONPATH`

`PYTHONPATH` can make imports work temporarily, but it does not install dependencies or package metadata. Prefer editable install.

## 14. Healthy Project Template

```text
my_project/
  pyproject.toml
  README.md
  my_project/
    __init__.py
    cli.py
  tests/
    test_cli.py
```

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-project"
version = "0.1.0"
description = "A healthy beginner Python project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "ruff>=0.5",
]

[project.scripts]
my-project = "my_project.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

`my_project/cli.py`:

```python
def main() -> None:
    print("Hello from my project")
```

Install and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
my-project
python -m pytest
```

## 15. Quick Debug Commands

```bash
python -c "import sys; print(sys.executable)"
python -m pip --version
python -m pip show my-project
python -c "import my_project; print(my_project.__file__)"
python -m site
```

If those commands point to different environments or unexpected folders, your issue is environment/path related, not usually a Python language problem.
