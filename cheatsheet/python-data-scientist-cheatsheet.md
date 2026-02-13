# Python Cheatsheet — Jupyter-Ready
### For Python Developers & Data Scientists
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

# Type checking & conversion
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True
print(int("42"))             # 42
print(str(3.14))             # "3.14"
print(float("2.7"))          # 2.7

# Multiple assignment & swap
a, b, c = 1, 2, 3
a, b = b, a
print(f"a={a}, b={b}, c={c}")  # a=2, b=1, c=3
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
    print(i, end=" ")           # 0 1 2 3 4
print()

for i in range(2, 10, 2):
    print(i, end=" ")           # 2 4 6 8
print()

for k, v in d.items():
    print(f"{k}: {v}")

# While with break/continue
counter = 0
while True:
    counter += 1
    if counter == 3:
        continue
    if counter > 5:
        break
    print(f"counter={counter}")
```

---

## Strings

### String Operations

```python
s = "Hello, World!"

# Slicing
print(s[0:5])        # "Hello"
print(s[::-1])       # "!dlroW ,olleH" (reverse)

# Methods
print(s.lower())     # "hello, world!"
print(s.upper())     # "HELLO, WORLD!"
print(s.title())     # "Hello, World!"
print(s.strip())     # "Hello, World!"
print(s.split(","))  # ["Hello", " World!"]
print("-".join(["a","b","c"]))  # "a-b-c"
print(s.replace("World", "Python"))
print(s.startswith("He"))  # True
print(s.endswith("!"))     # True
print(s.find("World"))    # 7
print(s.count("l"))        # 3
print(s.isdigit())         # False
print(s.isalpha())         # False

# f-strings (Python 3.6+)
name, age = "Alice", 30
print(f"{name} is {age} years old")
print(f"{3.14159:.2f}")         # "3.14"
print(f"{1000000:,}")           # "1,000,000"
print(f"{'hi':>10}")            # "        hi"
x = 42
print(f"{x = }")                # "x = 42" (debug, 3.8+)
```

---

## Data Structures

### Lists

```python
lst = [1, 2, 3, 4, 5]

# CRUD
lst.append(6)
print("append:", lst)          # [1,2,3,4,5,6]

lst.insert(0, 0)
print("insert:", lst)          # [0,1,2,3,4,5,6]

lst.extend([7, 8])
print("extend:", lst)          # [0,1,2,3,4,5,6,7,8]

popped = lst.pop()
print(f"pop last: {popped}, list: {lst}")

popped = lst.pop(0)
print(f"pop first: {popped}, list: {lst}")

lst.remove(3)
print("remove 3:", lst)

# Searching & Sorting
print(4 in lst)               # True
lst.sort()
print("sorted:", lst)
lst.sort(key=lambda x: -x)
print("reverse sorted:", lst)
new_sorted = sorted(lst)
print("sorted copy:", new_sorted)

# Slicing
lst = [10, 20, 30, 40, 50]
print(lst[1:4])     # [20, 30, 40]
print(lst[::2])     # [10, 30, 50]
print(lst[::-1])    # [50, 40, 30, 20, 10]

# Unpacking
first, *rest = lst
print(f"first={first}, rest={rest}")

a, b, *_ = lst
print(f"a={a}, b={b}")
```

### Dictionaries

```python
d = {"name": "Alice", "age": 30}

print(d["name"])                  # "Alice"
print(d.get("email", "N/A"))     # safe access: "N/A"

d["city"] = "NYC"
print("after add:", d)

d.update({"age": 31})
print("after update:", d)

merged = d | {"x": 1}            # merge (3.9+)
print("merged:", merged)

removed = d.pop("age")
print(f"popped age={removed}, dict={d}")

d.setdefault("tags", [])
print("setdefault:", d)

print("keys:", list(d.keys()))
print("values:", list(d.values()))
print("items:", list(d.items()))
```

### Sets

```python
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}

s1.add(5)
print("after add:", s1)

s1.discard(5)
print("after discard:", s1)

