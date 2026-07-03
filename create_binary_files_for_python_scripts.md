# Building Binary Files for Python Scripts on Windows or Mac

To build binary files for Python scripts on Windows or Mac, you can use tools like **PyInstaller**, **cx_Freeze**, or *
*Py2exe** (Windows only). These tools package your Python script along with the necessary dependencies into a standalone
executable, which can be distributed without requiring the end-user to have Python installed.

## 1. **Using PyInstaller**

**PyInstaller** is one of the most popular tools for this purpose. Here's how you can use it:

### Install PyInstaller

```bash
pip install pyinstaller
```

### Create an Executable

Navigate to the directory containing your Python script and run:

```bash
pyinstaller --onefile your_script.py
```

- The `--onefile` option packages everything into a single executable file.
- The executable will be generated in the `dist` directory.

### Including Local Packages and Dependencies

**What Gets Included Automatically:**

- ✅ Packages imported via standard imports (`from package import module`)
- ✅ Local modules in the same folder or subfolders with `__init__.py`
- ✅ External packages installed via pip

**What Does NOT Get Included Automatically:**

- ❌ Dynamically imported modules (`importlib.import_module()`)
- ❌ String-based imports (`__import__("module_name")`)
- ❌ Conditionally imported modules at runtime

**Example - Proper Project Structure (Recommended):**

```
my_app/
├── main.py              (entry point)
├── mypackage/
│   ├── __init__.py      (makes it a package)
│   ├── helpers.py
│   └── utils.py
└── requirements.txt
```

```python
# main.py
from mypackage.helpers import do_something  # ✅ Automatically included
from mypackage.utils import helper_func  # ✅ Automatically included

do_something()
```

Then build:

```bash
pyinstaller --onefile main.py
```

**If PyInstaller Misses a Module (Dynamic Imports):**
Use `--hidden-import` to explicitly include it:

```bash
pyinstaller --onefile --hidden-import=mypackage.helpers --hidden-import=mypackage.utils main.py
```

**Quick Check:**

- Use standard imports in your code
- Create a `__init__.py` file in package folders
- Avoid dynamic/string-based imports when possible
- If something is missing, use `--hidden-import=package_name`

## 2. **Using cx_Freeze**

**cx_Freeze** is another cross-platform tool:

### Install cx_Freeze

```bash
pip install cx_Freeze
```

### Create a Setup Script

Create a `setup.py` file:

```python
from cx_Freeze import setup, Executable

setup(
    name="your_program_name",
    version="0.1",
    description="Your program description",
    executables=[Executable("your_script.py")],
)
```

### Build the Executable

Run the following command:

```bash
python setup.py build
```

## 3. **Using Py2exe (Windows Only)**

**Py2exe** is specific to Windows:

### Install Py2exe

```bash
pip install py2exe
```

### Create a Setup Script

Similar to cx_Freeze, create a `setup.py` file:

```python
from distutils.core import setup
import py2exe

setup(console=['your_script.py'])
```

### Build the Executable

Run the command:

```bash
python setup.py py2exe
```

## Bundling with a `.whl` File

If you want to bundle the binary with a `.whl` (wheel) file, you can create a wheel that includes your binary files
using `setuptools`. Here’s how you can do that:

1. **Organize your project** so that your binaries and Python code are in the appropriate directories.

2. **Create a setup.py file** with the necessary configurations to include the binaries.

3. **Build the wheel** using the following command:
   ```bash
   python setup.py bdist_wheel
   ```

This will create a `.whl` file that includes your Python code and any additional files (including binaries) you’ve
specified.

### Complete Project Structure

Organize your project before creating the executable:

```
my_project/
├── setup.py                    (configuration file)
├── requirements.txt            (external packages: numpy, pandas, etc.)
├── MANIFEST.in                 (include binary files)
│
├── my_package/                 (your main package - local code)
│   ├── __init__.py
│   ├── main.py
│   └── helpers.py
│
├── scripts/                    (standalone scripts)
│   ├── __init__.py
│   └── my_app.py               (entry point for PyInstaller)
│
├── binaries/                   (pre-compiled binaries or data files)
│   ├── model.bin
│   └── data.pkl
│
└── tests/                      (test files)
    ├── __init__.py
    └── test_main.py
```

### Example `setup.py` for Bundling Binary Files

```python
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    description="My Python application with binaries",
    author="Your Name",

    # Your local packages (automatically found by find_packages)
    packages=find_packages(),

    # Include binary/data files
    include_package_data=True,
    package_data={
        '': ['binaries/*'],  # Include binaries folder
    },

    # External dependencies (from pip)
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "requests",
    ],

    # Optional: Make your script executable as command
    entry_points={
        'console_scripts': [
            'my-app=scripts.my_app:main',  # Creates 'my-app' command
        ],
    },
)
```

### `MANIFEST.in` (to include binary files in distribution)

```ini
# MANIFEST.in
recursive-include my_package *.py
recursive-include binaries *
include requirements.txt
include README.md
```

### `requirements.txt` (external packages for pip)

```
numpy>=1.20.0
pandas>=1.3.0
requests>=2.28.0
```

### What Gets Bundled in PyInstaller Binary

When you run:

```bash
pyinstaller --onefile scripts/my_app.py
```

The executable will include:

- ✅ All code from `my_package/` (local package)
- ✅ All code from `scripts/` (entry point)
- ✅ All external packages from `install_requires` (numpy, pandas, etc.)
- ✅ All binary files from `binaries/` folder
- ✅ Everything specified in `MANIFEST.in`

### Installation & Building

**For development:**

```bash
pip install -r requirements.txt
```

**To build the wheel:**

```bash
python setup.py bdist_wheel
```

**To create PyInstaller executable:**

```bash
pyinstaller --onefile scripts/my_app.py
```

> see [version_management_with_bumpversion.md](version_management_with_bumpversion.md)

## The "Executable Script" Method (Linux/macOS)

This is the most common way to make a script feel like a binary without actually compiling it.

**Add a Shebang**
Add this exact line as the very first line of your Python file. This tells the system which interpreter to use.
**my_script**

```python
#!/usr/bin/env python3
print("Hello from the script!")
```

> chmod +x **my_script**
>> Move the file to a folder in your $PATH
>>> You can run it from anywhere just by typing **my_script**.

## Summary

- **PyInstaller** or **cx_Freeze** are the go-to tools for creating executables on Windows or Mac.
- To bundle binaries with a `.whl` file, you can use `setuptools` with `package_data` to include the binaries in the
  wheel.
