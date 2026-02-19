## Chapter 11: Intermediate Python

### 11.1 Decorators

A decorator is a function that takes another function and extends its behavior without modifying it.

**Step-by-step: How decorators work:**

```python
# Step 1: Functions can be passed as arguments
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def greet(func):
    """Takes a function, calls it, prints result."""
    result = func("Hello, World")
    print(result)

greet(shout)    # HELLO, WORLD
greet(whisper)  # hello, world
```

```python
# Step 2: Functions can return other functions
def create_greeting(style):
    def formal(name):
        return f"Good day, {name}. How do you do?"
    def casual(name):
        return f"Hey {name}! What's up?"

    if style == "formal":
        return formal
    else:
        return casual

greet = create_greeting("casual")
print(greet("Alice"))  # Hey Alice! What's up?
```

```python
# Step 3: A decorator combines both concepts
from functools import wraps

def timer(func):
    """Decorator that measures execution time."""
    @wraps(func)  # Preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)  # Call the original function
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}() took {elapsed:.4f}s")
        return result
    return wrapper

# Using the decorator:
@timer
def slow_function():
    """This function is slow."""
    import time
    time.sleep(1)
    return "done"

result = slow_function()
# Output: slow_function() took 1.0012s

# @timer is syntactic sugar for:
# slow_function = timer(slow_function)
```

**Decorator with parameters:**

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Decorator factory - returns a decorator configured with parameters."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        print(f"All {max_attempts} attempts failed for {func.__name__}")
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Server down")
    return {"data": "success"}

# Stacking decorators (applied bottom to top):
@timer          # 2nd: wraps the retry-wrapped function
@retry(max_attempts=3)  # 1st: wraps fetch_data
def api_call():
    pass
```

### 11.2 Context Managers

Context managers handle setup and cleanup automatically (files, connections, locks, etc.):

```python
# You've already used one:
with open("file.txt") as f:
    content = f.read()
# File is automatically closed here

# Creating your own context manager - Method 1: class-based
class Timer:
    """Context manager that measures execution time."""
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        print("Timer started")
        return self  # This becomes the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"Timer stopped: {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

# Usage:
with Timer() as t:
    total = sum(range(1_000_000))
print(f"Elapsed: {t.elapsed:.4f}s")

# Method 2: contextlib (simpler for most cases)
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.perf_counter()
    yield  # Everything before yield is __enter__, after is __exit__
    elapsed = time.perf_counter() - start
    print(f"Elapsed: {elapsed:.4f}s")

with timer():
    total = sum(range(1_000_000))

# Practical example: temporary directory change
import os
from contextlib import contextmanager

@contextmanager
def change_directory(path):
    """Temporarily change to a directory, then restore."""
    original = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original)

with change_directory("/tmp"):
    print(f"Now in: {os.getcwd()}")  # /tmp
print(f"Back in: {os.getcwd()}")     # original directory
```

### 11.3 Dataclasses

Dataclasses auto-generate `__init__`, `__repr__`, `__eq__`, and more:

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Employee:
    name: str
    age: int
    department: str
    salary: float = 50000.0                    # Default value
    skills: List[str] = field(default_factory=list)  # Mutable default

    @property
    def is_senior(self):
        return self.age >= 40

# Auto-generated __init__:
emp = Employee("Alice", 35, "Engineering", 95000, ["Python", "SQL"])

# Auto-generated __repr__:
print(emp)
# Employee(name='Alice', age=35, department='Engineering', salary=95000, skills=['Python', 'SQL'])

# Auto-generated __eq__:
emp2 = Employee("Alice", 35, "Engineering", 95000, ["Python", "SQL"])
print(emp == emp2)  # True

# Frozen (immutable) dataclass:
@dataclass(frozen=True)
class Point:
    x: float
    y: float
# Can be used as dict key or in sets

# Ordered dataclass (enables sorting):
@dataclass(order=True)
class Priority:
    priority: int
    name: str = field(compare=False)  # Excluded from comparison

tasks = [Priority(3, "low"), Priority(1, "high"), Priority(2, "med")]
print(sorted(tasks))  # Sorted by priority
```

### 11.4 Regular Expressions

```python
import re

text = "Contact alice@example.com or bob@test.org. Call 555-123-4567 on 2024-01-15."

# findall - find ALL matches
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
print(emails)  # ['alice@example.com', 'bob@test.org']

dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
print(dates)  # ['2024-01-15']

phones = re.findall(r'\d{3}-\d{3}-\d{4}', text)
print(phones)  # ['555-123-4567']

# search - find FIRST match
match = re.search(r'(\w+)@([\w.]+)', text)
if match:
    print(match.group(0))  # 'alice@example.com' (full match)
    print(match.group(1))  # 'alice' (first group)
    print(match.group(2))  # 'example.com' (second group)

# sub - replace matches
cleaned = re.sub(r'\d{3}-\d{3}-\d{4}', '[PHONE REDACTED]', text)
print(cleaned)

# compile - pre-compile for reuse (faster in loops)
email_pattern = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')
matches = email_pattern.findall(some_large_text)
```

### 11.5 Date and Time

```python
from datetime import datetime, date, timedelta, timezone

# Current date/time
now = datetime.now()
today = date.today()
utc_now = datetime.now(timezone.utc)

print(now)          # 2024-03-15 14:30:45.123456
print(today)        # 2024-03-15

# Formatting (datetime -> string)
print(now.strftime("%Y-%m-%d"))          # 2024-03-15
print(now.strftime("%B %d, %Y"))         # March 15, 2024
print(now.strftime("%I:%M %p"))          # 02:30 PM

# Parsing (string -> datetime)
dt = datetime.strptime("2024-03-15 14:30:00", "%Y-%m-%d %H:%M:%S")

# Arithmetic
tomorrow = now + timedelta(days=1)
next_week = now + timedelta(weeks=1)
two_hours_later = now + timedelta(hours=2)

# Difference between dates
diff = datetime(2024, 12, 31) - datetime(2024, 1, 1)
print(f"{diff.days} days")  # 365 days

# Timezones (pip install pytz)
import pytz
est = pytz.timezone('US/Eastern')
now_est = datetime.now(est)
print(f"EST: {now_est.strftime('%Y-%m-%d %H:%M %Z')}")
```

---

## Chapter 12: Advanced Python

### 12.1 Metaclasses

A metaclass is a "class of a class" - it controls how classes themselves are created:

```python
# Every class is an instance of 'type':
print(type(int))    # <class 'type'>
print(type(str))    # <class 'type'>

# Custom metaclass for Singleton pattern
class SingletonMeta(type):
    """Metaclass that ensures only one instance of a class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"
        print("Database initialized")

# Usage:
db1 = Database()  # Prints "Database initialized"
db2 = Database()  # Does NOT print again - returns same instance
print(db1 is db2)  # True
```

### 12.2 The GIL (Global Interpreter Lock)

The GIL is a mutex that allows only one thread to execute Python bytecode at a time:

