# Python Cheatsheet
### For Python Developers & Data Engineers

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
type(x)              # <class 'int'>
isinstance(x, int)   # True
int("42")  /  str(3.14)  /  float("2.7")

# Multiple assignment & swap
a, b, c = 1, 2, 3
a, b = b, a
```

### Control Flow

```python
# Conditionals
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary
label = "even" if x % 2 == 0 else "odd"

# Loops
for i in range(5):          # 0,1,2,3,4
for i in range(2, 10, 2):   # 2,4,6,8
for k, v in d.items():      # dict iteration

# While with break/continue
while True:
    data = fetch()
    if not data: break
    if skip(data): continue
    process(data)

# Match statement (3.10+)
match status_code:
    case 200:
        handle_ok()
    case 404:
        handle_not_found()
    case _:
        handle_error()
```

---

## Strings

```python
s = "Hello, World!"

# Slicing
s[0:5]        # "Hello"
s[::-1]       # "!dlroW ,olleH" (reverse)

# Key methods
s.lower() / s.upper() / s.title() / s.strip()
s.split(",")          # ["Hello", " World!"]
"-".join(["a","b"])   # "a-b"
s.replace("World", "Python")
s.startswith("He") / s.endswith("!")
s.find("World")       # 7 (-1 if not found)
s.count("l")          # 3
s.isdigit() / s.isalpha() / s.isalnum()
s.encode("utf-8")     # bytes (important for data pipelines)

# f-strings (Python 3.6+)
name, age = "Alice", 30
f"{name} is {age} years old"
f"{3.14159:.2f}"         # "3.14"
f"{1000000:,}"           # "1,000,000"
f"{'hi':>10}"            # "        hi"
f"{x = }"                # "x = 42" (debug, 3.8+)

# Raw strings (useful for regex & Windows paths)
path = r"C:\data\files\output"
pattern = r"\d{4}-\d{2}-\d{2}"
```

---

## Data Structures

### Lists

```python
lst = [1, 2, 3, 4, 5]

# CRUD
lst.append(6)          # [1,2,3,4,5,6]
lst.insert(0, 0)       # insert at position
lst.extend([7, 8])     # append multiple
lst.pop()              # remove & return last
lst.pop(0)             # remove & return first
lst.remove(3)          # remove first occurrence
del lst[1:3]           # remove slice

# Searching & Sorting
3 in lst               # True
lst.index(3)           # first index of 3
lst.sort()             # in-place sort
lst.sort(key=lambda x: -x)
sorted(lst)            # returns new list

# Slicing
lst[1:4]     # [2,3,4]
lst[::2]     # every 2nd item
lst[::-1]    # reversed copy

# Unpacking
first, *rest = lst
a, b, *_ = lst
```

### Dictionaries

```python
d = {"name": "Alice", "age": 30}

d["name"]                 # "Alice"
d.get("email", "N/A")    # safe access
d["city"] = "NYC"         # add/update
d.update({"age": 31})     # merge
d | {"x": 1}              # merge (3.9+)
d.pop("age")              # remove & return
d.setdefault("k", [])     # get or set default

d.keys() / d.values() / d.items()

# Useful patterns for data engineering
from collections import defaultdict, OrderedDict
dd = defaultdict(list)
dd["key"].append(1)       # no KeyError!
```

### Sets & Tuples

```python
# Sets — deduplication & lookups
s = {1, 2, 3}
s.add(4) / s.discard(2)
s1 & s2   # intersection
s1 | s2   # union
s1 - s2   # difference

# Tuples — immutable, hashable
t = (1, "a", 3.14)
x, y, z = t           # unpack

# Named tuples — lightweight records
from collections import namedtuple
Record = namedtuple("Record", ["id", "name", "value"])
r = Record(1, "sensor_a", 42.5)
r.name  # "sensor_a"
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

# *args and **kwargs
def flexible(*args, **kwargs):
    print(args)    # tuple
    print(kwargs)  # dict

# Lambda
square = lambda x: x ** 2

# Higher-order functions
list(map(lambda x: x*2, [1,2,3]))      # [2,4,6]
list(filter(lambda x: x>2, [1,2,3]))   # [3]
from functools import reduce
reduce(lambda a, b: a+b, [1,2,3])      # 6

