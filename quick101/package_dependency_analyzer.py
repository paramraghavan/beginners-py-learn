from importlib.metadata import distribution
import importlib.metadata
import subprocess
import sys
from pip._internal.commands.show import search_packages_info
from typing import Dict, List, Tuple, Optional


def is_package_installed(package_name: str) -> bool:
    """
    Check if a package is installed in the current environment.
    """
    try:
        importlib.metadata.distribution(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


def install_package(package_name: str) -> bool:
    """
    Install a package using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}")
        return False


def get_package_info(package_name: str) -> Optional[Dict]:
    """
    Get detailed information about a package using pip's API.
    """
    try:
        # Get package information using importlib.metadata
        dist = importlib.metadata.distribution(package_name)
        requires = [str(req) for req in dist.requires] if dist.requires else []

        return {
            'name': dist.metadata['Name'],
            'version': dist.version,
            'requires': requires
        }
    except (importlib.metadata.PackageNotFoundError, KeyError) as e:
        return None


def parse_requirement(req_string: str) -> str:
    """
    Parse a requirement string to get the base package name.
    """
    # Remove version specifiers and extras
    for operator in ['>=', '<=', '==', '>', '<', '~=', '!=']:
        if operator in req_string:
            req_string = req_string.split(operator)[0]

    # Remove any extras (e.g., package[extra])
    if '[' in req_string:
        req_string = req_string.split('[')[0]

    return req_string.strip()


def get_package_dependencies(package_name: str, auto_install: bool = False) -> Optional[
    Tuple[List[str], List[str], Dict[str, str]]]:
    """
    Get all dependencies for a given package name.
    """
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
        pkg_info = get_package_info(package_name)
        if not pkg_info:
            print(f"Could not find information for package {package_name}")
            return None

        # Get direct dependencies
        direct_deps = pkg_info['requires']

        # Store all dependencies (including transitive ones)
        all_deps = set()
        visited = set()  # Track visited packages to avoid infinite recursion

        def collect_deps(pkg_name: str) -> None:
            """Recursively collect all dependencies"""
            if pkg_name in visited:
                return

            visited.add(pkg_name)
            pkg_info = get_package_info(pkg_name)

            if pkg_info and pkg_info['requires']:
                for dep in pkg_info['requires']:
                    base_dep = parse_requirement(dep)
                    all_deps.add(base_dep)

                    if auto_install and not is_package_installed(base_dep):
                        print(f"Installing missing dependency: {base_dep}")
                        install_package(base_dep)

                    collect_deps(base_dep)

        # Start collecting dependencies
        collect_deps(package_name)

        # Get versions for all dependencies
        versions = {}
        for dep in all_deps:
            try:
                versions[dep] = importlib.metadata.version(dep)
            except importlib.metadata.PackageNotFoundError:
                versions[dep] = "Not installed"

        return direct_deps, sorted(all_deps), versions

    except Exception as e:
        print(f"Error analyzing dependencies: {str(e)}")
        return None


def print_dependency_tree(package_name: str, auto_install: bool = False) -> None:
    """
    Print a formatted dependency tree for the package.
    """
    result = get_package_dependencies(package_name, auto_install)

    if result is None:
        return

    direct_deps, all_deps, versions = result

    try:
        package_version = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        package_version = "Not installed"

    print(f"\nDependency analysis for {package_name}:")
    print(f"Package version: {package_version}")

    print("\nDirect dependencies:")
    if direct_deps:
        for dep in direct_deps:
            print(f"  • {dep}")
    else:
        print("  No direct dependencies found")

    print("\nAll dependencies (including transitive):")
    if all_deps:
        for dep in all_deps:
            print(f"  • {dep} (version: {versions[dep]})")
    else:
        print("  No dependencies found")

    print(f"\nTotal number of dependencies: {len(all_deps)}")


if __name__ == "__main__":
    import argparse

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