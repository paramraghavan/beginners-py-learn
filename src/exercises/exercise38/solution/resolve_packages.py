#!/usr/bin/env python3
"""
Package Compatibility Resolver

Finds compatible versions for new packages with existing installed packages.

Usage:
    python resolve_packages.py <existing_packages.txt> <new_packages.txt> [OPTIONS]

Arguments:
    existing_packages.txt   File with currently installed packages (from: pip freeze > existing_packages.txt)
    new_packages.txt        File with new packages to add

Options:
    --index-url URL         Custom PyPI index URL (default: https://pypi.org/simple)
    --strict                Pin existing versions exactly (default: allow upgrades)
    --output FILE           Output file name (default: requirements_resolved.txt)
    --help                  Show this help message

Examples:
    python resolve_packages.py existing.txt new.txt
    python resolve_packages.py existing.txt new.txt --index-url https://my-pypi.com/simple
    python resolve_packages.py existing.txt new.txt --strict --output resolved.txt
"""

import subprocess
import sys
import os
import argparse
import tempfile
import shutil
from datetime import datetime


def run_command(cmd, capture_output=True, cwd=None):
    """Run a shell command and return result."""
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=capture_output, 
        text=True,
        cwd=cwd
    )
    return result


def read_packages_from_file(filepath):
    """Read packages from a requirements file."""
    packages = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#') and not line.startswith('-'):
                # Handle lines with comments at end
                line = line.split('#')[0].strip()
                if line:
                    packages.append(line)
    return packages


def parse_package_line(line):
    """Parse package line into name and version spec."""
    line = line.strip()
    for sep in ['==', '>=', '<=', '>', '<', '~=', '!=']:
        if sep in line:
            parts = line.split(sep, 1)
            return parts[0].strip(), sep + parts[1].strip()
    return line, None


def create_test_venv(base_path):
    """Create a temporary virtual environment for testing."""
    venv_path = os.path.join(base_path, "test_venv")
    print(f"🔨 Creating temporary test environment...")
    
    result = run_command(f"{sys.executable} -m venv {venv_path}")
    if result.returncode != 0:
        print(f"❌ Failed to create virtual environment")
        print(f"   Error: {result.stderr}")
        return None
    
    # Get pip path in new venv
    if sys.platform == "win32":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    # Upgrade pip in test venv
    print("   Upgrading pip...")
    run_command(f"{pip_path} install --upgrade pip -q")
    
    print("   ✅ Test environment ready\n")
    return {"venv": venv_path, "pip": pip_path, "python": python_path}


def install_and_freeze(venv_info, requirements_file, index_url=None):
    """Install packages in test env and get resolved versions."""
    pip_cmd = venv_info["pip"]
    
    # Build install command
    cmd = f"{pip_cmd} install -r {requirements_file}"
    if index_url:
        cmd += f" --index-url {index_url}"
    
    print(f"📦 Installing packages in test environment...")
    print(f"   (This may take several minutes)\n")
    
    result = run_command(cmd, capture_output=False)
    
    if result.returncode != 0:
        return None, "Installation failed - see errors above"
    
    # Check for conflicts
    print("\n🔍 Checking for dependency conflicts...")
    check_result = run_command(f"{pip_cmd} check")
    if check_result.returncode != 0:
        print(f"⚠️  Conflicts detected:")
        print(check_result.stdout)
        print(check_result.stderr)
    else:
        print("   ✅ No conflicts found")
    
    # Get resolved versions
    freeze_result = run_command(f"{pip_cmd} freeze")
    if freeze_result.returncode != 0:
        return None, "Failed to get package list"
    
    resolved = {}
    for line in freeze_result.stdout.strip().split('\n'):
        if line and '==' in line and not line.startswith('#'):
            line = line.split('#')[0].strip()
            if '==' in line:
                name, version = line.split('==', 1)
                resolved[name] = version
    
    return resolved, None


