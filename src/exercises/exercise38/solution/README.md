# Python Package Compatibility Resolver

A script to find compatible versions of new Python packages **without updating any existing installed packages** on your AWS edge node.

## Problem Solved

When you have an environment with many pre-installed packages (like an AWS edge node), installing new packages can accidentally upgrade existing ones, breaking dependencies. This script:

1. Captures your current environment state
2. Uses pip's dependency resolver with constraints
3. Finds versions of new packages that work with your existing setup
4. Generates ready-to-use installation commands

## Quick Start

```bash
# Basic usage - resolve a few packages
python find_compatible_versions.py --new-packages httpx celery fastapi

# Use a file with package list
python find_compatible_versions.py --new-packages-file new_packages.txt

# Dry run - just show what would be resolved without generating files
python find_compatible_versions.py --new-packages pandas numpy --dry-run
```

## Usage Options

| Option | Description |
|--------|-------------|
| `--new-packages` | Space-separated list of packages to install |
| `--new-packages-file` | File containing packages (one per line) |
| `--constraints-output` | Output file for constraints (default: `current_constraints.txt`) |
| `--requirements-output` | Output file for resolved versions (default: `new_requirements.txt`) |
| `--script-output` | Output install script (default: `install_new_packages.sh`) |
| `--dry-run` | Only show results, don't generate files |
| `--verbose` | Show detailed output |

## How It Works

1. **Scans installed packages**: Gets all currently installed packages and versions
2. **Creates constraints file**: Pins all existing packages to their current versions
3. **Resolves dependencies**: Uses pip's `--constraint` flag to find compatible versions
4. **Handles conflicts**: If batch resolution fails, tries packages individually
5. **Generates output**: Creates requirements.txt and install script

## Example Workflow

### Step 1: Create your package list

Create `new_packages.txt`:
```
httpx
celery
fastapi
pydantic
redis
boto3
```

### Step 2: Run the resolver

```bash
python find_compatible_versions.py --new-packages-file new_packages.txt
```

### Step 3: Review output

The script will show:
- Which packages are already installed (skipped)
- Compatible versions for new packages
- Additional dependencies that will be installed

### Step 4: Install

Option A - Use the generated requirements file:
```bash
pip install -r new_requirements.txt -c current_constraints.txt
```

Option B - Use the generated script:
```bash
./install_new_packages.sh
```

## Output Files

| File | Description |
|------|-------------|
| `current_constraints.txt` | All current packages pinned to their versions |
| `new_requirements.txt` | New packages with resolved compatible versions |
| `install_new_packages.sh` | Ready-to-run installation script |

## Handling Conflicts

If a package cannot be resolved, the script will tell you. Common solutions:

1. **Version conflict**: The new package requires a version of a dependency that conflicts with your existing packages
2. **Try alternatives**: Look for alternative packages that provide similar functionality
3. **Selective upgrade**: If absolutely necessary, you may need to upgrade specific packages

## Example Output

```
============================================================
PYTHON PACKAGE COMPATIBILITY RESOLVER
============================================================

Step 1: Scanning currently installed packages...
  Found 142 installed packages

Step 2: Creating constraints file...
Created constraints file with 142 packages: current_constraints.txt

  Already installed packages (will be skipped):
    - requests (2.31.0)

Step 3: Resolving compatible versions...
  New packages to resolve: httpx, celery

============================================================
RESOLUTION RESULTS
============================================================

Compatible versions found:

  Package                        Version        
  ------------------------------ ---------------
  celery                         5.6.2          
  httpx                          0.28.1          
  ... (dependencies)

  Note: 15 additional dependencies will be installed
```

## Tips for AWS Edge Nodes

1. **Test first**: Always use `--dry-run` first to see what would happen
2. **Backup state**: Keep a copy of `pip freeze > backup_requirements.txt`
3. **Check disk space**: Edge nodes may have limited storage
4. **Network access**: Ensure pip can reach PyPI
5. **Python version**: Some packages may not support older Python versions

## Requirements

- Python 3.7+
- pip 21.0+ (for `--report` flag support)

## Troubleshooting

**"No compatible version found"**
- The package has hard requirements that conflict with your existing packages
- Try an older version: `package<=1.0` in your package list

**"Package not found on PyPI"**  
- Check the package name spelling
- Package might be named differently (e.g., `Pillow` vs `PIL`)

**Script seems slow**
- Dependency resolution can take time for many packages
- Try smaller batches if resolving many packages
