To get a clean list of unused modules using the built-in `trace` tool, you have to look for the `.cover` files where *
*every executable line** is marked as unexecuted (using the `>>>>>>` prefix).
> cleanup code
> cleanup unused code
> cleanup library

Here is how to combine `grep` with `trace` to find those "dead" modules.

### 1. Run the Trace

First, run your command to generate the `.cover` files in your output directory:

```bash
python -m trace --count -C ./output_dir --ignore-dir=$(python -c "import sys; print(sys.prefix)") my_script.py
```

### 2. Use `grep` to find "Totally Unused" files

We want to find files where **all** lines are unexecuted. However, a simpler and more effective way with `grep` is to
find files that contain *only* unexecuted markers and no actual execution counts.

Run this command from your terminal:

```bash
grep -L "1:" ./output_dir/*.cover
```

* **`-L` (or `--files-without-match`):** This tells grep to list the filenames that **do not** contain the string "1:".
* **"1:":** Since `trace` puts a `1:` (or `2:`, etc.) next to any line that ran at least once, any file missing "1:" is
  a file where **no lines were touched**.

### 3. Refined Search (The "Pure Dead Wood" List)

If you want to be more specific and look for files that are heavily flagged with the "unexecuted" marker (`>>>>>>`), you
can use this:

```bash
grep -l ">>>>>>" ./output_dir/*.cover | xargs grep -L "1:"
```

* This finds files that have unexecuted lines AND excludes any file that has at least one executed line.

---

### 4. Cleaning up the Output

The output will give you paths like `./output_dir/my_module.cover`. To get the actual module names to delete them, you
can pipe it to `sed`:

```bash
grep -L "1:" ./output_dir/*.cover | sed 's/.*\///;s/\.cover//'
```

* This strips the directory path and the `.cover` extension, leaving you with just the module name (e.g.,
  `unused_helper`).

## Cleanup Script

This script will analyze the .cover files in your output directory. Identify which .py files were never executed (no
line counts)
and move those unused files into a _trash_bin folder instead of deleting them.

```python
import os
import shutil
import glob

# --- Configuration ---
SOURCE_DIR = "./"
COVERAGE_DIR = "./output_dir"
TRASH_DIR = "./_trash_bin"

# ADD YOUR DRIVER FILENAME HERE to ensure it is never moved
PROTECTED_FILES = ["my_script.py", "config.py", "clean_modules.py"]


def get_unused_modules():
    unused = []
    # Get a list of all .py files in the source directory
    all_py_files = [os.path.basename(f) for f in glob.glob(os.path.join(SOURCE_DIR, "*.py"))]

    # Get a list of files that actually show execution in the trace output
    used_files = []
    for cover_file in glob.glob(os.path.join(COVERAGE_DIR, "*.cover")):
        with open(cover_file, 'r') as f:
            if any(line.strip().startswith(tuple(f"{i}:" for i in range(1, 10))) for line in f):
                # If any line starts with 1:, 2:, etc., it was used
                base_name = os.path.basename(cover_file).replace(".cover", ".py")
                used_files.append(base_name)

    # Logic: If it's a .py file, NOT in the 'used' list, and NOT protected -> it's unused
    for py_file in all_py_files:
        if py_file not in used_files and py_file not in PROTECTED_FILES:
            unused.append(py_file)

    return unused


def move_to_trash(files):
    if not os.path.exists(TRASH_DIR):
        os.makedirs(TRASH_DIR)

    for filename in files:
        src = os.path.join(SOURCE_DIR, filename)
        dst = os.path.join(TRASH_DIR, filename)

        if os.path.exists(src):
            print(f"Moving {filename} to {TRASH_DIR}")
            shutil.move(src, dst)


if __name__ == "__main__":
    unused_files = get_unused_modules()
    if not unused_files:
        print("Everything is in use or protected.")
    else:
        print(f"Found {len(unused_files)} unused modules.")
        print(f"Items to move: {unused_files}")
        confirm = input("Move these to trash bin? (y/n): ")
        if confirm.lower() == 'y':
            move_to_trash(unused_files)
```