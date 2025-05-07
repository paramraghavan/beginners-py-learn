#!/usr/bin/env python3
"""
Static Module Dependency Mapper

This tool maps static import dependencies in Python code and combines with
runtime analysis to show which imports are actually used in different execution paths.

Usage:
    python module_mapper.py path/to/project [options]

Options:
    --run SCRIPT      Run the SCRIPT and track imports during execution
    --entry SCRIPT    Specify the entry point script for analysis without running
    --args "ARG1..."  Pass arguments to the script when using --run
    --exclude PATTERN Exclude files matching pattern (can be used multiple times)
    --graph           Generate a dependency graph visualization (requires graphviz)
    --user-only       Only show user-defined modules (filter out standard library)
"""

import sys
import os
import ast
import importlib
import pkgutil
import argparse
import re
from pathlib import Path
import time
from typing import Dict, Set, List, Tuple, Optional
import json

# For visualizing the import graph
try:
    import graphviz

    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False


# Store import information
class ImportInfo:
    def __init__(self, name, level=0, alias=None, lineno=0, asname=None):
        self.name = name  # The module name being imported
        self.level = level  # Relative import level
        self.alias = alias  # For 'from X import Y'
        self.lineno = lineno  # Line number in the file
        self.asname = asname  # For 'import X as Y'

    def __repr__(self):
        if self.alias:
            return f"from {self.name} import {self.alias}"
        return f"import {self.name}"


class ModuleVisitor(ast.NodeVisitor):
    """AST visitor to find all imports in a Python file"""

    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        """Handle 'import X' statements"""
        for name in node.names:
            self.imports.append(ImportInfo(
                name=name.name,
                lineno=node.lineno,
                asname=name.asname
            ))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Handle 'from X import Y' statements"""
        if node.module is None:
            # Handle relative imports like 'from . import module'
            for name in node.names:
                self.imports.append(ImportInfo(
                    name="",
                    level=node.level,
                    alias=name.name,
                    lineno=node.lineno,
                    asname=name.asname
                ))
        else:
            module_name = node.module
            for name in node.names:
                self.imports.append(ImportInfo(
                    name=module_name,
                    level=node.level,
                    alias=name.name,
                    lineno=node.lineno,
                    asname=name.asname
                ))
        self.generic_visit(node)


def get_source_code_imports(file_path: str) -> List[ImportInfo]:
    """Parse a Python file and extract all import statements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=file_path)
        visitor = ModuleVisitor()
        visitor.visit(tree)
        return visitor.imports
    except (SyntaxError, UnicodeDecodeError, PermissionError) as e:
        print(f"Error parsing {file_path}: {e}")
        return []


def is_stdlib_module(module_name: str) -> bool:
    """Check if a module is part of the standard library"""
    try:
        spec = importlib.util.find_spec(module_name.split('.')[0])
        if spec and spec.origin:
            # If it's in the standard library path
            return spec.origin.startswith(os.path.dirname(os.__file__))

        # Check if it's a built-in module
        return module_name in sys.builtin_module_names
    except (ImportError, AttributeError, ValueError):
        return False


def find_python_files(directory: str, exclude_patterns: List[str] = None) -> List[str]:
    """Find all Python files in a directory recursively"""
    if exclude_patterns is None:
        exclude_patterns = []

    python_files = []

    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(re.match(pattern, os.path.join(root, d)) for pattern in exclude_patterns)]

        # Add Python files that aren't excluded
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if not any(re.match(pattern, file_path) for pattern in exclude_patterns):
                    python_files.append(file_path)

    return python_files


def resolve_relative_import(base_module: str, import_info: ImportInfo) -> str:
    """Resolve a relative import to an absolute module name"""
    if import_info.level == 0 or not base_module:
        return import_info.name

    # Split the base module
    parts = base_module.split('.')

    # Remove as many parts as the level of the relative import
    if import_info.level > len(parts):
        raise ValueError(f"Invalid relative import: level {import_info.level} is too high for module {base_module}")

    new_parts = parts[:-import_info.level]

    # Add the imported module name
    if import_info.name:
        new_parts.append(import_info.name)

    return '.'.join(new_parts)


def module_from_file_path(file_path: str, project_root: str) -> str:
    """Convert a file path to a Python module name"""
    rel_path = os.path.relpath(file_path, project_root)
    # Remove '.py' extension and replace path separators with dots
    module_name = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
    return module_name


