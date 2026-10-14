# Dunder Methods and Context Managers

"Dunder" means **double underscore**.

Dunder methods are methods with names like this:

```python
__init__
__str__
__add__
__enter__
__exit__
```

Python officially calls them **special methods**. People also call them
**magic methods**.

They are special because Python's own syntax knows how to call them.

For example:

```python
len(obj)      # may call obj.__len__()
print(obj)   # may call obj.__str__()
obj1 + obj2  # may call obj1.__add__(obj2)
with obj:    # may call obj.__enter__() and obj.__exit__()
```

You do not invent random dunder names. You use the standard ones Python already
understands.

---

## Beginner Idea: Python Syntax Calls Methods

When you write normal Python syntax, Python often translates it into a special
method call.

This:

```python
p3 = p1 + p2
```

is roughly like this:

```python
p3 = p1.__add__(p2)
```

That is how your own objects can work with operators like `+`.

---

## How Does `Point` Know to Call `__add__`?

The `Point` class does not "know" by itself.

Python knows.

The `+` operator is part of Python's data model. When Python sees:

```python
p1 + p2
```

it follows a standard rule:

1. Look at the type of `p1`.
2. Check whether that type defines `__add__`.
3. If it does, call `p1.__add__(p2)`.
4. Use the returned value as the result of `p1 + p2`.

Example:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p1 = Point(1, 2)
p2 = Point(3, 4)

print(p1 + p2)
```

Output:

```text
Point(4, 6)
```

The important part is:

```python
def __add__(self, other):
```

Python has a standard rule that says `+` uses `__add__`.

So yes, `__add__` is a standard dunder method.

Advanced detail: for many special methods, Python looks on the object's class,
not just on the individual object. So the important thing is that `Point`
defines `__add__` as part of the class.

---

## What If Python Cannot Find `__add__`?

If an object does not support `+`, Python raises a `TypeError`.

```python
class Point:
    pass


p1 = Point()
p2 = Point()

print(p1 + p2)
```

Output:

```text
TypeError: unsupported operand type(s) for +: 'Point' and 'Point'
```

That error means Python looked for a way to add those objects, but the class did
not define the needed behavior.

---

## Common Standard Dunder Methods

Python has many standard dunder methods. You do not need to memorize all of
them, but you should recognize the common ones.

### Object Setup and Display

| Method | Triggered by | Purpose |
|---|---|---|
| `__init__` | `ClassName(...)` | Initialize a new object after it is created |
| `__repr__` | `repr(obj)`, developer tools | Developer-friendly representation |
| `__str__` | `str(obj)`, `print(obj)` | Human-friendly string |
| `__bool__` | `if obj:` | Truth value |

Example:

```python
class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User({self.name!r})"

    def __str__(self):
        return self.name


user = User("Ada")

print(repr(user))
print(str(user))
```

Output:

```text
User('Ada')
Ada
```

---

### Operators

| Method | Triggered by | Purpose |
|---|---|---|
| `__add__` | `a + b` | Addition |
| `__radd__` | `b + a`, when the left operand cannot handle addition | Reflected (right-side) addition |
| `__sub__` | `a - b` | Subtraction |
| `__mul__` | `a * b` | Multiplication |
| `__truediv__` | `a / b` | True division |
| `__eq__` | `a == b` | Equality |
| `__lt__` | `a < b` | Less-than comparison |

This teaching example adds and subtracts two `Money` objects, adds a number of
dollars, and multiplies or divides an amount by a number. It uses ordinary
numbers to keep the focus on operators; real currency calculations need more
care with precision.

```python
class Money:
    def __init__(self, dollars):
        self.dollars = dollars

    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.dollars + other.dollars)
        if isinstance(other, (int, float)):
            return Money(self.dollars + other)
        return NotImplemented

    def __radd__(self, other):
        # Addition has the same result in either order in this example.
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Money):
            return Money(self.dollars - other.dollars)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.dollars * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.dollars / other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.dollars == other.dollars
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Money):
            return self.dollars < other.dollars
        return NotImplemented

    def __repr__(self):
        return f"Money({self.dollars})"


wallet = Money(10)
bonus = Money(5)

print(wallet + bonus)       # __add__
print(wallet + 5)           # __add__ with a number
print(5 + wallet)           # __radd__ on wallet
print(wallet - bonus)       # __sub__
print(wallet * 3)           # __mul__
print(wallet / 2)           # __truediv__
print(wallet == Money(10))  # __eq__
print(bonus < wallet)       # __lt__
```

Output:

```text
Money(15)
Money(15)
Money(15)
Money(5)
Money(30)
Money(5.0)
True
True
```

In `wallet + 5`, `wallet` is on the left, so Python uses its `__add__`.
In `5 + wallet`, the integer cannot add a `Money` object, so Python tries
`wallet.__radd__(5)`. The `r` means **reflected**: your object handles the
operation from the right side.

`NotImplemented` is a special return value that means "this method does not
support that operand type." It lets Python try an appropriate fallback. It is
different from raising `NotImplementedError`. If neither side supports an
arithmetic operation, Python raises `TypeError`.

For different operand types, Python can try the reflected method if the left
method is missing or returns `NotImplemented`. A right operand whose type is a
subclass of the left operand's type can get priority when it provides a different
reflected implementation.

Multiplication also has `__rmul__`, subtraction has `__rsub__`, and division has
`__rtruediv__`. This class does not define them, so `3 * wallet`, `20 - wallet`,
and `20 / wallet` are unsupported. For subtraction and division, operand order
matters: `__rsub__` computes `other - self`, and `__rtruediv__` computes
`other / self`.

`/` uses `__truediv__`; `//` uses a separate method, `__floordiv__`. Here,
`wallet / 2` contains `5.0` because dividing the stored integers with `/` produces
a float. Dividing by zero raises `ZeroDivisionError` as usual.

