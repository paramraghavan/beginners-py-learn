# `__new__` and `__init__`
- Differences between `__new__` and `__init__` in Python 
- How they work together in object creation.

1. `__new__(cls)`:

```python
def __new__(cls):
    # Create and return the instance
    return super().__new__(cls)
```

- This is the first step in object creation
- It's a static method (though you don't need to decorate it with @staticmethod)
- Receives the class (`cls`) as its first argument
- Called BEFORE `__init__`
- Responsible for creating and returning the new instance
- **Rarely overridden unless you need to customize instance creation**
- Common use cases include:
    - Implementing singletons
    - Modifying instance creation
    - Creating immutable objects

2. `__init__(self)`:

```python
def __init__(self):
    # Initialize the instance
    self.name = "default"
```

- `__init__` is called after `__new__`
- Receives the instance (`self`) created by `__new__`
- Used to initialize the instance attributes
- Cannot return any value (must return None)
- Commonly overridden to set up new objects
- Used for setting initial state of the object

Here's a complete example showing both methods in action:

```python
class Example:
    def __new__(cls, *args, **kwargs):
        print("1. __new__() called")
        # Create and return the instance
        instance = super().__new__(cls)
        print("2. Instance created")
        return instance

    def __init__(self, value=None):
        print("3. __init__() called")
        # Initialize the instance
        self.value = value
        print("4. Instance initialized")


# Creating an instance
obj = Example("test")
```

Output:

```
1. __new__() called
2. Instance created
3. __init__() called
4. Instance initialized
```

**Real-world Usage:**

1. Singleton Pattern:

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # This will be called every time but instance remains same
        pass
```

2. Immutable Object:

```python
class ImmutablePoint:
    def __new__(cls, x, y):
        instance = super().__new__(cls)
        # Set attributes directly in __new__
        instance._x = x
        instance._y = y
        return instance

    def __init__(self, x, y):
        # No initialization needed as it's done in __new__
        pass

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
```

3. Type Checking and Validation:

```python
class PositiveNumber:
    def __new__(cls, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number")
        if value <= 0:
            raise ValueError("Value must be positive")
        instance = super().__new__(cls)
        instance._value = value
        return instance

    def __init__(self, value):
        # Value already validated and set in __new__
        pass
```

Key points to remember:

1. `__new__` creates the instance, `__init__` initializes it
2. `__new__` must return an instance
3. `__init__` is called automatically with the instance returned by `__new__`
4. `__init__` cannot return any value
5. Most classes only need to override `__init__`
6. Override `__new__` when you need to control instance creation itself