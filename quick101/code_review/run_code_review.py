#!/usr/bin/env python3
import os
import sys
import subprocess
import ast
import argparse
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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
        output_path = Path(options.output)

        # Determine if we should generate HTML or Markdown
        if output_path.suffix.lower() == '.html' or options.html:
            generate_html_report(output_path, python_files, results, file_or_dir,
                                 files_with_issues, start_time, sorted_results)
            print(f"\n📊 HTML Report saved to {output_path}")
        else:
            # Save markdown report to file
            with open(output_path, "w") as f:
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

            print(f"\n📝 Report saved to {output_path}")


def generate_html_report(output_path, python_files, results, file_or_dir,
                         files_with_issues, start_time, sorted_results):
    """Generate an HTML report with charts and detailed findings."""

    # Count issues by tool
    tools_count = {}
    file_issues = {}

    for result in results:
        file_path = str(result["file"])
        file_name = result["file"].name

        if file_name not in file_issues:
            file_issues[file_name] = {}

        for issue in result["issues"]:
            tool = issue["tool"]
            if tool not in tools_count:
                tools_count[tool] = 0
            tools_count[tool] += 1

            if tool not in file_issues[file_name]:
                file_issues[file_name][tool] = issue["findings"]

    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Code Review Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .header {{
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header h1 {{
            margin: 0;
            color: white;
        }}
        .summary-box {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-item {{
            flex: 1;
            min-width: 200px;
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            text-align: center;
        }}
        .metric {{
            font-size: 2rem;
            font-weight: bold;
            margin: 10px 0;
            color: #3498db;
        }}
        .charts-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-container {{
            flex: 1;
            min-width: 300px;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
        }}
        thead {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tbody tr {{
            border-bottom: 1px solid #dddddd;
        }}
        tbody tr:nth-of-type(even) {{
            background-color: #f8f9fa;
        }}
        .severity-high {{
            background-color: #ff6b6b;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        .severity-medium {{
            background-color: #feca57;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        .severity-low {{
            background-color: #1dd1a1;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        .issues-container {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        .file-issues {{
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            background-color: #f8f9fa;
        }}
        .file-name {{
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 1.1rem;
            color: #2c3e50;
        }}
        .tool-list {{
            list-style-type: none;
            padding-left: 10px;
        }}
        .tool-item {{
            margin-bottom: 5px;
            padding: 8px;
            border-radius: 4px;
            background-color: #e8eaf6;
        }}
        .tool-name {{
            font-weight: bold;
            color: #3f51b5;
        }}
        .search-box {{
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        #issueFilters {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .filter-button {{
            padding: 8px 15px;
            background-color: #e8eaf6;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }}
        .filter-button.active {{
            background-color: #3f51b5;
            color: white;
        }}
        .hidden {{
            display: none;
        }}
        footer {{
            margin-top: 50px;
            text-align: center;
            font-size: 0.9rem;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Python Code Review Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <h2>Project Overview</h2>
    <div class="summary-box">
        <div class="summary-item">
            <h3>Files Analyzed</h3>
            <div class="metric">{len(python_files)}</div>
            <p>Python files</p>
        </div>
        <div class="summary-item">
            <h3>Files with Issues</h3>
            <div class="metric">{files_with_issues}</div>
            <p>{round(files_with_issues / len(python_files) * 100, 1)}% of all files</p>
        </div>
        <div class="summary-item">
            <h3>Analysis Time</h3>
            <div class="metric">{round(time.time() - start_time, 2)}</div>
            <p>seconds</p>
        </div>
        <div class="summary-item">
            <h3>Total Issues</h3>
            <div class="metric">{sum(tools_count.values())}</div>
            <p>across all tools</p>
        </div>
    </div>

    <h2>Analysis Results</h2>

    <div class="charts-container">
        <div class="chart-container">
            <h3>Issues by Tool</h3>
            <canvas id="toolsChart"></canvas>
        </div>
        <div class="chart-container">
            <h3>Top Files with Issues</h3>
            <canvas id="filesChart"></canvas>
        </div>
    </div>

    <h2>Detailed Findings</h2>

    <input type="text" id="searchBox" class="search-box" placeholder="Search for files...">

    <div id="issueFilters">
        <button class="filter-button active" data-filter="all">All</button>
        {' '.join([f'<button class="filter-button" data-filter="{tool}">{tool}</button>' for tool in tools_count])}
    </div>

    <div class="issues-container" id="issuesContainer">
    """

    # Generate HTML for each file with issues
    for result in sorted_results:
        if result["issues"]:
            file_name = result["file"].name
            file_path = str(result["file"])

            issue_classes = " ".join([issue["tool"] for issue in result["issues"]])

            html_content += f"""
        <div class="file-issues" data-file="{file_name}" data-tools="{issue_classes}">
            <div class="file-name">{file_path}</div>
            <ul class="tool-list">
            """

            for issue in result["issues"]:
                html_content += f"""
                <li class="tool-item">
                    <span class="tool-name">{issue["tool"]}:</span> {issue["findings"]}
                </li>
                """

            html_content += """
            </ul>
        </div>
            """

    # Add JavaScript for interactivity
    html_content += """
    </div>

    <script>
        // Charts
        document.addEventListener('DOMContentLoaded', function() {
            // Tools chart
            const toolsCtx = document.getElementById('toolsChart').getContext('2d');
            const toolsChart = new Chart(toolsCtx, {
                type: 'doughnut',
                data: {
                    labels: TOOLS_LABELS,
                    datasets: [{
                        data: TOOLS_DATA,
                        backgroundColor: [
                            '#ff6b6b', '#feca57', '#1dd1a1', '#5f27cd', '#54a0ff',
                            '#ff9ff3', '#00d2d3', '#f368e0', '#48dbfb', '#341f97'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                        }
                    }
                }
            });

            // Files chart
            const filesCtx = document.getElementById('filesChart').getContext('2d');
            const filesChart = new Chart(filesCtx, {
                type: 'bar',
                data: {
                    labels: FILES_LABELS,
                    datasets: [{
                        label: 'Number of Issues',
                        data: FILES_DATA,
                        backgroundColor: '#3498db',
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });

            // Search functionality
            const searchBox = document.getElementById('searchBox');
            const issuesContainer = document.getElementById('issuesContainer');
            const fileIssues = issuesContainer.getElementsByClassName('file-issues');

            searchBox.addEventListener('keyup', function() {
                const searchTerm = this.value.toLowerCase();

                for (let i = 0; i < fileIssues.length; i++) {
                    const fileName = fileIssues[i].getAttribute('data-file').toLowerCase();

                    if (fileName.includes(searchTerm)) {
                        fileIssues[i].classList.remove('hidden');
                    } else {
                        fileIssues[i].classList.add('hidden');
                    }
                }
            });

            // Filter functionality
            const filterButtons = document.querySelectorAll('.filter-button');

            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const filter = this.getAttribute('data-filter');

                    // Update active button
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');

                    // Show/hide file issues based on filter
                    for (let i = 0; i < fileIssues.length; i++) {
                        if (filter === 'all') {
                            fileIssues[i].classList.remove('hidden');
                        } else {
                            const tools = fileIssues[i].getAttribute('data-tools');

                            if (tools.includes(filter)) {
                                fileIssues[i].classList.remove('hidden');
                            } else {
                                fileIssues[i].classList.add('hidden');
                            }
                        }
                    }
                });
            });
        });
    </script>

    <script>
        // Data for charts
        const TOOLS_LABELS = JSON.parse('TOOLS_LABELS_JSON');
        const TOOLS_DATA = JSON.parse('TOOLS_DATA_JSON');
        const FILES_LABELS = JSON.parse('FILES_LABELS_JSON');
        const FILES_DATA = JSON.parse('FILES_DATA_JSON');
    </script>

    <footer>
        <p>Generated by Python Code Review Tool</p>
    </footer>
</body>
</html>
    """

    # Prepare data for charts
    tools_labels = list(tools_count.keys())
    tools_data = list(tools_count.values())

    # Get top 10 files with most issues
    top_files = sorted(file_issues.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    files_labels = [file_name for file_name, _ in top_files]
    files_data = [len(issues) for _, issues in top_files]

    # Convert to JSON strings
    tools_labels_json = json.dumps(tools_labels)
    tools_data_json = json.dumps(tools_data)
    files_labels_json = json.dumps(files_labels)
    files_data_json = json.dumps(files_data)

    # Insert data into HTML
    html_content = html_content.replace('TOOLS_LABELS_JSON', tools_labels_json)
    html_content = html_content.replace('TOOLS_DATA_JSON', tools_data_json)
    html_content = html_content.replace('FILES_LABELS_JSON', files_labels_json)
    html_content = html_content.replace('FILES_DATA_JSON', files_data_json)

    # Write to file
    with open(output_path, "w") as f:
        f.write(html_content)


def main():
    """Parse arguments and run the code review."""
    parser = argparse.ArgumentParser(description="Python Code Review Tool")
    parser.add_argument("path", help="File or directory to review")
    parser.add_argument("-o", "--output", help="Save report to file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Show minimal output")
    parser.add_argument("--html", action="store_true",
                        help="Generate HTML report (even if output doesn't have .html extension)")

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