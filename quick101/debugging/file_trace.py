"""
We are importing many python modules each of these modules read yaml file from various folder.
 A single point of change to introspect python file open or file read operation , this way we
can do this before all the module imports and  can print out files and respective folders
from where they are loaded
"""

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