```python
# CPU-bound: GIL is a bottleneck -> use multiprocessing
# I/O-bound: GIL is released during I/O -> threading works fine

# Example: CPU-bound (GIL hurts performance)
import time
from threading import Thread
from multiprocessing import Process

def cpu_heavy(n):
    total = sum(i * i for i in range(n))
    return total

# Threading: NOT faster for CPU work (GIL blocks parallel execution)
start = time.perf_counter()
threads = [Thread(target=cpu_heavy, args=(5_000_000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Threads: {time.perf_counter() - start:.2f}s")  # ~4s (serial!)

# Multiprocessing: FASTER (each process has its own GIL)
start = time.perf_counter()
processes = [Process(target=cpu_heavy, args=(5_000_000,)) for _ in range(4)]
for p in processes: p.start()
for p in processes: p.join()
print(f"Processes: {time.perf_counter() - start:.2f}s")  # ~1s (parallel!)
```

### 12.3 `__slots__` (Memory Optimization)

```python
import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ['x', 'y']  # No __dict__, saves memory
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Memory comparison (for millions of instances, this matters):
regular = RegularPoint(1, 2)
slotted = SlottedPoint(1, 2)
print(sys.getsizeof(regular.__dict__))  # ~104 bytes per instance
# slotted has no __dict__ - saves ~50% memory

# Tradeoff: can't add new attributes
# slotted.z = 3  # AttributeError!
```

### 12.4 Deep Copy vs Shallow Copy

```python
import copy

# Shallow copy: copies the outer object, but inner objects are SHARED
original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)

# They look the same:
print(original)  # [[1, 2, 3], [4, 5, 6]]
print(shallow)   # [[1, 2, 3], [4, 5, 6]]

# But modifying an inner list affects both:
original[0].append(99)
print(original)  # [[1, 2, 3, 99], [4, 5, 6]]
print(shallow)   # [[1, 2, 3, 99], [4, 5, 6]]  <- ALSO CHANGED!

# Deep copy: copies EVERYTHING recursively
original2 = [[1, 2, 3], [4, 5, 6]]
deep = copy.deepcopy(original2)

original2[0].append(99)
print(original2)  # [[1, 2, 3, 99], [4, 5, 6]]
print(deep)       # [[1, 2, 3], [4, 5, 6]]  <- NOT affected
```

---

## Chapter 13: Concurrency & Parallelism

### 13.1 Threading (For I/O-bound Tasks)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def download_page(url):
    """Simulate downloading a web page."""
    time.sleep(1)  # Simulate network I/O
    return f"Content of {url}"

urls = [f"https://example.com/page/{i}" for i in range(10)]

# Sequential: ~10 seconds
start = time.perf_counter()
results = [download_page(url) for url in urls]
print(f"Sequential: {time.perf_counter() - start:.1f}s")

# Parallel with ThreadPoolExecutor: ~2 seconds
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(download_page, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
            print(f"Done: {url}")
        except Exception as e:
            print(f"Failed: {url} - {e}")
print(f"Threaded: {time.perf_counter() - start:.1f}s")
```

### 13.2 Multiprocessing (For CPU-bound Tasks)

```python
from multiprocessing import Pool

def cpu_task(n):
    """CPU-intensive calculation."""
    return sum(i * i for i in range(n))

# Parallel processing
with Pool(processes=4) as pool:
    results = pool.map(cpu_task, [10**6, 10**6, 10**6, 10**6])
    print(f"Total: {sum(results)}")
```

### 13.3 asyncio (Modern Async I/O)

```python
import asyncio

async def fetch_data(name, delay):
    print(f"Starting {name}...")
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(f"Done {name}")
    return f"{name}: {delay}s of data"

async def main():
    # Run all three concurrently
    results = await asyncio.gather(
        fetch_data("users", 2),
        fetch_data("orders", 1),
        fetch_data("products", 1.5),
    )
    for r in results:
        print(r)

asyncio.run(main())
# All three complete in ~2s (the longest), not 4.5s (sequential)
```

### When to Use What

| Task Type | Tool | Example |
|---|---|---|
| Download files, API calls | `ThreadPoolExecutor` | HTTP requests |
| Database queries | `threading` / `asyncio` | SELECT/INSERT |
| Number crunching | `multiprocessing.Pool` | Math, image processing |
| Many concurrent connections | `asyncio` | Web servers, chat |

---

## Chapter 14: Design Patterns

### 14.1 Singleton

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True

s1 = Singleton("first")
s2 = Singleton("second")
print(s1 is s2)      # True - same object
print(s1.value)       # "first" - not overwritten
```

### 14.2 Factory Pattern

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message): pass

class EmailNotification(Notification):
    def send(self, message): print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message): print(f"SMS: {message}")

class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        klass = cls._registry.get(channel)
        if not klass:
            raise ValueError(f"Unknown channel: {channel}")
        return klass()

    @classmethod
    def register(cls, channel: str, klass):
        cls._registry[channel] = klass

# Usage:
notif = NotificationFactory.create("email")
notif.send("Hello!")
```

### 14.3 Observer Pattern

```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

# Usage
bus = EventEmitter()
bus.on("user_created", lambda user: print(f"Welcome {user}!"))
bus.on("user_created", lambda user: print(f"Sending email to {user}"))
bus.emit("user_created", "Alice")
# Welcome Alice!
# Sending email to Alice
```

---

## Chapter 15: Data Science with Python

Data science in Python revolves around three core libraries: **NumPy** for numerical computation, **Pandas** for data manipulation, and **Matplotlib/Seaborn** for visualization. Together with **scikit-learn** for machine learning, they form the standard data science toolkit.

### 15.1 NumPy - Numerical Computing

NumPy arrays are the foundation of scientific computing in Python. They're **up to 100x faster** than Python lists for math because they use contiguous memory and C-optimized operations.

```python
import numpy as np

# Creating arrays
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros(5)                    # [0. 0. 0. 0. 0.]
ones = np.ones((3, 3))                 # 3x3 matrix of 1s
range_arr = np.arange(0, 10, 2)        # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)        # [0.  0.25 0.5  0.75 1. ]
random_arr = np.random.rand(5)         # 5 random floats [0, 1)
random_int = np.random.randint(1, 100, size=10)  # 10 random ints

# Element-wise operations (no loops needed!)
arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)       # [ 2  4  6  8 10]
print(arr ** 2)      # [ 1  4  9 16 25]
print(arr + 10)      # [11 12 13 14 15]
print(np.sqrt(arr))  # [1.   1.41 1.73 2.   2.24]

# Aggregation
print(np.mean(arr))   # 3.0
print(np.std(arr))    # 1.414
print(np.median(arr)) # 3.0
print(np.sum(arr))    # 15
print(np.min(arr), np.max(arr))  # 1 5
```

**2D arrays (matrices) - the bread and butter of data science:**

```python
# 2D arrays
matrix = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])

