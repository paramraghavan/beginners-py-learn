import os
import ast
import sys
import re
import subprocess
import pkg_resources
from pathlib import Path
from collections import defaultdict, Counter
import argparse


class RequirementsGenerator:
    def __init__(self):
        # Standard library modules (Python 3.x)
        self.stdlib_modules = self._get_stdlib_modules()

        # Common import mappings (import name -> package name)
        self.import_mappings = {
            'cv2': 'opencv-python',
            'PIL': 'Pillow',
            'skimage': 'scikit-image',
            'sklearn': 'scikit-learn',
            'yaml': 'PyYAML',
            'dotenv': 'python-dotenv',
            'requests': 'requests',
            'bs4': 'beautifulsoup4',
            'flask': 'Flask',
            'django': 'Django',
            'tf': 'tensorflow',
            'torch': 'torch',
            'np': 'numpy',  # common alias
            'pd': 'pandas',  # common alias
            'plt': 'matplotlib',  # common alias
            'sns': 'seaborn',  # common alias
        }

        self.found_imports = Counter()
        self.files_analyzed = []

    def _get_stdlib_modules(self):
        """Get list of standard library modules for current Python version"""
        stdlib_modules = set()

        # Core built-in modules
        stdlib_modules.update([
            'os', 'sys', 'time', 'datetime', 'json', 'csv', 'math', 'random',
            'collections', 'itertools', 'functools', 'operator', 'typing',
            'pathlib', 'glob', 're', 'string', 'io', 'pickle', 'copy',
            'threading', 'multiprocessing', 'subprocess', 'argparse',
            'logging', 'unittest', 'sqlite3', 'urllib', 'http', 'email',
            'html', 'xml', 'zipfile', 'tarfile', 'tempfile', 'shutil',
            'platform', 'socket', 'ssl', 'hashlib', 'hmac', 'secrets',
            'base64', 'binascii', 'struct', 'array', 'heapq', 'bisect',
            'weakref', 'gc', 'contextlib', 'abc', 'numbers', 'decimal',
            'fractions', 'statistics', 'enum', 'dataclasses', 'asyncio',
            'concurrent', 'queue', 'sched', 'signal', 'warnings', 'traceback',
            'inspect', 'importlib', 'pkgutil', 'modulefinder', 'runpy',
            'ast', 'dis', 'py_compile', 'compileall', 'keyword', 'token',
            'tokenize', 'parser', 'symbol', 'code', 'codeop'
        ])

        return stdlib_modules

    def extract_imports_from_file(self, file_path):
        """Extract all imports from a Python file using AST"""
        imports = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Parse the file into an AST
            tree = ast.parse(content)

            # Walk through all nodes in the AST
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])

            # Also check for requirements in comments
            comment_imports = self._extract_from_comments(content)
            imports.update(comment_imports)

        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
            # Fallback to regex parsing
            imports.update(self._extract_imports_regex(file_path))

        return imports

    def _extract_from_comments(self, content):
        """Extract package names from comments like # pip install package"""
        imports = set()

        # Look for pip install commands in comments
        pip_pattern = r'#.*?pip install\s+([\w\-\[\]>=<.,\s]+)'
        matches = re.findall(pip_pattern, content, re.IGNORECASE)

        for match in matches:
            # Split by spaces and clean up
            packages = match.split()
            for pkg in packages:
                # Remove version specifiers and extras
                clean_pkg = re.sub(r'[>=<!\[\].,0-9\s].*$', '', pkg)
                if clean_pkg:
                    imports.add(clean_pkg)

        return imports

    def _extract_imports_regex(self, file_path):
        """Fallback regex-based import extraction"""
        imports = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Regular expressions for different import patterns
            patterns = [
                r'^import\s+(\w+)',
                r'^from\s+(\w+)\s+import',
                r'^\s*import\s+(\w+)',
                r'^\s*from\s+(\w+)\s+import'
            ]

            for line in content.split('\n'):
                for pattern in patterns:
                    match = re.match(pattern, line.strip())
                    if match:
                        imports.add(match.group(1))

        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")

        return imports

    def find_python_files(self, path):
        """Find all Python files in a directory or return single file"""
        python_files = []

        path = Path(path)

        if path.is_file() and path.suffix == '.py':
            python_files.append(path)
        elif path.is_dir():
            # Recursively find all .py files
            python_files = list(path.rglob('*.py'))
        else:
            raise ValueError(f"Path {path} is not a valid Python file or directory")

        return python_files

    def analyze_path(self, path):
        """Analyze all Python files in the given path"""
        python_files = self.find_python_files(path)

        print(f"Found {len(python_files)} Python files to analyze...")

        all_imports = set()

        for file_path in python_files:
            print(f"Analyzing: {file_path}")
            imports = self.extract_imports_from_file(file_path)
            all_imports.update(imports)
            self.files_analyzed.append(str(file_path))

            # Count frequency of imports
            for imp in imports:
                self.found_imports[imp] += 1

        return all_imports

    def filter_third_party_packages(self, imports):
        """Filter out standard library modules"""
        third_party = set()

        for imp in imports:
            # Skip standard library modules
            if imp not in self.stdlib_modules:
                third_party.add(imp)

        return third_party

    def resolve_package_names(self, imports):
        """Resolve import names to actual package names"""
        packages = set()

        for imp in imports:
            # Check if we have a mapping for this import
            if imp in self.import_mappings:
                packages.add(self.import_mappings[imp])
            else:
                # Try to find the package name
                package_name = self._find_package_name(imp)
                if package_name:
                    packages.add(package_name)
                else:
                    # If we can't find it, use the import name
                    packages.add(imp)

        return packages

    def _find_package_name(self, import_name):
        """Try to find the actual package name for an import"""
        try:
            # Try to import the module and get its package info
            __import__(import_name)

            # Look through installed packages to find which one provides this module
            for dist in pkg_resources.working_set:
                if dist.has_metadata('top_level.txt'):
                    top_level = dist.get_metadata('top_level.txt').strip().split('\n')
                    if import_name in top_level:
                        return dist.project_name

        except ImportError:
            pass

        return None

    def get_package_versions(self, packages):
        """Get installed versions of packages"""
        versions = {}

        for package in packages:
            try:
                dist = pkg_resources.get_distribution(package)
                versions[package] = dist.version
            except pkg_resources.DistributionNotFound:
                versions[package] = None

        return versions

    def generate_requirements(self, path, output_file='requirements.txt',
                              include_versions=True, sort_by_frequency=False):
        """Generate requirements.txt file"""

        print(f"Analyzing Python files in: {path}")
        print("-" * 50)

        # Extract all imports
        all_imports = self.analyze_path(path)

        # Filter third-party packages
        third_party = self.filter_third_party_packages(all_imports)

        # Resolve to package names
        packages = self.resolve_package_names(third_party)

        # Get versions if requested
        if include_versions:
            versions = self.get_package_versions(packages)

        # Sort packages
        if sort_by_frequency:
            # Sort by how often they appear in files
            package_freq = {}
            for pkg in packages:
                # Try to map back to import name for frequency lookup
                import_name = None
                for imp, mapped_pkg in self.import_mappings.items():
                    if mapped_pkg == pkg:
                        import_name = imp
                        break
                if not import_name:
                    import_name = pkg

                package_freq[pkg] = self.found_imports.get(import_name, 0)

            packages = sorted(packages, key=lambda x: package_freq.get(x, 0), reverse=True)
        else:
            packages = sorted(packages)

        # Generate requirements.txt content
        requirements_lines = []

        for package in packages:
            if include_versions and package in versions and versions[package]:
                line = f"{package}=={versions[package]}"
            else:
                line = package
            requirements_lines.append(line)

        # Write to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(requirements_lines))

        # Print summary
        print(f"\nAnalysis complete!")
        print(f"Files analyzed: {len(self.files_analyzed)}")
        print(f"Total imports found: {len(all_imports)}")
        print(f"Third-party packages: {len(packages)}")
        print(f"Requirements saved to: {output_file}")

        # Show the generated requirements
        print(f"\nGenerated {output_file}:")
        print("-" * 30)
        for line in requirements_lines:
            print(line)

        # Show most common imports
        if self.found_imports:
            print(f"\nMost frequently imported packages:")
            for imp, count in self.found_imports.most_common(10):
                if imp not in self.stdlib_modules:
                    print(f"  {imp}: {count} files")