# Type hints (3.5+)
def process(data: list[dict]) -> list[dict]:
    return [clean(row) for row in data]

# Return type with Optional
from typing import Optional
def find_user(user_id: int) -> Optional[dict]:
    return db.get(user_id)
```

### Decorators & Generators

```python
# Decorator — retry logic (common in pipelines)
import time
from functools import wraps

def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

@retry(max_retries=3, delay=2)
def fetch_api_data(url):
    return requests.get(url).json()

# Generator — memory-efficient streaming
def read_in_chunks(file_path, chunk_size=1024):
    with open(file_path, "r") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Generator expression
total = sum(len(line) for line in open("big.txt"))

# Generator pipeline (lazy, memory-safe)
lines  = (line.strip() for line in open("data.csv"))
rows   = (line.split(",") for line in lines)
cleaned = (row for row in rows if len(row) == 5)
```

---

## Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]

# Nested — flatten
flat = [x for row in matrix for x in row]

# Dict comprehension
column_map = {col: col.lower().replace(" ", "_") for col in raw_columns}

# Set comprehension
unique_types = {type(v).__name__ for v in data.values()}

# Conditional expression
labels = ["valid" if is_valid(x) else "invalid" for x in records]

# Walrus operator (3.8+)
results = [cleaned for x in data if (cleaned := clean(x)) is not None]
```

---

## Object-Oriented Programming

```python
# Dataclass (3.7+) — great for data models
from dataclasses import dataclass, field, asdict
from datetime import datetime

@dataclass
class PipelineConfig:
    source: str
    destination: str
    batch_size: int = 1000
    created_at: datetime = field(default_factory=datetime.now)
    tags: list = field(default_factory=list)

config = PipelineConfig("s3://input", "postgres://db")
asdict(config)    # convert to dict

# Pydantic — validation for configs & schemas
from pydantic import BaseModel, validator

class EventSchema(BaseModel):
    event_id: str
    timestamp: datetime
    payload: dict
    source: str = "unknown"

    @validator("event_id")
    def must_be_uuid(cls, v):
        if len(v) != 36:
            raise ValueError("Invalid UUID")
        return v

event = EventSchema.model_validate(raw_json)

# Abstract base class — enforce interface
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> list[dict]:
        pass

    @abstractmethod
    def validate(self, data: list[dict]) -> bool:
        pass
```

---

## File I/O & Serialization

```python
# Read / Write text
with open("file.txt") as f:
    content = f.read()

with open("out.txt", "w") as f:
    f.write("Hello\n")

# Read large files line-by-line (memory safe)
with open("huge_file.csv") as f:
    for line in f:
        process(line.strip())

# JSON
import json
data = json.loads(json_string)
json_string = json.dumps(data, indent=2, default=str)

# Read/write JSON files
with open("config.json") as f:
    config = json.load(f)
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

# CSV
import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)   # {'col1': 'val1', ...}

with open("out.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name"])
    writer.writeheader()
    writer.writerows(records)

# YAML (pip install pyyaml)
import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# pathlib (modern paths)
from pathlib import Path
p = Path("data") / "raw" / "file.csv"
p.exists()  /  p.is_file()  /  p.is_dir()
p.read_text()  /  p.write_text("content")
p.stem  /  p.suffix  /  p.parent
list(Path("data").glob("**/*.csv"))    # recursive glob
p.mkdir(parents=True, exist_ok=True)

# Pickle — serialize Python objects
import pickle
pickle.dump(obj, open("model.pkl", "wb"))
obj = pickle.load(open("model.pkl", "rb"))
```

---

## Error Handling & Logging

### Exception Handling