# Indexing and slicing
print(matrix[0, :])        # First row: [1, 2, 3]
print(matrix[:, 0])        # First column: [1, 4, 7]
print(matrix[0:2, 1:3])    # Sub-matrix: [[2, 3], [5, 6]]
print(matrix.shape)        # (3, 3)

# Boolean indexing (very powerful!)
print(matrix[matrix > 5])  # [6, 7, 8, 9]
print(matrix[matrix % 2 == 0])  # [2, 4, 6, 8]

# Reshape
flat = np.arange(12)             # [0,1,2,...,11]
reshaped = flat.reshape(3, 4)    # 3x4 matrix
print(reshaped)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Matrix operations
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(a @ b)           # Matrix multiplication (dot product)
print(a * b)           # Element-wise multiplication
print(a.T)             # Transpose
print(np.linalg.inv(a))  # Inverse
print(np.linalg.det(a))  # Determinant: -2.0
```

**Why NumPy over lists - a speed comparison:**

```python
import time

size = 1_000_000

# Python list
py_list = list(range(size))
start = time.perf_counter()
result = [x * 2 for x in py_list]
print(f"List: {time.perf_counter() - start:.4f}s")

# NumPy array
np_arr = np.arange(size)
start = time.perf_counter()
result = np_arr * 2
print(f"NumPy: {time.perf_counter() - start:.4f}s")
# NumPy is typically 50-100x faster!
```

### 15.2 Pandas - Data Manipulation

Pandas is *the* tool for working with tabular data (think spreadsheets, CSV files, database tables).

**Creating DataFrames:**

```python
import pandas as pd

# From a dictionary
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [30, 25, 35, 28, 32],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
    "salary": [95000, 72000, 88000, 78000, 105000],
    "department": ["Eng", "Sales", "Eng", "HR", "Eng"]
})

# From CSV file
# df = pd.read_csv("employees.csv")

# From JSON
# df = pd.read_json("data.json")
```

**Exploring your data (always do this first!):**

```python
print(df.head())       # First 5 rows
print(df.tail(3))      # Last 3 rows
print(df.shape)        # (5, 5) = 5 rows, 5 columns
print(df.dtypes)       # Data type of each column
print(df.info())       # Summary: types, non-null counts, memory
print(df.describe())   # Statistics: mean, std, min, max, percentiles
print(df.columns.tolist())  # Column names as a list
print(df.nunique())    # Number of unique values per column
```

**Selecting and filtering:**

```python
# Select columns
print(df["name"])              # Single column (Series)
print(df[["name", "salary"]]) # Multiple columns (DataFrame)

# Filter rows
nyc = df[df["city"] == "NYC"]
high_salary = df[df["salary"] > 80000]

# Multiple conditions (use & for AND, | for OR, ~ for NOT)
eng_nyc = df[(df["department"] == "Eng") & (df["city"] == "NYC")]
not_sales = df[~(df["department"] == "Sales")]

# .query() - more readable for complex filters
result = df.query("salary > 80000 and city == 'NYC'")

# .loc (label-based) and .iloc (position-based)
print(df.loc[0, "name"])      # "Alice" (by label)
print(df.iloc[0, 0])          # "Alice" (by position)
print(df.loc[0:2, ["name", "salary"]])  # Rows 0-2, specific columns
```

**Transforming data:**

```python
# Add new columns
df["bonus"] = df["salary"] * 0.1
df["tax_bracket"] = df["salary"].apply(
    lambda s: "high" if s > 90000 else "medium" if s > 75000 else "low"
)

# Rename columns
df = df.rename(columns={"name": "employee_name"})

# Sort
df_sorted = df.sort_values("salary", ascending=False)
df_multi_sort = df.sort_values(["city", "salary"], ascending=[True, False])

# Drop columns or rows
df_slim = df.drop(columns=["bonus"])
df_no_dupes = df.drop_duplicates(subset=["city"])
```

**GroupBy - split-apply-combine (most powerful Pandas feature):**

```python
# Average salary by city
print(df.groupby("city")["salary"].mean())
# Chicago    78000.0
# LA         88500.0
# NYC        91500.0

# Multiple aggregations
summary = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    headcount=("name", "count"),
    avg_age=("age", "mean")
).round(0)
print(summary)

# Pivot tables (like Excel pivot tables)
pivot = df.pivot_table(
    values="salary",
    index="department",
    columns="city",
    aggfunc="mean",
    fill_value=0
)
print(pivot)
```

**Handling missing data (critical for real-world data):**

```python
df_dirty = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Diana"],
    "age": [30, None, 35, 28],
    "salary": [95000, 72000, None, 78000]
})

# Detect missing data
print(df_dirty.isnull())           # Boolean mask
print(df_dirty.isnull().sum())     # Count per column
print(df_dirty.isnull().sum().sum())  # Total missing

# Handle missing data
df_clean = df_dirty.dropna()                    # Remove rows with ANY NaN
df_clean = df_dirty.dropna(subset=["name"])     # Remove only if name is NaN
df_filled = df_dirty.fillna({"age": df_dirty["age"].median(), "salary": 0})
df_interpolated = df_dirty.interpolate()        # Fill with interpolated values
df_forward = df_dirty.fillna(method="ffill")    # Forward fill
```

**Merging DataFrames (like SQL JOINs):**

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer": ["Alice", "Bob", "Alice", "Charlie"],
    "amount": [100, 200, 150, 300]
})

customers = pd.DataFrame({
    "name": ["Alice", "Bob", "Diana"],
    "city": ["NYC", "LA", "Chicago"]
})

# Inner join (only matching rows)
merged = orders.merge(customers, left_on="customer", right_on="name", how="inner")

# Left join (keep all orders, even if customer not found)
merged_left = orders.merge(customers, left_on="customer", right_on="name", how="left")

# Concatenate (stack DataFrames)
df_all = pd.concat([df_part1, df_part2], ignore_index=True)
```

### 15.3 Visualization with Matplotlib and Seaborn

```python
import matplotlib.pyplot as plt
import numpy as np

# Line plot
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), 'b-', label="sin(x)", linewidth=2)
plt.plot(x, np.cos(x), 'r--', label="cos(x)", linewidth=2)
plt.xlabel("X axis", fontsize=12)
plt.ylabel("Y axis", fontsize=12)
plt.title("Trigonometric Functions", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("plot.png", dpi=150)  # Save to file
plt.show()
```

```python
# Multiple plot types in subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Bar chart
categories = ["Eng", "Sales", "HR", "Marketing"]
values = [45, 30, 15, 25]
axes[0, 0].bar(categories, values, color=['#5b9cf5', '#50d890', '#f5a623', '#e878a0'])
axes[0, 0].set_title("Headcount by Department")

# Scatter plot
np.random.seed(42)
x = np.random.randn(100)
y = x * 2 + np.random.randn(100) * 0.5
axes[0, 1].scatter(x, y, alpha=0.6, c=y, cmap='viridis')
axes[0, 1].set_title("Correlation Plot")

# Histogram
data = np.random.normal(70000, 15000, 1000)
axes[1, 0].hist(data, bins=30, color='#a78bfa', edgecolor='black', alpha=0.7)
axes[1, 0].set_title("Salary Distribution")

# Pie chart
sizes = [45, 30, 15, 10]
axes[1, 1].pie(sizes, labels=categories, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title("Department Share")

plt.tight_layout()
plt.show()
```

