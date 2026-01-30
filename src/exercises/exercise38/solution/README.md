# Package Compatibility Resolver

A Python script to find compatible versions when adding new packages to an existing virtual environment.

## What It Does

```
pip freeze > exiting_packages.txt
┌─────────────────────────────────────────────────────────────────┐
│                         INPUTS                                  │
├─────────────────────────────────────────────────────────────────┤
│  existing_packages.txt     +     new_packages.txt               │
│  (from your venv)                (packages to add)              │
│                                                                 │
│  numpy==1.24.0                   scikit-learn                   │
│  pandas==2.0.0                   matplotlib>=3.5                │
│  requests==2.28.0                seaborn                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESOLUTION PROCESS                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Creates a temporary isolated virtual environment            │
│  2. Combines existing + new packages into one requirements      │
│  3. Installs everything in the temp venv                        │
│  4. pip's resolver finds compatible versions automatically      │
│  5. Checks for any dependency conflicts                         │
│  6. Exports the resolved versions                               │
│  7. Cleans up temp environment                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         OUTPUT                                  │
├─────────────────────────────────────────────────────────────────┤
│  requirements_resolved.txt                                      │
│                                                                 │
│  numpy==1.26.0          ← upgraded for sklearn compatibility    │
│  pandas==2.0.0          ← unchanged                             │
│  requests==2.28.0       ← unchanged                             │
│  scikit-learn==1.3.0    ← new                                   │
│  matplotlib==3.8.0      ← new                                   │
│  seaborn==0.13.0        ← new                                   │
│  ...plus all transitive dependencies                            │
└─────────────────────────────────────────────────────────────────┘
```

## Why Use This?

| Problem | Solution |
|---------|----------|
| Adding new packages might break existing ones | Tests in isolated environment first |
| Don't know which versions are compatible | pip's resolver figures it out |
| Manual trial-and-error takes forever | Automated single command |
| Afraid to modify production venv | Safe - doesn't touch your real environment |

## Usage

### Step 1: Export Existing Packages

```bash
# Activate your TARGET virtual environment
source /path/to/your/venv/bin/activate

# Export installed packages
pip freeze > existing_packages.txt

# Deactivate (optional)
deactivate
```

### Step 2: Create New Packages File

```bash
# List packages you want to add (one per line)
cat > new_packages.txt << EOF
scikit-learn
matplotlib>=3.5
seaborn
EOF
```

### Step 3: Run the Resolver

```bash
# Basic usage
python resolve_packages.py existing_packages.txt new_packages.txt

# With custom index URL
python resolve_packages.py existing_packages.txt new_packages.txt \
    --index-url https://your-pypi.com/simple

# With all options
python resolve_packages.py existing_packages.txt new_packages.txt \
    --index-url https://your-pypi.com/simple \
    --output resolved.txt \
    --strict
```

### Step 4: Install Resolved Packages

```bash
# Activate your TARGET venv again
source /path/to/your/venv/bin/activate

# Install the resolved versions
pip install -r requirements_resolved.txt --index-url https://your-pypi.com/simple

# Verify no conflicts
pip check
```

## Command Line Options

```
python resolve_packages.py <existing_packages.txt> <new_packages.txt> [OPTIONS]

Arguments:
    existing_packages.txt   File from 'pip freeze' of your current environment
    new_packages.txt        File with new packages to add

Options:
    --index-url URL         Custom PyPI index URL
    --strict                Keep existing versions pinned exactly (may fail)
    --output FILE           Output filename (default: requirements_resolved.txt)
    --help                  Show help message
```

## Resolution Strategies

### Flexible (Default)

- Converts `==` to `>=` for existing packages
- Allows pip to upgrade packages if needed for compatibility
- **Recommended** - higher success rate

```bash
python resolve_packages.py existing.txt new.txt
```

### Strict

- Keeps existing package versions exactly as specified
- May fail if new packages require different versions
- Use when you cannot upgrade existing packages

```bash
python resolve_packages.py existing.txt new.txt --strict
```

## Output Files

| File | Description |
|------|-------------|
| `requirements_resolved.txt` | Final resolved versions - use this to install |
| `requirements_combined.txt` | Combined input file (for debugging) |

## Example Output

```
=================================================================
🐍 Package Compatibility Resolver
=================================================================

  Existing packages: existing_packages.txt
  New packages:      new_packages.txt
  Index URL:         https://pypi.org/simple (default)
  Strategy:          FLEXIBLE (allow upgrades)
  Output file:       requirements_resolved.txt

-----------------------------------------------------------------
📁 Reading input files...
-----------------------------------------------------------------
   Existing packages: 45
   New packages:      3

📦 New packages to add:
   - scikit-learn
   - matplotlib
   - seaborn

-----------------------------------------------------------------
🔄 Resolving dependencies...
-----------------------------------------------------------------
📄 Combined requirements: requirements_combined.txt
🔨 Creating temporary test environment...
   Upgrading pip...
   ✅ Test environment ready

📦 Installing packages in test environment...
   (This may take several minutes)

🔍 Checking for dependency conflicts...
   ✅ No conflicts found

=================================================================
✅ SUCCESS!
=================================================================

📄 Output: requirements_resolved.txt

-----------------------------------------------------------------
📊 CHANGES SUMMARY
-----------------------------------------------------------------

   Unchanged: 42

🔄 Version changes (3):
   numpy: 1.24.0 → 1.26.0
   scipy: 1.10.0 → 1.11.0
   threadpoolctl: 3.1.0 → 3.2.0

➕ New packages (15):
   contourpy==1.2.0
   cycler==0.12.1
   fonttools==4.47.0
   joblib==1.3.2
   ...

-----------------------------------------------------------------
🚀 INSTALL COMMAND
-----------------------------------------------------------------

pip install -r requirements_resolved.txt

🧹 Cleaning up...

✅ Done!
```

## Troubleshooting

### "Could not find a version that satisfies the requirement"

- Check package name spelling
- Verify index URL is correct and accessible
- Try removing version constraints from new packages

### "Conflicting dependencies"

- Try without `--strict` flag
- Some packages may have incompatible requirements
- Check the specific error message for which packages conflict

### Resolution takes too long

- Normal for large environments (50+ packages)
- Can take 5-15 minutes
- pip is resolving the entire dependency tree

### Installation fails in target venv

```bash
# Check what's wrong
pip check

# See dependency tree
pip install pipdeptree
pipdeptree --reverse --packages <problem-package>
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library + pip)