```python
try:
    result = 10 / x
    data = json.loads(raw)
except ZeroDivisionError:
    print("Can't divide by zero")
except (ValueError, KeyError) as e:
    print(f"Error: {e}")
except Exception as e:
    logger.error(f"Unexpected: {e}", exc_info=True)
    raise
else:
    print("Success!")
finally:
    cleanup()

# Custom exception
class PipelineError(Exception):
    def __init__(self, stage, message, record=None):
        super().__init__(f"[{stage}] {message}")
        self.stage = stage
        self.record = record

class ExtractionError(PipelineError): pass
class TransformError(PipelineError): pass
class LoadError(PipelineError): pass

# Context manager
from contextlib import contextmanager

@contextmanager
def db_transaction(conn):
    try:
        yield conn.cursor()
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### Logging (Production-Grade)

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipeline.log")
    ]
)
logger = logging.getLogger("etl.extract")

logger.info("Starting extraction from %s", source)
logger.warning("Skipped %d malformed records", count)
logger.error("Connection failed", exc_info=True)

# Structured logging (pip install structlog)
import structlog
log = structlog.get_logger()
log.info("record_processed", record_id=123, duration_ms=45)
```

---

## SQL & Databases

### SQLite

```python
import sqlite3

conn = sqlite3.connect("data.db")  # or ":memory:"
conn.row_factory = sqlite3.Row     # dict-like rows
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Parameterized queries (NEVER use f-strings for SQL!)
cur.execute("INSERT INTO events (name, value) VALUES (?, ?)", ("temp", 23.5))
cur.executemany("INSERT INTO events (name, value) VALUES (?, ?)", records)
conn.commit()

# Read
rows = cur.execute("SELECT * FROM events WHERE value > ?", (20,)).fetchall()
conn.close()
```

### SQLAlchemy (ORM & Core)

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Connection
engine = create_engine("postgresql://user:pass@host:5432/db", pool_size=10)

# Raw SQL with params
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM users WHERE age > :age"),
        {"age": 25}
    )
    rows = result.mappings().all()  # list of dicts

# Bulk insert (fast)
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO events (name, value) VALUES (:name, :val)"),
        [{"name": "a", "val": 1}, {"name": "b", "val": 2}]
    )

# Pandas integration
import pandas as pd
df = pd.read_sql("SELECT * FROM events", engine)
df.to_sql("events_clean", engine, if_exists="replace", index=False,
          method="multi", chunksize=5000)
```

### PostgreSQL with psycopg2

```python
import psycopg2
from psycopg2.extras import execute_values, RealDictCursor

conn = psycopg2.connect(
    host="localhost", dbname="mydb", user="user", password="pass"
)
cur = conn.cursor(cursor_factory=RealDictCursor)

# Bulk insert (very fast)
data = [(1, "alice", 100), (2, "bob", 200)]
execute_values(cur,
    "INSERT INTO users (id, name, score) VALUES %s", data)
conn.commit()

# COPY — fastest bulk load
with open("data.csv") as f:
    cur.copy_expert(
        "COPY events FROM STDIN WITH CSV HEADER", f
    )
conn.commit()
```

---

## Pandas for Data Engineering

### DataFrames — Create & Inspect

```python
import pandas as pd

# Read data
df = pd.read_csv("data.csv")
df = pd.read_json("data.json", lines=True)     # JSONL
df = pd.read_parquet("data.parquet")
df = pd.read_sql("SELECT * FROM events", engine)

# Inspect
df.head(10)   /  df.tail()
df.shape      /  df.dtypes
df.info()     /  df.describe()
df.memory_usage(deep=True)     # check RAM usage
df.isnull().sum()
df.nunique()
```

### Select, Filter & Transform

```python
# Selecting
df["col"]               # Series
df[["col1", "col2"]]    # DataFrame
df.loc[0:5, "name"]     # label-based
df.iloc[0:5, 0:2]       # position-based

# Filtering
df[df["age"] > 25]
df[df["status"].isin(["active", "pending"])]
df.query("age > 25 and city == 'NYC'")

# Sorting
df.sort_values("created_at", ascending=False)
df.nlargest(10, "revenue")

# New columns
df["full_name"] = df["first"] + " " + df["last"]
df["flag"] = np.where(df["x"] > 0, 1, 0)
df["date"] = pd.to_datetime(df["date_str"])
df["year"] = df["date"].dt.year

# Apply / Map
df["name"] = df["name"].str.lower().str.strip()
df["category"] = df["raw_cat"].map({"A": "alpha", "B": "beta"})
df["result"] = df.apply(lambda row: compute(row["x"], row["y"]), axis=1)
```

### GroupBy, Merge & Clean

```python
# GroupBy
df.groupby("city")["revenue"].agg(["sum", "mean", "count"])
df.groupby("dept")["salary"].transform("mean")  # broadcast back

