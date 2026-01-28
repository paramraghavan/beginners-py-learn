#!/usr/bin/env python3
"""
Script to find compatible versions of new Python packages
without updating existing installed packages.

Usage:
    python find_compatible_versions.py --new-packages package1 package2 package3
    python find_compatible_versions.py --new-packages-file new_packages.txt
    python find_compatible_versions.py --new-packages requests flask --dry-run
"""

import subprocess
import sys
import argparse
import json
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def get_installed_packages() -> Dict[str, str]:
    """Get all currently installed packages and their versions."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        check=True
    )
    packages = json.loads(result.stdout)
    return {pkg["name"].lower(): pkg["version"] for pkg in packages}


def create_constraints_file(installed_packages: Dict[str, str], filepath: str) -> None:
    """Create a constraints file with all installed packages pinned."""
    with open(filepath, "w") as f:
        for name, version in sorted(installed_packages.items()):
            f.write(f"{name}=={version}\n")
    print(f"Created constraints file with {len(installed_packages)} packages: {filepath}")


def check_package_availability(package: str) -> bool:
    """Check if a package exists on PyPI."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "index", "versions", package],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def try_resolve_with_constraints(
    new_packages: List[str],
    constraints_file: str,
    installed_packages: Dict[str, str]
) -> Tuple[bool, str, Dict[str, str]]:
    """
    Try to resolve new packages with constraints.
    Returns (success, message, resolved_versions).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use pip's dry-run to check what would be installed
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--dry-run",
            "--ignore-installed",
            "--constraint", constraints_file,
            "--report", os.path.join(tmpdir, "report.json"),
        ] + new_packages

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return False, result.stderr, {}

        # Parse the report to get resolved versions
        report_path = os.path.join(tmpdir, "report.json")
        if os.path.exists(report_path):
            with open(report_path) as f:
                report = json.load(f)

            resolved = {}
            for item in report.get("install", []):
                meta = item.get("metadata", {})
                name = meta.get("name", "").lower()
                version = meta.get("version", "")
                if name and version:
                    # Only include if it's a new package or a dependency not already installed
                    if name not in installed_packages:
                        resolved[name] = version

            return True, "Resolution successful", resolved

        return True, "Resolution successful (no report generated)", {}


def try_resolve_with_pip_tools(
    new_packages: List[str],
    constraints_file: str,
    installed_packages: Dict[str, str]
) -> Tuple[bool, str, Dict[str, str]]:
    """
    Alternative method using pip-tools if available.
    """
    # Check if pip-tools is available
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "pip-tools"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return False, "pip-tools not installed", {}

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create requirements.in with new packages
        req_in = os.path.join(tmpdir, "requirements.in")
        with open(req_in, "w") as f:
            for pkg in new_packages:
                f.write(f"{pkg}\n")

        req_out = os.path.join(tmpdir, "requirements.txt")

        cmd = [
            sys.executable, "-m", "piptools", "compile",
            "--constraint", constraints_file,
            "--output-file", req_out,
            req_in
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return False, result.stderr, {}

        # Parse output requirements
        resolved = {}
        with open(req_out) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-"):
                    if "==" in line:
                        name, version = line.split("==")
                        name = name.strip().lower()
                        version = version.split()[0].strip()  # Remove any comments
                        if name not in installed_packages:
                            resolved[name] = version

        return True, "Resolution successful with pip-tools", resolved


def find_compatible_version_individually(
    package: str,
    constraints_file: str,
    installed_packages: Dict[str, str]
) -> Tuple[Optional[str], str]:
    """
    Try to find a compatible version for a single package.
    Returns (version, message).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--dry-run",
            "--ignore-installed",
            "--constraint", constraints_file,
            "--report", os.path.join(tmpdir, "report.json"),
            package
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # Try to extract useful error info
            error_msg = result.stderr
            if "Could not find a version" in error_msg:
                return None, f"No compatible version found: version conflict"
            elif "No matching distribution" in error_msg:
                return None, f"Package not found on PyPI"
            else:
                return None, f"Resolution failed: {error_msg[:200]}"

        report_path = os.path.join(tmpdir, "report.json")
        if os.path.exists(report_path):
            with open(report_path) as f:
                report = json.load(f)

            for item in report.get("install", []):
                meta = item.get("metadata", {})
                name = meta.get("name", "").lower()
                version = meta.get("version", "")
                if name == package.lower():
                    return version, "Compatible version found"

        return None, "Could not determine version from report"