```python
# Seaborn - statistical visualizations (prettier defaults)
# pip install seaborn
import seaborn as sns

# Use a built-in dataset for demonstration
tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Box plot - shows distribution, outliers, median
sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0])
axes[0].set_title("Bill by Day")

# Violin plot - box plot + kernel density
sns.violinplot(data=tips, x="day", y="tip", ax=axes[1])
axes[1].set_title("Tips by Day")

# Heatmap - correlation matrix
numeric_tips = tips.select_dtypes(include='number')
sns.heatmap(numeric_tips.corr(), annot=True, cmap="coolwarm", ax=axes[2])
axes[2].set_title("Correlation Heatmap")

plt.tight_layout()
plt.show()
```

### 15.4 scikit-learn - Machine Learning Basics

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import numpy as np
import pandas as pd

# --- Regression example: Predict house prices ---
np.random.seed(42)
n = 200
sqft = np.random.uniform(800, 3000, n)
bedrooms = np.random.randint(1, 6, n)
price = sqft * 150 + bedrooms * 20000 + np.random.normal(0, 15000, n)

df = pd.DataFrame({"sqft": sqft, "bedrooms": bedrooms, "price": price})

# Step 1: Split into features (X) and target (y)
X = df[["sqft", "bedrooms"]]
y = df["price"]

# Step 2: Train/test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Scale features (important for many algorithms)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaler!

# Step 4: Train model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Step 5: Evaluate
predictions = model.predict(X_test_scaled)
rmse = mean_squared_error(y_test, predictions, squared=False)
print(f"RMSE: ${rmse:,.0f}")
print(f"R² score: {model.score(X_test_scaled, y_test):.3f}")
```

```python
# --- Classification example: Predict customer churn ---
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Simulated data
np.random.seed(42)
n = 500
data = pd.DataFrame({
    "tenure_months": np.random.randint(1, 72, n),
    "monthly_charge": np.random.uniform(20, 100, n),
    "support_calls": np.random.randint(0, 10, n),
})
# Churn more likely with short tenure, high charges, many support calls
data["churned"] = (
    (data["tenure_months"] < 12) &
    (data["monthly_charge"] > 60) |
    (data["support_calls"] > 7)
).astype(int)

X = data[["tenure_months", "monthly_charge", "support_calls"]]
y = data["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))

# Feature importance (which features matter most)
for name, importance in zip(X.columns, clf.feature_importances_):
    print(f"  {name}: {importance:.3f}")
```

### Exercise 15.1: Data Analysis Challenge

Using pandas, analyze this sales dataset:

```python
sales = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=100, freq="D"),
    "product": np.random.choice(["Widget", "Gadget", "Doohickey"], 100),
    "quantity": np.random.randint(1, 50, 100),
    "unit_price": np.random.choice([9.99, 24.99, 49.99], 100),
    "region": np.random.choice(["North", "South", "East", "West"], 100)
})
sales["revenue"] = sales["quantity"] * sales["unit_price"]
```

Tasks:
1. What's the total revenue by product?
2. Which region has the highest average order value?
3. What's the weekly revenue trend?
4. Create a bar chart of revenue by product and a line chart of weekly revenue.

<details>
<summary>Solution</summary>

```python
# 1. Revenue by product
print(sales.groupby("product")["revenue"].sum().sort_values(ascending=False))

# 2. Highest avg order by region
print(sales.groupby("region")["revenue"].mean().sort_values(ascending=False))

# 3. Weekly revenue trend
sales["week"] = sales["date"].dt.isocalendar().week
weekly = sales.groupby("week")["revenue"].sum()

# 4. Visualize
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

sales.groupby("product")["revenue"].sum().plot(kind="bar", ax=ax1, color=['#5b9cf5', '#50d890', '#f5a623'])
ax1.set_title("Revenue by Product")
ax1.set_ylabel("Revenue ($)")

weekly.plot(ax=ax2, marker='o', color='#a78bfa')
ax2.set_title("Weekly Revenue Trend")
ax2.set_ylabel("Revenue ($)")

plt.tight_layout()
plt.show()
```
</details>

---

## Chapter 16: Data Engineering with Python

Data engineering is about building reliable pipelines to move and transform data. Python is the dominant language in this space, especially with tools like Apache Spark (PySpark), Airflow, and boto3.

### 16.1 Database Operations

**SQLite (built-in, great for prototyping):**

```python
import sqlite3

# Connect (creates file if it doesn't exist)
conn = sqlite3.connect("local.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert data - ALWAYS use parameterized queries to prevent SQL injection!
cursor.execute(
    "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Alice", "alice@example.com", 30)
)

