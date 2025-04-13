import os
import sys
import subprocess
import ast
from pathlib import Path

def run_subprocess(command, description):
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout or "✅ No issues found.")
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

    run_subprocess(f"flake8 {file_or_dir}", "PEP8/flake8 style check")
    run_subprocess(f"pylint {file_or_dir}", "Pylint code quality analysis")
    run_subprocess(f"radon cc {file_or_dir} -a", "Radon cyclomatic complexity check")
    run_subprocess(f"radon mi {file_or_dir}", "Radon maintainability index")
    run_subprocess(f"pydocstyle {file_or_dir}", "Docstring style check (pydocstyle)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python code_review.py <file_or_directory>")
    else:
        analyze_code(sys.argv[1])