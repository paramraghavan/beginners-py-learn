# Jupyter Notebook — Setup & Tutorial
## Windows and Mac · Standard Python Install

---

## Part 1 — Installation

---

### Windows Setup

#### Step 1 — Install Python (if not already installed)

1. Go to **https://www.python.org/downloads/**
2. Click **Download Python 3.x.x** (latest stable)
3. Run the installer
4. ⚠️ **Critical:** Check **"Add Python to PATH"** at the bottom of the installer screen before clicking Install Now
5. Click **Install Now**
6. When done, click **"Disable path length limit"** if prompted (recommended)

**Verify Python installed correctly:**

Open **Command Prompt** (search "cmd" in Start menu) and type:

```
python --version
```

You should see something like `Python 3.12.3`

If you see `python is not recognized`, Python was not added to PATH.
Fix: Uninstall and reinstall, making sure to check the PATH box.

---

#### Step 2 — Install Jupyter

In Command Prompt:

```
pip install notebook
```

This installs Jupyter Notebook and all dependencies. Takes 1–2 minutes.

**Also install common data science packages while you're here:**

```
pip install pandas numpy matplotlib seaborn
```

---

#### Step 3 — Launch Jupyter

In Command Prompt:

```
jupyter notebook
```

This will:
- Start the Jupyter server in your terminal (leave it open)
- Automatically open your browser to `http://localhost:8888`
- Show your home directory file tree

**To open a specific folder:**

```
cd C:\Users\YourName\Documents\notebooks
jupyter notebook
```

---

#### Step 4 — Create Your First Notebook

1. In the browser, click **New** → **Python 3 (ipykernel)**
2. A new tab opens with an empty notebook
3. Click on the title **"Untitled"** at the top to rename it
4. You're ready to code

---

#### Windows Troubleshooting

| Problem | Fix |
|---|---|
| `jupyter is not recognized` | Run `pip install notebook` again; restart cmd |
| Browser doesn't open | Go to `http://localhost:8888` manually |
| Port 8888 in use | Run `jupyter notebook --port 8889` |
| Permission errors on pip | Run `pip install --user notebook` |
| Slow startup | Normal first time — wait 30 seconds |

---

### Mac Setup

#### Step 1 — Install Python (if not already installed)

Macs come with Python 2 (old) or sometimes Python 3, but it's best to
install a clean version from python.org.

1. Go to **https://www.python.org/downloads/mac-osx/**
2. Download the **macOS installer** for Python 3.x.x
3. Open the `.pkg` file and follow the installer
4. The installer adds Python to your PATH automatically

**Verify in Terminal** (Applications → Utilities → Terminal):

```bash
python3 --version
```

You should see `Python 3.12.x`

> On Mac, always use `python3` and `pip3` (not `python` or `pip`)
> to make sure you're using Python 3, not the old system Python 2.

---

#### Step 2 — Install Jupyter

In Terminal:

```bash
pip3 install notebook
```

**Install common packages:**

```bash
pip3 install pandas numpy matplotlib seaborn
```

---

#### Step 3 — Launch Jupyter

```bash
jupyter notebook
```

To open in a specific folder:

```bash
cd ~/Documents/notebooks
jupyter notebook
```

---

#### Step 4 — Create Your First Notebook

Same as Windows:
1. Click **New** → **Python 3 (ipykernel)**
2. Rename the notebook
3. Start coding

---

#### Mac Troubleshooting

| Problem | Fix |
|---|---|
| `jupyter: command not found` | Use `python3 -m notebook` instead |
| Wrong Python version | Make sure you used `pip3`, not `pip` |
| Permission denied | Use `pip3 install --user notebook` |
| Browser opens wrong address | Try `http://localhost:8888` manually |
| SSL certificate error on pip | Run `pip3 install --trusted-host pypi.org notebook` |

---

### Checking Your Install (Both Platforms)

Run this in the terminal/cmd after installing:

```bash
# Windows
python -m notebook --version

# Mac
python3 -m notebook --version
```

You should see a version number like `7.2.1`

---

## Part 2 — The Jupyter Interface

---

### The Dashboard (File Browser)

When Jupyter opens in your browser you see the **Dashboard**:

