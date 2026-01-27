To apply this globally, we use **Monkey Patching**. This involves replacing the `open` function in the `builtins` module. Once patched, every single call to `open()`—whether in your code, a third-party library, or a YAML loader—will pass through your security check.

### Global Monkey-Patch Implementation

This is powerful but should be done at the very top of your entry point (e.g., `main.py`) before other modules are imported.

```python
import builtins
import io
from pathlib import Path

def apply_global_path_guard(safe_directory):
    # Standardize the jail directory
    base_path = Path(safe_directory).resolve()
    
    # Keep a reference to the original functional open
    original_open = builtins.open

    def secure_open(file, mode='r', *args, **kwargs):
        # We only validate if 'file' is a string or Path (ignore file descriptors)
        if isinstance(file, (str, Path)):
            requested_path = Path(file).resolve()
            
            # CWE-22 Check: Is the resolved path inside the base_path?
            if not (requested_path == base_path or base_path in requested_path.parents):
                raise PermissionError(
                    f"Security Access Denied: {file} is outside authorized directory."
                )
        
        return original_open(file, mode, *args, **kwargs)

    # Overwrite the builtin open
    builtins.open = secure_open
    # Also patch io.open as many libraries use it specifically
    io.open = secure_open

# --- Execution ---
# Define the 'jail'
apply_global_path_guard("./my_project_files")

import yaml # Now even yaml.safe_load is protected!

try:
    # This will fail even though it's inside a library call
    with open("../../../etc/shadow", "r") as f:
        print(f.read())
except PermissionError as e:
    print(f"Caught by guard: {e}")

```

---

### Understanding the "Jail" Logic

When you use `Path.resolve()`, Python handles the heavy lifting of path normalization. This prevents bypasses that look like this:

| Attack Vector | Input String | Resolved Path (Safe) |
| --- | --- | --- |
| **Parent Traversal** | `data/../../etc/passwd` | `/etc/passwd` (Blocked) |
| **Null Byte** | `data/file.txt\0.pdf` | `/your/app/data/file.txt` (Cleaned) |
| **Symlink Loop** | `data/link_to_root` | `/` (Blocked) |

### Important Caveats

1. **System Dependencies**: If your app needs to read system fonts, locales, or site-packages located outside your `base_dir`, this global patch will block them. You may need to add an "allow-list" of directories to the wrapper.
2. **Performance**: Adding `Path.resolve()` to every file open adds a tiny bit of overhead. For most web apps, it's negligible, but for high-frequency file I/O, it's worth noting.
