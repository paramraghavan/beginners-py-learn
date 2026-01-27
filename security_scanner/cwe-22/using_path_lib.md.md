Using `pathlib` is the modern, more readable standard in Python. It treats paths as objects rather than strings, which makes the logic for a **CWE-22** check much more intuitive.

Here is how to implement the guard using `is_relative_to` (available in Python 3.9+) or a manual parent check for older versions.

### The Modern Pathlib Implementation

The `pathlib.Path.resolve()` method is your best friend here—it automatically follows symlinks and eliminates `..` segments, which is exactly how attackers try to escape directories.

```python
import io
from pathlib import Path
from functools import wraps

def safe_path_decorator(base_directory):
    """
    A decorator that ensures the file path is physically 
    located within the base_directory.
    """
    # Resolve the base directory once at the start
    base_path = Path(base_directory).resolve()

    def decorator(func):
        @wraps(func)
        def wrapper(file, *args, **kwargs):
            # 1. Convert input to a Path object and resolve it
            # This handles '../', './', and symlinks
            requested_path = Path(file).resolve()

            # 2. Check if the path is within the allowed base
            # is_relative_to is available in Python 3.9+
            try:
                requested_path.relative_to(base_path)
            except ValueError:
                raise PermissionError(
                    f"Security Block: {file} is outside of {base_directory}"
                )

            return func(file, *args, **kwargs)
        return wrapper
    return decorator

# --- Usage Example ---

DATA_DIR = "./app_data"
# Create the directory if it doesn't exist for the demo
Path(DATA_DIR).mkdir(exist_ok=True)

@safe_path_decorator(DATA_DIR)
def secure_open(path, mode='r'):
    return open(path, mode)

# This works
with secure_open("app_data/user_profile.txt", "w") as f:
    f.write("Hello World")

# This raises a PermissionError
# even if the attacker uses complex nesting like 'app_data/../etc/passwd'
# secure_open("../../etc/passwd") 

```

---

### Integration with YAML (PyYAML)

Since you mentioned loading YAML, here is how you would apply this specifically to a loader. This prevents an attacker from tricking your application into reading a sensitive system file (like a `.env` or SSH key) via a YAML path parameter.

```python
import yaml

@safe_path_decorator("./configs")
def load_config_safely(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

# Usage
# config = load_config_safely("configs/production.yaml") # Safe
# config = load_config_safely("../secrets.yaml")        # Blocked

```

### Why `pathlib` is better for CWE-22

* **Symlink Resolution**: `Path.resolve()` handles symlinks that might point outside your directory—a common edge case string-based checks miss.
* **Case Sensitivity**: On Windows, `Path` objects handle case-insensitivity automatically, preventing bypasses like `C:\DATA` vs `c:\data`.
* **Readable Logic**: `requested_path.relative_to(base_path)` is much harder to "get wrong" than complex string manipulations with `os.path.commonprefix`.