```
┌─────────────────────────────────────────────────────────┐
│  jupyter                              [Quit] [Logout]   │
├─────────────────────────────────────────────────────────┤
│  Files   Running   Clusters                             │
│                              [Upload] [New ▼]           │
│  ─────────────────────────────────────────────────────  │
│  📁 Documents                                           │
│  📁 notebooks                                           │
│  📄 my_analysis.ipynb                                   │
└─────────────────────────────────────────────────────────┘
```

- **Files tab** — browse and open notebooks
- **Running tab** — see which notebooks are currently running
- **New** button — create a new notebook or text file
- **Upload** button — upload files from your computer

---

### Inside a Notebook

```
┌─────────────────────────────────────────────────────────────┐
│  📓 my_analysis  [Last saved: 2 minutes ago]                │
├──────────────────────────────────────────────────────────── │
│  File  Edit  View  Insert  Cell  Kernel  Help               │
├──────────────────────────────────────────────────────────── │
│  [▶ Run] [■ Stop] [⟳ Restart] [⊞ +]  Code ▼              │
├──────────────────────────────────────────────────────────── │
│                                                             │
│  In [1]:  ┌────────────────────────────────────────────┐   │
│           │ import pandas as pd                        │   │
│           │ print("Hello Jupyter")                     │   │
│           └────────────────────────────────────────────┘   │
│  Out[1]:  Hello Jupyter                                     │
│                                                             │
│  In [2]:  ┌────────────────────────────────────────────┐   │
│           │ 2 + 2                                      │   │
│           └────────────────────────────────────────────┘   │
│  Out[2]:  4                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Cell Types

| Type | Purpose | How to switch |
|---|---|---|
| **Code** | Run Python code | Dropdown menu → Code |
| **Markdown** | Write formatted text, headings, notes | Dropdown → Markdown |
| **Raw** | Plain text, not executed | Dropdown → Raw |

---

### Essential Keyboard Shortcuts

**Two modes:**
- **Edit mode** (green border) — you are typing inside a cell
- **Command mode** (blue border) — you are navigating between cells

Press **Esc** to go from Edit → Command mode
Press **Enter** to go from Command → Edit mode

#### In Command Mode (press Esc first)

| Key | Action |
|---|---|
| `Shift + Enter` | Run cell and move to next |
| `Ctrl + Enter` | Run cell, stay on same cell |
| `Alt + Enter` | Run cell, insert new cell below |
| `A` | Insert cell **above** current |
| `B` | Insert cell **below** current |
| `D D` | Delete current cell (press D twice) |
| `Z` | Undo cell deletion |
| `M` | Change cell to Markdown |
| `Y` | Change cell to Code |
| `L` | Toggle line numbers |
| `0 0` | Restart kernel (press 0 twice) |
| `H` | Show all shortcuts |

#### In Edit Mode (cell is green)

| Key | Action |
|---|---|
| `Tab` | Auto-complete |
| `Shift + Tab` | Show docstring / help for function |
| `Ctrl + /` | Comment / uncomment line |
| `Ctrl + Z` | Undo |
| `Ctrl + S` | Save notebook |

---

## Part 3 — Jupyter Tutorial

The following sections are designed to be typed into cells in your notebook.
Each code block is one cell.

---

### Cell 1 — Import Libraries

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Check versions
print(f"pandas  : {pd.__version__}")
print(f"numpy   : {np.__version__}")
```

---

### Cell 2 — Jupyter Displays Tables Automatically

One of Jupyter's best features: DataFrames render as formatted HTML tables.
Just put the DataFrame as the **last line** of a cell — no print() needed.

```python
df = pd.DataFrame({
    'employee_id': ['C1234', 'F5678', 'C9012', 'F3456', 'C7890'],
    'department':  ['Quant', 'Risk',  'Quant', 'Tech',  'Risk'],
    'month':       ['2025-01', '2025-01', '2025-02', '2025-02', '2025-02'],
    'cost':        [1200.0, 850.0, 2100.0, 450.0, 3200.0],
    'cpu_hours':   [120, 80, 210, 45, 310],
})

df   # ← last line = displayed as a table, no print() needed
```

---

### Cell 3 — Multiple Outputs in One Cell

```python
print("Shape:", df.shape)
print("Columns:", list(df.columns))
print()
df.describe().round(2)   # ← last line renders as table
```

---

### Cell 4 — Tab Completion and Help

