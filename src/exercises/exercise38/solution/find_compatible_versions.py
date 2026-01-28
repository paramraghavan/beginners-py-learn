#!/usr/bin/env python3
"""
Script to find compatible versions of new Python packages
without updating existing installed packages.

Supports custom package indexes (internal PyPI mirrors/repositories).

Usage:
    # Using custom index and installed packages file
    python find_compatible_versions.py \
        --installed-packages-file installed.txt \
        --new-packages-file new_packages.txt \
        --index-url https://your-internal-index.com/simple/

    # With extra index and trusted host
    python find_compatible_versions.py \
        --installed-packages-file installed.txt \
        --new-packages-file new_packages.txt \
        --index-url https://your-internal-index.com/simple/ \
        --trusted-host your-internal-index.com
"""

import subprocess
import sys
import argparse
import json
import tempfile
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def parse_installed_packages_file(filepath: str) -> Dict[str, str]:
    """
    Parse installed packages from a file.
    Supports multiple formats:
    - pip list format: "package    version"
    - pip freeze format: "package==version"
    - Simple format: "package version"
    """
    packages = {}
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Skip header lines (pip list format)
        if line.startswith('Package') or line.startswith('---') or line.startswith('==='):
            continue
        
        # Skip lines that are all dashes or special characters
        if all(c in '-=' for c in line.replace(' ', '')):
            continue
        
        # Try pip freeze format: package==version
        if '==' in line:
            parts = line.split('==')
            if len(parts) >= 2:
                name = parts[0].strip()
                version = parts[1].strip().split()[0]  # Handle any trailing comments
                # Validate it looks like a real package name
                if name and not all(c in '-=' for c in name) and re.match(r'^[a-zA-Z]', name):
                    packages[name.lower()] = version
                continue
        
        # Try pip list format: package    version (whitespace separated)
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0].strip()
            version = parts[1].strip()
            # Skip if this looks like a header or separator
            if name.lower() == 'package' or version.lower() == 'version':
                continue
            # Skip lines that are separators (all dashes)
            if all(c == '-' for c in name):
                continue
            # Validate it looks like a real package name (starts with letter)
            if name and re.match(r'^[a-zA-Z]', name):
                packages[name.lower()] = version
    
    return packages


def get_installed_packages_from_env() -> Dict[str, str]:
    """Get all currently installed packages from the current environment."""
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


def build_pip_index_args(index_url: Optional[str], extra_index_url: Optional[str], 
                          trusted_host: Optional[str]) -> List[str]:
    """Build pip arguments for custom index URLs."""
    args = []
    if index_url:
        args.extend(["--index-url", index_url])
    if extra_index_url:
        args.extend(["--extra-index-url", extra_index_url])
    if trusted_host:
        args.extend(["--trusted-host", trusted_host])
    return args


def try_resolve_with_constraints(
    new_packages: List[str],
    constraints_file: str,
    installed_packages: Dict[str, str],
    index_url: Optional[str] = None,
    extra_index_url: Optional[str] = None,
    trusted_host: Optional[str] = None
) -> Tuple[bool, str, Dict[str, str]]:
    """
    Try to resolve new packages with constraints.
    Returns (success, message, resolved_versions).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Build command with index URL options
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--dry-run",
            "--ignore-installed",
            "--constraint", constraints_file,
            "--report", os.path.join(tmpdir, "report.json"),
        ]
        
        # Add custom index arguments
        cmd.extend(build_pip_index_args(index_url, extra_index_url, trusted_host))
        
        # Add packages
        cmd.extend(new_packages)

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


def find_compatible_version_individually(
    package: str,
    constraints_file: str,
    installed_packages: Dict[str, str],
    index_url: Optional[str] = None,
    extra_index_url: Optional[str] = None,
    trusted_host: Optional[str] = None
) -> Tuple[Optional[str], str, Dict[str, str]]:
    """
    Try to find a compatible version for a single package.
    Returns (version, message, all_resolved_packages).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--dry-run",
            "--ignore-installed",
            "--constraint", constraints_file,
            "--report", os.path.join(tmpdir, "report.json"),
        ]
        
        # Add custom index arguments
        cmd.extend(build_pip_index_args(index_url, extra_index_url, trusted_host))
        
        cmd.append(package)

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # Try to extract useful error info
            error_msg = result.stderr
            if "Could not find a version" in error_msg:
                return None, f"No compatible version found: version conflict", {}
            elif "No matching distribution" in error_msg:
                return None, f"Package not found in index", {}
            else:
                return None, f"Resolution failed: {error_msg[:200]}", {}

        report_path = os.path.join(tmpdir, "report.json")
        if os.path.exists(report_path):
            with open(report_path) as f:
                report = json.load(f)

            resolved = {}
            main_version = None
            
            for item in report.get("install", []):
                meta = item.get("metadata", {})
                name = meta.get("name", "").lower()
                version = meta.get("version", "")
                if name and version:
                    if name not in installed_packages:
                        resolved[name] = version
                    if name == package.lower():
                        main_version = version

            return main_version, "Compatible version found", resolved

        return None, "Could not determine version from report", {}


