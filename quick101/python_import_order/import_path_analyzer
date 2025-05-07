#!/usr/bin/env python3
"""
Import Path Analyzer - Tracks imports and execution paths

Usage:
    python import_path_analyzer.py your_script.py [script arguments]

Options:
    --user-only       Show only user-defined packages (non-standard library)
    --export=FORMAT   Export results (json, csv, html)
"""

import sys
import os
import time
import importlib
import inspect
import argparse
import json
import csv
from pathlib import Path
import coverage
import subprocess
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze import sequences and execution paths")
    parser.add_argument('script', help='Python script to run and analyze')
    parser.add_argument('script_args', nargs='*', help='Arguments to pass to the script')
    parser.add_argument('--user-only', action='store_true', help='Show only user-defined packages')
    parser.add_argument('--export', choices=['json', 'csv', 'html'],
                        help='Export results in the specified format')
    return parser.parse_args()

def collect_import_data(script_path, script_args, user_only=False):
    """Collect import data by running the script with custom PYTHONPATH hooks"""

    # Create temporary script to track imports
    temp_dir = Path("./import_tracking_temp")
    temp_dir.mkdir(exist_ok=True)

    import_tracker_script = temp_dir / "import_tracker.py"
    with open(import_tracker_script, 'w') as f:
        f.write("""
import sys
import os
import time
import importlib.util
import json
from pathlib import Path

# Track imports
original_import = __import__
tracked_imports = []
import_times = {}
import_stack = {}

def custom_import(name, *args, **kwargs):
    start_time = time.time()
    module = original_import(name, *args, **kwargs)

    # Get caller information
    frame = sys._getframe(1)
    caller = frame.f_code.co_filename
    lineno = frame.f_lineno

    if name not in tracked_imports:
        tracked_imports.append(name)
        import_times[name] = time.time() - start_time
        import_stack[name] = {'caller': caller, 'line': lineno}

    return module

# Install the import hook
sys.__import__ = sys.modules['builtins'].__import__ = custom_import

# Continue with normal execution
""")

    # Create sitecustomize.py to automatically load our tracker
    sitecustomize = temp_dir / "sitecustomize.py"
    with open(sitecustomize, 'w') as f:
        f.write("""
import os
import sys
from pathlib import Path

# Load the import tracker
tracker_path = Path(__file__).parent / "import_tracker.py"
if tracker_path.exists():
    with open(tracker_path) as f:
        exec(f.read())
""")

    # Set up environment to use our custom import tracker
    env = os.environ.copy()
    python_path = str(temp_dir)
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = f"{python_path}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env['PYTHONPATH'] = python_path

    # Use coverage to track execution paths
    cov = coverage.Coverage()
    cov.start()

    # Run the target script with our custom import tracker
    cmd = [sys.executable, str(script_path)] + script_args
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)

    cov.stop()

    # Analyze results
    import_data = {}
    execution_paths = {}

    # Get coverage data for execution paths
    for filename in cov.get_data().measured_files():
        if user_only and _is_stdlib_module(filename):
            continue

        file_data = cov.analysis(filename)
        executed_lines = file_data[1]
        missing_lines = file_data[2]

        execution_paths[filename] = {
            'executed_lines': executed_lines,
            'missing_lines': missing_lines,
            'execution_percentage': len(executed_lines) / (len(executed_lines) + len(missing_lines)) * 100 if executed_lines or missing_lines else 0
        }

    # Try to extract the tracked imports from our custom tracking
    try:
        # This approach assumes we can access the sys.modules data
        # In a real implementation, you might need to serialize this data from the subprocess
        import_data = {
            'sequence': tracked_imports,
            'times': import_times,
            'stack': import_stack
        }
    except NameError:
        # Fallback to a simpler approach just listing the modules
        import_data = {
            'sequence': list(sys.modules.keys())
        }

    return {
        'imports': import_data,
        'execution_paths': execution_paths,
        'stdout': proc.stdout,
        'stderr': proc.stderr
    }

def _is_stdlib_module(module_path):
    """Check if a module is part of the standard library"""
    stdlib_paths = [os.path.dirname(os.__file__)]
    return any(module_path.startswith(path) for path in stdlib_paths)

