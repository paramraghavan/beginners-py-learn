# Python Cheatsheet — Jupyter-Ready
### For Python Developers & Data Engineers
> Every code cell below runs standalone in a Jupyter notebook. Just copy-paste and run!

---

## Core Python

### Variables & Data Types

```python
# Dynamic typing
x = 10              # int
pi = 3.14           # float
name = "Alice"      # str
active = True       # bool
nothing = None      # NoneType
raw = b"bytes"      # bytes

# Type checking & conversion
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True
print(int("42"))             # 42
print(str(3.14))             # "3.14"
print(float("2.7"))          # 2.7

# Multiple assignment & swap
a, b, c = 1, 2, 3
a, b = b, a
print(f"a={a}, b={b}, c={c}")
```

### Control Flow

```python
x = 10
d = {"name": "Alice", "age": 30, "city": "NYC"}

# Conditionals
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary
label = "even" if x % 2 == 0 else "odd"
print(f"x={x} is {label}")

# Loops
for i in range(5):
    print(i, end=" ")
print()

for i in range(2, 10, 2):
    print(i, end=" ")
print()

for k, v in d.items():
    print(f"{k}: {v}")

# Match statement (3.10+)
status_code = 200
match status_code:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _:
        print("Other")
```

---

## Strings

```python
s = "Hello, World!"

# Slicing
print(s[0:5])         # "Hello"
print(s[::-1])        # reversed

# Key methods
print(s.lower())
print(s.upper())
print(s.strip())
print(s.split(","))           # ["Hello", " World!"]
print("-".join(["a","b"]))    # "a-b"
print(s.replace("World", "Python"))
print(s.startswith("He"))     # True
print(s.find("World"))        # 7
print(s.count("l"))           # 3
print(s.encode("utf-8"))      # bytes — important for pipelines

# f-strings (3.6+)
name, age = "Alice", 30
print(f"{name} is {age} years old")
print(f"{3.14159:.2f}")       # "3.14"
print(f"{1000000:,}")         # "1,000,000"
x = 42
print(f"{x = }")              # "x = 42" (3.8+)

# Raw strings (regex & Windows paths)
path = r"C:\data\files\output"
pattern = r"\d{4}-\d{2}-\d{2}"
print(f"path: {path}")
print(f"pattern: {pattern}")
```

---

## Data Structures

### Lists

```python
lst = [1, 2, 3, 4, 5]

# CRUD
lst.append(6)
print("append:", lst)
lst.insert(0, 0)
print("insert:", lst)
lst.extend([7, 8])
print("extend:", lst)

popped = lst.pop()
print(f"pop: {popped}, list: {lst}")
lst.remove(3)
print("remove 3:", lst)

# Searching & Sorting
print(4 in lst)
lst.sort(key=lambda x: -x)
print("desc sorted:", lst)
print("sorted copy:", sorted(lst))

# Slicing
lst = [10, 20, 30, 40, 50]
print(lst[1:4])     # [20,30,40]
print(lst[::2])     # every 2nd
print(lst[::-1])    # reversed

# Unpacking
first, *rest = lst
print(f"first={first}, rest={rest}")
```

### Dictionaries, Sets & Tuples

```python
# Dictionary
d = {"name": "Alice", "age": 30}
print(d["name"])
print(d.get("email", "N/A"))   # safe access

d["city"] = "NYC"
d.update({"age": 31})
merged = d | {"x": 1}          # merge (3.9+)
print("merged:", merged)

d.setdefault("tags", [])
print("setdefault:", d)

print("keys:", list(d.keys()))
print("values:", list(d.values()))

# defaultdict — no KeyError
from collections import defaultdict, OrderedDict
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
print("defaultdict:", dict(dd))

# Sets — deduplication & lookups
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}
print("intersection:", s1 & s2)
print("union:", s1 | s2)
print("difference:", s1 - s2)

# Tuples & Named tuples
t = (1, "a", 3.14)
x, y, z = t
print(f"unpacked: x={x}, y={y}, z={z}")

from collections import namedtuple
Record = namedtuple("Record", ["id", "name", "value"])
r = Record(1, "sensor_a", 42.5)
print(f"namedtuple: {r.name} = {r.value}")
```

### Tuples — Immutable Sequences

```python
# Creating tuples
t = (1, 2, 3, 4, 5)
single = (42,)            # trailing comma required for single-element tuple
empty = ()
from_list = tuple([1, 2, 3])

print(f"tuple: {t}, single: {single}, empty: {empty}")

# Indexing & slicing (same as lists)
print(t[0])       # 1
print(t[-1])      # 5
print(t[1:4])     # (2, 3, 4)
print(t[::-1])    # (5, 4, 3, 2, 1)

# Unpacking
a, b, *rest = t
print(f"a={a}, b={b}, rest={rest}")  # a=1, b=2, rest=[3, 4, 5]

# Swap idiom uses tuples under the hood
x, y = 10, 20
x, y = y, x
print(f"swapped: x={x}, y={y}")

# Tuple methods (only 2!)
print(t.count(3))   # 1
print(t.index(4))   # 3

# Tuples as dict keys (immutable = hashable)
location_cache = {(40.7, -74.0): "NYC", (34.1, -118.2): "LA"}
print(location_cache[(40.7, -74.0)])  # "NYC"

# Tuples as return values
def min_max(data):
    return min(data), max(data)

lo, hi = min_max([5, 2, 8, 1, 9])
print(f"min={lo}, max={hi}")

# Tuple vs list: immutability
try:
    t[0] = 99
except TypeError as e:
    print(f"Can't mutate tuple: {e}")

# Nested tuples (inner mutables CAN change)
nested = ([1, 2], [3, 4])
nested[0].append(99)
print(f"nested with mutated inner list: {nested}")

# Named tuples — lightweight records
from collections import namedtuple
Record = namedtuple("Record", ["id", "name", "value"])
r = Record(1, "sensor_a", 42.5)
print(f"namedtuple: {r.name} = {r.value}")
print(f"as dict: {r._asdict()}")
print(f"replace: {r._replace(value=99.9)}")

# typing.NamedTuple (modern alternative)
from typing import NamedTuple

class PipelineResult(NamedTuple):
    rows_processed: int
    errors: int
    duration_sec: float

result = PipelineResult(1500, 3, 12.5)
print(f"result: {result}, rows={result.rows_processed}")
```