def generate_install_script(
    resolved_packages: Dict[str, str],
    constraints_file: str,
    output_file: str,
    index_url: Optional[str] = None,
    extra_index_url: Optional[str] = None,
    trusted_host: Optional[str] = None
) -> None:
    """Generate a shell script to install the resolved packages."""
    with open(output_file, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("# Auto-generated installation script\n")
        f.write("# This script installs new packages with pinned versions\n")
        f.write("# that are compatible with your existing environment\n\n")
        f.write("set -e  # Exit on error\n\n")
        
        # Add index URL configuration
        if index_url:
            f.write(f'INDEX_URL="{index_url}"\n')
        if extra_index_url:
            f.write(f'EXTRA_INDEX_URL="{extra_index_url}"\n')
        if trusted_host:
            f.write(f'TRUSTED_HOST="{trusted_host}"\n')
        f.write("\n")
        
        # Build pip options
        pip_opts = []
        if index_url:
            pip_opts.append('--index-url "$INDEX_URL"')
        if extra_index_url:
            pip_opts.append('--extra-index-url "$EXTRA_INDEX_URL"')
        if trusted_host:
            pip_opts.append('--trusted-host "$TRUSTED_HOST"')
        
        pip_opts_str = " ".join(pip_opts)

        f.write("echo 'Installing compatible packages...'\n\n")

        for name, version in sorted(resolved_packages.items()):
            if pip_opts_str:
                f.write(f'pip install "{name}=={version}" --constraint "{constraints_file}" {pip_opts_str}\n')
            else:
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


def generate_pip_conf_example(
    index_url: Optional[str],
    extra_index_url: Optional[str],
    trusted_host: Optional[str],
    output_file: str
) -> None:
    """Generate an example pip.conf for the custom index."""
    with open(output_file, "w") as f:
        f.write("# Example pip.conf for your internal index\n")
        f.write("# Place this in ~/.pip/pip.conf or /etc/pip.conf\n\n")
        f.write("[global]\n")
        if index_url:
            f.write(f"index-url = {index_url}\n")
        if extra_index_url:
            f.write(f"extra-index-url = {extra_index_url}\n")
        if trusted_host:
            f.write(f"trusted-host = {trusted_host}\n")
    
    print(f"Generated pip.conf example: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Find compatible versions of new Python packages without updating existing ones.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using internal index with installed packages file
  python %(prog)s \\
      --installed-packages-file pip_list_output.txt \\
      --new-packages-file new_packages.txt \\
      --index-url https://your-internal-index.com/simple/

  # With trusted host for self-signed certificates
  python %(prog)s \\
      --installed-packages-file installed.txt \\
      --new-packages boto3 redis celery \\
      --index-url https://internal-pypi.company.com/simple/ \\
      --trusted-host internal-pypi.company.com

  # Dry run to preview
  python %(prog)s \\
      --installed-packages-file installed.txt \\
      --new-packages-file packages.txt \\
      --index-url https://internal-index.com/simple/ \\
      --dry-run
        """
    )
    
    # Package input options
    pkg_group = parser.add_argument_group('Package Options')
    pkg_group.add_argument(
        "--new-packages",
        nargs="+",
        help="List of new packages to install"
    )
    pkg_group.add_argument(
        "--new-packages-file",
        type=str,
        help="File containing new packages (one per line)"
    )
    pkg_group.add_argument(
        "--installed-packages-file",
        type=str,
        help="File containing currently installed packages (pip list or pip freeze output)"
    )
    
    # Index URL options
    index_group = parser.add_argument_group('Package Index Options')
    index_group.add_argument(
        "--index-url", "-i",
        type=str,
        help="Custom package index URL (replaces PyPI)"
    )
    index_group.add_argument(
        "--extra-index-url",
        type=str,
        help="Additional package index URL (used alongside primary index)"
    )
    index_group.add_argument(
        "--trusted-host",
        type=str,
        help="Trusted host for index (skip SSL verification)"
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        "--constraints-output",
        type=str,
        default="current_constraints.txt",
        help="Output file for current package constraints (default: current_constraints.txt)"
    )
    output_group.add_argument(
        "--requirements-output",
        type=str,
        default="new_requirements.txt",
        help="Output file for resolved new package versions (default: new_requirements.txt)"
    )
    output_group.add_argument(
        "--script-output",
        type=str,
        default="install_new_packages.sh",
        help="Output file for installation script (default: install_new_packages.sh)"
    )
    output_group.add_argument(
        "--generate-pip-conf",
        action="store_true",
        help="Generate an example pip.conf file for your index"
    )
    
    # Behavior options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show what would be resolved, don't generate files"
    )
    parser.add_argument(
        "--verbose", "-v",
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
    
    # Show index configuration
    if args.index_url:
        print(f"Package Index: {args.index_url}")
    if args.extra_index_url:
        print(f"Extra Index: {args.extra_index_url}")
    if args.trusted_host:
        print(f"Trusted Host: {args.trusted_host}")
    if args.index_url or args.extra_index_url:
        print()

    # Step 1: Get installed packages
    print("Step 1: Loading currently installed packages...")
    
    if args.installed_packages_file:
        print(f"  Reading from file: {args.installed_packages_file}")
        installed_packages = parse_installed_packages_file(args.installed_packages_file)
    else:
        print("  Scanning current environment...")
        installed_packages = get_installed_packages_from_env()
    
    print(f"  Found {len(installed_packages)} installed packages\n")
    
    if args.verbose:
        print("  Sample of installed packages:")
        for i, (name, version) in enumerate(sorted(installed_packages.items())[:10]):
            print(f"    {name}=={version}")
        if len(installed_packages) > 10:
            print(f"    ... and {len(installed_packages) - 10} more")
        print()

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
        found = False
        for key in installed_packages:
            if key.lower().replace("-", "_") == pkg.lower().replace("-", "_"):
                already_installed.append((pkg, installed_packages[key]))
                found = True
                break
        if not found:
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
        new_packages, 
        args.constraints_output, 
        installed_packages,
        args.index_url,
        args.extra_index_url,
        args.trusted_host
    )

    if not success:
        print(f"  Batch resolution failed: {message[:300]}")
        print("\n  Trying individual package resolution...\n")

        # Try each package individually
        resolved = {}
        failed = []

        for pkg in new_packages:
            print(f"  Resolving {pkg}...", end=" ", flush=True)
            version, msg, pkg_resolved = find_compatible_version_individually(
                pkg, 
                args.constraints_output, 
                installed_packages,
                args.index_url,
                args.extra_index_url,
                args.trusted_host
            )
            if version:
                print(f"✓ {version}")
                resolved.update(pkg_resolved)
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
            generate_install_script(
                resolved, 
                args.constraints_output, 
                args.script_output,
                args.index_url,
                args.extra_index_url,
                args.trusted_host
            )
            
            if args.generate_pip_conf and (args.index_url or args.extra_index_url):
                generate_pip_conf_example(
                    args.index_url,
                    args.extra_index_url,
                    args.trusted_host,
                    "pip.conf.example"
                )

            print(f"\nTo install the packages, run:")
            install_cmd = f"  pip install -r {args.requirements_output} -c {args.constraints_output}"
            if args.index_url:
                install_cmd += f" --index-url {args.index_url}"
            if args.extra_index_url:
                install_cmd += f" --extra-index-url {args.extra_index_url}"
            if args.trusted_host:
                install_cmd += f" --trusted-host {args.trusted_host}"
            print(install_cmd)
            
            print(f"\nOr use the generated script:")
            print(f"  ./{args.script_output}")
    else:
        print("No compatible versions could be resolved.")
        print("\nPossible solutions:")
        print("  1. Check if the package names are correct")
        print("  2. Verify packages exist in your internal index")
        print("  3. Some packages may have conflicting requirements")
        print("  4. Consider updating some existing packages")
        print("  5. Check if packages are available for your Python version")
        if args.index_url:
            print(f"  6. Verify index URL is accessible: {args.index_url}")

    print(f"\n{'='*60}")
    print("DONE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
