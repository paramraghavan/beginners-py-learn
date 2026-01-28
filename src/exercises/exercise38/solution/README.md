# Python Package Compatibility Resolver

A script to find compatible versions of new Python packages **without updating any existing installed packages** on your AWS edge node.

**Supports custom internal package indexes (not just PyPI).**

## Quick Start

```bash
# Using your internal index with installed packages from a file
python find_compatible_versions.py \
    --installed-packages-file pip_list_output.txt \
    --new-packages-file new_packages.txt \
    --index-url https://your-internal-index.com/simple/ \
    --trusted-host your-internal-index.com
```

## Step-by-Step Usage

### Step 1: Export installed packages from your AWS edge node

On your edge node, run:
```bash
pip list > installed_packages.txt
# OR
pip freeze > installed_packages.txt
```

### Step 2: Create your new packages list

Create `new_packages.txt` with one package per line:
```
httpx
celery
fastapi
pydantic
redis
boto3
kafka-python
aiohttp
sqlalchemy
paramiko
python-dotenv
pyyaml
cryptography
uvicorn
websockets
```

### Step 3: Run the resolver

```bash
python find_compatible_versions.py \
    --installed-packages-file installed_packages.txt \
    --new-packages-file new_packages.txt \
    --index-url https://your-internal-pypi.company.com/simple/ \
    --trusted-host your-internal-pypi.company.com
```

### Step 4: Install using generated files

```bash
# Option A: Use requirements file with constraints
pip install -r new_requirements.txt -c current_constraints.txt \
    --index-url https://your-internal-pypi.company.com/simple/ \
    --trusted-host your-internal-pypi.company.com

# Option B: Use generated script
./install_new_packages.sh
```

## All Options

| Option | Description |
|--------|-------------|
| **Package Options** | |
| `--new-packages` | Space-separated list of packages to install |
| `--new-packages-file` | File containing new packages (one per line) |
| `--installed-packages-file` | File with installed packages (pip list/freeze output) |
| **Index Options** | |
| `--index-url`, `-i` | Your internal package index URL |
| `--extra-index-url` | Additional index (use alongside primary) |
| `--trusted-host` | Skip SSL verification for this host |
| **Output Options** | |
| `--constraints-output` | Output constraints file (default: `current_constraints.txt`) |
| `--requirements-output` | Output requirements file (default: `new_requirements.txt`) |
| `--script-output` | Output install script (default: `install_new_packages.sh`) |
| `--generate-pip-conf` | Generate example pip.conf for your index |
| **Behavior** | |
| `--dry-run` | Preview only, don't generate files |
| `--verbose`, `-v` | Show detailed output |

## Supported Input Formats

### Installed Packages File

The script accepts multiple formats:

**pip list format:**
```
Package              Version
-------------------- ----------
boto3                1.26.0
requests             2.31.0
numpy                1.24.3
```

**pip freeze format:**
```
boto3==1.26.0
requests==2.31.0
numpy==1.24.3
```

**Simple format:**
```
boto3 1.26.0
requests 2.31.0
numpy 1.24.3
```

### New Packages File

```
# Comments are supported
httpx
celery
fastapi>=0.100.0    # Version constraints work too
pydantic
```

## Example Output

```
============================================================
PYTHON PACKAGE COMPATIBILITY RESOLVER
============================================================

Package Index: https://internal-pypi.company.com/simple/
Trusted Host: internal-pypi.company.com

Step 1: Loading currently installed packages...
  Reading from file: installed_packages.txt
  Found 45 installed packages

Step 2: Creating constraints file...
Created constraints file with 45 packages: current_constraints.txt

  Already installed packages (will be skipped):
    - requests (2.31.0)
    - boto3 (1.26.0)

Step 3: Resolving compatible versions...
  New packages to resolve: httpx, celery, fastapi

============================================================
RESOLUTION RESULTS
============================================================

Compatible versions found:

  Package                        Version        
  ------------------------------ ---------------
  celery                         5.3.1          
  fastapi                        0.103.0        
  httpx                          0.24.1         
  ... (dependencies listed)

  Note: 12 additional dependencies will be installed

============================================================
GENERATING OUTPUT FILES
============================================================

Generated requirements file: new_requirements.txt
Generated installation script: install_new_packages.sh

To install the packages, run:
  pip install -r new_requirements.txt -c current_constraints.txt --index-url https://internal-pypi.company.com/simple/

Or use the generated script:
  ./install_new_packages.sh
```

## Output Files Generated

| File | Description |
|------|-------------|
| `current_constraints.txt` | All current packages pinned to their versions |
| `new_requirements.txt` | New packages with resolved compatible versions |
| `install_new_packages.sh` | Ready-to-run installation script (includes your index URL) |
| `pip.conf.example` | (Optional) Example pip config for your index |

## How It Works

1. **Reads installed packages** from your provided file (or scans current env)
2. **Creates constraints file** pinning all existing packages to current versions
3. **Uses pip's resolver** with `--constraint` flag to find compatible versions
4. **Queries your internal index** for available package versions
5. **Generates installation files** with your index URL baked in

## Tips for AWS Edge Nodes

1. **Export packages first**: Run `pip list > installed.txt` on your edge node
2. **Test with dry-run**: Always preview with `--dry-run` before generating files
3. **Use trusted-host**: If your internal index uses self-signed certs
4. **Check network access**: Ensure the resolver machine can reach your index
5. **Transfer files**: Copy generated files to your edge node for installation

## Troubleshooting

**"Package not found in index"**
- Verify the package exists in your internal index
- Check the package name spelling
- Try `pip search <package> --index-url <your-url>` to verify

**"No compatible version found"**
- The package requires a newer version of an existing dependency
- Try installing an older version: `package<=1.0` in your list

**Network/SSL errors**
- Use `--trusted-host` for self-signed certificates
- Verify the index URL is correct and accessible

## Requirements

- Python 3.7+
- pip 21.0+ (for `--report` flag support)
- Network access to your package index
