# Dunder

"Dunder" is short for **Double Underscore**. These are the methods that look like `__method__`. In the Python community,
they are officially called **Special Methods** or **Magic Methods**.

They are the "secret sauce" that allows your custom objects to interact with Python's built-in syntax (like `+`,
`len()`, or `print()`).

---

### 1. The Most Common Dunders

You likely use these every day without thinking about them as "magic."

| Method     | Triggered by...                  | Purpose                                                           |
|:-----------|:---------------------------------|:------------------------------------------------------------------|
| `__init__` | `ClassName()`                    | **Initializer:** Sets up the object's starting state.             |
| `__str__`  | `print(obj)` or `str(obj)`       | **User-friendly string:** What a human should see.                |
| `__repr__` | `repr(obj)` or Developer console | **Developer string:** A "code-like" representation for debugging. |
| `__len__`  | `len(obj)`                       | **Length:** Returns the size of your object.                      |

---

### 2. Making Objects "Act Like" Built-in Types

**The power of dunders is that they let your custom classes "mimic" integers, lists, or even functions.**

#### **Arithmetic (The Calculator Mimic)**

If you want to use the `+` operator between two objects, you define `__add__`.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # This triggers p1.__add__(p2)
```

#### **Container/Sequence (The List Mimic)**

If you want to access your object using square brackets `obj[0]`, you use `__getitem__`.

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __getitem__(self, index):
        return self.songs[index]


my_hits = Playlist(["Song A", "Song B"])
print(my_hits[0])  # Triggers __getitem__
```

---

### 3. Lifecycle & Context Dunders

These manage how an object lives and dies within your code.

* **`__call__`**: Makes your object **callable** like a function. If you run `my_obj()`, this method executes.
* **`__enter__` & `__exit__`**: These turn your object into a **Context Manager**. They are triggered when you use the
  `with` statement (great for closing files or database connections automatically).
* **`__iter__` & `__next__`**: These make your object **iterable**, allowing you to use it in a `for` loop.

Lifecycle and context dunders are the "hooks" Python uses to manage an object from the moment it is born to the moment
it is destroyed, as well as how it behaves inside a `with` block.

#### 1. The Lifecycle Dunders: `__init__` and `__del__`

These manage the "Birth" and "Death" of an object.

* **`__init__(self, ...)`**: The initializer. It runs immediately after the object is created to set up its initial
  state.
* **`__del__(self)`**: The destructor. It runs when the object is about to be destroyed (garbage collected). This is
  less commonly used because Python handles memory automatically, but it's useful for closing external resources like
  network sockets.

---

#### 2. The Context Dunders: `__enter__` and `__exit__`

These allow your object to work with the **`with`** statement. This is known as the **Context Management Protocol**.

* **`__enter__(self)`**: Runs at the start of the `with` block. It usually sets up a resource (like opening a file or
  connecting to a database) and returns the object to be used.
* **`__exit__(self, exc_type, exc_value, traceback)`**: Runs at the end of the `with` block, **even if an error occurred
  **. It’s used for cleanup (like closing the file or releasing a lock).

---

#### Full Example: A Database Connection Simulator

Imagine you want to ensure that every time you "connect" to a database, you definitely "disconnect," no matter what
happens in your code.

```python
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        print(f"1. [Lifecycle] __init__: Created object for {self.db_name}")

    def __enter__(self):
        print(f"2. [Context] __enter__: Opening connection to {self.db_name}")
        return self  # This is what the 'as' variable becomes

    def execute(self, query):
        print(f"3. [Action]: Executing '{query}'")
        # Uncomment the next line to see how __exit__ still runs during an error!
        # raise Exception("Query Failed!") 

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"4. [Context] __exit__: Closing connection to {self.db_name}")
        if exc_type:
            print(f"   (Note: Closed safely after error: {exc_val})")

    def __del__(self):
        print(f"5. [Lifecycle] __del__: Object for {self.db_name} is being deleted from memory")


# --- Using the class ---
with DatabaseConnection("Production_DB") as db:
    db.execute("SELECT * FROM users")

print("--- End of script ---")
```

### contextmanager

Using `contextlib` is the "Pythonic" way to create context managers without having to write a whole class with
`__enter__` and `__exit__` methods. It turns a simple **generator** into a fully functional context manager.

### The `contextmanager` Decorator

This approach is usually preferred for simple tasks because it keeps the setup and teardown logic in one continuous
block of code.

Here is how you would rewrite the Database example:

```python
from contextlib import contextmanager


@contextmanager
def database_connection(db_name):
    # --- This is the __enter__ part ---
    print(f"Connecting to {db_name}...")
    connection = f"Conn({db_name})"

    try:
        # The code inside the 'with' block runs here
        yield connection
    finally:
        # --- This is the __exit__ part ---
        # The 'finally' block ensures this runs even if an error occurs
        print(f"Closing connection to {db_name}...")


# Usage
with database_connection("Production_DB") as conn:
    print(f"Using {conn} to read data.")
    # If an error happened here, 'finally' would still catch it.
```

### Why use this over the Dunder Class?

1. **Less Boilerplate:** You don't need to define a class or remember the specific arguments for `__exit__` (like
   `exc_type`).
2. **Readability:** The "setup" is before the `yield`, and the "cleanup" is after the `yield`. It reads chronologically.
3. **State Management:** It’s easier to maintain local variables between the setup and teardown phases.

### When to stay with Dunder Methods?

If your context manager needs to hold a lot of internal state, have other methods (like our `db.execute()` example
earlier), or be part of a complex class hierarchy, the **Dunder Class** approach is still the better architectural
choice.



---

### 4. Important "Rules of the Road"

1. **Don't invent your own:** Only use the dunder names defined by Python. Creating `__my_cool_method__` is considered
   bad practice because Python might add a method with that name in a future version, breaking your code.
2. **`__str__` vs `__repr__`**: Always try to implement `__repr__` first. If `__str__` is missing, Python falls back to
   `__repr__`.
3. **The "Under the Hood" Truth**: When you call `len(my_list)`, Python actually calls `my_list.__len__()`. The built-in
   functions are just wrappers that make the code look cleaner.

---

> **Pro-Tip:** If you ever want to see every dunder method available to an object, run `dir(object_name)` in your
> terminal. You'll see a long list of all the "magic" it can perform.

