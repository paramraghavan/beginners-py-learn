We want to catch these file reads *during* the import phase of third-party
or sub-modules, you can't easily refactor their code. Instead, you need to perform a **monkey patch**.

In Python, almost all file-reading operations eventually funnel through the built-in `open()` function or the `io`
module. By replacing the standard `builtins.open` with a custom wrapper, you can intercept every call, log the file
path, and then hand the execution back to the original function.

### The Monkey Patch Solution

You should place this code at the very top of your main entry point (before any other imports).

```python
import builtins
import os

# 1. Keep a reference to the original open function
original_open = builtins.open


def monitored_open(file, *args, **kwargs):
    # 2. Get the absolute path for clarity
    try:
        if isinstance(file, (str, bytes, os.PathLike)):
            abs_path = os.path.abspath(file)

            # 3. Filter for YAML files specifically
            if abs_path.endswith(('.yaml', '.yml')):
                print(f"[LOG] Loading YAML from: {abs_path}")
    except Exception:
        # We catch exceptions to ensure the app doesn't crash 
        # just because our logging failed
        pass

    # 4. Call the original open function so the app works normally
    return original_open(file, *args, **kwargs)


# 5. Global redirect: Overwrite the built-in open
builtins.open = monitored_open

# --- Now proceed with your imports ---
# import module_a
# import module_b
```

---

### Why this works

* **Built-in Scope:** By modifying `builtins.open`, you affect every module loaded afterward, because they all look to
  the `builtins` namespace for that function.
* **Transparency:** The wrapper uses `*args` and `**kwargs` to pass everything (mode, encoding, etc.) exactly as
  intended to the real `original_open`, so the functional logic of your modules remains unchanged.
* **Zero Refactoring:** You don't have to touch a single line of code in the YAML-reading modules.

### A Few Caveats

* **C-Extensions:** If a module uses a C-extension that calls the C-level `fopen()` directly, this Python-level patch
  might miss it. However, standard libraries like `PyYAML` or `ruamel.yaml` typically use Python's `open()`.
* **Performance:** Printing to the console is "expensive" in terms of time. Once you're done debugging, remember to
  remove the patch to avoid slowing down your I/O.
* **Standard Library internal reads:** You will see a lot of activity! You might want to add logic to ignore certain
  directories (like `site-packages` or `.venv`) if you only care about your local configuration files.

> =====================================================================================================
# Additional options to trace a file

Here are several ways to check if your Python script is accessing a `.yaml` file:

---

## 1. Search with `grep` (quickest)

```bash
grep -rn "\.yaml" your_script.py
```

This finds every line referencing `.yaml`. Add `-i` for case-insensitive (catches `.YAML` too).

---

## 2. Search for common YAML-loading patterns

```bash
grep -En "open\(|yaml\.load|yaml\.safe_load|yaml\.full_load" your_script.py
```

This targets the actual file-reading calls, not just string mentions.

---

## 3. Look for variable names holding YAML paths

```bash
grep -En '["\'].*\.yaml["\']|\.yaml' your_script.py
```

This catches both hardcoded paths like `"config.yaml"` and variable references.

---

## 4. Audit at runtime with a monkey-patch (dynamic tracing)

Add this **at the top** of your script temporarily — it intercepts every `open()` call and logs YAML access:

```python
import builtins

_real_open = builtins.open


def patched_open(file, *args, **kwargs):
    if isinstance(file, str) and file.endswith(".yaml"):
        print(f"[YAML ACCESS] Opening: {file}")
    return _real_open(file, *args, **kwargs)


builtins.open = patched_open
```

---

## 5. Use `strace` (Linux) to trace file access at OS level

```bash
strace -e openat python your_script.py 2>&1 | grep ".yaml"
```

This catches **all** file opens, even from libraries you didn't write.

---

## Which to use?

| Method       | Best for                           |
|--------------|------------------------------------|
| `grep`       | Quick static scan                  |
| Monkey-patch | Runtime paths (dynamic filenames)  |
| `strace`     | Third-party libraries loading YAML |

The **monkey-patch approach** is the most reliable if your YAML filenames are built dynamically at runtime (e.g.,
`f"{env}.yaml"`), since `grep` won't catch those.