# Insert many rows at once (much faster than individual inserts)
users = [
    ("Bob", "bob@example.com", 25),
    ("Charlie", "charlie@example.com", 35),
    ("Diana", "diana@example.com", 28),
]
cursor.executemany(
    "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)
conn.commit()

# Query
cursor.execute("SELECT name, age FROM users WHERE age > ? ORDER BY age", (26,))
for row in cursor.fetchall():
    print(row)  # ('Alice', 30), ('Diana', 28), ('Charlie', 35)

# Use context manager for automatic cleanup
conn.close()
```

**Using Pandas with databases (recommended for data work):**

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect("local.db")

# Read SQL query into DataFrame (much easier than manual iteration)
df = pd.read_sql_query("SELECT * FROM users WHERE age > 25", conn)
print(df)

# Write DataFrame to SQL table
new_users = pd.DataFrame({
    "name": ["Eve", "Frank"],
    "email": ["eve@example.com", "frank@example.com"],
    "age": [29, 33]
})
new_users.to_sql("users", conn, if_exists="append", index=False)

conn.close()
```

**PostgreSQL with psycopg2 (production databases):**

```python
# pip install psycopg2-binary
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="password"  # In production: use env vars!
    )
    try:
        yield conn
    finally:
        conn.close()

# Usage
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users LIMIT 10")
        rows = cur.fetchall()
        for row in rows:
            print(row)
```

### 16.2 Processing Large Files

When files don't fit in memory, you need streaming/chunked approaches:

```python
# Chunked CSV processing (for files too large for memory)
import pandas as pd

total_revenue = 0
row_count = 0

for chunk in pd.read_csv("huge_file.csv", chunksize=50_000):
    # Process each chunk (50,000 rows at a time)
    filtered = chunk[chunk["amount"] > 100]
    total_revenue += filtered["amount"].sum()
    row_count += len(filtered)
    print(f"Processed chunk: {row_count} qualifying rows so far")

print(f"Total revenue: ${total_revenue:,.2f} from {row_count} rows")
```

```python
# Line-by-line processing (for non-CSV or custom formats)
import json

def process_jsonl(filepath):
    """Process a JSON Lines file (one JSON object per line)."""
    results = []
    errors = 0
    with open(filepath) as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line.strip())
                if record.get("status") == "active":
                    results.append(record)
            except json.JSONDecodeError:
                errors += 1
            if line_num % 100_000 == 0:
                print(f"Processed {line_num:,} lines...")
    print(f"Done: {len(results)} active records, {errors} errors")
    return results
```

```python
# Generator-based pipeline (memory-efficient chaining)
def read_lines(filepath):
    """Generator: yields lines from file."""
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def parse_csv_lines(lines):
    """Generator: parse CSV lines into dicts."""
    headers = next(lines).split(",")
    for line in lines:
        values = line.split(",")
        yield dict(zip(headers, values))

def filter_records(records, min_amount=100):
    """Generator: filter by amount."""
    for record in records:
        if float(record.get("amount", 0)) > min_amount:
            yield record

# Chain generators - processes one record at a time, any file size!
pipeline = filter_records(parse_csv_lines(read_lines("sales.csv")))
for record in pipeline:
    print(record)
```

### 16.3 AWS S3 with boto3

```python
# pip install boto3
import boto3
import json

s3 = boto3.client("s3")

# Upload a file
s3.upload_file("local_data.csv", "my-bucket", "data/2024/sales.csv")

# Download a file
s3.download_file("my-bucket", "data/2024/sales.csv", "downloaded.csv")

# List objects in a bucket
response = s3.list_objects_v2(Bucket="my-bucket", Prefix="data/2024/")
for obj in response.get("Contents", []):
    print(f"{obj['Key']}: {obj['Size']} bytes")

# Read file directly into pandas (without downloading)
import io
obj = s3.get_object(Bucket="my-bucket", Key="data/sales.csv")
df = pd.read_csv(io.BytesIO(obj["Body"].read()))
```

### 16.4 Simple ETL Pipeline

```python
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract(source_path: str) -> pd.DataFrame:
    """Extract: read raw data from source."""
    logger.info(f"Extracting from {source_path}")
    df = pd.read_csv(source_path)
    logger.info(f"Extracted {len(df)} rows")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform: clean and reshape data."""
    logger.info("Transforming data...")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {before - len(df)} duplicates")

    # Clean column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Handle missing values
    df["amount"] = df["amount"].fillna(0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Add derived columns
    df["year_month"] = df["date"].dt.to_period("M")
    df["amount_category"] = pd.cut(df["amount"], bins=[0, 100, 500, float("inf")],
                                     labels=["small", "medium", "large"])
    logger.info(f"Transformed: {len(df)} rows")
    return df

def load(df: pd.DataFrame, dest_path: str):
    """Load: write processed data to destination."""
    logger.info(f"Loading {len(df)} rows to {dest_path}")
    df.to_parquet(dest_path, index=False)
    logger.info("Load complete")

# Run the ETL pipeline
if __name__ == "__main__":
    raw = extract("raw_sales.csv")
    clean = transform(raw)
    load(clean, f"processed/sales_{datetime.now():%Y%m%d}.parquet")
```

### Exercise 16.1: Build a Data Pipeline

Write a pipeline that:
1. Reads a CSV file with columns: `date, product, quantity, price`
2. Removes rows where quantity <= 0
3. Adds a `revenue` column (quantity * price)
4. Groups by product and month, summing revenue
5. Saves the result to a new CSV

<details>
<summary>Solution</summary>

```python
import pandas as pd

# Extract
df = pd.read_csv("sales_raw.csv")

# Transform
df = df[df["quantity"] > 0]
df["revenue"] = df["quantity"] * df["price"]
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly = df.groupby(["month", "product"])["revenue"].sum().reset_index()
monthly = monthly.sort_values(["month", "revenue"], ascending=[True, False])

# Load
monthly.to_csv("monthly_revenue.csv", index=False)
print(f"Saved {len(monthly)} rows")
print(monthly.head(10))
```
</details>

---

## Chapter 17: Testing & Code Quality

Testing isn't optional - it's what separates professional code from scripts that break. Python's testing ecosystem is excellent, with **pytest** as the de facto standard.

### 17.1 pytest - The Testing Framework

**Installation and basic setup:**

```bash
pip install pytest
```

**Your first tests:**

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# test_calculator.py
import pytest
from calculator import add, divide

# Basic tests - function names must start with test_
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0

# Testing exceptions
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_normal():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5
```

```bash
# Run tests
pytest                          # Run all tests
pytest test_calculator.py       # Run specific file
pytest -v                       # Verbose output (shows each test name)
pytest -v -k "test_add"         # Run only tests matching pattern
pytest --tb=short               # Shorter traceback on failure
pytest -x                       # Stop on first failure
```

**Parametrize - test many inputs without writing many functions:**

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
    (0.1, 0.2, pytest.approx(0.3)),  # Floating point comparison!
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

**Fixtures - reusable test setup:**

```python
import pytest
import sqlite3

@pytest.fixture
def db_connection():
    """Create a test database, yield it, then clean up."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice', 30)")
    conn.execute("INSERT INTO users VALUES (2, 'Bob', 25)")
    conn.commit()
    yield conn  # Test runs here
    conn.close()  # Cleanup after test

def test_query_users(db_connection):
    cursor = db_connection.execute("SELECT * FROM users")
    users = cursor.fetchall()
    assert len(users) == 2

def test_query_by_age(db_connection):
    cursor = db_connection.execute("SELECT name FROM users WHERE age > 27")
    names = [row[0] for row in cursor.fetchall()]
    assert names == ["Alice"]

@pytest.fixture
def sample_data():
    """Reusable test data."""
    return {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
    }

def test_user_count(sample_data):
    assert len(sample_data["users"]) == 2
```

### 17.2 Mocking - Testing Without External Dependencies

Mocking replaces real objects with fake ones. Use it to test code that calls APIs, databases, or other external services.

```python
from unittest.mock import Mock, patch, MagicMock

# Mock a function
@patch("requests.get")
def test_fetch_user(mock_get):
    # Configure the mock to return a specific response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Alice", "age": 30}
    mock_get.return_value = mock_response

    # Now test YOUR code that calls requests.get
    import requests
    response = requests.get("https://api.example.com/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

    # Verify the mock was called correctly
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

```python
# Mock for testing email sending
class NotificationService:
    def __init__(self, email_client):
        self.email_client = email_client

    def notify_user(self, user_email, message):
        if not user_email:
            raise ValueError("Email required")
        self.email_client.send(to=user_email, body=message)
        return True

def test_notify_user():
    # Create a mock email client (no real emails sent!)
    mock_client = Mock()
    service = NotificationService(mock_client)

    result = service.notify_user("alice@test.com", "Hello!")

    assert result is True
    mock_client.send.assert_called_once_with(to="alice@test.com", body="Hello!")

def test_notify_no_email():
    mock_client = Mock()
    service = NotificationService(mock_client)

    with pytest.raises(ValueError):
        service.notify_user("", "Hello!")

    mock_client.send.assert_not_called()  # Email should NOT be sent
```

### 17.3 Test Organization Best Practices

```
my_project/
    src/
        __init__.py
        calculator.py
        user_service.py
    tests/
        __init__.py
        test_calculator.py
        test_user_service.py
        conftest.py          # Shared fixtures go here
```

```python
# conftest.py - shared fixtures available to ALL test files
import pytest

@pytest.fixture
def api_url():
    return "https://api.example.com"

@pytest.fixture(autouse=True)
def reset_env(monkeypatch):
    """Automatically reset environment for every test."""
    monkeypatch.setenv("ENV", "test")
```

### 17.4 Code Quality Tools

```bash
# Formatting
black src/               # Auto-format code (opinionated, consistent)
black --check src/       # Check without changing (for CI)

# Linting
ruff check src/          # Fast linter (replaces flake8, isort, etc.)
ruff check --fix src/    # Auto-fix what it can
pylint src/              # More thorough (but slower) linting

# Type checking
mypy src/                # Static type checker
mypy src/ --strict       # Strict mode (catches more issues)

# Security
bandit -r src/           # Find security issues
pip-audit                # Check dependencies for vulnerabilities

# Import sorting
isort src/               # Sort imports consistently

# All at once in CI:
# black --check src/ && ruff check src/ && mypy src/ && pytest tests/ -v
```

### Exercise 17.1: Write Tests

Given this function, write at least 5 tests:

```python
def validate_password(password: str) -> tuple[bool, str]:
    """Validate password. Returns (is_valid, message)."""
    if len(password) < 8:
        return False, "Must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Must contain uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Must contain a digit"
    return True, "Valid"
```

<details>
<summary>Solution</summary>

```python
import pytest

@pytest.mark.parametrize("password, expected_valid, expected_msg", [
    ("Ab1defgh", True, "Valid"),
    ("short1A", False, "Must be at least 8 characters"),
    ("alllowercase1", False, "Must contain uppercase letter"),
    ("ALLUPPERcase", False, "Must contain a digit"),
    ("", False, "Must be at least 8 characters"),
    ("A1bcdefg", True, "Valid"),
    ("12345678A", True, "Valid"),
])
def test_validate_password(password, expected_valid, expected_msg):
    is_valid, msg = validate_password(password)
    assert is_valid == expected_valid
    assert msg == expected_msg
```
</details>

---

## Chapter 18: Data Structures & Algorithms

Understanding DSA helps you write efficient code and is essential for technical interviews. Python's built-in data structures are highly optimized, but knowing *when* to use each one matters.

### 18.1 Big-O Notation

Big-O describes how an algorithm's runtime grows as input size grows. It's about the **worst case** scaling pattern, not the exact time.

| Notation | Name | Example | For n=1000 |
|---|---|---|---|
| O(1) | Constant | Dict lookup, array index | 1 operation |
| O(log n) | Logarithmic | Binary search | ~10 operations |
| O(n) | Linear | List scan, linear search | 1,000 operations |
| O(n log n) | Linearithmic | Merge sort, Python's `sorted()` | ~10,000 operations |
| O(n^2) | Quadratic | Nested loops, bubble sort | 1,000,000 operations |
| O(2^n) | Exponential | Recursive fibonacci (naive) | 10^301 operations! |

**Python built-in data structure complexity:**

| Operation | list | dict | set |
|---|---|---|---|
| Access by index | O(1) | N/A | N/A |
| Search (in) | O(n) | **O(1)** | **O(1)** |
| Insert/append | O(1)* | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) |
| Sort | O(n log n) | N/A | N/A |

*O(1) amortized for list.append()

**Key takeaway:** If you're doing lots of membership checks (`if x in collection`), use a `set` or `dict`, not a `list`!

```python
# Bad: O(n) per lookup * O(n) items = O(n^2)
large_list = list(range(100_000))
for item in items_to_check:
    if item in large_list:  # O(n) each time!
        process(item)

# Good: O(1) per lookup * O(n) items = O(n)
large_set = set(range(100_000))   # One-time O(n) conversion
for item in items_to_check:
    if item in large_set:  # O(1) each time!
        process(item)
```

### 18.2 Binary Search

Binary search finds an element in a **sorted** array in O(log n) time by repeatedly halving the search space.

```python
def binary_search(arr, target):
    """
    Find target in sorted array. Returns index or -1.

    How it works:
    - Look at the middle element
    - If it's the target, we're done
    - If target is smaller, search the left half
    - If target is larger, search the right half
    - Repeat until found or search space is empty
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1    # Target is in right half
        else:
            high = mid - 1   # Target is in left half

    return -1  # Not found

# Example
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(arr, 23))   # 5 (index of 23)
print(binary_search(arr, 50))   # -1 (not found)