def generate_report(data, user_only=False, export_format=None):
    """Generate a human-readable report of the import and execution data"""

    # Print header
    print("\n" + "="*80)
    print("IMPORT AND EXECUTION PATH ANALYSIS")
    print("="*80)

    # Print import sequence
    print("\nIMPORT SEQUENCE:")
    for i, module_name in enumerate(data['imports'].get('sequence', []), 1):
        if user_only and _is_stdlib_module(sys.modules.get(module_name, '').__file__ if module_name in sys.modules else ''):
            continue
        print(f"{i}. {module_name}")

        # Print additional details if available
        if 'times' in data['imports'] and module_name in data['imports']['times']:
            print(f"   Time: {data['imports']['times'][module_name]:.6f}s")

        if 'stack' in data['imports'] and module_name in data['imports']['stack']:
            caller_info = data['imports']['stack'][module_name]
            print(f"   Imported at: {caller_info['caller']}:{caller_info['line']}")

    # Print execution path summary
    print("\nEXECUTION PATH SUMMARY:")
    for filename, path_data in data['execution_paths'].items():
        rel_path = os.path.relpath(filename)
        print(f"\n{rel_path}:")
        print(f"  Executed {len(path_data['executed_lines'])} out of {len(path_data['executed_lines']) + len(path_data['missing_lines'])} lines")
        print(f"  Execution coverage: {path_data['execution_percentage']:.1f}%")

    # Export if requested
    if export_format:
        export_data(data, export_format)

def export_data(data, format):
    """Export the analysis data in the specified format"""

    if format == 'json':
        with open('import_analysis.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("\nExported data to import_analysis.json")

    elif format == 'csv':
        # Export imports
        with open('import_sequence.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Order', 'Module', 'Import Time', 'Caller', 'Line'])

            for i, module_name in enumerate(data['imports'].get('sequence', []), 1):
                import_time = data['imports'].get('times', {}).get(module_name, '')
                caller_info = data['imports'].get('stack', {}).get(module_name, {})
                writer.writerow([
                    i,
                    module_name,
                    import_time,
                    caller_info.get('caller', ''),
                    caller_info.get('line', '')
                ])

        # Export execution paths
        with open('execution_paths.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Executed Lines', 'Missing Lines', 'Coverage Percentage'])

            for filename, path_data in data['execution_paths'].items():
                writer.writerow([
                    filename,
                    len(path_data['executed_lines']),
                    len(path_data['missing_lines']),
                    path_data['execution_percentage']
                ])

        print("\nExported data to import_sequence.csv and execution_paths.csv")

    elif format == 'html':
        # Create a simple HTML report
        with open('import_analysis.html', 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Import and Execution Path Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .module-name { font-weight: bold; }
        .progress-bar {
            background-color: #4CAF50;
            height: 20px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <h1>Import and Execution Path Analysis</h1>

    <h2>Import Sequence</h2>
    <table>
        <tr>
            <th>#</th>
            <th>Module</th>
            <th>Import Time (s)</th>
            <th>Imported At</th>
        </tr>
""")

            for i, module_name in enumerate(data['imports'].get('sequence', []), 1):
                import_time = data['imports'].get('times', {}).get(module_name, '')
                caller_info = data['imports'].get('stack', {}).get(module_name, {})
                caller = f"{caller_info.get('caller', '')}:{caller_info.get('line', '')}" if caller_info else ''

                f.write(f"""
        <tr>
            <td>{i}</td>
            <td class="module-name">{module_name}</td>
            <td>{import_time}</td>
            <td>{caller}</td>
        </tr>
""")

            f.write("""
    </table>

    <h2>Execution Path Summary</h2>
    <table>
        <tr>
            <th>Module</th>
            <th>Coverage</th>
            <th>Executed Lines</th>
            <th>Missing Lines</th>
        </tr>
""")

            for filename, path_data in data['execution_paths'].items():
                rel_path = os.path.relpath(filename)
                coverage = path_data['execution_percentage']
                executed = len(path_data['executed_lines'])
                missing = len(path_data['missing_lines'])

                f.write(f"""
        <tr>
            <td>{rel_path}</td>
            <td>
                <div class="progress-bar" style="width: {coverage}%;"></div>
                {coverage:.1f}%
            </td>
            <td>{executed}</td>
            <td>{missing}</td>
        </tr>
""")

            f.write("""
    </table>
</body>
</html>
""")

            print("\nExported data to import_analysis.html")

def main():
    args = parse_args()

    print(f"Analyzing imports and execution paths for: {args.script}")
    if args.script_args:
        print(f"Script arguments: {' '.join(args.script_args)}")

    # Run the analysis
    data = collect_import_data(args.script, args.script_args, args.user_only)
    generate_report(data, args.user_only, args.export)

if __name__ == "__main__":
    main()