def normalize_name(name):
    """Normalize package name for comparison."""
    return name.lower().replace('-', '_').replace('.', '_')


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Find compatible package versions for existing + new packages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s existing.txt new.txt
    %(prog)s existing.txt new.txt --index-url https://my-pypi.com/simple
    %(prog)s existing.txt new.txt --strict --output resolved.txt
        """
    )
    parser.add_argument('existing_packages', 
                        help='File with existing installed packages (pip freeze output)')
    parser.add_argument('new_packages', 
                        help='File with new packages to install')
    parser.add_argument('--index-url', 
                        help='Custom PyPI index URL')
    parser.add_argument('--strict', action='store_true',
                        help='Pin existing versions exactly (default: allow upgrades)')
    parser.add_argument('--output', default='requirements_resolved.txt',
                        help='Output file (default: requirements_resolved.txt)')
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.existing_packages):
        print(f"❌ Error: File not found: {args.existing_packages}")
        sys.exit(1)
    
    if not os.path.exists(args.new_packages):
        print(f"❌ Error: File not found: {args.new_packages}")
        sys.exit(1)
    
    # Print header
    print("=" * 65)
    print("🐍 Package Compatibility Resolver")
    print("=" * 65)
    print()
    print(f"  Existing packages: {args.existing_packages}")
    print(f"  New packages:      {args.new_packages}")
    print(f"  Index URL:         {args.index_url or 'https://pypi.org/simple (default)'}")
    print(f"  Strategy:          {'STRICT (pin versions)' if args.strict else 'FLEXIBLE (allow upgrades)'}")
    print(f"  Output file:       {args.output}")
    print()
    
    # Read input files
    print("-" * 65)
    print("📁 Reading input files...")
    print("-" * 65)
    
    existing_packages = read_packages_from_file(args.existing_packages)
    new_packages = read_packages_from_file(args.new_packages)
    
    print(f"   Existing packages: {len(existing_packages)}")
    print(f"   New packages:      {len(new_packages)}")
    
    if not existing_packages:
        print("⚠️  Warning: No existing packages found")
    
    if not new_packages:
        print("❌ Error: No new packages specified")
        sys.exit(1)
    
    print(f"\n📦 New packages to add:")
    for pkg in new_packages:
        print(f"   - {pkg}")
    
    # Create temp directory
    print("\n" + "-" * 65)
    print("🔄 Resolving dependencies...")
    print("-" * 65 + "\n")
    
    temp_dir = tempfile.mkdtemp(prefix="pkg_resolve_")
    requirements_file = os.path.join(temp_dir, "requirements.txt")
    
    try:
        # Write combined requirements file
        with open(requirements_file, 'w') as f:
            f.write("# Existing packages\n")
            for pkg_line in existing_packages:
                if args.strict:
                    f.write(f"{pkg_line}\n")
                else:
                    # Convert == to >= to allow upgrades
                    name, version_spec = parse_package_line(pkg_line)
                    if version_spec and version_spec.startswith('=='):
                        f.write(f"{name}>={version_spec[2:]}\n")
                    else:
                        f.write(f"{pkg_line}\n")
            
            f.write("\n# New packages to add\n")
            for pkg in new_packages:
                f.write(f"{pkg}\n")
        
        # Save a copy locally for debugging
        combined_file = "requirements_combined.txt"
        shutil.copy(requirements_file, combined_file)
        print(f"📄 Combined requirements: {combined_file}")
        
        # Create test venv and resolve
        venv_info = create_test_venv(temp_dir)
        if not venv_info:
            print("❌ Failed to create test environment")
            sys.exit(1)
        
        resolved, error = install_and_freeze(venv_info, requirements_file, args.index_url)
        
        if error:
            print(f"\n❌ Resolution failed: {error}")
            print("\n🔍 Troubleshooting:")
            print("   1. Check package names in new_packages file")
            print("   2. Try without version constraints")
            print("   3. Verify index URL is accessible")
            print("   4. Try without --strict flag")
            print(f"\n   See combined requirements: {combined_file}")
            sys.exit(1)
        
        # Save resolved requirements
        with open(args.output, 'w') as f:
            f.write(f"# Resolved package versions\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Existing packages file: {args.existing_packages}\n")
            f.write(f"# New packages file: {args.new_packages}\n")
            if args.index_url:
                f.write(f"# Index URL: {args.index_url}\n")
            f.write("#\n")
            for pkg, version in sorted(resolved.items()):
                f.write(f"{pkg}=={version}\n")
        
        # Show results
        print("\n" + "=" * 65)
        print("✅ SUCCESS!")
        print("=" * 65)
        
        print(f"\n📄 Output: {args.output}")
        
        # Calculate changes
        print("\n" + "-" * 65)
        print("📊 CHANGES SUMMARY")
        print("-" * 65)
        
        # Parse existing into dict
        existing_dict = {}
        for pkg_line in existing_packages:
            name, version_spec = parse_package_line(pkg_line)
            if version_spec and version_spec.startswith('=='):
                existing_dict[normalize_name(name)] = (name, version_spec[2:])
            else:
                existing_dict[normalize_name(name)] = (name, None)
        
        resolved_norm = {normalize_name(k): (k, v) for k, v in resolved.items()}
        
        changed = []
        new_added = []
        unchanged = 0
        
        for pkg_norm, (pkg_name, new_ver) in resolved_norm.items():
            if pkg_norm in existing_dict:
                orig_name, old_ver = existing_dict[pkg_norm]
                if old_ver and old_ver != new_ver:
                    changed.append((orig_name, old_ver, new_ver))
                else:
                    unchanged += 1
            else:
                new_added.append((pkg_name, new_ver))
        
        print(f"\n   Unchanged: {unchanged}")
        
        if changed:
            print(f"\n🔄 Version changes ({len(changed)}):")
            for name, old_v, new_v in sorted(changed)[:25]:
                print(f"   {name}: {old_v} → {new_v}")
            if len(changed) > 25:
                print(f"   ... and {len(changed) - 25} more")
        
        if new_added:
            print(f"\n➕ New packages ({len(new_added)}):")
            for name, version in sorted(new_added)[:25]:
                print(f"   {name}=={version}")
            if len(new_added) > 25:
                print(f"   ... and {len(new_added) - 25} more")
        
        # Installation command
        print("\n" + "-" * 65)
        print("🚀 INSTALL COMMAND")
        print("-" * 65)
        print()
        if args.index_url:
            print(f"pip install -r {args.output} --index-url {args.index_url}")
        else:
            print(f"pip install -r {args.output}")
        print()
        
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"   Warning: {e}")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