# Pivot table
pd.pivot_table(df, values="sales", index="region",
               columns="quarter", aggfunc="sum")

# Merge / Join
pd.merge(df1, df2, on="id", how="left")         # left, right, inner, outer
pd.merge(df1, df2, left_on="uid", right_on="user_id")
pd.concat([df1, df2], ignore_index=True)         # stack vertically

# Cleaning
df.dropna(subset=["required_col"])
df.fillna({"score": 0, "name": "unknown"})
df.drop_duplicates(subset=["id"], keep="last")
df.rename(columns={"old": "new"})
df.astype({"age": int, "name": "string"})

# Chunked reading (large files)
chunks = pd.read_csv("huge.csv", chunksize=100_000)
for chunk in chunks:
    process(chunk)

# Save
df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet", engine="pyarrow", compression="snappy")
df.to_json("out.jsonl", orient="records", lines=True)
```

---

## ETL Patterns

### Extract-Transform-Load Pipeline

```python
import logging
from datetime import datetime

logger = logging.getLogger("etl")

class ETLPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.stats = {"extracted": 0, "transformed": 0, "loaded": 0, "errors": 0}

    def extract(self) -> list[dict]:
        logger.info("Extracting from %s", self.config["source"])
        # API, DB, file, S3, etc.
        raw = fetch_data(self.config["source"])
        self.stats["extracted"] = len(raw)
        return raw

    def transform(self, raw: list[dict]) -> list[dict]:
        cleaned = []
        for record in raw:
            try:
                cleaned.append({
                    "id": record["id"],
                    "name": record["name"].strip().lower(),
                    "value": float(record.get("value", 0)),
                    "processed_at": datetime.utcnow().isoformat()
                })
            except (KeyError, ValueError) as e:
                self.stats["errors"] += 1
                logger.warning("Bad record: %s — %s", record, e)
        self.stats["transformed"] = len(cleaned)
        return cleaned

    def load(self, data: list[dict]):
        logger.info("Loading %d records", len(data))
        bulk_insert(self.config["destination"], data)
        self.stats["loaded"] = len(data)

    def run(self):
        raw = self.extract()
        clean = self.transform(raw)
        self.load(clean)
        logger.info("Pipeline complete: %s", self.stats)
        return self.stats
```

### Batch Processing Pattern

```python
from itertools import islice

def batched(iterable, batch_size):
    """Yield successive batches from iterable."""
    it = iter(iterable)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch

# Usage — process large datasets in batches
for batch in batched(all_records, batch_size=5000):
    transformed = [transform(r) for r in batch]
    bulk_insert(db, transformed)
    logger.info("Loaded batch of %d records", len(transformed))
```

### Dead Letter Queue Pattern

```python
def process_with_dlq(records, processor, dlq_path="dead_letters.jsonl"):
    """Process records; write failures to dead letter queue."""
    success, failed = 0, 0
    with open(dlq_path, "a") as dlq:
        for record in records:
            try:
                processor(record)
                success += 1
            except Exception as e:
                failed += 1
                dlq.write(json.dumps({
                    "record": record,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }) + "\n")
    logger.info("Processed: %d success, %d failed", success, failed)
```

---

## Cloud & Object Storage

### AWS S3 (boto3)

```python
import boto3
from io import BytesIO, StringIO

s3 = boto3.client("s3")

# Upload
s3.upload_file("local.csv", "my-bucket", "data/file.csv")

# Download
s3.download_file("my-bucket", "data/file.csv", "local.csv")

# Read directly into pandas
obj = s3.get_object(Bucket="my-bucket", Key="data/file.csv")
df = pd.read_csv(BytesIO(obj["Body"].read()))

# Or simpler with s3 URI
df = pd.read_parquet("s3://my-bucket/data/file.parquet")

# List objects
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket="my-bucket", Prefix="data/"):
    for obj in page.get("Contents", []):
        print(obj["Key"], obj["Size"])