# Python's built-in: bisect module
import bisect
arr = [1, 3, 5, 7, 9, 11]
idx = bisect.bisect_left(arr, 5)     # 2 (insertion point for 5)
bisect.insort(arr, 6)                # Insert 6 in sorted position
print(arr)                           # [1, 3, 5, 6, 7, 9, 11]
```

### 18.3 Common Algorithm Patterns

**Two Pointers - efficient for sorted arrays:**

```python
def two_sum_sorted(nums, target):
    """Find two numbers in SORTED array that sum to target. O(n)."""
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

print(two_sum_sorted([1, 3, 5, 7, 11], 12))  # [1, 4] (3 + 11 = 14? No, 1+11=12)
# Actually: [0, 4] -> 1 + 11 = 12
```

**Hash Map pattern - O(1) lookups:**

```python
def two_sum(nums, target):
    """Find two numbers that add up to target. Return their indices. O(n)."""
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1] (2 + 7 = 9)
```

**Sliding Window - subarray problems:**

```python
def max_subarray_sum(arr, k):
    """Find maximum sum of subarray of size k. O(n)."""
    if len(arr) < k:
        return None

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window: add new element, remove old element
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_subarray_sum([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))  # 39 (2+10+23+3... no, 10+23+3+1=37? Let me check: [2,10,23,3]=38)
```

**Memoization / Dynamic Programming:**

```python
from functools import lru_cache

# Fibonacci - naive recursive: O(2^n), with memoization: O(n)
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Climbing stairs: how many ways to reach step n (1 or 2 steps at a time)?
@lru_cache(maxsize=None)
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)

print(climb_stairs(5))  # 8 ways
```

**Sorting - Python's built-in is excellent:**

```python
# sorted() returns a NEW list, .sort() modifies in place
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))              # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(nums, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]

# Sort by custom key
words = ["banana", "pie", "Washington", "a"]
print(sorted(words, key=len))    # ['a', 'pie', 'banana', 'Washington']

# Sort objects by attribute
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    grade: float

students = [Student("Alice", 92), Student("Bob", 88), Student("Charlie", 95)]
print(sorted(students, key=lambda s: s.grade, reverse=True))
# [Student(name='Charlie', grade=95), Student(name='Alice', grade=92), ...]

