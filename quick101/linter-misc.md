# PyCharm plugins and Python tools for increased productivity including linter:

## Code Quality & Linting:

- Flake8: Style guide enforcement
  ```bash
  pip install flake8
  ```
  In PyCharm: Settings → External Tools → Add Flake8
  Configure in project: Create `.flake8` configuration file

- pylint: Deep code analysis
  ```bash
  pip install pylint
  ```
  PyCharm has built-in integration: Settings → Editor → Inspections → Python → Enable Pylint

- black: Code formatter
  ```bash
  pip install black
  ```
  In PyCharm: Settings → External Tools → Add Black
  Use: Right-click on file/folder → External Tools → black

Development Tools:

1. pytest

```bash
pip install pytest
```

- Configure in PyCharm: Settings → Tools → Python Integrated Tools → Default test runner
- Run tests: Right-click on test file → Run

2. mypy (Type checking)

```bash
pip install mypy
```

- Add type hints to your code
- Configure in PyCharm: Settings → External Tools → Add mypy

## Practical PyCharm Shortcuts

1. Essential shortcuts:

```
# Essential shortcuts:
Ctrl+Alt+L (Cmd+Alt+L on Mac): Reformat code
Shift+F6: Rename
Ctrl+B (Cmd+B): Go to definition
Alt+Enter: Show intention actions/quick fixes
Ctrl+Space: Basic code completion
```

2. Debug Configuration
   In PyCharm:
1. Add breakpoints by clicking left margin
2. Run → Debug
3. Use Debug toolbar:
    - Step Over (F8)
    - Step Into (F7)
    - Step Out (Shift+F8)
    - Resume (F9)

# Details

1. Black (Code Formatter) Setup

```bash
# Install
pip install black

# In PyCharm:
# 1. Go to Settings → Tools → External Tools → + (Add)
# 2. Configure:
Name: Black
Program: $PyInterpreterDirectory$/black
Arguments: $FilePath$
Working Directory: $ProjectFileDir$
```

Usage:

- Right-click any Python file → External Tools → Black
- Or set up a keyboard shortcut: Settings → Keymap → External Tools → Black
- Create `pyproject.toml` for configuration:

```toml
[tool.black]
line-length = 88
target-version = ['py37']
include = '\.pyi?$'
```

2. Flake8 Integration

```bash
# Install with extras
pip install flake8 flake8-docstrings flake8-bugbear

# Create .flake8 configuration:
[flake8]
max-line-length = 88
extend-ignore = E203
exclude = .git,__pycache__,build,dist
```

Usage in PyCharm:

- Settings → Editor → Inspections → Python → Flake8
- View errors in real-time in editor
- Run on whole project: Right-click project → External Tools → Flake8

3. pytest Effective Usage

```bash
pip install pytest pytest-cov

# Create test structure:
tests/
    __init__.py
    test_module.py
```

Example test file:

```python
# test_module.py
def test_example():
    expected = "hello"
    actual = "hello"
    assert actual == expected


# Run with coverage
def test_with_fixtures(tmp_path):
    # tmp_path is a pytest fixture
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    assert file_path.read_text() == "content"
```

In PyCharm:

- Right-click test file → Run 'pytest in test_...'
- View coverage: Run → Run with Coverage

4. mypy Type Checking

```bash
pip install mypy

# Create mypy.ini:
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

Example with type hints:

```python
from typing import List, Dict


def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

5. Setting Up Pre-commit Hooks

```bash
pip install pre-commit

# Create .pre-commit-config.yaml:
repos:
-   repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 3.9.2
    hooks:
    -   id: flake8
```

Initialize:

```bash
pre-commit install
```

## pre-commit hook how to

The `.pre-commit-config.yaml` file should be created in your project's root directory, at the same level as your `.git`
folder.

File structure example:

```
your-project/
├── .git/
├── .pre-commit-config.yaml  # Here
├── .gitignore
├── src/
│   └── your_code.py
├── tests/
│   └── test_code.py
└── README.md
```

After creating the file, run:

```bash
pre-commit install
```

This installs the git hook scripts in your `.git/hooks/` directory. Now every time you run `git commit`, the pre-commit
hooks will run automatically.

## Bandit linter

Bandit is a security linter that finds common security issues in Python code. Here's how to use it:

Install:

```bash
pip install bandit
```

Here are examples of security issues Bandit catches:

1. Hardcoded Passwords (Bad):

```python
# Bandit will flag this
password = "my_hardcoded_password"
connection = connect(user="admin", password=password)
```

2. Unsafe YAML Loading (Bad):

```python
import yaml

# Bandit will flag this - unsafe!
data = yaml.load(file_content)

# Safe version:
data = yaml.safe_load(file_content)
```

3. SQL Injection Risk (Bad):

```python
# Bandit will flag this
query = "SELECT * FROM users WHERE id = " + user_id
cursor.execute(query)

# Safe version:
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

4. Command Injection Risk (Bad):

```python
import subprocess

# Bandit will flag this
subprocess.Popen("cat " + user_input, shell=True)

# Safe version:
subprocess.Popen(["cat", user_input], shell=False)
```

Run Bandit:

```bash
# Scan single file
bandit file.py

# Scan directory
bandit -r ./your_project_directory

# Generate HTML report
bandit -r ./your_project_directory -f html -o bandit-report.html

# Ignore certain tests
bandit -r ./your_project_directory -s B101,B102
```

Configure with `.bandit` file in project root:

```yaml
skips: [ 'B101','B601' ]
exclude_dirs: [ 'tests', 'venv' ]
```

## Bandit linter on pycharm

Here's how to set up Bandit in PyCharm:

1. First install Bandit:

```bash
pip install bandit
```

2. Configure in PyCharm:

- Go to Settings/Preferences (Ctrl+Alt+S)
- Navigate to Tools → External Tools
- Click + to add new tool
- Fill in these details:

```
Name: Bandit
Program: $PyInterpreterDirectory$/bandit
Arguments: -r $FileDir$
Working Directory: $ProjectFileDir$
```

3. Optional: Create keyboard shortcut

- Go to Settings → Keymap
- Find External Tools → External Tools → Bandit
- Right-click and Add Keyboard Shortcut
- Choose your preferred shortcut

4. Usage:

- Right-click on a Python file/folder
- Select External Tools → Bandit
- View results in PyCharm's console

5. For specific file:

```
Arguments: $FilePath$
```

For recursive directory scan with report:

```
Arguments: -r $FileDir$ -f html -o $ProjectFileDir$/bandit-report.html
```

