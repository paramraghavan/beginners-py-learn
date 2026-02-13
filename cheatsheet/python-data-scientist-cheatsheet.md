# Python Cheatsheet
### For Python Developers & Data Scientists

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

# Type checking & conversion
type(x)              # <class 'int'>
isinstance(x, int)   # True
int("42")            # 42
str(3.14)            # "3.14"
float("2.7")         # 2.7

# Multiple assignment
a, b, c = 1, 2, 3
a, b = b, a          # swap!
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
```

---

## Strings

### String Operations

```python
s = "Hello, World!"

# Slicing
s[0:5]        # "Hello"
s[::-1]       # "!dlroW ,olleH" (reverse)

# Methods
s.lower() / s.upper() / s.title()
s.strip()  / s.lstrip() / s.rstrip()
s.split(",")          # ["Hello", " World!"]
"-".join(["a","b"])   # "a-b"
s.replace("World", "Python")
s.startswith("He") / s.endswith("!")
s.find("World")       # 7 (-1 if not found)
s.count("l")          # 3
s.isdigit() / s.isalpha() / s.isalnum()

# f-strings (Python 3.6+)
name, age = "Alice", 30
f"{name} is {age} years old"
f"{3.14159:.2f}"         # "3.14"
f"{1000000:,}"           # "1,000,000"
f"{'hi':>10}"            # "        hi"
f"{x = }"                # "x = 42" (debug, 3.8+)
```

---

## Data Structures

### Lists

```python
lst = [1, 2, 3, 4, 5]

# CRUD
lst.append(6)          # [1,2,3,4,5,6]
lst.insert(0, 0)       # [0,1,2,3,4,5,6]
lst.extend([7, 8])     # append multiple
lst.pop()              # remove & return last
lst.pop(0)             # remove & return first
lst.remove(3)          # remove first occurrence of 3
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
```

### Sets

```python
s = {1, 2, 3}
s.add(4) / s.discard(2)
s1 & s2   # intersection
s1 | s2   # union
s1 - s2   # difference
s1 ^ s2   # symmetric diff
```

### Counter

```python
from collections import Counter
Counter("banana")
# Counter({'a': 3, 'n': 2, 'b': 1})
```

---

## Functions

### Functions & Lambdas

```python
# Standard function
def greet(name, greeting="Hello"):
    """Docstring: describes function."""
    return f"{greeting}, {name}!"

# *args and **kwargs
def flex(*args, **kwargs):
    print(args)    # tuple
    print(kwargs)  # dict

# Lambda
square = lambda x: x ** 2

# Higher-order functions
map(lambda x: x*2, [1,2,3])     # [2,4,6]
filter(lambda x: x>2, [1,2,3])  # [3]
from functools import reduce
reduce(lambda a, b: a+b, [1,2,3])  # 6

# Type hints (3.5+)
def add(a: int, b: int) -> int:
    return a + b
```

### Decorators & Generators

```python
# Decorator
import time
def timer(func):
    def wrapper(*args, **kw):
        t0 = time.time()
        result = func(*args, **kw)
        print(f"{time.time()-t0:.3f}s")
        return result
    return wrapper

@timer
def slow(): time.sleep(1)

# Generator (lazy evaluation)
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
next(gen)  # 0
next(gen)  # 1

# Generator expression
squares = (x**2 for x in range(10))
```

---

## Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]

# Nested
flat = [x for row in matrix for x in row]

# Dict comprehension
word_len = {w: len(w) for w in ["hello", "world"]}

# Set comprehension
unique_lengths = {len(w) for w in words}

# Conditional expression in comprehension
labels = ["even" if x%2==0 else "odd" for x in range(5)]

# Walrus operator (3.8+)
results = [y for x in data if (y := process(x)) > 0]
```

---

## Object-Oriented Programming

```python
# Standard class
class Animal:
    species_count = 0              # class variable

    def __init__(self, name, sound):
        self.name = name           # instance variable
        self.sound = sound
        Animal.species_count += 1

    def speak(self):
        return f"{self.name} says {self.sound}!"

    def __repr__(self):
        return f"Animal({self.name!r})"

# Inheritance
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")

    def fetch(self, item):
        return f"{self.name} fetches {item}"

# Dataclass (3.7+) — less boilerplate!
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"

p = Point(1.0, 2.0)   # auto __init__, __repr__, __eq__
```

