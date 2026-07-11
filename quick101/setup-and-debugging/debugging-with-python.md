# Debugging with python

Various options

## pdb

```python
import pdb

pdb_settrace()
```

# Importing jwt and invoking functon jwt.decode(), error decode not found in module jwt.

> Note: I am amble to import mmodule jwt, most likely either the install did not go well or using incorrect python path.
> If isntall did not go well, oefrome a force pip install

## Start python console

- import jwt
- dir(jwt) , this is short and sweet
- or help(jwt)

# Other ways

For debugging Python import issues like this, **strace won't help much** - it only shows system calls, not Python-level
module loading details. 

## 1. Check what JWT package you actually have

```python
import jwt

print(jwt.__file__)  # Shows the actual file location
print(jwt.__version__)  # Shows version
print(jwt.__name__)  # Shows module name
```

You likely have the wrong `jwt` package. There are multiple JWT packages on PyPI:

- `PyJWT` (correct one, has `decode()`)
- `jwt` (different package, minimal functionality)

## 2. Use Python's import tracing

```bash
python -v test_jwt.py  # Shows all import activity
```

## 3. Use the `trace` module

```bash
python -m trace --trace test_jwt.py
```

## 4. Check imports programmatically

```python
import sys
import jwt

print("JWT module location:", jwt.__file__)
print("Available attributes:", [attr for attr in dir(jwt) if not attr.startswith('_')])
print("Has decode?", hasattr(jwt, 'decode'))

# Check what's in sys.modules
print("JWT in sys.modules:", 'jwt' in sys.modules)
```

## 5. Install the correct package

```bash
pip uninstall jwt PyJWT  # Remove both
pip install PyJWT        # Install the correct one
```

The issue is almost certainly that you have the wrong `jwt` package installed. The `PyJWT` package is what provides
the `decode()` function you're looking for.


# Force pip install

To force a pip install in Python, you can use several approaches depending on what you're trying to achieve:

## Force reinstall a package

```bash
pip install --force-reinstall package_name
```

## Ignore dependency conflicts

```bash
pip install --force-reinstall --no-deps package_name
```

## Force upgrade to latest version

```bash
pip install --upgrade --force-reinstall package_name
```

## Install despite compatibility warnings

```bash
pip install --force-reinstall --no-deps --disable-pip-version-check package_name
```

## Break system packages (use with caution)

```bash
pip install --break-system-packages package_name
```

## Use --force-reinstall with specific version

```bash
pip install --force-reinstall package_name==1.2.3
```

The `--force-reinstall` flag will reinstall the package even if it's already installed, while `--no-deps` skips
dependency checks. The `--break-system-packages` flag is needed on some systems (like newer Ubuntu versions) that
protect system Python packages.

**Warning**: Using `--force-reinstall` and `--no-deps` can break your Python environment if dependencies become
incompatible. It's generally better to use virtual environments (`venv` or `conda`) to avoid conflicts with system
packages.