```python
# Type df. and press Tab to see all available methods
# df.

# Type a function name + Shift+Tab to see its documentation
# df.groupby(   ← put cursor here and press Shift+Tab
```

---

### Cell 5 — Magic Commands

Jupyter has special `%` commands called "magic commands":

```python
# Time how long a cell takes to run
%time df.sort_values('cost')

# Time multiple runs and show average
%timeit df['cost'].sum()

# List all variables in memory
%whos

# Run a shell command directly from a cell
# Windows:
%ls
# Mac/Linux:
%ls -la
```

---

### Cell 6 — Inline Plots (most important Jupyter feature)

```python
# %matplotlib inline makes plots appear inside the notebook
%matplotlib inline

plt.figure(figsize=(8, 4))
plt.bar(df['employee_id'], df['cost'], color=['#4472C4','#ED7D31','#4472C4','#ED7D31','#4472C4'])
plt.title('Cost by Employee')
plt.xlabel('Employee ID')
plt.ylabel('Cost ($)')
plt.tight_layout()
plt.show()
```

---

### Cell 7 — Multiple Plots in One Cell

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left plot
axes[0].bar(df['employee_id'], df['cost'])
axes[0].set_title('Cost by Employee')
axes[0].set_xlabel('Employee ID')
axes[0].set_ylabel('Cost ($)')

# Right plot
dept_cost = df.groupby('department')['cost'].sum()
axes[1].pie(dept_cost, labels=dept_cost.index, autopct='%1.1f%%')
axes[1].set_title('Cost by Department')

plt.tight_layout()
plt.show()
```

---

### Cell 8 — Markdown Cells for Documentation

Switch this cell type to **Markdown** (press Esc then M):

```markdown
## Analysis Results

This notebook analyses **chargeback costs** for the EMR cluster.

Key findings:
- Risk department has the **highest** total spend at $4,050
- C7890 is the single largest user at $3,200/month

### Formula used

$$
\text{User Share} = \frac{\text{User Direct Cost}}{\text{Total User Cost}} \times 100
$$
```

Markdown supports:
- `**bold**`, `*italic*`
- `# H1`, `## H2`, `### H3` headings
- Bullet lists and numbered lists
- `` `inline code` `` and code blocks
- LaTeX math with `$formula$`
- HTML tables

---

### Cell 9 — Groupby and Display

```python
# Aggregate
summary = df.groupby('department').agg(
    total_cost  = ('cost',        'sum'),
    avg_cost    = ('cost',        'mean'),
    num_users   = ('employee_id', 'nunique'),
).round(2)

# Style the output table
summary.style.format('${:,.2f}', subset=['total_cost','avg_cost']) \
             .background_gradient(subset=['total_cost'], cmap='Blues') \
             .set_caption('Cost Summary by Department')
```

---

### Cell 10 — Interactive Widgets

```python
# Install first if needed:
# pip install ipywidgets   (then restart kernel)

from ipywidgets import interact, Dropdown

@interact(department=list(df['department'].unique()) + ['All'])
def show_by_dept(department='All'):
    if department == 'All':
        display(df[['employee_id','department','cost']])
    else:
        display(df[df['department']==department][['employee_id','cost']])
```

This creates a **live dropdown** — changing the selection instantly
updates the table without re-running the cell.

---

### Cell 11 — Reading and Writing Files

```python
# Save DataFrame to CSV
df.to_csv('chargeback.csv', index=False)
print("Saved chargeback.csv")

# Read it back
df2 = pd.read_csv('chargeback.csv')
df2.head()
```

---

### Cell 12 — Full Mini Analysis (put it all together)

