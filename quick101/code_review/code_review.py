import os
import sys
import subprocess
import ast
import re
from pathlib import Path

# Flake8 error code descriptions
flake8_error_descriptions = {
    'F401': 'Module imported but unused',
    'F821': 'Undefined name',
    'E302': 'Expected 2 blank lines, found 1',
    # Add more codes as needed
}

# Pylint error code descriptions
pylint_error_descriptions = {
    'C0114': 'Missing module docstring',
    'C0115': 'Missing class docstring',
    'C0116': 'Missing function or method docstring',
    'E1101': 'Module has no member',
    # Add more codes as needed
}

def run_subprocess(command, description, tool=None):
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout or "✅ No issues found."
        print(output)

        # Choose the appropriate error descriptions
        if tool == 'flake8':
            error_descriptions = flake8_error_descriptions
        elif tool == 'pylint':
            error_descriptions = pylint_error_descriptions
        else:
            error_descriptions = {}

        # Parse and annotate each line with descriptions
        for line in output.strip().split('\n'):
            match = re.search(r'([A-Z]\d{3,4})', line)
            if match:
                code = match.group(1)
                desc = error_descriptions.get(code, 'Description not found.')
                print(f"{line}\n   👉 {desc}\n")
            else:
                print(line)

        if result.stderr:
            print("⚠️  Errors:\n", result.stderr)
    except Exception as e:
        print(f"❌ Error running {description}: {e}")

def check_ast(file_path):
    print(f"\n📘 Analyzing structure and docstrings in: {file_path}")
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    for cls in classes:
        doc = ast.get_docstring(cls)
        print(f"\n🔹 Class: {cls.name}")
        print("   📄 Docstring:", "✅ Yes" if doc else "❌ Missing")

    for func in functions:
        doc = ast.get_docstring(func)
        print(f"\n🔸 Function: {func.name}")
        print("   📄 Docstring:", "✅ Yes" if doc else "❌ Missing")

def analyze_code(file_or_dir):
    path = Path(file_or_dir)
    if not path.exists():
        print(f"❌ Path not found: {file_or_dir}")
        return

    if path.is_file() and path.suffix == '.py':
        check_ast(file_or_dir)
    else:
        for py_file in path.rglob("*.py"):
            check_ast(py_file)

    run_subprocess(f"flake8 {file_or_dir}", "PEP8/flake8 style check", tool='flake8')
    run_subprocess(f"pylint {file_or_dir}", "Pylint code quality analysis", tool='pylint')
    run_subprocess(f"radon cc {file_or_dir} -a", "Radon cyclomatic complexity check")
    run_subprocess(f"radon mi {file_or_dir}", "Radon maintainability index")
    run_subprocess(f"pydocstyle {file_or_dir}", "Docstring style check (pydocstyle)")

if __name__ == "__main__":
    """
    # pip install flake8 pylint radon pydocstyle
    python code_review.py your_script_or_package/
    """

    if len(sys.argv) != 2:
        print("Usage: python code_review.py <file_or_directory>")
    else:
        analyze_code(sys.argv[1])