def analyze_project(project_root: str, exclude_patterns: List[str] = None) -> Dict:
    """Analyze all Python files in a project and build a dependency graph"""
    python_files = find_python_files(project_root, exclude_patterns)

    # Map of module names to their file paths
    module_to_file = {}
    # Map of file paths to their module names
    file_to_module = {}
    # Map of modules to their imports
    module_imports = {}
    # Map of modules to modules that import them
    reverse_imports = {}

    # First pass: Build the module mapping
    for file_path in python_files:
        module_name = module_from_file_path(file_path, project_root)
        module_to_file[module_name] = file_path
        file_to_module[file_path] = module_name
        module_imports[module_name] = []
        reverse_imports[module_name] = []

    # Second pass: Parse imports and build the dependency graph
    for module_name, file_path in module_to_file.items():
        imports = get_source_code_imports(file_path)

        for imp in imports:
            try:
                if imp.level > 0:
                    # Resolve relative imports
                    absolute_name = resolve_relative_import(module_name, imp)
                else:
                    absolute_name = imp.name

                # Store the import info
                module_imports[module_name].append({
                    'name': absolute_name,
                    'alias': imp.alias,
                    'lineno': imp.lineno,
                    'asname': imp.asname
                })

                # Add to reverse imports if it's a project module
                if absolute_name in module_imports:
                    reverse_imports[absolute_name].append(module_name)

            except ValueError as e:
                print(f"Warning: {e}")

    return {
        'module_to_file': module_to_file,
        'file_to_module': file_to_module,
        'module_imports': module_imports,
        'reverse_imports': reverse_imports
    }


def track_runtime_imports(script: str, args: List[str] = None) -> Dict:
    """Run a script and track which imports are used at runtime"""
    if args is None:
        args = []

    # Save the original import function
    original_import = __import__

    # Storage for runtime import data
    runtime_imports = []
    import_times = {}
    import_order = {}
    import_count = 0

    # Custom import hook
    def custom_import(name, *args, **kwargs):
        nonlocal import_count
        start_time = time.time()

        # Call the original import
        module = original_import(name, *args, **kwargs)

        # Record the import
        if name not in runtime_imports:
            runtime_imports.append(name)
            import_times[name] = time.time() - start_time
            import_order[name] = import_count
            import_count += 1

        return module

    # Install the custom import hook
    sys.__import__ = sys.modules['builtins'].__import__ = custom_import

    # Set up command line arguments
    sys.argv = [script] + args

    # Import the script module
    try:
        # Use execfile-like approach to run the script
        with open(script, 'rb') as f:
            script_code = compile(f.read(), script, 'exec')

        # Create a new module context and execute the script
        script_globals = {
            '__name__': '__main__',
            '__file__': script,
            '__builtins__': __builtins__
        }

        # Execute the script
        exec(script_code, script_globals)

    except Exception as e:
        print(f"Error running {script}: {e}")
    finally:
        # Restore the original import function
        sys.__import__ = sys.modules['builtins'].__import__ = original_import

    # Order the runtime imports by the order they were imported
    ordered_imports = sorted(runtime_imports, key=lambda x: import_order.get(x, 0))

    return {
        'imports': ordered_imports,
        'times': import_times,
        'order': import_order
    }


def generate_dependency_graph(project_data: Dict, runtime_data: Dict = None,
                              user_only: bool = False) -> graphviz.Digraph:
    """Generate a visual dependency graph of the project modules"""
    if not GRAPHVIZ_AVAILABLE:
        print("Error: graphviz library not available. Install with 'pip install graphviz'.")
        return None

    dot = graphviz.Digraph(comment='Module Dependencies')

    # Define node styles
    dot.attr('node', shape='box', style='filled', fontname='Arial')

    # Add the nodes (modules)
    for module_name in project_data['module_to_file']:
        if user_only and is_stdlib_module(module_name.split('.')[0]):
            continue

        # Check if this module was used at runtime
        is_runtime = runtime_data and module_name in runtime_data['imports']

        # Set color based on runtime usage
        if runtime_data:
            if is_runtime:
                dot.node(module_name, fillcolor='lightblue')
            else:
                dot.node(module_name, fillcolor='lightgrey')
        else:
            dot.node(module_name, fillcolor='lightgreen')

    # Add the edges (imports)
    for module_name, imports in project_data['module_imports'].items():
        if user_only and is_stdlib_module(module_name.split('.')[0]):
            continue

        for imp_info in imports:
            target_module = imp_info['name']

            # Skip standard library modules if requested
            if user_only and is_stdlib_module(target_module.split('.')[0]):
                continue

            # Only add edges between project modules
            if target_module in project_data['module_to_file']:
                # Color the edge based on runtime usage
                if runtime_data and module_name in runtime_data['imports'] and target_module in runtime_data['imports']:
                    dot.edge(module_name, target_module, color='blue', penwidth='2.0')
                else:
                    dot.edge(module_name, target_module, color='black', penwidth='1.0')

    return dot