```python
# ── Data ────────────────────────────────────────────────
df = pd.DataFrame({
    'employee_id': ['C1234','F5678','C9012','F3456','C7890'],
    'department':  ['Quant','Risk','Quant','Tech','Risk'],
    'month':       ['2025-01','2025-01','2025-02','2025-02','2025-02'],
    'cost':        [1200.0, 850.0, 2100.0, 450.0, 3200.0],
    'cpu_hours':   [120, 80, 210, 45, 310],
    'gpu_hours':   [10, 0, 30, 5, 50],
})

# ── Derived columns ──────────────────────────────────────
df['total_hours'] = df['cpu_hours'] + df['gpu_hours']
df['cost_per_hr'] = (df['cost'] / df['total_hours']).round(2)
df['cost_pct']    = (df['cost'] / df['cost'].sum() * 100).round(1)

# ── Summary table ────────────────────────────────────────
summary = df.groupby('department').agg(
    users         = ('employee_id', 'nunique'),
    total_cost    = ('cost',        'sum'),
    avg_cost      = ('cost',        'mean'),
    total_cpu_hrs = ('cpu_hours',   'sum'),
).round(2)

# ── Chart ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle('EMR Cluster Chargeback Summary', fontsize=14, fontweight='bold')

# Bar chart
axes[0].barh(df['employee_id'], df['cost'])
axes[0].set_title('Cost by User')
axes[0].set_xlabel('Cost ($)')

# Pie chart
dept = df.groupby('department')['cost'].sum()
axes[1].pie(dept, labels=dept.index, autopct='%1.0f%%', startangle=90)
axes[1].set_title('Share by Department')

# Scatter
axes[2].scatter(df['cpu_hours'], df['cost'], s=100)
for _, r in df.iterrows():
    axes[2].annotate(r['employee_id'], (r['cpu_hours'], r['cost']),
                     textcoords='offset points', xytext=(5,5), fontsize=8)
axes[2].set_title('Cost vs CPU Hours')
axes[2].set_xlabel('CPU Hours')
axes[2].set_ylabel('Cost ($)')

plt.tight_layout()
plt.show()

# ── Display summary ──────────────────────────────────────
print("Cost Summary by Department:")
summary
```

---

## Part 4 — Managing Notebooks

### Saving

- **Ctrl+S** (Windows) / **Cmd+S** (Mac) — save manually
- Jupyter auto-saves every 2 minutes
- File → Download as → Notebook (.ipynb) — save a copy

### Exporting

```bash
# Export to HTML (share without needing Python)
jupyter nbconvert --to html my_notebook.ipynb

# Export to PDF (requires LaTeX installed)
jupyter nbconvert --to pdf my_notebook.ipynb

# Export to a plain Python script
jupyter nbconvert --to script my_notebook.ipynb
```

### Restarting the Kernel

The **kernel** is the Python process running your code.
If things get stuck or variables are in a bad state:

- **Kernel → Restart** — clears all variables, keeps cell outputs
- **Kernel → Restart & Clear Output** — clean slate
- **Kernel → Restart & Run All** — restart then re-run every cell top to bottom

> Always run **Restart & Run All** before sharing a notebook to make sure
> it works cleanly from top to bottom.

### Closing a Notebook

Closing the browser tab does **not** stop the kernel.
To fully stop it:
- Go to the dashboard → Running tab → Click **Shutdown** next to your notebook
- Or: **File → Close and Halt** inside the notebook

### Stopping the Jupyter Server

Go back to your terminal/cmd where `jupyter notebook` is running
and press **Ctrl+C**, then confirm with `y`.

---

## Part 5 — Useful Extensions

### JupyterLab (modern version of Jupyter)

JupyterLab is the next-generation interface — same notebooks,
better layout with side panels and tabs.

```bash
pip install jupyterlab      # Windows
pip3 install jupyterlab     # Mac

# Launch
jupyter lab
```

### nbextensions (extra toolbar buttons)

```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

Adds useful features: table of contents, collapsible sections,
code folding, spell check.

---

## Quick Reference Card

```
LAUNCH
  jupyter notebook              Windows terminal / Mac terminal
  jupyter lab                   JupyterLab (modern UI)
  jupyter notebook --port 8889  If default port is busy

SHORTCUTS (Command Mode — press Esc first)
  Shift+Enter   Run cell, go to next
  Ctrl+Enter    Run cell, stay
  A / B         Insert cell above / below
  D D           Delete cell
  M / Y         Markdown / Code cell
  Z             Undo delete
  0 0           Restart kernel
  H             Help (all shortcuts)

SHORTCUTS (Edit Mode — inside a cell)
  Tab           Autocomplete
  Shift+Tab     Show docs
  Ctrl+/        Toggle comment
  Ctrl+S        Save

MAGIC COMMANDS
  %time         Time one execution
  %timeit       Time average of many runs
  %whos         List all variables
  %matplotlib inline  Show plots in notebook
  %run file.py  Run a .py file

EXPORT
  jupyter nbconvert --to html   my_notebook.ipynb
  jupyter nbconvert --to script my_notebook.ipynb
```
