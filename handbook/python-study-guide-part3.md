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

### 15.1 NumPy

```python
import numpy as np

# Arrays (much faster than Python lists for math)
arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)       # [2, 4, 6, 8, 10]  - element-wise!
print(arr ** 2)      # [1, 4, 9, 16, 25]
print(np.mean(arr))  # 3.0
print(np.std(arr))   # 1.414

# 2D arrays (matrices)
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0, :])   # First row: [1, 2, 3]
print(matrix[:, 0])   # First column: [1, 4, 7]
print(matrix[matrix > 5])  # Boolean indexing: [6, 7, 8, 9]
```

### 15.2 Pandas

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [30, 25, 35, 28],
    "city": ["NYC", "LA", "NYC", "Chicago"],
    "salary": [95000, 72000, 88000, 78000]
})

# Explore
print(df.head())
print(df.describe())
print(df.info())

# Filter
nyc = df[df["city"] == "NYC"]
high_salary = df[df["salary"] > 80000]

# GroupBy
print(df.groupby("city")["salary"].mean())

# Missing data
df_dirty = pd.DataFrame({"A": [1, None, 3], "B": [None, 5, 6]})
print(df_dirty.isnull().sum())
clean = df_dirty.fillna(df_dirty.mean())
```

### 15.3 Visualization

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y, 'b-o', label="Linear")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Simple Plot")
plt.legend()
plt.show()
```

---

## Chapter 16: Data Engineering with Python

### 16.1 Database Operations

```python
# SQLite (built-in, no server needed)
import sqlite3

conn = sqlite3.connect("local.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
""")
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
conn.commit()

cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

conn.close()
```

### 16.2 Processing Large Files

```python
# Stream large CSV without loading into memory
import pandas as pd

for chunk in pd.read_csv("huge_file.csv", chunksize=10000):
    # Process each chunk (10,000 rows at a time)
    filtered = chunk[chunk["amount"] > 100]
    # Save or aggregate results
```

---

## Chapter 17: Testing & Code Quality

### 17.1 pytest

```python
# test_calculator.py
import pytest

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_raises():
    with pytest.raises(TypeError):
        add("hello", 5)

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

```bash
pytest tests/ -v
pytest tests/ -v -k "test_add"  # Run specific tests
```

### 17.2 Mocking

```python
from unittest.mock import Mock, patch

@patch('requests.get')
def test_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "test"}

    import requests
    response = requests.get("https://api.example.com")
    assert response.status_code == 200
    assert response.json()["data"] == "test"
```

### 17.3 Code Quality Tools

```bash
black src/               # Auto-format code
ruff check src/          # Fast linter
mypy src/                # Type checking
bandit -r src/           # Security linter
isort src/               # Sort imports
```

---

## Chapter 18: Data Structures & Algorithms

### Big-O Reference

| Notation | Name | Example |
|---|---|---|
| O(1) | Constant | Dict lookup, array index |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | List scan |
| O(n log n) | Linearithmic | Merge sort, Python sort |
| O(n^2) | Quadratic | Nested loops |

### Binary Search

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Python built-in
import bisect
arr = [1, 3, 5, 7, 9]
idx = bisect.bisect_left(arr, 5)  # 2
```

### Fibonacci with Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

print([fibonacci(i) for i in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Two Sum (Classic Interview Problem)

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

---

## Chapter 19: Interview Questions & Answers

### Q1: List vs Tuple vs Set?
**List**: ordered, mutable, duplicates allowed. Use for collections that change.
**Tuple**: ordered, immutable, duplicates allowed. Use for fixed data, dict keys.
**Set**: unordered, mutable, NO duplicates. Use for membership testing (O(1)), deduplication.

### Q2: Deep copy vs Shallow copy?
Shallow copy (`copy.copy()`) copies the outer object but shares inner references. Deep copy (`copy.deepcopy()`) copies everything recursively.

### Q3: What is the GIL?
Global Interpreter Lock - only one thread runs Python bytecode at a time. For CPU work: use `multiprocessing`. For I/O work: threading/asyncio work fine since GIL is released during I/O.

### Q4: What are decorators?
Functions that wrap other functions to add behavior. `@decorator` is syntactic sugar for `func = decorator(func)`.

### Q5: `*args` vs `**kwargs`?
`*args` collects extra positional arguments as a tuple. `**kwargs` collects extra keyword arguments as a dict.

### Q6: What is a generator?
Functions that use `yield` to produce values lazily. Memory-efficient for large datasets (generator: ~200 bytes vs list: ~85KB for 10K items).

### Q7: Mutable default argument trap?
```python
def bad(items=[]):     # BUG: shared across all calls!
def good(items=None):  # Correct: create new list each time
    items = items or []
```

### Q8: `==` vs `is`?
`==` compares **values**. `is` compares **identity** (same object in memory). Use `is` only for `None`, `True`, `False`.

### Q9: `if __name__ == "__main__"`?
Runs code only when file is executed directly, not when imported as a module.

### Q10: How to handle missing data in pandas?
```python
df.dropna()           # Remove rows with NaN
df.fillna(0)          # Fill with value
df.fillna(df.mean())  # Fill with column mean
df.interpolate()      # Interpolate
df.isnull().sum()     # Count missing per column
```

### Q11: What is MRO?
Method Resolution Order - the order Python searches for methods in multiple inheritance. Uses C3 linearization. Check with `ClassName.__mro__`.

### Q12: What are context managers?
Objects with `__enter__`/`__exit__` for `with` statements. Guarantee cleanup even on exceptions. Use for files, DB connections, locks.

### Q13: Explain bias-variance tradeoff?
**Bias**: error from wrong assumptions (underfitting, model too simple). **Variance**: error from sensitivity to training data (overfitting, model too complex). Goal: find the sweet spot using cross-validation, regularization, ensemble methods.

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
```

### Built-in Functions

| Category | Functions |
|---|---|
| Iteration | `enumerate, zip, reversed, sorted, range` |
| Aggregation | `len, sum, min, max, any, all` |
| Types | `int, float, str, bool, list, tuple, set, dict` |
| Functional | `map, filter, isinstance, getattr, hasattr` |
| I/O | `print, input, open` |
| Introspection | `type, dir, help, vars, id` |

---

## Appendix B: Resources

- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Google's Python Class](https://developers.google.com/edu/python)
- [LeetCode](https://leetcode.com/) - Practice problems
- [Project Euler](https://projecteuler.net/) - Math + programming
- [D-Tale](https://pypi.org/project/dtale/) - Interactive DataFrame exploration

---

*Generated from the [beginners-py-learn](https://github.com/paramraghavan/beginners-py-learn) repository.*