def print_import_sequence_report(project_data: Dict, runtime_data: Dict = None, user_only: bool = False):
    """Print a detailed report of module import sequences"""

    print("\n" + "=" * 80)
    print("MODULE IMPORT SEQUENCE ANALYSIS")
    print("=" * 80)

    # If we have runtime data, show the runtime import sequence first
    if runtime_data:
        print("\nRUNTIME IMPORT SEQUENCE:")
        for i, module_name in enumerate(runtime_data['imports'], 1):
            if user_only and is_stdlib_module(module_name.split('.')[0]):
                continue

            import_time = runtime_data['times'].get(module_name, 0)

            # Check if it's a project module or external
            is_project_module = module_name in project_data['module_to_file']
            module_type = "Project" if is_project_module else "External"

            print(f"{i:3d}. {module_name} [{module_type}] - {import_time:.6f}s")

    # Then show the static dependencies
    print("\nSTATIC IMPORT DEPENDENCIES:")

    # Group modules by their import hierarchy (entry points first)
    entry_points = []
    imported_by = {}

    for module_name in project_data['module_to_file']:
        if user_only and is_stdlib_module(module_name.split('.')[0]):
            continue

        importers = project_data['reverse_imports'][module_name]
        imported_by[module_name] = len(importers)

        # An entry point has no importers within the project
        if len(importers) == 0:
            entry_points.append(module_name)

    # Print the entry points
    print("\nENTRY POINTS (modules not imported by other modules):")
    for i, module_name in enumerate(sorted(entry_points), 1):
        file_path = project_data['module_to_file'][module_name]
        rel_path = os.path.relpath(file_path)
        print(f"{i}. {module_name} ({rel_path})")

    # Print modules by how many times they're imported
    print("\nMOST IMPORTED MODULES:")
    most_imported = sorted(imported_by.items(), key=lambda x: x[1], reverse=True)
    for i, (module_name, count) in enumerate(most_imported[:10], 1):
        if count > 0:
            file_path = project_data['module_to_file'][module_name]
            rel_path = os.path.relpath(file_path)
            print(f"{i}. {module_name} - imported by {count} modules ({rel_path})")

    # Print import relationships for each module
    print("\nDETAILED MODULE IMPORTS:")
    for module_name in sorted(project_data['module_to_file'].keys()):
        if user_only and is_stdlib_module(module_name.split('.')[0]):
            continue

        file_path = project_data['module_to_file'][module_name]
        rel_path = os.path.relpath(file_path)

        # Skip modules with no imports if they're not runtime modules
        has_imports = len(project_data['module_imports'][module_name]) > 0
        is_runtime = runtime_data and module_name in runtime_data['imports']

        if has_imports or is_runtime:
            print(f"\n{module_name} ({rel_path}):")

            # Print its imports
            imports = project_data['module_imports'][module_name]
            if imports:
                print("  Imports:")
                for imp_info in sorted(imports, key=lambda x: x['lineno']):
                    name = imp_info['name']
                    alias = imp_info['alias']
                    lineno = imp_info['lineno']

                    # Skip standard library modules if requested
                    if user_only and is_stdlib_module(name.split('.')[0]):
                        continue

                    # Check if it was used at runtime
                    used_at_runtime = runtime_data and name in runtime_data['imports']
                    runtime_marker = "* " if used_at_runtime else "  "

                    if alias:
                        print(f"  {runtime_marker}Line {lineno}: from {name} import {alias}")
                    else:
                        print(f"  {runtime_marker}Line {lineno}: import {name}")

            # Print modules that import this one
            importers = project_data['reverse_imports'][module_name]
            if importers:
                print("  Imported by:")
                for importer in sorted(importers):
                    if user_only and is_stdlib_module(importer.split('.')[0]):
                        continue

                    used_at_runtime = runtime_data and importer in runtime_data['imports']
                    runtime_marker = "* " if used_at_runtime else "  "
                    print(f"  {runtime_marker}{importer}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python module dependencies and import sequences",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('project_root', help='Root directory of the Python project to analyze')
    parser.add_argument('--run', help='Run a script and track imports during execution')
    parser.add_argument('--entry', help='Specify entry point script without running it')
    parser.add_argument('--args', help='Arguments to pass to the script (in quotes)')
    parser.add_argument('--exclude', action='append', default=[],
                        help='Exclude files matching pattern (can be used multiple times)')
    parser.add_argument('--graph', action='store_true', help='Generate a dependency graph visualization')
    parser.add_argument('--user-only', action='store_true', help='Only show user-defined modules')
    parser.add_argument('--output', help='Output file for the report (default: print to console)')

    args = parser.parse_args()

    # Parse script arguments if provided
    script_args = []
    if args.args:
        import shlex
        script_args = shlex.split(args.args)

    # Analyze the project
    print(f"Analyzing project: {args.project_root}")
    project_data = analyze_project(args.project_root, args.exclude)

    # Track runtime imports if requested
    runtime_data = None
    if args.run:
        print(f"Running script and tracking imports: {args.run}")
        runtime_data = track_runtime_imports(args.run, script_args)

    # Print the report
    print_import_sequence_report(project_data, runtime_data, args.user_only)

    # Generate graph if requested
    if args.graph and GRAPHVIZ_AVAILABLE:
        print("Generating dependency graph...")
        graph = generate_dependency_graph(project_data, runtime_data, args.user_only)

        # Save the graph
        graph_file = 'module_dependencies'
        graph.render(graph_file, format='pdf', cleanup=True)
        print(f"Graph saved to {graph_file}.pdf")
    elif args.graph and not GRAPHVIZ_AVAILABLE:
        print("Warning: Cannot generate graph. Install graphviz with 'pip install graphviz'.")


if __name__ == "__main__":
    main()