---

## Functions

### Functions & Lambdas

```python
# Standard function
def transform(record, mapping=None):
    """Transform a single record."""
    mapping = mapping or {}
    return {mapping.get(k, k): v for k, v in record.items()}

raw = {"First Name": "Alice", "Last Name": "Smith"}
mapping = {"First Name": "first_name", "Last Name": "last_name"}
print("transformed:", transform(raw, mapping))
print("no mapping:", transform(raw))

# *args and **kwargs
def flexible(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

flexible(1, 2, 3, x=10, y=20)

# Lambda & higher-order functions
square = lambda x: x ** 2
print(f"square(5) = {square(5)}")
print("map:", list(map(lambda x: x*2, [1,2,3])))
print("filter:", list(filter(lambda x: x>2, [1,2,3,4,5])))

from functools import reduce
print("reduce:", reduce(lambda a, b: a+b, [1,2,3,4]))  # 10

# Type hints
from typing import Optional

def process(data: list[dict]) -> list[dict]:
    return [{"key": d.get("key", "").lower()} for d in data]

print("typed:", process([{"key": "HELLO"}, {"key": "WORLD"}]))
```

### Decorators & Generators

```python
import time
from functools import wraps

# Retry decorator (common in pipelines)
def retry(max_retries=3, delay=0.01):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"  Retry {attempt+1}/{max_retries}: {e}")
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

call_count = 0

@retry(max_retries=3, delay=0.01)
def flaky_function():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("Simulated failure")
    return "Success!"

call_count = 0
print(flaky_function())

# Generator — memory-efficient streaming
def read_in_chunks(data, chunk_size=3):
    """Simulate reading data in chunks."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

big_data = list(range(10))
for chunk in read_in_chunks(big_data, chunk_size=3):
    print(f"  Processing chunk: {chunk}")

# Generator pipeline (lazy, composable)
raw_lines = ["  Alice,30,NYC  ", "  Bob,25,LA  ", "  ,invalid,  ", "  Charlie,35,SF  "]
lines   = (line.strip() for line in raw_lines)
rows    = (line.split(",") for line in lines)
cleaned = [row for row in rows if len(row) == 3 and row[0]]
print("cleaned rows:", cleaned)
```

---

## Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
print("squares:", squares)

evens = [x for x in range(20) if x % 2 == 0]
print("evens:", evens)

# Nested — flatten
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print("flat:", flat)

# Dict comprehension — column renaming
raw_columns = ["First Name", "Last Name", "Phone Number"]
column_map = {col: col.lower().replace(" ", "_") for col in raw_columns}
print("column_map:", column_map)

# Set comprehension
data = {"a": 1, "b": "hello", "c": 3.14, "d": True, "e": [1,2]}
unique_types = {type(v).__name__ for v in data.values()}
print("unique_types:", unique_types)

# Conditional expression
records = [10, -5, 20, -3, 15]
labels = ["valid" if x >= 0 else "invalid" for x in records]
print("labels:", labels)

# Walrus operator (3.8+)
data = [1, -2, 3, -4, 5, 0]
def clean(x):
    return x * 10 if x > 0 else None

results = [cleaned for x in data if (cleaned := clean(x)) is not None]
print("walrus results:", results)
```

---

## Object-Oriented Programming

```python
from dataclasses import dataclass, field, asdict
from datetime import datetime
from abc import ABC, abstractmethod

# Dataclass (3.7+) — great for data models
@dataclass
class PipelineConfig:
    source: str
    destination: str
    batch_size: int = 1000
    created_at: datetime = field(default_factory=datetime.now)
    tags: list = field(default_factory=list)

config = PipelineConfig("s3://input", "postgres://db", tags=["etl", "daily"])
print("config:", config)
print("as dict:", asdict(config))

# Abstract base class — enforce interface
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> list[dict]:
        pass

class CSVExtractor(BaseExtractor):
    def __init__(self, data):
        self.data = data

    def extract(self) -> list[dict]:
        return self.data

extractor = CSVExtractor([{"id": 1, "val": 10}, {"id": 2, "val": 20}])
print("extracted:", extractor.extract())

# Verify abstract enforcement
try:
    bad = BaseExtractor()
except TypeError as e:
    print(f"Cannot instantiate ABC: {e}")
```

---

## File I/O & Serialization

```python
import json
import csv
import os
from pathlib import Path

# Write & Read text
with open("demo.txt", "w") as f:
    f.write("Line 1\nLine 2\nLine 3\n")
with open("demo.txt") as f:
    content = f.read()
print("text:", repr(content))

# Large file — line-by-line (memory safe)
with open("demo.txt") as f:
    for line in f:
        print(f"  line: {line.strip()}")

# JSON
data = {"pipeline": "etl", "records": 1500, "success": True}
json_str = json.dumps(data, indent=2, default=str)
print("\nJSON:", json_str)
parsed = json.loads(json_str)
print("parsed:", parsed)

with open("demo.json", "w") as f:
    json.dump(data, f, indent=2)
with open("demo.json") as f:
    loaded = json.load(f)
print("loaded:", loaded)

# CSV
rows = [{"id": 1, "name": "Alice", "score": 95},
        {"id": 2, "name": "Bob", "score": 87}]
