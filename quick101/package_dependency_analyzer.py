import pkg_resources
import subprocess
import sys
from collections import defaultdict


def is_package_installed(package_name):
    """
    Check if a package is installed in the current environment.

    Args:
        package_name (str): Name of the package to check

    Returns:
        bool: True if installed, False otherwise
    """
    try:
        pkg_resources.working_set.by_key[package_name]
        return True
    except KeyError:
        return False


def install_package(package_name):
    """
    Install a package using pip.

    Args:
        package_name (str): Name of the package to install

    Returns:
        bool: True if installation successful, False otherwise
    """
    try:
        # Use pip to install the package
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}")
        return False


def get_package_dependencies(package_name, auto_install=False):
    """
    Get all dependencies for a given package name.

    Args:
        package_name (str): Name of the package to analyze
        auto_install (bool): Whether to automatically install missing packages

    Returns:
        tuple: (direct_deps, all_deps, versions) or None if package cannot be analyzed
    """
    # Check if package is installed
    if not is_package_installed(package_name):
        print(f"\nPackage '{package_name}' is not installed.")

        if auto_install:
            print(f"Attempting to install {package_name}...")
            if install_package(package_name):
                print(f"Successfully installed {package_name}")
            else:
                print(f"Could not install {package_name}. Please install it manually.")
                return None
        else:
            print("You can:")
            print(f"1. Install it manually: pip install {package_name}")
            print("2. Run this script with auto-install: --install flag")
            return None

    try:
        # Get the distribution object for the package
        dist = pkg_resources.working_set.by_key[package_name]
    except KeyError:
        print(f"Error accessing package '{package_name}' after installation.")
        return None

    # Get direct dependencies
    direct_deps = [str(req) for req in dist.requires()]

    # Get all dependencies (including transitive)
    def get_all_deps(package):
        deps = set()
        try:
            dist = pkg_resources.working_set.by_key[package]
            for req in dist.requires():
                dep_name = req.key
                deps.add(dep_name)
                # If auto_install is enabled, try to install missing dependencies
                if auto_install and not is_package_installed(dep_name):
                    print(f"Installing missing dependency: {dep_name}")
                    install_package(dep_name)
                deps.update(get_all_deps(dep_name))
        except KeyError:
            pass
        return deps

    all_deps = get_all_deps(package_name)

    # Get installed versions
    versions = {}
    for dep in all_deps:
        try:
            versions[dep] = pkg_resources.working_set.by_key[dep].version
        except KeyError:
            versions[dep] = "Not installed"

    return direct_deps, sorted(all_deps), versions


def print_dependency_tree(package_name, auto_install=False):
    """
    Print a formatted dependency tree for the package.

    Args:
        package_name (str): Name of the package to analyze
        auto_install (bool): Whether to automatically install missing packages
    """
    result = get_package_dependencies(package_name, auto_install)

    if result is None:
        return

    direct_deps, all_deps, versions = result

    print(f"\nDependency analysis for {package_name}:")
    print("\nDirect dependencies:")
    for dep in direct_deps:
        print(f"  • {dep}")

    print("\nAll dependencies (including transitive):")
    for dep in all_deps:
        print(f"  • {dep} (version: {versions[dep]})")

    print(f"\nTotal number of dependencies: {len(all_deps)}")


if __name__ == "__main__":
    import argparse

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Analyze Python package dependencies")
    parser.add_argument("package_name", help="Name of the package to analyze")
    parser.add_argument("--install", action="store_true",
                        help="Automatically install missing packages")

    args = parser.parse_args()
    print_dependency_tree(args.package_name, args.install)


"""
parser.add_argument("--install", action="store_true")
- When action="store_true" is used, the argument becomes a flag
- If the flag is present, the value becomes True
- If the flag is not present, the value defaults to False
"""