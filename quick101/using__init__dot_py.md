It is a common misconception that `__init__.py` went away after Python 3.3
introduced **implicit namespace packages**. It is true that a directory without
`__init__.py` can sometimes be imported, but that creates a different kind of
package: a namespace package.

For most beginner and application projects, you still want `__init__.py`. It
marks a directory as a regular Python package and gives you one clear place to
define what the package exposes.

---

## 1. Marking a Regular Package

The simplest useful `__init__.py` is an empty file:

```text
my_math_pkg/
├── __init__.py
├── calculators.py
└── utilities.py
```

That file tells Python, your editor, your test tools, and other developers:
"this directory is a normal package."

An empty `__init__.py` means:

- This folder should be treated as a regular Python package.
- Python should create a package object when you import it.
- Code inside this folder can use package-style imports.

It does not mean the package has no code. The package's code can still live in
other files, such as `calculators.py` or `utilities.py`. The empty
`__init__.py` is just the package marker.

Without it, Python may treat the directory as a namespace package. Namespace
packages are useful, but they are usually for advanced cases where one package
is spread across multiple directories.

---

## 2. Defining a Clean Public API

`__init__.py` can re-export selected functions, classes, or constants so users
do not need to know your internal file layout.

**Inside `calculators.py`:**

```python
def complex_internal_calculator_function(a, b):
    return a + b
```

**Inside `__init__.py`:**

```python
from .calculators import complex_internal_calculator_function as add

__all__ = ["add"]
```

**The benefit:**

Now a user does not have to type:

```python
from my_math_pkg.calculators import complex_internal_calculator_function
```

They can write:

```python
import my_math_pkg

my_math_pkg.add(5, 5)
```

Or:

```python
from my_math_pkg import add

add(5, 5)
```

---

## 3. Controlling `from package import *`

Wildcard imports are usually discouraged because they make code harder to read,
but Python still supports them.

If your `__init__.py` defines `__all__`, then this:

```python
from my_math_pkg import *
```

imports only the names listed in `__all__`:

```python
# __init__.py
from .calculators import complex_internal_calculator_function as add

__all__ = ["add"]
```

If `__all__` is missing, Python exports names from the package namespace that do
not start with an underscore. That can accidentally expose helper imports,
constants, or implementation details, so defining `__all__` is useful when you
want an intentional public API.

---

## 4. Package-Level Values

`__init__.py` is a good place for lightweight package-level values, such as a
version string or convenient imports:

```python
# __init__.py
__version__ = "1.0.0"
```

Avoid heavy work in `__init__.py`. Opening database connections, reading large
files, making network calls, or changing environment variables during import can
make your package slow, surprising, and difficult to test.

If setup is needed, prefer an explicit function:

```python
# __init__.py
def configure(app_mode="development"):
    return {"app_mode": app_mode}
```

Then users can choose when setup happens:

```python
import my_math_pkg

config = my_math_pkg.configure("production")
```

---

## 5. Regular Packages vs. Namespace Packages

Python 3.3+ supports both regular packages and namespace packages.

| Feature | Regular Package (`__init__.py`) | Namespace Package (no `__init__.py`) |
|---|---|---|
| Common use | Most projects and libraries | One logical package spread across multiple locations |
| Package code | Can run package-level code in `__init__.py` | No `__init__.py`, so no package-level initialization file |
| Public API | Can define imports, `__all__`, and package values | Mostly acts as a container for subpackages/modules |
| Simplicity | Easier for beginners and most tools | Useful, but more specialized |

For example, a namespace package can allow two separate directories on
`sys.path` to contribute modules under the same top-level package name. That is
powerful, but it is not what most beginner projects need.

Here is a small example:

```text
folder_a/
└── my_tools/
    └── strings.py

folder_b/
└── my_tools/
    └── numbers.py
```

Notice that neither `my_tools/` directory contains `__init__.py`.

If both `folder_a` and `folder_b` are on Python's import path, Python can treat
both `my_tools/` directories as parts of the same namespace package:

```python
from my_tools import strings
from my_tools import numbers
```

Even though `strings.py` and `numbers.py` live in different physical folders,
they share the same top-level package name: `my_tools`.

For normal beginner projects, this is usually more flexibility than you need.
Use a regular package with `__init__.py` unless you specifically want multiple
directories to contribute to the same package name.

---

## How Popular Packages Use `__init__.py`

Libraries often use `__init__.py` to make their public API convenient.

For example, a package may keep implementation details in internal modules but
re-export the most important pieces at the package level. That is why many
libraries let users write simple imports such as:

```python
import requests

requests.get("https://example.com")
```

Instead of requiring users to import from a deeper internal module.

Packages may also expose metadata:

```python
__version__ = "1.0.0"
```

---

## Summary

Use `__init__.py` when you want a normal, easy-to-understand Python package.
It can be empty, or it can define a small public API for your package.

Leave it out only when you intentionally want a namespace package, which is a
more specialized feature for spreading one package across multiple directories.