print("intersection:", s1 & s2)
print("union:", s1 | s2)
print("difference:", s1 - s2)
print("symmetric diff:", s1 ^ s2)
```

### Counter

```python
from collections import Counter

c = Counter("banana")
print(c)                    # Counter({'a': 3, 'n': 2, 'b': 1})
print(c.most_common(2))    # [('a', 3), ('n', 2)]

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_counts = Counter(words)
print(word_counts)
```

---

## Functions

### Functions & Lambdas

```python
# Standard function
def greet(name, greeting="Hello"):
    """Docstring: describes function."""
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Hi"))

# *args and **kwargs
def flex(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

flex(1, 2, 3, x=10, y=20)

# Lambda
square = lambda x: x ** 2
print(f"square(5) = {square(5)}")

# Higher-order functions
print("map:", list(map(lambda x: x*2, [1,2,3])))
print("filter:", list(filter(lambda x: x>2, [1,2,3,4,5])))

from functools import reduce
print("reduce:", reduce(lambda a, b: a+b, [1,2,3,4]))  # 10

# Type hints (3.5+)
def add(a: int, b: int) -> int:
    return a + b

print(f"add(3, 4) = {add(3, 4)}")
```

### Decorators & Generators

```python
import time

# Decorator — timer
def timer(func):
    def wrapper(*args, **kw):
        t0 = time.time()
        result = func(*args, **kw)
        print(f"  ⏱ {func.__name__}: {time.time()-t0:.3f}s")
        return result
    return wrapper

@timer
def slow():
    time.sleep(0.1)
    return "done"

print(slow())

# Generator (lazy evaluation)
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

gen = fibonacci(10)
print("fibonacci:", list(gen))

# Generator expression
squares = (x**2 for x in range(10))
print("sum of squares:", sum(squares))
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

# Dict comprehension
word_len = {w: len(w) for w in ["hello", "world", "python"]}
print("word_len:", word_len)

# Set comprehension
words = ["hello", "world", "hi", "hey", "python"]
unique_lengths = {len(w) for w in words}
print("unique_lengths:", unique_lengths)

# Conditional expression in comprehension
labels = ["even" if x%2==0 else "odd" for x in range(6)]
print("labels:", labels)

# Walrus operator (3.8+)
data = [1, -2, 3, -4, 5]
def process(x):
    return x * 10 if x > 0 else None

results = [y for x in data if (y := process(x)) is not None]
print("walrus results:", results)
```

---

## Object-Oriented Programming

```python
# Standard class
class Animal:
    species_count = 0

    def __init__(self, name, sound):
        self.name = name
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

dog = Dog("Rex")
print(dog.speak())
print(dog.fetch("ball"))
print(repr(dog))
print(f"Species count: {Animal.species_count}")

# Dataclass (3.7+)
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"

p = Point(1.0, 2.0, "A")
print(p)
print(f"x={p.x}, y={p.y}")
print(p == Point(1.0, 2.0, "A"))  # True — auto __eq__
```

---

## File I/O

```python
import json
import csv
import os
from pathlib import Path

# Write a text file
with open("demo_file.txt", "w") as f:
    f.write("Hello, Jupyter!\nSecond line\n")

# Read it back
with open("demo_file.txt") as f:
    content = f.read()
print("File content:", repr(content))

# Append
with open("demo_file.txt", "a") as f:
    f.write("Appended line\n")

with open("demo_file.txt") as f:
    lines = f.readlines()
print("Lines:", lines)

# JSON
data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
json_str = json.dumps(data, indent=2)
print("JSON:\n", json_str)

parsed = json.loads(json_str)
print("Parsed:", parsed)

# Write/Read JSON file
with open("demo.json", "w") as f:
    json.dump(data, f, indent=2)
with open("demo.json") as f:
    loaded = json.load(f)
print("Loaded JSON:", loaded)

# CSV
rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
with open("demo.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)

with open("demo.csv") as f:
    for row in csv.DictReader(f):
        print("CSV row:", row)

# pathlib
p = Path("demo.csv")
print(f"exists: {p.exists()}, suffix: {p.suffix}, stem: {p.stem}")
print("glob .txt:", list(Path(".").glob("demo*")))

# Cleanup
for f in ["demo_file.txt", "demo.json", "demo.csv"]:
    Path(f).unlink(missing_ok=True)
```

---

## Error Handling

```python
import json

# Try/except with all clauses
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
    print("Finally block always runs")

# Custom exception
class ValidationError(Exception):
    def __init__(self, field, msg):
        super().__init__(f"{field}: {msg}")
        self.field = field

try:
    raise ValidationError("email", "invalid format")
except ValidationError as e:
    print(f"Caught: {e}, field={e.field}")

# Context manager
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"  Opening {name}")
    try:
        yield name
    finally:
        print(f"  Closing {name}")

with managed_resource("database") as r:
    print(f"  Using {r}")
```

---

## NumPy

```python
import numpy as np

# Creating arrays
a = np.array([1, 2, 3, 4, 5])
print("array:", a)

print("zeros:\n", np.zeros((2, 3)))
print("ones:\n", np.ones((2, 3)))
print("eye:\n", np.eye(3))
print("arange:", np.arange(0, 2, 0.5))
print("linspace:", np.linspace(0, 1, 5))

np.random.seed(42)
rand_arr = np.random.randn(3, 4)
print("random:\n", rand_arr)

# Shape & Reshape
print(f"shape: {rand_arr.shape}")
print("reshaped:\n", np.arange(12).reshape(3, 4))
print("flattened:", np.arange(12).reshape(3, 4).flatten())
print("transposed:\n", np.arange(6).reshape(2, 3).T)

# Indexing
arr = np.array([10, 20, 30, 40, 50])
print("boolean mask (>25):", arr[arr > 25])
print("where:", np.where(arr > 25, arr, 0))

mat = np.arange(12).reshape(3, 4)
print("row 0:", mat[0, :])
print("col 1:", mat[:, 1])

# Vectorized operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("a + b:", a + b)
print("a * b:", a * b)
print("dot:", np.dot(a, b))
print("sum axis=0:", np.sum(mat, axis=0))

# Statistics
data = np.random.randn(1000)
print(f"mean={data.mean():.3f}, std={data.std():.3f}")
print(f"min={data.min():.3f}, max={data.max():.3f}")
print(f"75th percentile={np.percentile(data, 75):.3f}")

x = np.random.randn(100)
y = x * 2 + np.random.randn(100) * 0.5
print(f"correlation:\n{np.corrcoef(x, y)}")

# Stacking
print("vstack:\n", np.vstack([a, b]))
print("hstack:", np.hstack([a, b]))
```

---

## Pandas

### DataFrames — Create & Inspect

```python
import pandas as pd
import numpy as np

# From dict (standalone — no files needed)
np.random.seed(42)
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [30, 25, 35, 28, 32],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
    "score": [85.5, 92.3, 78.1, 95.0, 88.7],
    "revenue": [1200, 1800, 950, 2100, 1600],
    "dept": ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"],
})
print(df)
print(f"\nShape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nDescribe:\n{df.describe()}")
print(f"\nNull counts:\n{df.isnull().sum()}")
print(f"\nUnique counts:\n{df.nunique()}")
```

### DataFrames — Select & Filter

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "age": [30, 25, 35, 28, 32, 22],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA", "NYC"],
    "score": [85.5, 92.3, 78.1, 95.0, 88.7, 70.2],
    "weight": [65, 80, 75, 55, 68, 90],
    "height": [1.65, 1.80, 1.75, 1.60, 1.70, 1.85],
})

# Selecting
print("Single column:\n", df["name"])
print("\nMultiple columns:\n", df[["name", "age"]])
print("\nloc:\n", df.loc[0:2, "name"])
print("\niloc:\n", df.iloc[0:3, 0:2])

# Filtering
print("\nage > 28:\n", df[df["age"] > 28])
print("\nisin:\n", df[df["name"].isin(["Alice", "Bob"])])
print("\nquery:\n", df.query("age > 25 and city == 'NYC'"))

# Sorting
print("\nsorted by age desc:\n", df.sort_values("age", ascending=False))
print("\ntop 3 scores:\n", df.nlargest(3, "score"))

# New columns
df["bmi"] = df["weight"] / df["height"]**2
df["grade"] = pd.cut(df["score"], bins=[0, 60, 80, 100], labels=["C", "B", "A"])
df["flag"] = np.where(df["score"] > 85, 1, 0)
print("\nWith new columns:\n", df[["name", "bmi", "grade", "flag"]])

# Apply
df["name_upper"] = df["name"].apply(lambda x: x.upper())
df["row_sum"] = df[["age", "score"]].apply(lambda row: row.sum(), axis=1)
print("\nApply results:\n", df[["name_upper", "row_sum"]])
```