# Sort dict by value
scores = {"Alice": 92, "Bob": 88, "Charlie": 95}
sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
print(sorted_scores)  # {'Charlie': 95, 'Alice': 92, 'Bob': 88}
```

### 18.4 Python collections Module

```python
from collections import Counter, defaultdict, deque, OrderedDict

# Counter - count things
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
freq = Counter(words)
print(freq)                    # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(freq.most_common(2))    # [('apple', 3), ('banana', 2)]

# defaultdict - dict with default values (no KeyError!)
graph = defaultdict(list)
graph["A"].append("B")  # No need to check if "A" exists
graph["A"].append("C")
graph["B"].append("C")
print(dict(graph))  # {'A': ['B', 'C'], 'B': ['C']}

word_count = defaultdict(int)
for word in "the cat sat on the mat".split():
    word_count[word] += 1  # No need for .get() or if-check
print(dict(word_count))

# deque - double-ended queue (O(1) append/pop from both ends)
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)    # [0, 1, 2, 3]
dq.append(4)        # [0, 1, 2, 3, 4]
dq.popleft()        # 0  (O(1) vs list.pop(0) which is O(n)!)
dq.rotate(1)        # [4, 1, 2, 3]

# Use deque as a fixed-size buffer
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
print(list(recent))  # [2, 3, 4] - oldest items dropped automatically
```

### Exercise 18.1: Algorithm Challenges

1. **Valid Anagram**: Write a function to check if two strings are anagrams (same letters, different order).
2. **Find Duplicates**: Given a list with duplicates, return all duplicate values.
3. **Merge Sorted Lists**: Merge two sorted lists into one sorted list.

<details>
<summary>Solutions</summary>

```python
# 1. Valid Anagram - O(n)
def is_anagram(s1, s2):
    from collections import Counter
    return Counter(s1.lower()) == Counter(s2.lower())

print(is_anagram("listen", "silent"))  # True
print(is_anagram("hello", "world"))    # False

# 2. Find Duplicates - O(n)
def find_duplicates(lst):
    from collections import Counter
    return [item for item, count in Counter(lst).items() if count > 1]

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # [2, 3]

# 3. Merge Sorted Lists - O(n+m)
def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]
```
</details>

---

## Chapter 19: Interview Questions & Answers

These are commonly asked Python interview questions with detailed answers and code examples. Understanding *why* is more important than memorizing answers.

### Q1: What's the difference between list, tuple, and set?

| Feature | List | Tuple | Set |
|---|---|---|---|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` | `{1, 2, 3}` |
| Mutable? | Yes | No | Yes |
| Ordered? | Yes | Yes | No |
| Duplicates? | Yes | Yes | No |
| Hashable? | No | Yes | No |
| Lookup speed | O(n) | O(n) | O(1) |

```python
# Use list when you need to modify the collection
shopping = ["milk", "bread", "eggs"]
shopping.append("butter")

# Use tuple for fixed data (coordinates, DB rows, dict keys)
point = (3, 4)
config = ("localhost", 5432, "mydb")  # Won't accidentally change

# Use set for unique items and fast membership testing
seen_ids = {101, 102, 103}
print(104 in seen_ids)  # O(1) lookup - much faster than list for large data
```

### Q2: Explain deep copy vs shallow copy with an example.

```python
import copy

original = {"name": "Alice", "scores": [90, 85, 95]}

# Assignment: NO copy - same object
ref = original
ref["name"] = "Bob"
print(original["name"])  # "Bob" - original changed!

# Shallow copy: new outer dict, but inner list is shared
shallow = copy.copy(original)
shallow["name"] = "Charlie"      # Doesn't affect original
shallow["scores"].append(100)    # DOES affect original!
print(original["scores"])        # [90, 85, 95, 100]

# Deep copy: completely independent copy
deep = copy.deepcopy(original)
deep["scores"].append(200)
print(original["scores"])        # [90, 85, 95, 100] - NOT affected
```

### Q3: What is the GIL and how does it affect your code?

The **Global Interpreter Lock (GIL)** is a mutex in CPython that allows only one thread to execute Python bytecode at a time, even on multi-core machines.

**Impact:**
- **CPU-bound tasks**: Threading gives NO speedup. Use `multiprocessing` instead.
- **I/O-bound tasks**: Threading works fine because the GIL is released during I/O (file reads, network calls, database queries).

```python
# CPU-bound: use multiprocessing
from multiprocessing import Pool
with Pool(4) as p:
    results = p.map(heavy_computation, data)

# I/O-bound: use threading or asyncio
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
```

### Q4: How do decorators work? Write one.

A decorator is a function that wraps another function to extend its behavior. When you write `@decorator`, Python does `func = decorator(func)`.

```python
from functools import wraps
import time

def timer(func):
    @wraps(func)  # Preserves func.__name__ and func.__doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_func():
    time.sleep(1)

slow_func()  # "slow_func took 1.0012s"
```

### Q5: Explain `*args` and `**kwargs` with examples.

```python
def example(*args, **kwargs):
    print(f"args (tuple): {args}")
    print(f"kwargs (dict): {kwargs}")

example(1, 2, 3, name="Alice", age=30)
# args (tuple): (1, 2, 3)
# kwargs (dict): {'name': 'Alice', 'age': 30}

# Real-world use: flexible wrapper functions
def log_call(func):
    def wrapper(*args, **kwargs):  # Accept ANY arguments
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)  # Pass them through
    return wrapper
```

### Q6: What is a generator and when would you use one?

Generators produce values **lazily** - one at a time, on demand. They use `yield` instead of `return` and are memory-efficient for large datasets.

```python
# List: creates ALL items in memory immediately
def get_squares_list(n):
    return [x**2 for x in range(n)]  # 10M items = ~85MB RAM

# Generator: produces ONE item at a time
def get_squares_gen(n):
    for x in range(n):
        yield x**2  # ~200 bytes regardless of n!

# Use generator for large/infinite sequences
for square in get_squares_gen(10_000_000):
    if square > 1000:
        break  # Only computed ~32 values, not 10M!
```

### Q7: What's the mutable default argument trap?

```python
# BUG: The default list is shared across ALL calls!
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] ← Expected [2]!
print(bad_append(3))  # [1, 2, 3] ← Expected [3]!

# FIX: Use None as default, create new list inside
def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2] ✓
```

### Q8: What's the difference between `==` and `is`?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  (same VALUE)
print(a is b)   # False (different OBJECTS in memory)
print(a is c)   # True  (same OBJECT - c points to a)

# Rule: use 'is' ONLY for None, True, False
if result is None:     # Correct
    pass
if result == None:     # Works but not Pythonic
    pass
```

### Q9: Explain `if __name__ == "__main__"`.

```python
# utils.py
def helper():
    return "I'm a helper"

if __name__ == "__main__":
    # This block runs ONLY when you execute: python utils.py
    # It does NOT run when someone does: import utils
    print(helper())
    print("Running as main script")