# Write DataFrame directly to S3
buffer = BytesIO()
df.to_parquet(buffer, engine="pyarrow")
buffer.seek(0)
s3.put_object(Bucket="my-bucket", Key="output/data.parquet", Body=buffer)
```

### Google Cloud Storage

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket("my-bucket")

# Upload
blob = bucket.blob("data/file.csv")
blob.upload_from_filename("local.csv")

# Download
blob.download_to_filename("local.csv")

# Read into pandas
df = pd.read_csv(f"gs://my-bucket/data/file.csv")
```

---

## Apache Spark (PySpark)

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Session
spark = SparkSession.builder \
    .appName("ETL") \
    .config("spark.sql.shuffle.partitions", 200) \
    .getOrCreate()

# Read
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.parquet("s3://bucket/data/")
df = spark.read.json("events.jsonl")

# Schema definition
schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), True),
])
df = spark.read.csv("data.csv", schema=schema, header=True)

# Transform
df = df.filter(F.col("age") > 25)
df = df.withColumn("name_lower", F.lower(F.col("name")))
df = df.withColumn("year", F.year(F.col("date")))
df = df.dropDuplicates(["id"])
df = df.fillna({"score": 0})

# GroupBy
summary = df.groupBy("city").agg(
    F.count("*").alias("count"),
    F.avg("salary").alias("avg_salary"),
    F.max("salary").alias("max_salary")
)

# Join
result = df1.join(df2, on="user_id", how="left")

# Window functions
from pyspark.sql.window import Window
w = Window.partitionBy("dept").orderBy(F.desc("salary"))
df = df.withColumn("rank", F.row_number().over(w))

# Write
df.write.parquet("output/", mode="overwrite", partitionBy=["year", "month"])
df.write.mode("append").saveAsTable("db.events_clean")

# SQL interface
df.createOrReplaceTempView("events")
result = spark.sql("""
    SELECT city, COUNT(*) as cnt
    FROM events
    WHERE date >= '2024-01-01'
    GROUP BY city
    ORDER BY cnt DESC
""")
```

---

## Scheduling & Orchestration

### Apache Airflow (DAG Basics)

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-eng",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}

with DAG(
    dag_id="daily_etl",
    default_args=default_args,
    schedule_interval="0 6 * * *",       # 6 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "production"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_from_api,
        op_kwargs={"endpoint": "/events"},
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_to_warehouse,
    )

    extract >> transform >> load
```

### Cron Expressions Quick Reference

| Expression | Schedule |
|---|---|
| `0 * * * *` | Every hour |
| `0 6 * * *` | Daily at 6 AM |
| `0 0 * * 0` | Weekly on Sunday |
| `0 0 1 * *` | Monthly on the 1st |
| `*/15 * * * *` | Every 15 minutes |
| `0 6 * * 1-5` | Weekdays at 6 AM |

---

## API Interaction & Requests

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Session with retry
session = requests.Session()
retries = Retry(total=3, backoff_factor=1,
                status_forcelist=[429, 500, 502, 503])
session.mount("https://", HTTPAdapter(max_retries=retries))

# GET
resp = session.get("https://api.example.com/data",
                    params={"page": 1, "limit": 100},
                    headers={"Authorization": "Bearer TOKEN"},
                    timeout=30)
resp.raise_for_status()
data = resp.json()

# POST
resp = session.post("https://api.example.com/events",
                     json={"name": "test", "value": 42})

# Paginated extraction
def extract_all(base_url, page_size=100):
    all_records = []
    page = 1
    while True:
        resp = session.get(base_url, params={"page": page, "limit": page_size})
        resp.raise_for_status()
        batch = resp.json()["data"]
        if not batch:
            break
        all_records.extend(batch)
        page += 1
    return all_records

# Async requests (pip install aiohttp)
import asyncio, aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]

