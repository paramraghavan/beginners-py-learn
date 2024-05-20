In Python, __repr__ and __str__ are special methods used to define string representations of objects. Both methods are
used to provide a string representation, but they serve different purposes and are used in different contexts.

## __repr__

- Purpose: The goal of __repr__ is to provide an "official" string representation of an object that can ideally be used to
recreate the object. It is more for developers and debugging.
- Usage: When you call repr() on an object or print an object in an interactive shell, the __repr__ method is used.
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

p = Point(1, 2)
print(repr(p))  # Output: Point(1, 2)

```

## __str__

In Python, you can add a __str__ method to your class to define how an instance of the class should be converted to a
string, similar to the toString method in Java. Here's an example:

- Purpose: The goal of __str__ is to provide a "nicely printable" string representation of an object, which is more
user-friendly. It is more for end-users.
- Usage: When you call str() on an object or use print() to display an object, the __str__ method is used.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

p = Point(1, 2)
print(str(p))  # Output: (1, 2)
print(p)       # Output: (1, 2)
```

## Summary

- __repr__: Aimed at developers. It is supposed to be unambiguous and, if possible, provide a string that can be used to
  recreate the object.
- __str__: Aimed at end-users. It is supposed to be readable and user-friendly.
- If __str__ is not defined, Python will use __repr__ as a fallback. However, the reverse is not true; if __repr__ is
  not defined, Python will use the default implementation provided by the base class.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

p = Point(1, 2)
print(repr(p))  # Output: Point(1, 2)
print(str(p))   # Output: (1, 2)
print(p)        # Output: (1, 2)

```