```

**Why it matters:** Without this guard, any code at the module level runs on import, which can cause unexpected side effects (tests running, servers starting, etc.).

### Q10: How do you handle missing data in Pandas?

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Diana"],
    "age": [30, None, 35, 28],
    "salary": [95000, 72000, None, 78000]
})

# Detect
print(df.isnull().sum())       # Count missing per column
print(df.isnull().any())       # Which columns have missing?

# Strategy 1: Remove rows
df.dropna()                     # Remove rows with ANY NaN
df.dropna(subset=["name"])      # Remove only if name is NaN

# Strategy 2: Fill with values
df.fillna(0)                    # Fill all with 0
df["age"].fillna(df["age"].median(), inplace=True)  # Fill with median

# Strategy 3: Interpolate (for time series)
df["salary"].interpolate()

# Strategy 4: Forward/backward fill
df.fillna(method="ffill")       # Use previous row's value
df.fillna(method="bfill")       # Use next row's value
```

### Q11: What is MRO (Method Resolution Order)?

MRO determines the order Python searches for methods in a class hierarchy with multiple inheritance. Python uses **C3 linearization**.

```python
class A:
    def greet(self): print("A")

class B(A):
    def greet(self): print("B")

class C(A):
    def greet(self): print("C")

class D(B, C):
    pass

d = D()
d.greet()  # "B" - follows MRO: D -> B -> C -> A
print(D.__mro__)
# (D, B, C, A, object)
```

### Q12: What are context managers and why use them?

Context managers ensure **cleanup happens even if exceptions occur**. They implement `__enter__` and `__exit__` (or use `@contextmanager`).

```python
# Without context manager (bug if exception before close):
f = open("file.txt")
data = f.read()       # What if this raises an exception?
f.close()             # This line might never execute!

# With context manager (always cleaned up):
with open("file.txt") as f:
    data = f.read()   # Even if this fails, file is closed

# Common uses: files, database connections, locks, temporary changes
```

### Q13: Explain the bias-variance tradeoff.

**Bias** = error from wrong assumptions (underfitting). Model is too simple, misses patterns.
**Variance** = error from sensitivity to training data (overfitting). Model memorizes noise.

```python
# High bias (underfitting): linear model for non-linear data
from sklearn.linear_model import LinearRegression
# Fits a straight line through curved data - too simple

# High variance (overfitting): very deep decision tree
from sklearn.tree import DecisionTreeClassifier
# model = DecisionTreeClassifier(max_depth=None)  # Memorizes training data

# Sweet spot: tune complexity
# model = DecisionTreeClassifier(max_depth=5)  # Regularized
# Use cross-validation to find optimal complexity
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)  # 5-fold CV
print(f"Mean accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

### Q14: How does Python memory management work?

Python uses **reference counting** + **garbage collection** (cycle detector).

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount's own reference)

b = a          # refcount = 3
del b          # refcount = 2
# When refcount reaches 0, memory is freed immediately

# Circular references: garbage collector handles these
class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b
b.ref = a  # Circular reference!
del a, b   # Refcount never reaches 0, but GC detects and collects the cycle

import gc
gc.collect()  # Force garbage collection
```

### Q15: What are Python's magic/dunder methods?

Dunder (double underscore) methods let you customize how your objects behave with built-in operations:

```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self):
        return f"${self.amount:.2f} {self.currency}"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        return self.amount < other.amount

    def __len__(self):
        return int(self.amount * 100)  # cents

m1 = Money(10.50)
m2 = Money(5.25)
print(m1 + m2)       # $15.75 USD  (uses __add__)
print(m1 == m2)       # False       (uses __eq__)
print(m1 > m2)        # True        (uses __lt__ via @total_ordering)
print(repr(m1))       # Money(10.5, 'USD')
```

---

## Appendix A: Quick Reference

### Common One-Liners

```python
# Flatten nested list
flat = [x for sub in nested for x in sub]

# Remove duplicates, preserve order
unique = list(dict.fromkeys(items))

# Merge dicts (3.9+)
merged = d1 | d2

# Safe nested dict access
val = d.get("a", {}).get("b", {}).get("c")

# Transpose matrix
transposed = list(zip(*matrix))

# Frequency count
from collections import Counter
freq = Counter(items)

# Invert a dictionary
inverted = {v: k for k, v in d.items()}

# Chunk a list into groups of n
def chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

# Read entire file as string
content = open("file.txt").read()

# Flatten dict to query string
params = {"page": 1, "sort": "name", "order": "asc"}
query = "&".join(f"{k}={v}" for k, v in params.items())
# "page=1&sort=name&order=asc"
```

### Built-in Functions You Should Know

| Category | Functions | Example |
|---|---|---|
| Iteration | `enumerate, zip, reversed, sorted, range` | `for i, x in enumerate(lst)` |
| Aggregation | `len, sum, min, max, any, all` | `any(x > 0 for x in lst)` |
| Types | `int, float, str, bool, list, tuple, set, dict` | `int("42")` |
| Functional | `map, filter, isinstance, getattr, hasattr` | `list(map(str, [1,2,3]))` |
| I/O | `print, input, open` | `open("f.txt")` |
| Introspection | `type, dir, help, vars, id` | `dir(object)` |
| Math | `abs, round, divmod, pow` | `divmod(17, 5)` -> `(3, 2)` |

### String Format Cheatsheet

```python
name = "Alice"
pi = 3.14159
big = 1000000

f"{name:>20}"       # Right-align in 20 chars
f"{name:<20}"       # Left-align
f"{name:^20}"       # Center
f"{pi:.2f}"          # "3.14"
f"{pi:.5f}"          # "3.14159"
f"{big:,}"           # "1,000,000"
f"{big:_}"           # "1_000_000"
f"{0.856:.1%}"       # "85.6%"
f"{42:08d}"          # "00000042"
f"{255:#x}"          # "0xff"
f"{255:#b}"          # "0b11111111"
```

---

## Appendix B: Resources & References

**Official:**
- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

**Learning:**
- [Google's Python Class](https://developers.google.com/edu/python)
- [Real Python](https://realpython.com/) - In-depth tutorials
- [Python Cookbook (O'Reilly)](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)

**Practice:**
- [LeetCode](https://leetcode.com/) - Algorithm problems with Python solutions
- [Project Euler](https://projecteuler.net/) - Math + programming challenges
- [HackerRank Python Track](https://www.hackerrank.com/domains/python)

**Data Science:**
- [Kaggle Learn](https://www.kaggle.com/learn) - Free micro-courses
- [D-Tale](https://pypi.org/project/dtale/) - Interactive DataFrame exploration
- [Pandas Documentation](https://pandas.pydata.org/docs/)

**Tools:**
- [PyPI](https://pypi.org/) - Python Package Index
- [Awesome Python](https://github.com/vinta/awesome-python) - Curated list of libraries

---

*Generated from the [beginners-py-learn](https://github.com/paramraghavan/beginners-py-learn) repository.*