---

### Containers and Iteration

| Method | Triggered by | Purpose |
|---|---|---|
| `__len__` | `len(obj)` | Length |
| `__getitem__` | `obj[index]` | Indexing |
| `__setitem__` | `obj[index] = value` | Setting by index/key |
| `__contains__` | `item in obj` | Membership test |
| `__iter__` | `for item in obj` | Start iteration |
| `__next__` | `next(iterator)` | Get the next item |

Example:

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]


playlist = Playlist(["Song A", "Song B"])

print(len(playlist))
print(playlist[0])
```

Output:

```text
2
Song A
```

Because `Playlist` defines `__getitem__`, Python also knows how to loop over it
by index:

```python
for song in playlist:
    print(song)
```

---

### Callable Objects

| Method | Triggered by | Purpose |
|---|---|---|
| `__call__` | `obj(...)` | Make an object act like a function |

Example:

```python
class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting

    def __call__(self, name):
        return f"{self.greeting}, {name}!"


hello = Greeter("Hello")

print(hello("Ada"))
```

Output:

```text
Hello, Ada!
```

---

## Context Manager Dunders: `__enter__` and `__exit__`

The `with` statement also uses standard dunder methods.

When Python sees:

```python
with resource as value:
    ...
```

it uses the **context manager protocol**:

1. Call `resource.__enter__()` at the start.
2. Assign the return value to `value`.
3. Run the code inside the `with` block.
4. Call `resource.__exit__(...)` at the end, even if an error happened.

Example:

```python
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        print(f"Opening connection to {self.db_name}")
        return self

    def execute(self, query):
        print(f"Running query: {query}")

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing connection to {self.db_name}")


with DatabaseConnection("Production_DB") as db:
    db.execute("SELECT * FROM users")
```

Output:

```text
Opening connection to Production_DB
Running query: SELECT * FROM users
Closing connection to Production_DB
```

The biggest benefit is cleanup. `__exit__` runs even if something inside the
`with` block fails.

---

## `__exit__` and Errors

`__exit__` receives error information:

```python
def __exit__(self, exc_type, exc_value, traceback):
```

If no error happened, those values are `None`.

If an error happened, Python passes the error type, error object, and traceback.

```python
class Demo:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit")
        print(exc_type)
        print(exc_value)


try:
    with Demo():
        raise ValueError("Something went wrong")
except ValueError:
    print("error handled outside the with block")
```

Output includes:

```text
enter
exit
<class 'ValueError'>
Something went wrong
error handled outside the with block
```

By default, the error continues after `__exit__` runs. If `__exit__` returns
`True`, Python suppresses the error. Be careful with that because hiding errors
can make debugging harder.

---

## `contextlib.contextmanager`

For simple context managers, you do not always need a full class with
`__enter__` and `__exit__`.

Python's `contextlib.contextmanager` decorator lets you write setup and cleanup
in one function.

```python
from contextlib import contextmanager


@contextmanager
def database_connection(db_name):
    print(f"Opening connection to {db_name}")
    connection = f"Connection({db_name})"

    try:
        yield connection
    finally:
        print(f"Closing connection to {db_name}")


with database_connection("Production_DB") as conn:
    print(f"Using {conn}")
```

Output:

```text
Opening connection to Production_DB
Using Connection(Production_DB)
Closing connection to Production_DB
```

The code before `yield` acts like `__enter__`.

The code after `yield`, usually inside `finally`, acts like `__exit__`.

---

## Class Context Manager vs `contextmanager`

Use a class with `__enter__` and `__exit__` when:

- The object has several methods.
- The object keeps meaningful internal state.
- You want a reusable object type.
- You are building a larger abstraction.

Use `contextlib.contextmanager` when:

- The setup and cleanup are simple.
- You want fewer lines of code.
- The context manager is mostly one small workflow.

Both approaches use the same idea: setup at the start, cleanup at the end.

---

## Important Rules

1. Do not invent your own dunder names.
2. Use standard dunders Python already understands.
3. Prefer `__repr__` for debugging-friendly output.
4. Add `__str__` when you also want a more human-friendly display.
5. Use context managers for resources that must be cleaned up.
6. Use `contextlib.contextmanager` for simple setup/cleanup workflows.

---

## Quick Mental Model

Python syntax asks your object:

```text
Can you behave like this?
```

If the class defines the right dunder method, the answer is yes.

```text
obj1 + obj2     -> __add__
len(obj)        -> __len__
obj[index]      -> __getitem__
for item in obj -> __iter__
with obj        -> __enter__ and __exit__
obj()           -> __call__
```

That is why dunder methods are powerful: they let your own classes participate
in normal Python syntax.