with open("demo.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "score"])
    writer.writeheader()
    writer.writerows(rows)
with open("demo.csv") as f:
    for row in csv.DictReader(f):
        print(f"  csv: {row}")

# pathlib — modern paths
p = Path("demo.csv")
print(f"\nexists: {p.exists()}, stem: {p.stem}, suffix: {p.suffix}")
print("glob:", list(Path(".").glob("demo*")))

# Cleanup
for f in ["demo.txt", "demo.json", "demo.csv"]:
    Path(f).unlink(missing_ok=True)
```

---

## Error Handling & Logging

```python
import json
import logging

# === Exception Handling ===
x = 2
raw = '{"key": "value"}'

try:
    result = 10 / x
    data = json.loads(raw)
except ZeroDivisionError:
    print("Can't divide by zero")
except (ValueError, KeyError) as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected: {e}")
    raise
else:
    print(f"Success! result={result}, data={data}")
finally:
    print("Finally always runs\n")

# Custom pipeline exceptions
class PipelineError(Exception):
    def __init__(self, stage, message):
        super().__init__(f"[{stage}] {message}")
        self.stage = stage

class ExtractionError(PipelineError): pass
class TransformError(PipelineError): pass

try:
    raise ExtractionError("extract", "Connection refused")
except PipelineError as e:
    print(f"Caught: {e}, stage={e.stage}\n")

# Context manager
from contextlib import contextmanager

@contextmanager
def db_transaction(name):
    print(f"  BEGIN {name}")
    try:
        yield name
        print(f"  COMMIT {name}")
    except Exception:
        print(f"  ROLLBACK {name}")
        raise

with db_transaction("insert_users") as tx:
    print(f"  Executing in {tx}")

# === Logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("etl.demo")
logger.info("Pipeline started, source=%s", "s3://bucket")
logger.warning("Skipped %d malformed records", 42)
logger.info("Pipeline complete")
```

---

## SQL & Databases

### SQLite (Built-in)

```python
import sqlite3

# Create in-memory database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Parameterized inserts (NEVER use f-strings for SQL!)
cur.execute("INSERT INTO events (name, value) VALUES (?, ?)", ("temperature", 23.5))
cur.execute("INSERT INTO events (name, value) VALUES (?, ?)", ("humidity", 65.2))

# Bulk insert
batch = [("pressure", 1013.25), ("wind_speed", 12.3), ("temperature", 24.1)]
cur.executemany("INSERT INTO events (name, value) VALUES (?, ?)", batch)
conn.commit()

# Query
rows = cur.execute("SELECT * FROM events WHERE value > ?", (20,)).fetchall()
for row in rows:
    print(f"  id={row['id']}, name={row['name']}, value={row['value']}")

print(f"\nTotal rows: {cur.execute('SELECT COUNT(*) FROM events').fetchone()[0]}")

# Aggregation
for row in cur.execute("SELECT name, AVG(value) as avg_val FROM events GROUP BY name"):
    print(f"  {row['name']}: avg={row['avg_val']:.2f}")

conn.close()
```

### SQLite + Pandas

```python
import sqlite3
import pandas as pd
import numpy as np

# Create demo database
conn = sqlite3.connect(":memory:")
np.random.seed(42)

# Create and populate tables
df_users = pd.DataFrame({
    "user_id": range(1, 6),
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
})
df_orders = pd.DataFrame({
    "order_id": range(1, 11),
    "user_id": np.random.choice(range(1, 6), 10),
    "amount": np.random.uniform(10, 500, 10).round(2),
    "date": pd.date_range("2024-01-01", periods=10).astype(str),
})

df_users.to_sql("users", conn, index=False)
df_orders.to_sql("orders", conn, index=False)

# Read with Pandas
result = pd.read_sql("""
    SELECT u.name, u.city, COUNT(o.order_id) as order_count, SUM(o.amount) as total
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.name, u.city
    ORDER BY total DESC
""", conn)
print(result)

# Write processed data back to SQL
result.to_sql("user_summary", conn, index=False, if_exists="replace")
print("\nSaved summary back to DB:")
print(pd.read_sql("SELECT * FROM user_summary", conn))

conn.close()
```

---

## Pandas for Data Engineering

### DataFrames — Create & Inspect

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "id": range(1, 8),
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace"],
    "age": [30, 25, 35, 28, 32, 22, 45],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA", "NYC", "Chicago"],
    "revenue": np.random.uniform(500, 3000, 7).round(2),
    "status": ["active", "active", "inactive", "active", "pending", "active", "active"],
})

print(df)
print(f"\nShape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nInfo:")
df.info()
print(f"\nDescribe:\n{df.describe()}")
print(f"\nMemory usage:\n{df.memory_usage(deep=True)}")
print(f"\nNull counts:\n{df.isnull().sum()}")
print(f"\nUnique counts:\n{df.nunique()}")
```

### Select, Filter & Transform

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "age": [30, 25, 35, 28, 32, 22],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA", "NYC"],
    "score": [85.5, 92.3, 78.1, 95.0, 88.7, 70.2],
    "date_str": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05", "2024-05-12", "2024-06-01"],
    "raw_cat": ["A", "B", "A", "C", "B", "A"],
})

# Selecting
print("Single column:\n", df["name"].head(3).to_list())
print("Multi column:\n", df[["name", "age"]].head(3))
print("loc:\n", df.loc[0:2, "name"])
print("iloc:\n", df.iloc[0:3, 0:2])

# Filtering
print("\nage > 28:\n", df[df["age"] > 28]["name"].to_list())
print("isin:\n", df[df["status" if "status" in df.columns else "city"].isin(["NYC"])]["name"].to_list())
print("query:\n", df.query("age > 25 and city == 'NYC'")[["name", "age"]])

# Sorting
print("\nsorted by score desc:")
print(df.sort_values("score", ascending=False)[["name", "score"]])
print("\ntop 3 scores:")
print(df.nlargest(3, "score")[["name", "score"]])

