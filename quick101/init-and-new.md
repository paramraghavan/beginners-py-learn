# `__new__` and `__init__`

When you first learn Python classes, you mostly use `__init__`.

That is the right place to start.

Later, as you move from beginner Python into more advanced Python, you may see
another method: `__new__`.

They are related, but they do different jobs:

```text
__new__  -> creates the object
__init__ -> initializes the object after it exists
```

Most of the time, you only write `__init__`.

---

## Beginner Level: Start With `__init__`

For normal classes, use `__init__` to set up the object.

```python
class User:
    def __init__(self, name):
        self.name = name


user = User("Ada")
print(user.name)
```

Output:

```text
Ada
```

What happened?

1. Python created a new `User` object.
2. Python passed that object into `__init__` as `self`.
3. `__init__` added the `name` attribute.

For beginner and everyday Python, this is the most important idea:

```python
def __init__(self, ...):
    # Put starting values on self
```

Example:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance


account = BankAccount("Ada", 100)

print(account.owner)
print(account.balance)
```

Output:

```text
Ada
100
```

`__init__` is for normal setup: names, numbers, lists, configuration, validation,
and other starting state.

---

## Important Rule: `__init__` Returns Nothing

`__init__` must return `None`.

This is correct:

```python
class User:
    def __init__(self, name):
        self.name = name
```

This is wrong:

```python
class User:
    def __init__(self, name):
        self.name = name
        return self  # Error
```

You do not need to return the object. Python already has it.

---

## Intermediate Level: What Happens Before `__init__`?

When you write this:

```python
user = User("Ada")
```

Python roughly does this behind the scenes:

1. Call `User.__new__(User, "Ada")` to create the object.
2. If `__new__` returns a `User` object, call `__init__` on it.
3. Return the finished object and store it in `user`.

So the full object creation flow is:

```text
User("Ada")
    |
    v
__new__ creates the object
    |
    v
__init__ initializes the object
    |
    v
user gets the finished object
```

Here is a small demonstration:

```python
class Example:
    def __new__(cls, value):
        print("1. __new__ called")
        obj = super().__new__(cls)
        print("2. object created")
        return obj

    def __init__(self, value):
        print("3. __init__ called")
        self.value = value
        print("4. object initialized")


example = Example("hello")
```

Output:

```text
1. __new__ called
2. object created
3. __init__ called
4. object initialized
```

This example is mainly for learning. In real code, you usually would not write
`__new__` for a normal class like this.

---

## What Is `__new__`?

`__new__` is the method responsible for creating the object.

```python
class User:
    def __new__(cls, name):
        print("__new__ creates the object")
        return super().__new__(cls)

    def __init__(self, name):
        print("__init__ initializes the object")
        self.name = name


user = User("Ada")
```

Output:

```text
__new__ creates the object
__init__ initializes the object
```

Notice the first parameter:

```python
def __new__(cls, ...):
```

`cls` means "the class being created." For example, when you call `User("Ada")`,
`cls` is `User`.

`__new__` must return an object. Usually it returns:

```python
super().__new__(cls)
```

That asks Python's parent object system to create a normal empty instance.

---

## Gentle Transition: When Do You Need `__new__`?

Most classes should not define `__new__`.

Use `__init__` for this kind of work:

- Setting attributes
- Checking values
- Preparing lists, dictionaries, or other normal data
- Normal application classes

Use `__new__` only when you need to control object creation itself.

That usually means one of these advanced cases:

- You are subclassing an immutable built-in type like `str`, `int`, or `tuple`.
- You want to return an existing object instead of a new object.
- You are writing framework-level or metaprogramming code.

Now we are moving into the advanced part.

---

## Advanced Example 1: Subclassing an Immutable Type

Strings are immutable. Once a `str` object exists, you cannot change the actual
text inside it.

That means this idea does not work well in `__init__`:

```python
class LowercaseString(str):
    def __init__(self, value):
        # Too late: the string value already exists.
        pass
```

If you want to control the actual string value, you must do it while the object
is being created. That means `__new__`.

```python
class LowercaseString(str):
    def __new__(cls, value):
        return super().__new__(cls, value.lower())


name = LowercaseString("ADA")
print(name)
```

Output:

```text
ada
```

This works because `__new__` creates the `str` object with the lowercase value
from the beginning.

---

## Advanced Example 2: Returning an Existing Object

Normally, every class call creates a new object:

```python
class User:
    pass


a = User()
b = User()

print(a is b)
```

Output:

```text
False
```

But `__new__` can return an object that already exists.

```python
class OnlyOne:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


a = OnlyOne()
b = OnlyOne()

print(a is b)
```

In this example, `_instance` is a class variable:

```python
class OnlyOne:
    _instance = None
```

It belongs to the class `OnlyOne`, not to one individual object. That is why all
calls to `OnlyOne()` can share the same stored object.

The leading underscore in `_instance` is a naming convention. It means "this is
for internal use," but it does not make the variable truly private.

Output:

```text
True
```

Both `a` and `b` refer to the same object.

This is a singleton-like pattern. It is useful to understand, but use it
carefully. In many programs, a normal object or a module-level variable is
simpler and easier to test.

---

## Advanced Example 3: Validation in the Right Place

Do not put normal validation in `__new__` just because `__new__` runs first.

For regular classes, validate in `__init__`:

```python
class PositiveNumber:
    def __init__(self, value):
        if value <= 0:
            raise ValueError("value must be positive")
        self.value = value
```

That is simple and correct.

Use `__new__` for validation only when the value must be checked before the
object can be created, usually with immutable types.

```python
class PositiveInt(int):
    def __new__(cls, value):
        if value <= 0:
            raise ValueError("value must be positive")
        return super().__new__(cls, value)


number = PositiveInt(10)
print(number)
```

Output:

```text
10
```

Here, `PositiveInt` is an `int`, and integers are immutable. So the value must be
accepted or rejected while the object is being created.

---

## Key Points

Beginner level:

1. Use `__init__` for most classes.
2. `__init__` receives `self`, the object Python already created.
3. `__init__` sets starting attributes.
4. `__init__` must return `None`.

Advanced level:

1. `__new__` creates the object before `__init__` runs.
2. `__new__` receives `cls`, the class being created.
3. `__new__` must return an object.
4. Override `__new__` only when you need to control object creation itself.
5. Common `__new__` cases include immutable types, object reuse, and framework code.

---

## Advanced Note: Thread Safety

The `OnlyOne` example above is simplified. It is not thread-safe.

If multiple threads call `OnlyOne()` at the same time, this can happen:

1. Thread A checks `_instance is None`.
2. Thread B also checks `_instance is None`.
3. Both threads create an object.

That means two objects could be created before `_instance` is fully shared.

In multi-threaded code, protect the creation step with a lock:

```python
import threading


class OnlyOne:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
```

For a beginner lesson, the simple singleton-like example is useful for
understanding `__new__`. For real multi-threaded programs, use a lock or choose a
simpler design when possible.