results = asyncio.run(fetch_all(urls))
```

---

## Concurrency & Parallelism

```python
# Threading — I/O-bound tasks (API calls, file reads)
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(url):
    return requests.get(url).json()

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = {pool.submit(fetch, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            data = future.result()
        except Exception as e:
            logger.error("Failed %s: %s", url, e)

# Multiprocessing — CPU-bound tasks (transforms, parsing)
from multiprocessing import Pool

def heavy_transform(chunk):
    return [process(record) for record in chunk]

with Pool(processes=8) as pool:
    results = pool.map(heavy_transform, data_chunks)
flat_results = [r for chunk in results for r in chunk]

# asyncio — high-concurrency I/O
import asyncio

async def process_queue(queue):
    while True:
        item = await queue.get()
        await process_async(item)
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    workers = [asyncio.create_task(process_queue(queue)) for _ in range(10)]
    for item in data:
        await queue.put(item)
    await queue.join()
```

---

## Data Validation & Quality

```python
# Schema validation with Pydantic
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class EventRecord(BaseModel):
    event_id: str
    timestamp: datetime
    value: float
    source: str
    metadata: Optional[dict] = None

    @field_validator("value")
    @classmethod
    def value_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("value must be non-negative")
        return v

# Validate batch
def validate_batch(records: list[dict]) -> tuple[list, list]:
    valid, invalid = [], []
    for r in records:
        try:
            valid.append(EventRecord(**r).model_dump())
        except Exception as e:
            invalid.append({"record": r, "error": str(e)})
    return valid, invalid

# Great Expectations style checks (manual)
def data_quality_checks(df):
    checks = {
        "no_nulls_in_id":    df["id"].notnull().all(),
        "positive_values":   (df["value"] >= 0).all(),
        "unique_ids":        df["id"].is_unique,
        "row_count_min":     len(df) >= 100,
        "valid_dates":       df["date"].between("2020-01-01", "2030-01-01").all(),
    }
    for name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        logger.info("DQ Check [%s]: %s", status, name)
    return all(checks.values())
```

---

## Environment & Configuration

```python
# Environment variables
import os
DB_HOST = os.environ["DB_HOST"]                  # raises KeyError
DB_PORT = os.environ.get("DB_PORT", "5432")      # default fallback
DEBUG   = os.environ.get("DEBUG", "false").lower() == "true"

# .env files (pip install python-dotenv)
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

# Config class pattern
from dataclasses import dataclass

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
```

---

## Docker & CLI

### Dockerfile for Python Pipeline

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### CLI with argparse

```python
import argparse

parser = argparse.ArgumentParser(description="ETL Pipeline")
parser.add_argument("--source", required=True, help="Source path or URL")
parser.add_argument("--dest", required=True, help="Destination table")
parser.add_argument("--batch-size", type=int, default=5000)
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--start-date", type=str, default=None)
args = parser.parse_args()

pipeline = ETLPipeline(
    source=args.source,
    destination=args.dest,
    batch_size=args.batch_size,
    dry_run=args.dry_run,
)
pipeline.run()
```

---

## Pro Tips & Patterns

### Built-in Superpowers

```python
# enumerate — index + value
for i, val in enumerate(items, start=1):
    print(i, val)

# zip — parallel iteration
for name, score in zip(names, scores):
    print(f"{name}: {score}")
dict(zip(keys, values))   # two lists → dict

# any / all — quick checks
any(r["status"] == "error" for r in records)
all(r.get("id") for r in records)

# sorted with key
sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)

# itertools
from itertools import chain, islice, groupby
list(chain([1,2], [3,4]))          # [1,2,3,4]
list(islice(huge_generator, 100))  # first 100 items
```

### One-Liners & Tricks

```python
# Flatten nested list
flat = [x for sub in nested for x in sub]

# Remove duplicates, preserve order
seen = set()
uniq = [x for x in lst if x not in seen and not seen.add(x)]

# Merge dicts (3.9+)
merged = d1 | d2

# Safe nested dict access
val = d.get("a", {}).get("b", {}).get("c")

# Timing code
from time import perf_counter
t0 = perf_counter()
# ... code ...
print(f"{perf_counter()-t0:.4f}s")

# Regex
import re
emails = re.findall(r'\S+@\S+', text)
clean  = re.sub(r'[^\w\s]', '', text)
dates  = re.findall(r'\d{4}-\d{2}-\d{2}', log_text)

# hashlib — checksums for data integrity
import hashlib
checksum = hashlib.md5(open("file.csv", "rb").read()).hexdigest()
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

*Python Cheatsheet — Developer & Data Engineering Edition*