---

## File I/O

```python
# Read
with open("file.txt") as f:
    content = f.read()          # whole file
    lines   = f.readlines()     # list

# Write
with open("out.txt", "w") as f:
    f.write("Hello\n")

# Append
with open("log.txt", "a") as f:
    f.write("new line\n")

# JSON
import json
data = json.loads(json_str)
json_str = json.dumps(data, indent=2)

# CSV
import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# pathlib (modern paths)
from pathlib import Path
p = Path("data") / "file.csv"
p.exists() / p.read_text()
list(Path(".").glob("*.py"))
```

---

## Error Handling

```python
try:
    result = 10 / x
    data = json.loads(raw)
except ZeroDivisionError:
    print("Can't divide by zero")
except (ValueError, KeyError) as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected: {e}")
    raise  # re-raise
else:
    print("Success!")
finally:
    cleanup()

# Custom exception
class ValidationError(Exception):
    def __init__(self, field, msg):
        super().__init__(f"{field}: {msg}")
        self.field = field

# Context manager
from contextlib import contextmanager
@contextmanager
def managed(resource):
    try:
        yield resource
    finally:
        resource.close()
```

---

## NumPy

```python
import numpy as np

# Creating arrays
a = np.array([1, 2, 3])
np.zeros((3, 4))  /  np.ones((2, 3))  /  np.eye(3)
np.arange(0, 10, 0.5)       # like range, float
np.linspace(0, 1, 50)       # 50 evenly spaced
np.random.randn(3, 4)       # normal distribution

# Shape & Reshape
a.shape  /  a.reshape(3, 1)  /  a.flatten()  /  a.T

# Indexing
a[a > 2]                     # boolean mask
a[np.where(a > 2, a, 0)]    # conditional
a[0, :]  /  a[:, 1]          # row / column

# Vectorized operations (fast!)
a + b  /  a * b  /  a @ b   # elementwise & matrix mult
np.dot(a, b)  /  np.sum(a, axis=0)

# Statistics
a.mean()  /  a.std()  /  a.min()  /  a.max()
np.percentile(a, 75)
np.corrcoef(x, y)

# Stacking
np.vstack([a, b])  /  np.hstack([a, b])
np.concatenate([a, b], axis=0)
```

---

## Pandas

### DataFrames — Create & Inspect

```python
import pandas as pd

# Read data
df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx")
df = pd.read_json("data.json")
df = pd.read_sql(query, conn)

# From dict
df = pd.DataFrame({
    "name": ["Alice", "Bob"],
    "age":  [30, 25]
})

# Inspect
df.head(10)   /  df.tail()
df.shape      /  df.dtypes
df.info()     /  df.describe()
df.columns    /  df.index
df.nunique()  /  df.value_counts()
df.isnull().sum()
```

### DataFrames — Select & Filter

```python
# Selecting
df["col"]               # Series
df[["col1", "col2"]]    # DataFrame
df.loc[0:5, "name"]     # label-based
df.iloc[0:5, 0:2]       # position-based

# Filtering
df[df["age"] > 25]
df[df["name"].isin(["Alice", "Bob"])]
df.query("age > 25 and city == 'NYC'")

# Sorting
df.sort_values("age", ascending=False)
df.nlargest(10, "revenue")

# New columns
df["bmi"] = df["weight"] / df["height"]**2
df["grade"] = pd.cut(df["score"],
    bins=[0, 60, 80, 100],
    labels=["C", "B", "A"])
df["flag"] = np.where(df["x"] > 0, 1, 0)

# Apply
df["name"].apply(lambda x: x.upper())
df.apply(lambda row: row.sum(), axis=1)
```

### DataFrames — Group, Merge & Clean

