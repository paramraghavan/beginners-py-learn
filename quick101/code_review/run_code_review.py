#!/usr/bin/env python3
import os
import sys
import subprocess
import ast
import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Define required packages
REQUIRED_PACKAGES = {
    "flake8": "PEP8 style checking",
    "pylint": "Code quality analysis",
    "radon": "Complexity metrics",
    "pydocstyle": "Docstring style checking"
}


def check_dependencies():
    """Check if all required packages are installed."""
    missing_packages = []

    for package in REQUIRED_PACKAGES:
        try:
            subprocess.run(
                [package, "--version"],
                capture_output=True,
                text=True,
                check=False
            )
        except FileNotFoundError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages. Please install:")
        for package in missing_packages:
            print(f"   - {package} ({REQUIRED_PACKAGES[package]})")
        print("\nInstall with: pip install " + " ".join(missing_packages))
        return False

    return True


def run_subprocess(command, description, verbose=True):
    """Run a subprocess command and return/print results based on verbosity."""
    if verbose:
        print(f"\n🔍 {description}...")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if verbose:
            if result.stdout:
                print(result.stdout)
            else:
                print("✅ No issues found.")

            if result.stderr:
                print("⚠️  Errors:\n", result.stderr)

        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        if verbose:
            print(f"❌ Error running {description}: {e}")
        return "", str(e), 1


