In Python, **attribute management** refers to how attributes (variables or properties) of a class instance are accessed,
modified, or deleted. Normally, attributes are accessed directly, but using **dunder methods**
like `__getattr__`, `__getattribute__`, `__setattr__`, and `__delattr__`, you can **intercept and control** these
actions dynamically.


## Normal Attribute Access (Default Behavior)

By default, Python handles attributes automatically using the class’s internal `__dict__`, which stores all values.

### Example (Normal Class)

```python
class NormalPerson:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# Usage
p = NormalPerson("Alice", 30)
print(p.name)  # Direct access
p.age = 31  # Direct modification
del p.name  # Attribute deleted directly
```

### Explanation

- No control over how attributes are changed or deleted.
- No way to automatically validate data or log changes.
- Python internally retrieves attributes from the object’s `__dict__`.

This approach is simple but **not flexible** for use cases that need validation, auto-logging, or computed attributes.

***

## Attribute Management with Dunder Methods

Dunder methods allow fine-grained control over attribute access, retrieval, and deletion.[6][1]

### Example (Using Attribute Management)

```python
class ManagedPerson:
    def __init__(self, name, age):
        super().__setattr__('name', name)
        super().__setattr__('age', age)

    def __getattr__(self, attr):
        print(f"'{attr}' not found!")
        return None

    def __setattr__(self, attr, value):
        print(f"Setting {attr} to {value}")
        if attr == "age" and value < 0:
            raise ValueError("Age cannot be negative")
        super().__setattr__(attr, value)

    def __delattr__(self, attr):
        print(f"Deleting attribute '{attr}'")
        super().__delattr__(attr)


# Usage
p = ManagedPerson("Alice", 30)
print(p.name)  # Normal access
p.age = 25  # Controlled setting
print(p.height)  # Attribute doesn't exist -> handled by __getattr__
del p.name  # Controlled deletion
```

### Explanation

- `__getattr__`: Triggered **only when** the attribute doesn’t exist.  
  Example: Accessing `p.height` prints `‘height’ not found!`.
- `__setattr__`: Called whenever you assign an attribute, letting you validate or log values.
- `__delattr__`: Called when deleting attributes.
- `super().__setattr__` is used to prevent infinite recursion—because calling `self.attr = value` inside `__setattr__`
  would call `__setattr__` again.

***

## Key Differences

| Feature                     | Normal Class            | With Attribute Management                             |
|-----------------------------|-------------------------|-------------------------------------------------------|
| Attribute validation        | Not possible            | Easily enforced (e.g. prevent invalid ages) [1]       |
| Handling missing attributes | Raises `AttributeError` | Custom handling through `__getattr__` [5]             |
| Logging or auditing         | Must add manually       | Automatic via `__setattr__` [6]                       |
| Deletion control            | Deletes silently        | Can intercept and restrict with `__delattr__` [1]     |
| Flexibility                 | Limited                 | High – supports validation, computed fields, defaults |

***

### Practical Use of Attribute Management

Dunder methods for attributes are useful in:

- **Data validation** (e.g., ensuring only valid data is set)
- **Automatic default values** for missing attributes
- **Logging or debugging** attribute changes
- **Property emulation** without using decorators
- **Frameworks** like Django ORM and Pydantic for dynamic attributes
