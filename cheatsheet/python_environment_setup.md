# Python Environment Setup Guide

Complete steps to install Python and Jupyter Notebook on Mac or Windows.

---

## Option A: Anaconda (Recommended - Easiest)

Anaconda includes Python + Jupyter + 250+ data science libraries pre-installed.

### Step 1: Download & Install

1. Go to [anaconda.com](https://www.anaconda.com/products/individual)
2. Download **Anaconda (Python 3.x)** for your OS
3. Run installer with default settings
4. Installation takes 2-3 minutes

### Step 2: Launch Jupyter Notebook

**Mac:**
```bash
# Open Terminal and run:
jupyter notebook
```

**Windows:**
```bash
# Open Anaconda Prompt and run:
jupyter notebook
```

A browser window will open with the Jupyter file browser.

### Step 3: Create Your First Notebook

1. Click **New** → **Python 3** (or ipykernel)
2. In the first cell, type:
   ```python
   print("Hello, World!")
   ```
3. Press **Shift + Enter** to execute
4. You should see output: `Hello, World!`

✅ You're ready to use the cheatsheets!

---

## Option B: Python + pip (Lightweight Alternative)

Use this if you already have Python 3.10+ installed and prefer a minimal setup.

### Step 1: Install/Verify Python

**Mac:**
```bash
python3 --version  # Check if installed
```

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Jupyter

```bash
# Update pip first
python -m pip install --upgrade pip

# Install Jupyter
python -m pip install notebook
```

### Step 3: Start Jupyter & Create Notebook

```bash
jupyter notebook
```

Then follow Step 3 from Option A (above).

---

## Troubleshooting

### "jupyter: command not found" (Mac/Linux)
Try using Python's module syntax:
```bash
python -m jupyter notebook
# or
python3 -m jupyter notebook
```

### "jupyter is not recognized" (Windows)
1. Close and reopen Command Prompt or PowerShell
2. Try: `python -m notebook`
3. If still fails, reinstall:
   ```bash
   pip uninstall jupyter
   pip install jupyter
   ```

### Multiple Python Versions
If you have Python 2 and 3:
```bash
python3 -m pip install notebook
python3 -m jupyter notebook
```

### Permission Denied Error
```bash
# Mac/Linux
sudo python -m pip install notebook
```

---

## Verify Your Setup

Once Jupyter opens in your browser, run this test:

```python
# Test in a cell:
import numpy as np
import pandas as pd
print("✅ Setup successful!")
print(f"Python version: {__import__('sys').version}")
```

You should see confirmation that all libraries are installed.

---

## Next Steps

1. Open the Python cheatsheets
2. Copy examples from the relevant cheatsheet
3. Paste into Jupyter cells
4. Modify and experiment!

All code examples are designed to run standalone in Jupyter cells.