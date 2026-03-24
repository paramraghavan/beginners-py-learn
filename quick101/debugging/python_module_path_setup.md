Managing how Python finds your modules is a classic hurdle. Whether you want a "set it and forget it" approach or a
quick temporary fix, you have two primary paths.

Here is the breakdown of how to use both methods effectively.

---

## 1. The Professional Way: `pip install -e .`

This is known as an **Editable Install** (or "Developer Mode"). It creates a link in your environment's `site-packages`
that points directly to your project folder.

**Why use it?** It’s the cleanest method. You can modify your code, and the changes are reflected instantly without
needing to reinstall, all while your module remains "globally" accessible within that environment.

### How to do it:

1. **Navigate** to the root directory of your project (where your `pyproject.toml` or `setup.py` lives).
2. **Run** the following command in your terminal:
   ```bash
   pip install -e .
   ```
   *(The dot `.` represents the current directory.)*

# Details pyproject.toml and setup.py

While you only need **one** of these files to make `pip install -e .` work, the industry has shifted toward
`pyproject.toml` as the primary standard. `setup.py` is now considered the "legacy" approach, though it is still widely
supported.

Here are minimal, functional samples of both.

---

## 1. The Modern Standard: `pyproject.toml`

This file is the current "source of truth" for Python projects. It uses the `setuptools` backend to handle the
installation.

```toml
[build-system]
# Tells pip what tools are needed to build your package
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my_package"  # The name you'll use in 'pip install'
version = "0.1.0"
description = "A brief description of my project"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
dependencies = [
    "requests>=2.28.0", # Example: your project's requirements
]

[tool.setuptools]
# Tells setuptools where to find your code
packages = ["my_package"] 
```

---

## 2. The Legacy Way: `setup.py`

Before `pyproject.toml`, this was the only way. It is essentially a Python script that executes during installation.

```python
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    # Automatically finds all sub-packages in your directory
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    author="Your Name",
    description="A legacy setup file example",
)
```

---

## Which one should you use?

* **Use `pyproject.toml`** if you are starting a new project. It is cleaner, less prone to security risks (since it's a
  config file, not an executable script), and follows the latest PEP (Python Enhancement Proposal) standards.
* **Use `setup.py`** only if you are maintaining an older project or need to perform complex, dynamic logic during the
  installation process (which is rare).

### How to use them:

1. Place **one** of these files in your project root (e.g., `/my_project/pyproject.toml`).
2. Open your terminal in that folder.
3. Run:
   ```bash
   pip install -e .
   ```

### Requirements:

To make this work, your project needs a basic configuration file. Modern Python uses `pyproject.toml`. A minimal version
looks like this:

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my_cool_module"
version = "0.1.0"
```

---

## 2. The Quick & Dirty Way: `sys.path.append()`

This modifies the search path **at runtime**. It’s useful for quick scripts or when you aren't allowed to install
packages in the environment.

**Why use it?**
It requires zero configuration files. However, it is generally considered "brittle" because if you move your files or
share the script, the hardcoded paths will break.

### How to do it:

At the very top of your entry script (before you import your module), add:

```python
import sys
import os

# Option A: Absolute path
sys.path.insert(0, '/path/to/your/module_root')

# Option B: Relative path (relative to the script being run)
script_dir = os.path.dirname(__file__)
module_path = os.path.join(script_dir, '..', 'my_module_folder')
sys.path.insert(0, module_path)

import my_module  # Now this works
```

> **Note:** Using `sys.path.insert(0, ...)` is usually better than `sys.path.append()` because it puts your path at the
front of the list, ensuring Python picks up *your* version of a module if there’s a naming conflict.

---

## Comparison at a Glance

| Feature | `pip install -e` | `sys.path` |
| :--- | :--- | :--- |
| **Best For** | Active development, large projects | One-off scripts, debugging |
| **Persistence** | Permanent (until uninstalled) | Temporary (lasts for the session) |
| **Setup** | Requires `pyproject.toml` or `setup.py` | Just a line of code |
| **Portability** | High (handles dependencies well) | Low (hardcoded paths) |

---

## A Third "Middle Ground": `PYTHONPATH`

If you don't want to edit code OR create a config file, you can set an environment variable before running Python. This
adds the directory to the search path for that specific terminal session.

**On Linux/macOS:**

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/your/module"
python main_script.py
```

**On Windows (PowerShell):**

```powershell
$env:PYTHONPATH += ";C:\path\to\your\module"
python main_script.py
```