def generate_install_script(
    resolved_packages: Dict[str, str],
    constraints_file: str,
    output_file: str
) -> None:
    """Generate a shell script to install the resolved packages."""
    with open(output_file, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("# Auto-generated installation script\n")
        f.write("# This script installs new packages with pinned versions\n")
        f.write("# that are compatible with your existing environment\n\n")
        f.write("set -e  # Exit on error\n\n")

        f.write("echo 'Installing compatible packages...'\n\n")

        for name, version in sorted(resolved_packages.items()):
            f.write(f'pip install "{name}=={version}" --constraint "{constraints_file}"\n')

        f.write("\necho 'Installation complete!'\n")

    os.chmod(output_file, 0o755)
    print(f"\nGenerated installation script: {output_file}")


def generate_requirements_file(
    resolved_packages: Dict[str, str],
    output_file: str
) -> None:
    """Generate a requirements.txt with resolved versions."""
    with open(output_file, "w") as f:
        f.write("# Auto-generated requirements file\n")
        f.write("# Compatible versions for new packages\n\n")
        for name, version in sorted(resolved_packages.items()):
            f.write(f"{name}=={version}\n")

    print(f"Generated requirements file: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Find compatible versions of new Python packages without updating existing ones."
    )
    parser.add_argument(
        "--new-packages",
        nargs="+",
        help="List of new packages to install"
    )
    parser.add_argument(
        "--new-packages-file",
        type=str,
        help="File containing new packages (one per line)"
    )
    parser.add_argument(
        "--constraints-output",
        type=str,
        default="current_constraints.txt",
        help="Output file for current package constraints"
    )
    parser.add_argument(
        "--requirements-output",
        type=str,
        default="new_requirements.txt",
        help="Output file for resolved new package versions"
    )
    parser.add_argument(
        "--script-output",
        type=str,
        default="install_new_packages.sh",
        help="Output file for installation script"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show what would be resolved, don't generate files"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Collect new packages
    new_packages = []
    if args.new_packages:
        new_packages.extend(args.new_packages)
    if args.new_packages_file:
        with open(args.new_packages_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    new_packages.append(line)

    if not new_packages:
        print("Error: No new packages specified.")
        print("Use --new-packages or --new-packages-file")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("PYTHON PACKAGE COMPATIBILITY RESOLVER")
    print(f"{'='*60}\n")

    # Step 1: Get installed packages
    print("Step 1: Scanning currently installed packages...")
    installed_packages = get_installed_packages()
    print(f"  Found {len(installed_packages)} installed packages\n")

    # Step 2: Create constraints file
    print("Step 2: Creating constraints file...")
    create_constraints_file(installed_packages, args.constraints_output)
    print()

    # Check which packages are already installed
    already_installed = []
    truly_new = []
    for pkg in new_packages:
        pkg_lower = pkg.lower().replace("-", "_").replace("_", "-")
        # Check various naming conventions
        if (pkg.lower() in installed_packages or 
            pkg.lower().replace("-", "_") in installed_packages or
            pkg.lower().replace("_", "-") in installed_packages):
            for key in installed_packages:
                if key.lower().replace("-", "_") == pkg.lower().replace("-", "_"):
                    already_installed.append((pkg, installed_packages[key]))
                    break
        else:
            truly_new.append(pkg)

    if already_installed:
        print("  Already installed packages (will be skipped):")
        for pkg, ver in already_installed:
            print(f"    - {pkg} ({ver})")
        print()

    if not truly_new:
        print("  All requested packages are already installed!")
        print(f"\n{'='*60}")
        print("DONE - No new packages to resolve")
        print(f"{'='*60}\n")
        return

    new_packages = truly_new

    # Step 3: Try to resolve all packages together
    print("Step 3: Resolving compatible versions...")
    print(f"  New packages to resolve: {', '.join(new_packages)}\n")

    success, message, resolved = try_resolve_with_constraints(
        new_packages, args.constraints_output, installed_packages
    )

    if not success:
        print(f"  Batch resolution failed: {message[:200]}")
        print("\n  Trying individual package resolution...\n")

        # Try each package individually
        resolved = {}
        failed = []

        for pkg in new_packages:
            print(f"  Resolving {pkg}...", end=" ")
            version, msg = find_compatible_version_individually(
                pkg, args.constraints_output, installed_packages
            )
            if version:
                print(f"✓ {version}")
                resolved[pkg.lower()] = version
            else:
                print(f"✗ {msg}")
                failed.append((pkg, msg))

        if failed:
            print(f"\n  WARNING: {len(failed)} package(s) could not be resolved:")
            for pkg, msg in failed:
                print(f"    - {pkg}: {msg}")

    # Step 4: Show results
    print(f"\n{'='*60}")
    print("RESOLUTION RESULTS")
    print(f"{'='*60}\n")

    if resolved:
        print("Compatible versions found:\n")
        print(f"  {'Package':<30} {'Version':<15}")
        print(f"  {'-'*30} {'-'*15}")
        for name, version in sorted(resolved.items()):
            print(f"  {name:<30} {version:<15}")

        # Also show new dependencies that will be installed
        new_deps = {k: v for k, v in resolved.items()
                    if k.lower() not in [p.lower() for p in new_packages]}
        if new_deps:
            print(f"\n  Note: {len(new_deps)} additional dependencies will be installed")

        if not args.dry_run:
            print(f"\n{'='*60}")
            print("GENERATING OUTPUT FILES")
            print(f"{'='*60}\n")

            generate_requirements_file(resolved, args.requirements_output)
            generate_install_script(resolved, args.constraints_output, args.script_output)

            print(f"\nTo install the packages, run:")
            print(f"  pip install -r {args.requirements_output} -c {args.constraints_output}")
            print(f"\nOr use the generated script:")
            print(f"  ./{args.script_output}")
    else:
        print("No compatible versions could be resolved.")
        print("\nPossible solutions:")
        print("  1. Check if the package names are correct")
        print("  2. Some packages may have conflicting requirements")
        print("  3. Consider updating some existing packages")
        print("  4. Check if packages are available for your Python version")

    print(f"\n{'='*60}")
    print("DONE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