def main():
    parser = argparse.ArgumentParser(
        description="Generate requirements.txt from Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python requirements_generator.py myproject/
  python requirements_generator.py script.py
  python requirements_generator.py . --output deps.txt
  python requirements_generator.py myproject/ --no-versions
  python requirements_generator.py . --sort-frequency
        """
    )

    parser.add_argument('path', help='Python file or directory to analyze')
    parser.add_argument('--output', '-o', default='requirements.txt',
                        help='Output file name (default: requirements.txt)')
    parser.add_argument('--no-versions', action='store_true',
                        help='Don\'t include version numbers')
    parser.add_argument('--sort-frequency', action='store_true',
                        help='Sort by import frequency instead of alphabetically')

    args = parser.parse_args()

    try:
        generator = RequirementsGenerator()
        generator.generate_requirements(
            path=args.path,
            output_file=args.output,
            include_versions=not args.no_versions,
            sort_by_frequency=args.sort_frequency
        )

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """
    This script automatically generates a requirements.txt file by analyzing  Python code/package
    """
    main()

# Quick usage examples:
"""
# Analyze current directory
python requirements_generator.py .

# Analyze specific file
python requirements_generator.py my_script.py

# Analyze project folder
python requirements_generator.py /path/to/project/

# Custom output file
python requirements_generator.py myproject/ --output my_requirements.txt

# Without version numbers
python requirements_generator.py . --no-versions

# Sort by frequency of use
python requirements_generator.py . --sort-frequency
"""
