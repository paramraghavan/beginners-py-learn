In Python, **dunder methods** (short for “double underscore” methods) are special methods surrounded by double underscores, like `__init__`, `__str__`, or `__add__`. They enable classes to interact seamlessly with Python’s built-in syntax and operations, forming the backbone of Python’s *data model*.[1][3][9]

### What Dunder Methods Do
Dunder methods allow you to **customize class behavior** for standard operations such as:
- **Object creation and initialization** (`__new__`, `__init__`, `__del__`)
- **String representation** (`__str__`, `__repr__`)
- **Arithmetic and comparisons** (`__add__`, `__sub__`, `__eq__`, `__lt__`)
- **Iteration and container behavior** (`__iter__`, `__next__`, `__getitem__`, `__len__`)
- **Attribute management** (`__getattr__`, `__setattr__`, `__delattr__`)
- **Callability and context management** (`__call__`, `__enter__`, `__exit__`).[3][4][5]

### Why They’re Useful
1. **Operator Overloading** – You can define how objects respond to mathematical or logical operators.  
   Example:
   ```python
   class Vector:
       def __init__(self, x, y):
           self.x = x
           self.y = y
       def __add__(self, other):
           return Vector(self.x + other.x, self.y + other.y)
       def __str__(self):
           return f"Vector({self.x}, {self.y})"
   v1 = Vector(1, 2)
   v2 = Vector(3, 4)
   print(v1 + v2)  # Vector(4, 6)
   ```
   This uses `__add__` and `__str__`.[3]

2. **Integration with Built-in Functions** – Many built-ins like `len()`, `abs()`, and `round()` rely on corresponding dunder methods (`__len__`, `__abs__`, `__round__`).[4][5]

3. **Code Readability and Consistency** – Dunder methods make user-defined classes act like native Python objects, maintaining predictable and Pythonic interfaces.[6][7][8]

### Example of Common Dunder Methods

| Operation | Dunder Method | Example |
|------------|----------------|----------|
| Object creation | `__init__` | `__init__(self, x)` sets up attributes |
| String conversion | `__str__` | Controls output of `print(obj)` |
| Addition | `__add__` | Defines `obj1 + obj2` |
| Equality | `__eq__` | Defines `obj1 == obj2` |
| Length | `__len__` | Used by `len(obj)` |
| Indexing | `__getitem__` | Handles `obj[key]` |
| Iteration | `__iter__`, `__next__` | Make objects iterable |
| Function-like behavior | `__call__` | Allows `obj()` syntax [3][4][5] |



## Iteration and Container Behavior
Dunder methods like __iter__, __next__, and __getitem__ make objects iterable (usable in loops). 
You can implement them with or without yield.

**Explanation:**
- __iter__ returns the iterator object.
- __next__ defines logic for each iteration and raises StopIteration when done.

```python

class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        self.n = self.start
        return self  # The iterator is the object itself

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        current = self.n
        self.n -= 1
        return current

# Usage
for number in Countdown(5):
    print(number)

```

**With yield**
Explanation:
Here, __iter__ uses yield to create a generator automatically handling iteration state.

```python
class CountdownYield:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        for n in range(self.start, 0, -1):
            yield n

# Usage
for number in CountdownYield(5):
    print(number)

```

## Attribute Management
- [attribute-management.md](attribute-management.md)

## Callability and Context Management

### Example 1 – Making Objects Callable

The `__call__` method lets you treat class instances as functions.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

# Usage
double = Multiplier(2)
print(double(5))  # Works like a function → Output: 10
```

**Explanation:**  
Once `__call__` is defined, instances can be *called like functions*, enabling reusable callable objects.

***

### Example 2 – Context Management (`with` Statement)

Context managers require `__enter__` and `__exit__`. They’re used in `with` statements to handle resource setup and cleanup automatically.

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("Opening file...")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing file...")
        self.file.close()

# Usage
with FileManager("example.txt", "w") as f:
    f.write("Hello, world!")
```

**Explanation:**  
- `__enter__`: Sets up resources and returns what `as` receives.  
- `__exit__`: Cleans resources or handles exceptions automatically.

***


## Reference
[1](https://www.geeksforgeeks.org/python/dunder-magic-methods-python/)
[2](https://www.reddit.com/r/Python/comments/1bioxer/every_dunder_method_in_python/)
[3](https://www.datacamp.com/tutorial/python-dunder-methods)
[4](https://www.pythonmorsels.com/every-dunder-method/)
[5](https://www.youtube.com/watch?v=E6XCXhHUtBI)
[6](https://codesolid.com/dunder-methods-in-python-the-ugliest-awesome-sauce/)
[7](https://mathspp.com/blog/pydonts/dunder-methods)
[8](https://stackoverflow.com/questions/66838840/what-are-the-advantages-of-dunder-methods-in-python)
[9](https://realpython.com/python-magic-methods/)