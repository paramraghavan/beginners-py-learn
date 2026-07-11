# Building Executables And Command-Line Tools From Python Scripts

This note explains three different goals that people often mix together:

1. Make a Python script easy to run as a command.
2. Package Python code as an installable wheel.
3. Build a standalone executable for Windows or macOS.

They are related, but they are not the same thing.

## 1. Pick The Right Goal

| Goal | Best Tool | Output | Does User Need Python? |
|---|---|---|---|
| Make a local script executable | shebang + `chmod` | runnable script | Yes |
| Create an installed CLI command | `pyproject.toml` console script | command in venv | Yes |
| Distribute a Python package | `python -m build` | `.whl` / `.tar.gz` | Yes |
| Create a standalone app/exe | PyInstaller, cx_Freeze, Nuitka | executable/app folder | Usually no separate Python install |

If you only want a command such as `my-tool`, start with console scripts in `pyproject.toml`. Use PyInstaller only when you need to give someone an executable that runs without them setting up Python.

## 2. Start From A Clean Virtual Environment

macOS/Linux:

```bash
cd my_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

Windows PowerShell:

```powershell
cd my_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

Use `python -m pip`, not bare `pip`, so packages install into the Python environment you are actually using.

## 3. Method A: Make A Script Executable On Linux/macOS

This makes a script feel like a binary, but it still requires Python on the machine.

Create `my_script`:

```python
#!/usr/bin/env python3

print("Hello from the script!")
```

Make it executable:

```bash
chmod +x my_script
./my_script
```

Move it to a folder in your `PATH` if you want to run it from anywhere:

```bash
mkdir -p ~/bin
mv my_script ~/bin/
```

Make sure `~/bin` is in your `PATH`.

## 4. Method B: Create A CLI Command With `pyproject.toml`

This is the clean professional way to expose a command from a Python package.

Project structure:

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
    print("Hello from my-tool")
```

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-tool"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.scripts]
my-tool = "my_tool.cli:main"
```

Install in editable mode:

```bash
python -m pip install -e .
```

Run:

```bash
my-tool
```

This creates a command in the active environment. It is not a standalone executable; it still depends on that Python environment.

## 5. Method C: Build A Standalone Executable With PyInstaller

PyInstaller packages your script, Python interpreter pieces, and many dependencies into a distributable executable or app folder.

Install:

```bash
python -m pip install pyinstaller
```

Build one file:

```bash
python -m PyInstaller --onefile your_script.py
```

The output appears in:

```text
dist/your_script
```

On Windows the output is usually:

```text
dist\your_script.exe
```

For many apps, prefer a folder build instead of `--onefile`:

```bash
python -m PyInstaller your_script.py
```

Folder mode usually starts faster and is easier to debug.

## 6. PyInstaller Project Structure

Recommended:

```text
my_app/
  main.py
  mypackage/
    __init__.py
    helpers.py
    utils.py
  assets/
    config.json
  requirements.txt
```

`main.py`:

```python
from mypackage.helpers import do_something
from mypackage.utils import helper_func


def main() -> None:
    do_something()
    helper_func()


if __name__ == "__main__":
    main()
```

Build:

```bash
python -m PyInstaller --onefile main.py
```

## 7. What PyInstaller Includes Automatically

Usually included:

- packages imported with normal `import` statements
- local modules imported from your project
- installed packages in the active environment
- many common shared libraries

Often not included automatically:

- dynamic imports with `importlib.import_module()`
- string imports with `__import__("module_name")`
- plugin systems discovered only at runtime
- data files such as JSON, images, templates, model files
- hidden native libraries

## 8. If PyInstaller Misses A Module

Use `--hidden-import`:

```bash
python -m PyInstaller --onefile --hidden-import=mypackage.helpers main.py
```

Multiple hidden imports:

```bash
python -m PyInstaller --onefile \
  --hidden-import=mypackage.helpers \
  --hidden-import=mypackage.utils \
  main.py
```

Tip: prefer standard imports in your code when possible. They are easier for PyInstaller to detect.

## 9. Including Data Files With PyInstaller

Data files are not always included automatically.

macOS/Linux syntax:

```bash
python -m PyInstaller --onefile --add-data "assets/config.json:assets" main.py
```

Windows syntax:

```powershell
python -m PyInstaller --onefile --add-data "assets\config.json;assets" main.py
```

Notice the separator difference:

```text
macOS/Linux: source:destination
Windows:     source;destination
```

In Python code, use a helper that works in both normal and PyInstaller modes:

```python
from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path


config = resource_path("assets/config.json")
print(config.read_text())
```

## 10. The `.spec` File

After the first PyInstaller run, you may see a `.spec` file.

```bash
python -m PyInstaller main.py
```