### DataFrames — Group, Merge & Clean

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
print(df.groupby("city")["revenue"].mean())
print()
print(df.groupby("city").agg({
    "revenue": ["sum", "mean"],
    "salary": "count"
}))

# Transform — broadcast aggregation back
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
    "name": ["Alice", "Bob", None, "Alice", "Eve"],
    "age": [30, None, 35, 30, 28],
    "date": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-01-15", "2024-04-05"]
})
print("\n=== Cleaning ===")
print("dropna:", dirty.dropna().shape)
print("fillna:\n", dirty.fillna({"name": "Unknown", "age": 0}))
print("drop_duplicates:\n", dirty.drop_duplicates(subset=["name"]))

dirty["date"] = pd.to_datetime(dirty["date"])
print("\nDtypes after conversion:\n", dirty.dtypes)

# Save/load demo
df.to_csv("demo_output.csv", index=False)
loaded = pd.read_csv("demo_output.csv")
print(f"\nSaved and loaded: {loaded.shape}")
import os; os.remove("demo_output.csv")
```

---

## Visualization

### Matplotlib & Seaborn

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

np.random.seed(42)

# === Matplotlib basics ===
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Line plot
x = np.linspace(0, 10, 50)
y = np.sin(x)
axes[0].plot(x, y, 'b-o', markersize=3, label="sin(x)")
axes[0].plot(x, np.cos(x), 'r--', label="cos(x)")
axes[0].set_title("Line Plot")
axes[0].legend()
axes[0].set_xlabel("x")

# Bar chart
categories = ["A", "B", "C", "D"]
values = [23, 45, 12, 67]
axes[1].bar(categories, values, color=["#4CAF50", "#2196F3", "#FF9800", "#9C27B0"])
axes[1].set_title("Bar Chart")
plt.tight_layout()
plt.show()
```

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

