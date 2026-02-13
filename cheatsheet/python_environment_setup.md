Here are **simple, reliable steps** for **Mac or Windows** to install Jupyter Notebook and run a **Hello World**.

## Option A (recommended): Install with Anaconda (easiest)

Anaconda includes Python + Jupyter + common data libraries.

### 1) Download & install

* Go to the Anaconda website and download **Anaconda (Python 3.x)** for your OS.
* Install with defaults.

### 2) Launch Jupyter Notebook

**Mac**

1. Open **Terminal**
2. Run:

   ```bash
   jupyter notebook
   ```

**Windows**

1. Open **Anaconda Prompt** (Start Menu → search “Anaconda Prompt”)
2. Run:

   ```bash
   jupyter notebook
   ```

A browser window/tab will open with the Jupyter file browser.

### 3) Create a notebook & run Hello World

1. In the Jupyter browser page: **New → Python 3 (ipykernel)** (or similar)
2. In the first cell, type:

   ```python
   print("Hello, World!")
   ```
3. Press **Shift + Enter** to run the cell.

You should see:

```
Hello, World!
```

---

## Option B: Install with Python + pip (lightweight)
I prefer this option as it has smaller footprint.
Use this if you already have Python installed and don’t want Anaconda.

### 1) Install Python

* Install Python 3 from python.org (make sure it’s Python 3.10+ ideally).
* **Windows important:** during install, check **“Add Python to PATH”**.

### 2) Install Jupyter

**Mac (Terminal) / Windows (Command Prompt or PowerShell)**

```bash
python -m pip install --upgrade pip
python -m pip install notebook
```

### 3) Start Jupyter Notebook

```bash
jupyter notebook
```

### 4) The jupyter notebook opens up, inteh jupyter notbook cell enter


```python
print("Hello, World!")
```

To run with **Shift + Enter**.

---

## If something goes wrong (fast fixes)

* If `jupyter` is “not recognized” (Windows): close/reopen terminal, or use:

  ```bash
  python -m notebook
  ```
* If you have multiple Python versions, try:

  ```bash
  python3 -m pip install notebook
  python3 -m notebook
  ```