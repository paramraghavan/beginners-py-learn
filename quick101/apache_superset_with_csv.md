## Using Apache Superset with CSV Files

There are **3 ways** to use CSV files in Superset:

---

## Method 1 — Upload CSV Directly (Easiest)

### Enable CSV Upload First

By default CSV upload is disabled. Enable it:

**Settings → Database Connections → Edit your DB → Advanced → Allow file uploads**

Toggle **"Allow data upload"** to ON.

> Works best with **SQLite** or **PostgreSQL** as the target database.

### Upload the CSV

Go to **Data → Upload a CSV file**:

```
1. Click "Data" in the top nav
2. Select "Upload a CSV"
3. Fill in:
   - Table name     → what to call it in the DB
   - CSV file       → browse & select your file
   - Delimiter      → , or ; or \t
   - Header row     → usually row 0
   - If table exists → Fail / Replace / Append
4. Click "Save"
```

Superset loads the CSV into the connected database as a table — then you can explore it like any other dataset.

---

## Method 2 — SQL Lab with a CSV via SQLite (Local Dev)

If you're running Superset locally with SQLite, load a CSV via Python first:

```python
import pandas as pd
import sqlalchemy

# Load your CSV
df = pd.read_csv("sales_data.csv")

# Push into SQLite (Superset's default local DB)
engine = sqlalchemy.create_engine("sqlite:////app/superset_home/superset.db")
df.to_sql("sales_data", engine, if_exists="replace", index=False)

print("Done! Table 'sales_data' is now in Superset.")
```

Then in Superset → **SQL Lab**, you can immediately query it:

```sql
SELECT * FROM sales_data LIMIT 10;
```

---

## Method 3 — Load CSV into PostgreSQL, then connect Superset

The most **production-friendly** approach:

### Step 1 — Load CSV into PostgreSQL

```python
import pandas as pd
from sqlalchemy import create_engine

# Read CSV
df = pd.read_csv("sales_data.csv")

# Clean column names (remove spaces, lowercase)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Preview
print(df.head())
print(df.dtypes)

# Push to PostgreSQL
engine = create_engine("postgresql://user:password@localhost:5432/mydb")
df.to_sql(
    "sales_data",  # table name in DB
    engine,
    if_exists="replace",  # or "append"
    index=False,
    chunksize=1000
)

print(f"Loaded {len(df)} rows into PostgreSQL")
```

### Step 2 — Connect Superset to PostgreSQL

In Superset: **Settings → Database Connections → + Database**

```
Database type : PostgreSQL
Host          : localhost
Port          : 5432
Database      : mydb
Username      : user
Password      : password
```

### Step 3 — Register the table as a Dataset

**Datasets → + Dataset → pick your DB → pick `sales_data` table → Add**

### Step 4 — Explore & Chart

Click the dataset → **Explore** → build charts!

---

## Handling Common CSV Issues

```python
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("messy_data.csv")

# Fix 1: parse dates properly
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Fix 2: clean numeric columns (remove $, commas)
df["revenue"] = df["revenue"].str.replace("[$,]", "", regex=True).astype(float)

# Fix 3: fill nulls so Superset doesn't break
df["region"] = df["region"].fillna("Unknown")
df["revenue"] = df["revenue"].fillna(0)

# Fix 4: clean column names (Superset prefers snake_case)
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

print(df.dtypes)
print(df.shape)

# Load to DB
engine = create_engine("postgresql://user:pass@localhost/mydb")
df.to_sql("clean_data", engine, if_exists="replace", index=False)
```

---

## Multiple CSV Files into One Dashboard

```python
import pandas as pd
from sqlalchemy import create_engine
import glob

engine = create_engine("postgresql://user:pass@localhost/mydb")

# Load all CSVs from a folder and merge into one table
all_files = glob.glob("./data/*.csv")

dfs = []
for f in all_files:
    df = pd.read_csv(f)
    df["source_file"] = f  # track which file each row came from
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
combined.to_sql("all_sales", engine, if_exists="replace", index=False)

print(f"Loaded {len(combined)} rows from {len(all_files)} files")
```

In Superset SQL Lab you can then filter by `source_file` or any column.

---

## Quick Reference

```
CSV file
   ↓  (pandas read_csv)
DataFrame  →  clean columns, fix types, fill nulls
   ↓  (df.to_sql)
Database table (SQLite / PostgreSQL)
   ↓  (Superset Dataset)
Charts  →  Dashboard
```

**Recommended setup for CSV work:**

| Scenario                | Best approach                     |
|-------------------------|-----------------------------------|
| Quick local exploration | SQLite + direct upload            |
| Production dashboards   | PostgreSQL + pandas loader        |
| Many CSV files          | Combine with pandas, load once    |
| Scheduled refresh       | Script + cron job to reload table |