# New columns & transforms
df["name_lower"] = df["name"].str.lower().str.strip()
df["flag"] = np.where(df["score"] > 85, 1, 0)
df["date"] = pd.to_datetime(df["date_str"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["category"] = df["raw_cat"].map({"A": "alpha", "B": "beta", "C": "gamma"})

print("\nTransformed:")
print(df[["name_lower", "flag", "date", "year", "category"]])
```

### GroupBy, Merge, Clean & Export

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA", "NYC"],
    "dept": ["Eng", "Mkt", "Eng", "Sales", "Mkt", "Eng"],
    "revenue": [1200, 1800, 950, 2100, 1600, 1100],
    "salary": [90000, 75000, 95000, 80000, 72000, 88000],
    "region": ["East", "West", "East", "Central", "West", "East"],
    "quarter": ["Q1", "Q1", "Q2", "Q2", "Q1", "Q2"],
    "sales": [100, 150, 120, 200, 130, 110],
})

# GroupBy
print("=== GroupBy ===")
print(df.groupby("city")["revenue"].agg(["sum", "mean", "count"]))

# Transform (broadcast back)
df["dept_avg_salary"] = df.groupby("dept")["salary"].transform("mean")
print("\nTransform:\n", df[["name", "dept", "salary", "dept_avg_salary"]])

# Pivot table
print("\n=== Pivot Table ===")
print(pd.pivot_table(df, values="sales", index="region", columns="quarter", aggfunc="sum"))

# Merge / Join
df1 = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
df2 = pd.DataFrame({"id": [2, 3, 4], "score": [85, 92, 78]})
print("\n=== Merge (left) ===")
print(pd.merge(df1, df2, on="id", how="left"))

# Concat
df_a = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
df_b = pd.DataFrame({"x": [5, 6], "y": [7, 8]})
print("\n=== Concat ===")
print(pd.concat([df_a, df_b], ignore_index=True))

# Cleaning
dirty = pd.DataFrame({
    "id": [1, 2, 3, 1, 4],
    "name": ["Alice", None, "Charlie", "Alice", "Eve"],
    "score": [85, 92, None, 85, 78],
})
print("\n=== Cleaning ===")
print("dropna:", dirty.dropna(subset=["name"]).shape)
print("fillna:\n", dirty.fillna({"score": 0, "name": "unknown"}))
print("dedup:\n", dirty.drop_duplicates(subset=["id"], keep="last"))
print("rename:\n", dirty.rename(columns={"id": "user_id"}).columns.tolist())

# Chunked reading demo
df.to_csv("demo_big.csv", index=False)
print("\n=== Chunked Reading ===")
for i, chunk in enumerate(pd.read_csv("demo_big.csv", chunksize=3)):
    print(f"  Chunk {i}: {len(chunk)} rows — {chunk['name'].tolist()}")

# Export formats
df.to_csv("demo_out.csv", index=False)
df.to_json("demo_out.jsonl", orient="records", lines=True)
print("\nExported CSV and JSONL")

import os
for f in ["demo_big.csv", "demo_out.csv", "demo_out.jsonl"]:
    os.remove(f)
```

---

## ETL Patterns

### ETL Pipeline Class

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("etl")

# Sample source data
SOURCE_DATA = [
    {"id": 1, "name": "  Alice ", "value": "100"},
    {"id": 2, "name": "Bob", "value": "invalid"},
    {"id": 3, "name": " Charlie", "value": "200"},
    {"id": 4, "name": "", "value": "150"},
    {"id": 5, "name": "Eve", "value": "300"},
]

LOADED_DATA = []  # simulated destination

class ETLPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.stats = {"extracted": 0, "transformed": 0, "loaded": 0, "errors": 0}

    def extract(self) -> list[dict]:
        logger.info("Extracting from %s", self.config["source"])
        raw = self.config.get("_data", [])  # use injected data for demo
        self.stats["extracted"] = len(raw)
        return raw

    def transform(self, raw: list[dict]) -> list[dict]:
        cleaned = []
        for record in raw:
            try:
                name = record.get("name", "").strip()
                if not name:
                    raise ValueError("Empty name")
                cleaned.append({
                    "id": record["id"],
                    "name": name.lower(),
                    "value": float(record.get("value", 0)),
                    "processed_at": datetime.utcnow().isoformat(),
                })
            except (KeyError, ValueError) as e:
                self.stats["errors"] += 1
                logger.warning("Bad record id=%s: %s", record.get("id"), e)
        self.stats["transformed"] = len(cleaned)
        return cleaned

    def load(self, data: list[dict]):
        logger.info("Loading %d records to %s", len(data), self.config["destination"])
        LOADED_DATA.extend(data)  # simulated bulk insert
        self.stats["loaded"] = len(data)

    def run(self):
        raw = self.extract()
        clean = self.transform(raw)
        self.load(clean)
        logger.info("Pipeline complete: %s", self.stats)
        return self.stats

# Run it!
config = {
    "source": "api://demo",
    "destination": "postgres://warehouse",
    "_data": SOURCE_DATA,
}
pipeline = ETLPipeline(config)
stats = pipeline.run()
print(f"\nResults: {stats}")
print(f"Loaded records: {LOADED_DATA}")
```

### Batching & Dead Letter Queue

```python
import json
from itertools import islice
from pathlib import Path

def batched(iterable, n):
    """Yield successive batches from iterable."""
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            break
        yield batch

# Demo: process records in batches
records = list(range(1, 14))
for i, batch in enumerate(batched(records, batch_size := 5)):
    print(f"  Batch {i}: {batch}")

# Dead Letter Queue pattern
def process_with_dlq(records, processor, dlq_path="dlq_demo.jsonl"):
    """Process records; write failures to dead letter queue."""
    success, failed = 0, 0
    with open(dlq_path, "w") as dlq:
        for record in records:
            try:
                processor(record)
                success += 1
            except Exception as e:
                failed += 1
                dlq.write(json.dumps({
                    "record": record,
                    "error": str(e),
                }) + "\n")
    print(f"  Processed: {success} success, {failed} failed")
    return success, failed

# Simulated processor that fails on negative values
def transform_record(record):
    if record["value"] < 0:
        raise ValueError(f"Negative value: {record['value']}")
    return record

sample_records = [
    {"id": 1, "value": 100},
    {"id": 2, "value": -50},
    {"id": 3, "value": 200},
    {"id": 4, "value": -10},
    {"id": 5, "value": 300},
]

print("=== Dead Letter Queue ===")
process_with_dlq(sample_records, transform_record)

# Show DLQ contents
print("\nDLQ contents:")
with open("dlq_demo.jsonl") as f:
    for line in f:
        print(f"  {json.loads(line)}")

Path("dlq_demo.jsonl").unlink()
```

---

## Cloud & Object Storage (Simulated)

```python
"""
Simulated AWS S3 / GCS operations.
Install real libraries with: pip install boto3 / google-cloud-storage

Below is the real code pattern — runs as documentation/reference.
Uncomment and configure to use with real credentials.
"""

import io
import json
import pandas as pd
import numpy as np

# === Simulated S3-like operations ===

# In-memory "bucket" for demo
fake_s3 = {}

def s3_put(bucket, key, data):
    fake_s3[f"{bucket}/{key}"] = data
    print(f"  Uploaded: s3://{bucket}/{key} ({len(data)} bytes)")

def s3_get(bucket, key):
    return fake_s3[f"{bucket}/{key}"]

def s3_list(bucket, prefix=""):
    return [k for k in fake_s3 if k.startswith(f"{bucket}/{prefix}")]

# Demo: write DataFrame to "S3"
np.random.seed(42)
df = pd.DataFrame({"id": range(5), "value": np.random.randn(5).round(3)})
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)
s3_put("my-bucket", "data/output.csv", csv_buffer.getvalue())

# Demo: read it back
content = s3_get("my-bucket", "data/output.csv")
df_loaded = pd.read_csv(io.StringIO(content))
print("\nLoaded from 'S3':")
print(df_loaded)

# List objects
print("\nObjects:", s3_list("my-bucket", "data/"))

# --- Real boto3 code (reference) ---
# import boto3
# s3 = boto3.client("s3")
# s3.upload_file("local.csv", "my-bucket", "data/file.csv")
# obj = s3.get_object(Bucket="my-bucket", Key="data/file.csv")
# df = pd.read_csv(io.BytesIO(obj["Body"].read()))
```

---

## API Interaction (Simulated)

```python
"""
Simulated HTTP requests for Jupyter demo.
Install real library: pip install requests

The patterns below work with `requests` — swap fake_api for real URLs.
"""

import json
import time

# === Simulated API ===
FAKE_DB = [{"id": i, "name": f"user_{i}", "score": i*10} for i in range(1, 26)]

def fake_api_get(url, params=None):
    """Simulate a paginated API response."""
    params = params or {}
    page = params.get("page", 1)
    limit = params.get("limit", 10)
    start = (page - 1) * limit
    data = FAKE_DB[start:start+limit]
    return {"status": 200, "data": data, "page": page}

# Paginated extraction
def extract_all(base_url, page_size=10):
    all_records = []
    page = 1
    while True:
        resp = fake_api_get(base_url, params={"page": page, "limit": page_size})
        batch = resp["data"]
        if not batch:
            break
        all_records.extend(batch)
        print(f"  Page {page}: fetched {len(batch)} records")
        page += 1
    return all_records

print("=== Paginated API Extraction ===")
all_data = extract_all("https://api.example.com/users", page_size=10)
print(f"Total extracted: {len(all_data)} records")
print(f"First: {all_data[0]}")
print(f"Last:  {all_data[-1]}")

# --- Real requests code (reference) ---
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
#
# session = requests.Session()
# retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503])
# session.mount("https://", HTTPAdapter(max_retries=retries))
# resp = session.get("https://api.example.com/data",
#     params={"page": 1}, headers={"Authorization": "Bearer TOKEN"}, timeout=30)
# resp.raise_for_status()
# data = resp.json()
```

---

## Concurrency & Parallelism

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import asyncio

# === ThreadPoolExecutor — I/O-bound ===
def fetch_url(url):
    """Simulate an API call with a small delay."""
    time.sleep(0.05)  # simulate network latency
    return {"url": url, "status": 200, "size": len(url) * 100}

urls = [f"https://api.example.com/page/{i}" for i in range(10)]

print("=== Threading (I/O-bound) ===")
t0 = time.perf_counter()
results = []
with ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(fetch_url, url): url for url in urls}
    for future in as_completed(futures):
        results.append(future.result())
print(f"  Fetched {len(results)} URLs in {time.perf_counter()-t0:.3f}s (parallel)")

t0 = time.perf_counter()
sequential = [fetch_url(url) for url in urls]
print(f"  Fetched {len(sequential)} URLs in {time.perf_counter()-t0:.3f}s (sequential)")

# === ProcessPoolExecutor — CPU-bound ===
def heavy_compute(n):
    """Simulate CPU-intensive work."""
    return sum(i*i for i in range(n))

print("\n=== Multiprocessing (CPU-bound) ===")
chunks = [100_000] * 8
t0 = time.perf_counter()
with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(heavy_compute, chunks))
print(f"  Processed {len(results)} chunks in {time.perf_counter()-t0:.3f}s")

# === asyncio — high-concurrency I/O ===
async def async_fetch(url, delay=0.05):
    await asyncio.sleep(delay)  # simulate I/O
    return {"url": url, "status": 200}

async def main():
    tasks = [async_fetch(f"https://api.example.com/p/{i}") for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"  Async fetched: {len(results)} results")

print("\n=== Asyncio ===")
await main()  # In Jupyter, use `await` directly. In scripts, use: asyncio.run(main())
```

---

## Data Validation & Quality

```python
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("dq")

# === Schema validation (manual Pydantic-style) ===
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventRecord:
    event_id: str
    timestamp: str
    value: float
    source: str

    def __post_init__(self):
        if not self.event_id:
            raise ValueError("event_id cannot be empty")
        if self.value < 0:
            raise ValueError(f"value must be >= 0, got {self.value}")
        datetime.fromisoformat(self.timestamp)  # validate timestamp

# Validate batch
def validate_batch(records):
    valid, invalid = [], []
    for r in records:
        try:
            evt = EventRecord(**r)
            valid.append({"event_id": evt.event_id, "timestamp": evt.timestamp,
                          "value": evt.value, "source": evt.source})
        except Exception as e:
            invalid.append({"record": r, "error": str(e)})
    return valid, invalid

sample = [
    {"event_id": "evt-001", "timestamp": "2024-06-15T10:30:00", "value": 42.5, "source": "sensor_a"},
    {"event_id": "", "timestamp": "2024-06-15T10:31:00", "value": 10.0, "source": "sensor_b"},
    {"event_id": "evt-003", "timestamp": "2024-06-15T10:32:00", "value": -5.0, "source": "sensor_c"},
    {"event_id": "evt-004", "timestamp": "bad-date", "value": 20.0, "source": "sensor_a"},
    {"event_id": "evt-005", "timestamp": "2024-06-15T10:34:00", "value": 99.9, "source": "sensor_b"},
]

valid, invalid = validate_batch(sample)
print(f"=== Validation: {len(valid)} valid, {len(invalid)} invalid ===")
for v in valid:
    print(f"  ✓ {v['event_id']}: {v['value']}")
for inv in invalid:
    print(f"  ✗ {inv['record'].get('event_id', '???')}: {inv['error']}")

# === Data quality checks on DataFrame ===
np.random.seed(42)
df = pd.DataFrame({
    "id": list(range(1, 201)),
    "value": np.random.uniform(-5, 100, 200),
    "date": pd.date_range("2024-01-01", periods=200).astype(str),
})
df.loc[5, "id"] = None  # inject a null
df.loc[10, "value"] = -999  # inject a bad value

def data_quality_checks(df):
    checks = {
        "no_nulls_in_id":    df["id"].notnull().all(),
        "positive_values":   (df["value"] >= 0).all(),
        "unique_ids":        df["id"].dropna().is_unique,
        "row_count_min":     len(df) >= 100,
        "valid_dates":       pd.to_datetime(df["date"]).between("2020-01-01", "2030-01-01").all(),
    }
    print("\n=== DQ Checks ===")
    for name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
    return all(checks.values())

all_passed = data_quality_checks(df)
print(f"\nAll checks passed: {all_passed}")
```

---

## Environment & Configuration

```python
import os
from dataclasses import dataclass

# Set demo environment variables (in production, these come from .env or the OS)
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "mydb"
os.environ["BATCH_SIZE"] = "5000"
os.environ["DEBUG"] = "true"

# Reading env vars
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
print(f"DB_HOST={DB_HOST}, DB_PORT={DB_PORT}, DEBUG={DEBUG}")

# Config class pattern
@dataclass
class Config:
    db_host: str = os.environ.get("DB_HOST", "localhost")
    db_port: int = int(os.environ.get("DB_PORT", "5432"))
    db_name: str = os.environ.get("DB_NAME", "mydb")
    batch_size: int = int(os.environ.get("BATCH_SIZE", "5000"))
    debug: bool = os.environ.get("DEBUG", "false").lower() == "true"

    @property
    def db_url(self):
        return f"postgresql://{self.db_host}:{self.db_port}/{self.db_name}"

config = Config()
print(f"\nConfig: {config}")
print(f"DB URL: {config.db_url}")

# Cleanup
for key in ["DB_HOST", "DB_PORT", "DB_NAME", "BATCH_SIZE", "DEBUG"]:
    os.environ.pop(key, None)
```

---

## Pro Tips & Patterns

### Built-in Superpowers

```python
# enumerate — index + value
items = ["apple", "banana", "cherry"]
for i, val in enumerate(items, start=1):
    print(f"{i}. {val}")

# zip — parallel iteration & dict creation
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")
print("zip → dict:", dict(zip(names, scores)))

# any / all — quick checks
records = [{"status": "ok"}, {"status": "error"}, {"status": "ok"}]
print(f"any errors: {any(r['status'] == 'error' for r in records)}")
print(f"all have id: {all(r.get('id') for r in records)}")

# sorted with key
from pathlib import Path
files = [Path("a.csv"), Path("bb.json"), Path("ccc.txt")]
print("sorted by name length:", sorted(files, key=lambda f: len(f.name), reverse=True))

# collections
from collections import Counter, deque
print("\nCounter:", Counter("banana").most_common(2))

# itertools
from itertools import chain, islice
print("chain:", list(chain([1, 2], [3, 4], [5])))

# First 5 from a generator
gen = (x**2 for x in range(1000))
print("islice:", list(islice(gen, 5)))
```

### One-Liners & Tricks

```python
# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6, 7]]
flat = [x for sub in nested for x in sub]
print("flatten:", flat)

# Remove duplicates, preserve order
lst = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
seen = set()
uniq = [x for x in lst if x not in seen and not seen.add(x)]
print("deduplicated:", uniq)

# Merge dicts (3.9+)
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print("merged:", d1 | d2)

# Safe nested dict access
d = {"a": {"b": {"c": 42}}}
val = d.get("a", {}).get("b", {}).get("c")
print("nested access:", val)

# Timing code
from time import perf_counter
t0 = perf_counter()
total = sum(range(1_000_000))
print(f"sum={total}, time={perf_counter()-t0:.4f}s")

# Regex — extract dates
import re
log_text = "Error at 2024-01-15 and warning at 2024-06-30 12:00:00"
dates = re.findall(r'\d{4}-\d{2}-\d{2}', log_text)
print("dates:", dates)

emails_text = "Contact alice@example.com or bob@test.org"
emails = re.findall(r'\S+@\S+', emails_text)
print("emails:", emails)

# hashlib — checksums for data integrity
import hashlib
data = b"Hello, data pipeline!"
checksum = hashlib.md5(data).hexdigest()
print(f"MD5 checksum: {checksum}")
sha = hashlib.sha256(data).hexdigest()
print(f"SHA256: {sha}")
```

---

## Dunder (Magic) Methods

```python
# Dunders = "double underscore" methods that Python calls implicitly
# They let your classes integrate with Python's built-in operations

class DataBatch:
    """A custom container that demonstrates key dunders."""

    def __init__(self, name, records):
        self.name = name
        self.records = list(records)

    # String representations
    def __repr__(self):
        """For developers — unambiguous. Called by repr() and in REPL."""
        return f"DataBatch(name={self.name!r}, size={len(self.records)})"

    def __str__(self):
        """For users — readable. Called by str() and print()."""
        return f"Batch '{self.name}' ({len(self.records)} records)"

    # Container protocol
    def __len__(self):
        """Called by len()."""
        return len(self.records)

    def __getitem__(self, index):
        """Called by batch[i] — enables indexing and iteration."""
        return self.records[index]

    def __contains__(self, item):
        """Called by 'in' operator."""
        return item in self.records

    def __iter__(self):
        """Called by for loop, list(), etc."""
        return iter(self.records)

    # Comparison
    def __eq__(self, other):
        """Called by ==."""
        return isinstance(other, DataBatch) and self.records == other.records

    def __lt__(self, other):
        """Called by <. Enables sorting."""
        return len(self.records) < len(other.records)

    # Arithmetic — combine batches
    def __add__(self, other):
        """Called by +."""
        return DataBatch(f"{self.name}+{other.name}", self.records + other.records)

    # Context manager protocol
    def __enter__(self):
        """Called on 'with' entry."""
        print(f"  Opening batch '{self.name}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called on 'with' exit."""
        print(f"  Closing batch '{self.name}' (error={exc_type is not None})")
        return False  # don't suppress exceptions

    # Callable
    def __call__(self, transform_fn):
        """Called when instance is used as a function: batch(fn)."""
        return DataBatch(self.name, [transform_fn(r) for r in self.records])

    # Boolean
    def __bool__(self):
        """Called by bool(), if, while."""
        return len(self.records) > 0

    # Hash (needed if used as dict key or in sets)
    def __hash__(self):
        return hash((self.name, tuple(self.records)))

# Demo all dunders
batch1 = DataBatch("users", [{"id": 1}, {"id": 2}, {"id": 3}])
batch2 = DataBatch("orders", [{"oid": 10}, {"oid": 20}])

print(repr(batch1))                    # __repr__
print(str(batch1))                     # __str__
print(f"len: {len(batch1)}")           # __len__
print(f"batch1[0]: {batch1[0]}")       # __getitem__
print(f"contains: {{'id': 1} in batch1}: {{'id': 1} in batch1}")  # __contains__
print(f"bool(batch1): {bool(batch1)}") # __bool__

# Iteration (__iter__)
for rec in batch1:
    print(f"  iterating: {rec}")

# Arithmetic (__add__)
combined = batch1 + batch2
print(f"combined: {combined}")

# Sorting (__lt__)
batches = [combined, batch2, batch1]
print(f"sorted sizes: {[len(b) for b in sorted(batches)]}")

# Callable (__call__)
upper_batch = DataBatch("names", ["alice", "bob"])
result = upper_batch(str.upper)
print(f"callable result: {list(result)}")

# Context manager (__enter__ / __exit__)
with batch1 as b:
    print(f"  working with {len(b)} records")
```

```python
# Other important dunders — quick reference

class SmartRecord:
    def __init__(self, data):
        self._data = data

    # Attribute access
    def __getattr__(self, name):
        """Called when normal attribute lookup fails."""
        return self._data.get(name, f"<no {name}>")

    # Dict-like access
    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    # Format
    def __format__(self, spec):
        """Called by f-strings and format()."""
        if spec == "short":
            return str(list(self._data.keys()))
        return str(self._data)

    def __sizeof__(self):
        """Called by sys.getsizeof()."""
        import sys
        return sys.getsizeof(self._data)

r = SmartRecord({"name": "Alice", "age": 30})
print(r.name)              # __getattr__ → "Alice"
print(r.email)             # __getattr__ → "<no email>"
r["city"] = "NYC"          # __setitem__
print(f"{r:short}")        # __format__
print(f"{r}")              # __format__ (default)

# __slots__ — memory optimization (no __dict__)
class OptimizedRecord:
    __slots__ = ["id", "value"]  # only these attributes allowed
    def __init__(self, id, value):
        self.id = id
        self.value = value

rec = OptimizedRecord(1, 42)
print(f"slots: id={rec.id}, value={rec.value}")
try:
    rec.extra = "nope"
except AttributeError as e:
    print(f"__slots__ prevents: {e}")
```

---

## Common Python Interview Questions (Data Engineering)

```python
# === Q1: Difference between list, tuple, and set? ===
# List: ordered, mutable, allows duplicates, uses []
# Tuple: ordered, immutable, allows duplicates, uses ()
# Set: unordered, mutable, NO duplicates, uses {}

lst = [1, 2, 2, 3]      # duplicates OK
tup = (1, 2, 2, 3)      # duplicates OK, immutable
st  = {1, 2, 2, 3}      # duplicates removed → {1, 2, 3}
print(f"list={lst}, tuple={tup}, set={st}")


# === Q2: Deep copy vs shallow copy ===
import copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)       # new list, same inner lists
deep = copy.deepcopy(original)      # new list, new inner lists

original[0].append(99)
print(f"original: {original}")
print(f"shallow (affected): {shallow}")
print(f"deep (not affected): {deep}")


# === Q3: What is a generator? Why use it? ===
# Generators yield values lazily — one at a time — saving memory.
# Critical for processing large files/streams that don't fit in memory.
def read_large_file(lines):
    for line in lines:
        yield line.strip().upper()

data = ["  hello  ", "  world  ", "  python  "]
for processed in read_large_file(data):
    print(f"  gen: {processed}")

# Memory comparison
import sys
list_comp = [x**2 for x in range(10000)]
gen_exp   = (x**2 for x in range(10000))
print(f"list size: {sys.getsizeof(list_comp):,} bytes")
print(f"gen size:  {sys.getsizeof(gen_exp):,} bytes")


# === Q4: *args vs **kwargs ===
def example(*args, **kwargs):
    print(f"positional: {args}, keyword: {kwargs}")

example(1, 2, 3, x=10, y=20)

# Unpacking into function calls
def add(a, b, c):
    return a + b + c

print(add(*[1, 2, 3]))           # unpack list
print(add(**{"a": 1, "b": 2, "c": 3}))  # unpack dict


# === Q5: GIL (Global Interpreter Lock) ===
# The GIL allows only one thread to execute Python bytecode at a time.
# Impact: threading does NOT speed up CPU-bound work.
# Solutions:
#   - CPU-bound → use multiprocessing (separate processes, separate GILs)
#   - I/O-bound → threading or asyncio works fine (GIL released during I/O)
print("GIL: use multiprocessing for CPU, threading/asyncio for I/O")


# === Q6: Mutable default argument trap ===
def bad_append(item, lst=[]):     # BUG: default list shared across calls!
    lst.append(item)
    return lst

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] — unexpected!

def good_append(item, lst=None):  # FIX: use None as sentinel
    lst = lst or []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2] — correct!


# === Q7: What does `if __name__ == "__main__"` do? ===
# It ensures code runs only when the file is executed directly,
# not when imported as a module.
# __name__ == "__main__" when running the script directly
# __name__ == "module_name" when imported
print(f"__name__ = {__name__}")


# === Q8: How do you handle large datasets in Python? ===
# 1. Generators / iterators — process row by row
# 2. pandas chunked reading — pd.read_csv(..., chunksize=10000)
# 3. Use columnar formats — Parquet, ORC (read only needed columns)
# 4. Use Dask or PySpark for distributed processing
# 5. Optimize dtypes — category, int32 vs int64
import pandas as pd
import numpy as np
df = pd.DataFrame({"status": np.random.choice(["A", "B", "C"], 10000)})
print(f"object dtype:   {df['status'].memory_usage(deep=True):,} bytes")
df["status"] = df["status"].astype("category")
print(f"category dtype: {df['status'].memory_usage(deep=True):,} bytes")


# === Q9: Difference between == and 'is'? ===
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(f"a == b: {a == b}")   # True — same VALUE
print(f"a is b: {a is b}")   # False — different OBJECTS
print(f"a is c: {a is c}")   # True — same object (alias)
# Use 'is' only for None, True, False: `if x is None`


# === Q10: What are decorators? ===
# A decorator wraps a function to add behavior without modifying its code.
import time
from functools import wraps

def log_calls(func):
    @wraps(func)  # preserves original function's name & docstring
    def wrapper(*args, **kwargs):
        print(f"  Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def multiply(a, b):
    """Multiply two numbers."""
    return a * b

print(multiply(3, 4))
print(f"name preserved: {multiply.__name__}")
print(f"docstring preserved: {multiply.__doc__}")


# === Q11: List comprehension vs map/filter ===
nums = [1, 2, 3, 4, 5]

# Comprehension (preferred — more Pythonic & readable)
squares = [x**2 for x in nums if x > 2]

# map/filter equivalent
squares2 = list(map(lambda x: x**2, filter(lambda x: x > 2, nums)))

print(f"comprehension: {squares}")
print(f"map/filter:    {squares2}")


# === Q12: Explain Python's method resolution order (MRO) ===
class A:
    def who(self): return "A"

class B(A):
    def who(self): return "B"

class C(A):
    def who(self): return "C"

class D(B, C):
    pass

d = D()
print(f"MRO: {[cls.__name__ for cls in D.__mro__]}")
print(f"d.who() = {d.who()}")  # "B" — follows MRO: D → B → C → A
```

---

## Quick Reference Table

| Operation | Syntax | Note |
|---|---|---|
| Virtual env | `python -m venv .venv && source .venv/bin/activate` | Isolate deps |
| Install pkg | `pip install -r requirements.txt` | Pin versions |
| Debugger | `breakpoint()` | Built-in (3.7+) |
| Profile | `python -m cProfile -s cumtime script.py` | Find bottlenecks |
| Type check | `mypy script.py` | Static analysis |
| Format | `black . && ruff check .` | Auto-format & lint |
| Docker run | `docker build -t etl . && docker run etl` | Containerize |
| Env vars | `export DB_HOST=localhost` | Set for session |
| Parquet | `df.to_parquet("f.parquet", compression="snappy")` | Columnar storage |
| JSONL | `df.to_json("f.jsonl", orient="records", lines=True)` | Line-delimited |

---

*Python Cheatsheet — Developer & Data Engineering Edition — Jupyter-Ready ✅*