Creates something like:

```text
main.spec
```

You can edit the `.spec` file for advanced builds, extra data files, hidden imports, icons, and custom options.

Build from the spec:

```bash
python -m PyInstaller main.spec
```

For serious apps, keep the `.spec` file in version control.

## 11. macOS Notes

Build on the same operating system you plan to distribute for. A PyInstaller build made on macOS creates a macOS executable, not a Windows `.exe`.

Useful macOS options:

```bash
python -m PyInstaller --windowed --name MyApp main.py
```

`--windowed` is useful for GUI apps because it avoids opening a terminal window.

Gatekeeper/quarantine can block downloaded executables. For personal/local use, you may need:

```bash
xattr -dr com.apple.quarantine dist/MyApp
```

For real distribution, learn about signing and notarization.

## 12. Windows Notes

Build Windows executables on Windows.

Useful options:

```powershell
python -m PyInstaller --onefile --name MyApp main.py
```

For GUI apps:

```powershell
python -m PyInstaller --onefile --windowed --name MyApp main.py
```

If antivirus flags your executable, try folder mode instead of `--onefile`, avoid suspicious packers, and sign the executable for real distribution.

## 13. cx_Freeze

`cx_Freeze` is another cross-platform option.

Install:

```bash
python -m pip install cx_Freeze
```

Minimal `setup.py`:

```python
from cx_Freeze import Executable, setup

setup(
    name="your_program_name",
    version="0.1.0",
    description="Your program description",
    executables=[Executable("your_script.py")],
)
```

Build:

```bash
python setup.py build
```

Use this when you prefer cx_Freeze's build model or PyInstaller has issues with your application.

## 14. py2exe Is Windows Only

`py2exe` is specific to Windows and older workflows.

Install:

```bash
python -m pip install py2exe
```

Minimal `setup.py`:

```python
from distutils.core import setup
import py2exe

setup(console=["your_script.py"])
```

Build:

```bash
python setup.py py2exe
```

For new cross-platform projects, try PyInstaller first.

## 15. Wheels Are Not Standalone Executables

A wheel (`.whl`) is an installable Python package, not a standalone binary app.

Build tools:

```bash
python -m pip install build
python -m build
```

Output:

```text
dist/my_package-0.1.0-py3-none-any.whl
dist/my_package-0.1.0.tar.gz
```

Install the wheel:

```bash
python -m pip install dist/my_package-0.1.0-py3-none-any.whl
```

A wheel is best when your users are Python users. PyInstaller is better when your users just want to run an app.

## 16. Include Files In A Wheel With `pyproject.toml`

Project:

```text
my_project/
  pyproject.toml
  my_package/
    __init__.py
    data/
      config.json
```

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"

[tool.setuptools.package-data]
my_package = ["data/*.json"]
```

Read package data with `importlib.resources`:

```python
from importlib.resources import files

text = files("my_package").joinpath("data/config.json").read_text()
```

This is better than relying on the current working directory.

## 17. Common PyInstaller Failures

### `ModuleNotFoundError` after building

Try:

```bash
python -m PyInstaller --onefile --hidden-import=missing_module main.py
```

### File not found after building

Use `--add-data` and read files with a PyInstaller-aware `resource_path()` helper.

### Works in terminal but not after double-clicking

The working directory is different. Do not rely on relative paths such as:

```python
open("config.json")
```

Use paths based on `__file__` or `importlib.resources`.

### App is huge

Standalone executables include Python and dependencies. This is normal. Remove unused heavy packages from the environment before building.

### Build works on my machine only

Build in a clean virtual environment and record your dependencies.

```bash
python -m pip freeze > requirements-lock.txt
```

## 18. Recommended Build Checklist

- Create a clean virtual environment.
- Install only required dependencies.
- Run the script normally first.
- Prefer standard imports over dynamic imports.
- Add data files explicitly.
- Test the executable on a clean machine or clean user account.
- Build on the target operating system.
- Keep build commands in a script or README.
- Do not commit `build/`, `dist/`, or `.spec` files unless intentionally needed.

## 19. Quick Commands

Script as command on macOS/Linux:

```bash
chmod +x my_script
./my_script
```

CLI command from `pyproject.toml`:

```bash
python -m pip install -e .
my-tool
```

PyInstaller one-file executable:

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile main.py
```

Build wheel:

```bash
python -m pip install build
python -m build
```

## 20. Summary

- Use a shebang and `chmod +x` for simple local scripts.
- Use `[project.scripts]` in `pyproject.toml` for clean Python CLI commands.
- Use wheels for Python package distribution.
- Use PyInstaller or cx_Freeze for standalone executables.
- A wheel is not the same as an executable.
- Always build from a clean virtual environment.
