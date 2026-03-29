Tools to find your "bare minimum" code.
> cleanup code
> cleanup unused code
---

## Option 1: Using `coverage.py` (Recommended)

This is the most accurate way to handle those "sometimes-executed" paths because it can merge multiple runs into one
report.

### 1. Installation

```bash
pip install coverage
```

### 2. Running your script

To capture every possible path, run your script for each different scenario.

* **First run:** `coverage run my_script.py --mode=fast`
* **Second run (adds to the first):** `coverage run -a my_script.py --mode=thorough`

The `-a` (append) flag is critical. It ensures that if a module is used in the second run but not the first, it stays
marked as "used."

### 3. Seeing the results

Once you've exercised all code paths, generate the report:

```bash
coverage report -m
```

The `-m` flag shows exactly which **line numbers** were missed. If an entire module or a large block of code shows as
missed, you can safely consider removing it.



---

## Option 2: Using `trace` (The Built-in Way)

If you cannot install `coverage.py`, use the built-in `trace` module. It is more "noisy" because it creates a file for
every single module touched.

### 1. Running the command

```bash
python -m trace --count -C ./output_dir my_script.py
```

* `--count`: Counts how many times each line was executed.
* `-C ./output_dir`: Tells Python where to save the results (otherwise it clutters your script folder).

### 2. Analyzing the `.cover` files

Inside your `output_dir`, you will see files ending in `.cover` for every module your script imported.

* Open a file (e.g., `useful_module.cover`).
* Lines starting with `>>>>>>` were **never executed**.
* Lines starting with a number (e.g., `1:`) were executed that many times.

---

By default, yes—the `trace` module is very thorough (and very loud). When you run it, it attempts to trace **every
single line of code** that gets executed from the moment the Python interpreter starts.

This includes:

1. Your main script.
2. The modules you wrote and imported.
3. **The Python Standard Library** (e.g., `os`, `sys`, `json`).
4. Any third-party packages installed in your site-packages.

If you don't filter it, `trace` will generate hundreds of `.cover` files for things you didn't write, like `abc.py` or
`_bootlocale.py`, which makes finding your own "bare minimum" code very difficult.

---

## How to limit `trace` to your files

To prevent `trace` from mapping every single import in the entire Python ecosystem, you should use the `--ignore-dir`
flag.

### 1. Ignore the Standard Library

On most systems, you can tell `trace` to ignore the directory where Python’s built-in modules live:

```bash
python -m trace --count -C ./output_dir --ignore-dir=$(python -c "import sys; print(sys.prefix)") my_script.py
```

### 2. Focus only on your local directory

If you only want to see the "coverage" for the modules in your current folder, you have to be careful. `trace` doesn't
have a "trace only this folder" flag, but it *does* let you ignore multiple directories.

## Comparison Table

| Feature      | `coverage.py`             | `trace` (Built-in)                 |
|:-------------|:--------------------------|:-----------------------------------|
| **Visuals**  | High-quality HTML/Tables  | Plain text files                   |
| **Merging**  | Easy (uses `-a` flag)     | Difficult/Manual                   |
| **Speed**    | Fast (C-based)            | Slower (Python-based)              |
| **Best For** | Pro cleanup & Refactoring | Quick checks on restricted systems |

---

## Your Cleanup Strategy

To keep the bare minimum without breaking those "sometimes-used" paths:

1. **Run your tool of choice** through every possible user scenario.
2. **Identify the "Dark Code":** Look for modules or functions with 0% coverage.
3. **The "Move, Don't Delete" Step:** Instead of deleting, move the unused `.py` files to a folder named `_unused`.
4. **Final Test:** Run the script one last time. If it still works, you can safely delete the `_unused` folder.