```python
# GroupBy
df.groupby("city")["revenue"].mean()
df.groupby("city").agg({
    "revenue": ["sum", "mean"],
    "users": "count"
})
df.groupby("dept")["salary"].transform("mean")  # broadcast back

# Pivot table
pd.pivot_table(df, values="sales", index="region",
               columns="quarter", aggfunc="sum")

# Merge / Join
pd.merge(df1, df2, on="id", how="left")         # left, right, inner, outer
pd.concat([df1, df2], ignore_index=True)         # stack vertically

# Cleaning
df.dropna()  /  df.fillna(0)  /  df.fillna(method="ffill")
df.drop_duplicates(subset=["col1"])
df.rename(columns={"old": "new"})
df["date"] = pd.to_datetime(df["date"])
df.astype({"age": int, "name": "category"})

# Save
df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet")
```

---

## Visualization

### Matplotlib & Seaborn

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib basics
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(x, y, 'b-o', label="data")
axes[0].set_title("Line Plot")
axes[0].legend()
axes[1].bar(categories, values)
plt.tight_layout()
plt.savefig("plot.png", dpi=150)
plt.show()

# Seaborn (statistical plots)
sns.set_theme(style="whitegrid")
sns.histplot(df["age"], kde=True)
sns.boxplot(data=df, x="dept", y="salary")
sns.scatterplot(data=df, x="x", y="y", hue="label")
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
sns.pairplot(df, hue="species")

# Pandas quick plots
df["col"].plot(kind="hist", bins=30)
df.plot.scatter(x="a", y="b", c="label", colormap="viridis")
```

---

## Scikit-learn

### Machine Learning Pipeline

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression

# 1. Prepare data
X = df[["feat1", "feat2", "feat3"]]
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 2. Build pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  RandomForestClassifier(n_estimators=100))
])

# 3. Train & Evaluate
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred))

# Cross-validation
scores = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
print(f"CV Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

# Feature importance (tree models)
importances = pipe["model"].feature_importances_
feat_imp = pd.Series(importances, index=X.columns).sort_values()
feat_imp.plot.barh()
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

# dict(zip(...)) — two lists → dict
dict(zip(keys, values))

# any / all
any(x > 10 for x in nums)
all(x > 0 for x in nums)

# sorted with key
sorted(users, key=lambda u: u["age"])
sorted(words, key=len, reverse=True)

# collections goodies
from collections import defaultdict, Counter, deque
dd = defaultdict(list)
dd["key"].append(1)  # no KeyError!

# itertools
from itertools import chain, product, groupby
list(chain([1, 2], [3, 4]))  # [1, 2, 3, 4]
```

### One-Liners & Tricks

```python
# Flatten nested list
flat = [x for sub in nested for x in sub]

# Remove duplicates, preserve order
seen = set()
uniq = [x for x in lst if x not in seen and not seen.add(x)]

# Frequency count
{x: lst.count(x) for x in set(lst)}

# Merge dicts (3.9+)
merged = d1 | d2

# Safe dict access chain
val = d.get("a", {}).get("b", {}).get("c")

# Timing code
from time import perf_counter
t0 = perf_counter()
# ... code ...
print(f"{perf_counter()-t0:.4f}s")

# Quick HTTP request
import requests
r = requests.get("https://api.example.com")
data = r.json()

# Regex
import re
emails = re.findall(r'\S+@\S+', text)
clean  = re.sub(r'[^\w\s]', '', text)
```

---

## Quick Reference Table

| Operation | Syntax | Note |
|---|---|---|
| Virtual env | `python -m venv .venv && source .venv/bin/activate` | Isolate deps |
| Install pkg | `pip install pandas && pip freeze > requirements.txt` | Pin versions |
| Debugger | `breakpoint()` | Built-in (3.7+) |
| Profile | `python -m cProfile script.py` | Find bottlenecks |
| Jupyter magic | `%timeit / %%time / %who / %matplotlib inline` | Notebook utils |
| Type check | `mypy script.py` | Static analysis |
| Format | `black script.py / ruff check .` | Auto-format |
| Pickle | `import pickle; pickle.dump(obj, open('f.pkl','wb'))` | Serialize objects |

---

*Python Cheatsheet — Dev & Data Science Edition*
