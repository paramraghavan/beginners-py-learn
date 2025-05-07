#!/usr/bin/env python3
"""
Import Tracker - A cleaner alternative to python -v

Usage:
    python import_tracker.py your_script.py [script arguments]

Options:
    --user-only  Show only user-defined packages (non-standard library)
    --detail     Show import timing and location information
"""

import sys
import os
import time
import importlib
import inspect
import argparse
from pathlib import Path
import runpy
from typing import Dict, Set, List, Tuple, Optional

# Original import hook to track imports
original_import = __import__

# Tracking state
tracked_imports = []
import_times = {}
import_locations = {}
start_times = {}
STANDARD_LIB_PATHS = [os.path.dirname(os.__file__)]


def parse_args():
    parser = argparse.ArgumentParser(description="Track Python imports with detailed sequence")
    parser.add_argument('script', help='Python script to run and analyze')
    parser.add_argument('script_args', nargs='*', help='Arguments to pass to the script')
    parser.add_argument('--user-only', action='store_true', help='Show only user-defined packages')
    parser.add_argument('--detail', action='store_true', help='Show import timing and location')
    return parser.parse_args()


def is_stdlib_module(module_name: str, module_path: Optional[str]) -> bool:
    """Check if a module is part of the standard library."""
    if module_path is None:
        return False

    for stdlib_path in STANDARD_LIB_PATHS:
        if module_path.startswith(stdlib_path):
            return True

    # Additional checks for built-in modules
    if module_name in sys.builtin_module_names:
        return True

    return False


def custom_import(name, *args, **kwargs):
    """Custom import hook to track module imports and their sequence."""
    # Record the start time
    start_times[name] = time.time()

    # Call the original import
    module = original_import(name, *args, **kwargs)

    # Track this import if we haven't seen it before
    if name not in tracked_imports:
        tracked_imports.append(name)

        # Record the import time
        import_times[name] = time.time() - start_times[name]

        # Try to get the file location
        module_path = getattr(module, '__file__', None)
        if module_path:
            import_locations[name] = module_path

        # Get call stack to find where the import was requested
        stack = inspect.stack()
        if len(stack) > 2:  # Skip this function and the import machinery
            caller = stack[2]
            if hasattr(caller, 'filename'):
                # Store tuple of (filename, line_number)
                import_locations[name] = (caller.filename, caller.lineno)

    return module


def print_import_report(user_only=False, detailed=False):
    """Print a report of all imports in the order they were loaded."""
    print("\n" + "=" * 80)
    print("IMPORT SEQUENCE REPORT")
    print("=" * 80)

    for i, module_name in enumerate(tracked_imports, 1):
        # Skip standard library modules if user_only is True
        module_path = import_locations.get(module_name, None)
        if user_only and is_stdlib_module(module_name, module_path):
            continue

        # Print the basic import info
        print(f"{i}. {module_name}")

        # If detailed mode, print more information
        if detailed:
            import_time = import_times.get(module_name, 0)
            print(f"   Time: {import_time:.6f}s")

            location = import_locations.get(module_name)
            if location:
                if isinstance(location, tuple):
                    print(f"   Imported at: {location[0]}:{location[1]}")
                else:
                    print(f"   Location: {location}")
            print()


def main():
    args = parse_args()

    # Set up the import hook
    sys.path.insert(0, os.path.dirname(os.path.abspath(args.script)))
    sys.__import__ = sys.modules['builtins'].__import__ = custom_import

    # Prepare script arguments
    sys.argv = [args.script] + args.script_args

    # Run the target script
    try:
        # Use runpy to run the script with the modified import
        script_path = Path(args.script).resolve()
        runpy.run_path(str(script_path), run_name='__main__')
    except Exception as e:
        print(f"Error running script: {e}")
    finally:
        # Print the import report
        print_import_report(args.user_only, args.detail)


if __name__ == "__main__":
    main()