def check_ast(file_path, verbose=True):
    """Analyze Python file structure and docstrings using AST."""
    if verbose:
        print(f"\n📘 Analyzing structure and docstrings in: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
    except Exception as e:
        if verbose:
            print(f"❌ Error parsing {file_path}: {e}")
        return

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    missing_docstrings = []

    for cls in classes:
        doc = ast.get_docstring(cls)
        if verbose:
            print(f"\n🔹 Class: {cls.name}")
            print("   📄 Docstring:", "✅ Yes" if doc else "❌ Missing")
        if not doc:
            missing_docstrings.append(f"Class: {cls.name}")

    for func in functions:
        doc = ast.get_docstring(func)
        if verbose:
            print(f"\n🔸 Function: {func.name}")
            print("   📄 Docstring:", "✅ Yes" if doc else "❌ Missing")
        if not doc:
            missing_docstrings.append(f"Function: {func.name}")

    return missing_docstrings


def display_progress(current, total, prefix="", suffix="", length=50):
    """Display a command-line progress bar."""
    percent = int(100 * (current / total))
    filled_length = int(length * current // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r{prefix} |{bar}| {percent}% {suffix}")
    sys.stdout.flush()
    if current == total:
        print()


def analyze_file(file_path, options):
    """Analyze a single Python file."""
    results = {"file": file_path, "issues": []}

    # AST analysis
    if options.ast:
        missing_docstrings = check_ast(file_path, options.verbose)
        if missing_docstrings:
            results["issues"].append({
                "tool": "AST",
                "findings": f"{len(missing_docstrings)} missing docstrings"
            })

    # Run other tools based on options
    if options.flake8:
        stdout, stderr, code = run_subprocess(
            f"flake8 {file_path}",
            "PEP8/flake8 style check",
            options.verbose
        )
        if stdout or stderr:
            results["issues"].append({
                "tool": "flake8",
                "findings": f"{stdout.count(file_path.name)} issues"
            })

    if options.pylint:
        stdout, stderr, code = run_subprocess(
            f"pylint {file_path}",
            "Pylint code quality analysis",
            options.verbose
        )
        if "Your code has been rated at" in stdout:
            rating = stdout.split("Your code has been rated at")[1].split("/")[0].strip()
            results["issues"].append({
                "tool": "pylint",
                "findings": f"Rating: {rating}/10"
            })

    if options.radon:
        stdout, stderr, code = run_subprocess(
            f"radon cc {file_path} -a",
            "Radon cyclomatic complexity check",
            options.verbose
        )
        # Check for high complexity
        if "C " in stdout or "D " in stdout or "E " in stdout or "F " in stdout:
            results["issues"].append({
                "tool": "radon_cc",
                "findings": "High complexity detected"
            })

        stdout, stderr, code = run_subprocess(
            f"radon mi {file_path}",
            "Radon maintainability index",
            options.verbose
        )
        if stdout and "B" in stdout or "C" in stdout:
            results["issues"].append({
                "tool": "radon_mi",
                "findings": "Low maintainability"
            })

    if options.pydocstyle:
        stdout, stderr, code = run_subprocess(
            f"pydocstyle {file_path}",
            "Docstring style check (pydocstyle)",
            options.verbose
        )
        issues_count = stdout.count(file_path.name)
        if issues_count:
            results["issues"].append({
                "tool": "pydocstyle",
                "findings": f"{issues_count} docstring style issues"
            })

    return results


def analyze_files_with_progress(files, options):
    """Analyze files with progress bar."""
    results = []
    total_files = len(files)

    if options.parallel:
        with ThreadPoolExecutor(max_workers=min(os.cpu_count(), 8)) as executor:
            futures = [executor.submit(analyze_file, file, options) for file in files]

            for i, future in enumerate(futures):
                if not options.verbose:
                    display_progress(i + 1, total_files, "Analyzing files:", f"{i + 1}/{total_files}")
                results.append(future.result())
    else:
        for i, file in enumerate(files):
            if not options.verbose:
                display_progress(i + 1, total_files, "Analyzing files:", f"{i + 1}/{total_files}")
            results.append(analyze_file(file, options))

    return results


def analyze_code(file_or_dir, options):
    """Analyze Python code in file or directory."""
    path = Path(file_or_dir)

    if not path.exists():
        print(f"❌ Path not found: {file_or_dir}")
        return

    start_time = time.time()

    # Collect Python files to analyze
    python_files = []
    if path.is_file() and path.suffix == '.py':
        python_files = [path]
    else:
        python_files = list(path.rglob("*.py"))

    if not python_files:
        print(f"No Python files found in {file_or_dir}")
        return

    print(f"Found {len(python_files)} Python files to analyze")

    # Analyze files with progress tracking
    results = analyze_files_with_progress(python_files, options)

    # Generate summary report
    print("\n📊 SUMMARY REPORT 📊")
    print(f"Analyzed {len(python_files)} files in {time.time() - start_time:.2f} seconds")

    files_with_issues = sum(1 for r in results if r["issues"])
    print(
        f"Files with issues: {files_with_issues}/{len(python_files)} ({files_with_issues / len(python_files) * 100:.1f}%)")

    # Display worst offenders
    if files_with_issues > 0:
        print("\n🔴 Files with most issues:")
        sorted_results = sorted(results, key=lambda x: len(x["issues"]), reverse=True)
        for i, result in enumerate(sorted_results[:5]):
            if result["issues"]:
                print(f"{i + 1}. {result['file'].name} - {len(result['issues'])} issue categories")
                for issue in result["issues"]:
                    print(f"   - {issue['tool']}: {issue['findings']}")

    if options.output:
        # Save report to file
        with open(options.output, "w") as f:
            f.write("# Code Review Report\n\n")
            f.write(f"Analyzed {len(python_files)} Python files in {file_or_dir}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- Files with issues: {files_with_issues}/{len(python_files)}\n")
            f.write(f"- Analysis time: {time.time() - start_time:.2f} seconds\n\n")

            f.write("## Detailed Findings\n\n")
            for result in sorted_results:
                if result["issues"]:
                    f.write(f"### {result['file']}\n\n")
                    for issue in result["issues"]:
                        f.write(f"- **{issue['tool']}**: {issue['findings']}\n")
                    f.write("\n")

        print(f"\n📝 Report saved to {options.output}")


def main():
    """Parse arguments and run the code review."""
    parser = argparse.ArgumentParser(description="Python Code Review Tool")
    parser.add_argument("path", help="File or directory to review")
    parser.add_argument("-o", "--output", help="Save report to file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Show minimal output")

    # Tool selection options
    parser.add_argument("--all", action="store_true", help="Run all checks (default)")
    parser.add_argument("--ast", action="store_true", help="Run AST analysis only")
    parser.add_argument("--flake8", action="store_true", help="Run flake8 only")
    parser.add_argument("--pylint", action="store_true", help="Run pylint only")
    parser.add_argument("--radon", action="store_true", help="Run radon only")
    parser.add_argument("--pydocstyle", action="store_true", help="Run pydocstyle only")

    # Performance options
    parser.add_argument("--parallel", action="store_true", help="Run checks in parallel")

    args = parser.parse_args()

    # If quiet is set, override verbose
    if args.quiet:
        args.verbose = False

    # If no specific tools are selected, run all
    if not any([args.ast, args.flake8, args.pylint, args.radon, args.pydocstyle]):
        args.all = True

    if args.all:
        args.ast = args.flake8 = args.pylint = args.radon = args.pydocstyle = True

    # Check dependencies
    if not check_dependencies():
        return

    analyze_code(args.path, args)


if __name__ == "__main__":
    main()