np.random.seed(42)

# === Seaborn statistical plots ===
df = pd.DataFrame({
    "age": np.random.normal(35, 10, 200).astype(int),
    "salary": np.random.normal(70000, 15000, 200),
    "dept": np.random.choice(["Engineering", "Marketing", "Sales"], 200),
    "score": np.random.uniform(50, 100, 200),
    "experience": np.random.uniform(1, 20, 200),
})
df["salary"] = df["salary"] + df["experience"] * 2000  # add correlation

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.histplot(df["age"], kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Age Distribution")

sns.boxplot(data=df, x="dept", y="salary", ax=axes[0, 1])
axes[0, 1].set_title("Salary by Department")

sns.scatterplot(data=df, x="experience", y="salary", hue="dept", ax=axes[1, 0])
axes[1, 0].set_title("Experience vs Salary")

corr_cols = df[["age", "salary", "score", "experience"]].corr()
sns.heatmap(corr_cols, annot=True, cmap="coolwarm", ax=axes[1, 1])
axes[1, 1].set_title("Correlation Heatmap")

plt.tight_layout()
plt.show()
```

```python
import seaborn as sns
import pandas as pd
import numpy as np

# Pairplot
np.random.seed(42)
iris_like = pd.DataFrame({
    "sepal_length": np.concatenate([np.random.normal(5.0, 0.4, 50), np.random.normal(6.5, 0.5, 50)]),
    "sepal_width": np.concatenate([np.random.normal(3.4, 0.4, 50), np.random.normal(2.8, 0.3, 50)]),
    "petal_length": np.concatenate([np.random.normal(1.5, 0.2, 50), np.random.normal(5.0, 0.5, 50)]),
    "species": ["setosa"]*50 + ["virginica"]*50,
})
sns.pairplot(iris_like, hue="species")
```

---

## Scikit-learn

### Machine Learning Pipeline

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

# 1. Create sample dataset
np.random.seed(42)
n = 300
df = pd.DataFrame({
    "feat1": np.random.randn(n),
    "feat2": np.random.randn(n),
    "feat3": np.random.randn(n),
})
# Target: 1 if feat1 + feat2 > 0, else 0 (with noise)
df["target"] = ((df["feat1"] + df["feat2"] + np.random.randn(n)*0.3) > 0).astype(int)
print(f"Dataset shape: {df.shape}")
print(f"Target distribution:\n{df['target'].value_counts()}\n")

# 2. Prepare data
X = df[["feat1", "feat2", "feat3"]]
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}\n")

# 3. Build pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  RandomForestClassifier(n_estimators=100, random_state=42))
])

# 4. Train & Evaluate
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))

# 5. Cross-validation
scores = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
print(f"CV Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

# 6. Feature importance
importances = pipe["model"].feature_importances_
feat_imp = pd.Series(importances, index=X.columns).sort_values()
print(f"\nFeature Importance:\n{feat_imp}")

import matplotlib.pyplot as plt
feat_imp.plot.barh(title="Feature Importance")
plt.tight_layout()
plt.show()
```

---

## Pro Tips & Patterns

### Built-in Superpowers

```python
# enumerate — index + value
items = ["apple", "banana", "cherry"]
for i, val in enumerate(items, start=1):
    print(f"{i}. {val}")

# zip — parallel iteration
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# dict(zip(...)) — two lists → dict
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))
print("dict from zip:", d)

# any / all
nums = [1, 5, 12, 3, 8]
print(f"any > 10: {any(x > 10 for x in nums)}")
print(f"all > 0: {all(x > 0 for x in nums)}")

# sorted with key
users = [{"name": "Bob", "age": 25}, {"name": "Alice", "age": 30}, {"name": "Charlie", "age": 22}]
sorted_users = sorted(users, key=lambda u: u["age"])
print("sorted by age:", [u["name"] for u in sorted_users])

words = ["python", "hi", "jupyter", "code"]
print("sorted by length:", sorted(words, key=len, reverse=True))

# collections goodies
from collections import defaultdict, Counter, deque
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["veggies"].append("carrot")
print("defaultdict:", dict(dd))

# itertools
from itertools import chain, product
print("chain:", list(chain([1, 2], [3, 4], [5])))
print("product:", list(product("AB", [1, 2])))
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

# Frequency count
print("frequency:", {x: lst.count(x) for x in set(lst)})

# Merge dicts (3.9+)
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2
print("merged dicts:", merged)

# Safe dict access chain
d = {"a": {"b": {"c": 42}}}
val = d.get("a", {}).get("b", {}).get("c")
print("nested access:", val)

# Timing code
from time import perf_counter
t0 = perf_counter()
total = sum(range(1_000_000))
elapsed = perf_counter() - t0
print(f"sum = {total}, time = {elapsed:.4f}s")

# Regex
import re
text = "Contact alice@example.com or bob@test.org for info on 2024-01-15 and 2024-06-30"
emails = re.findall(r'\S+@\S+', text)
print("emails:", emails)

dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
print("dates:", dates)

clean = re.sub(r'[^\w\s]', '', "Hello, World! How's it going?")
print("cleaned:", clean)
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

*Python Cheatsheet — Dev & Data Science Edition — Jupyter-Ready ✅*
