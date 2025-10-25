# Designing Python API, APIs

Designing great Python APIs is all about creating interfaces that hide complexity while providing powerful, intuitive
functionality. Here's a comprehensive guide to building APIs that are simple, reusable, and effective.
 
Here showing **both versions** code:
(1) **without encapsulation** (where internal details are exposed), and  
(2) **with encapsulation** (where the same API is refactored into a clean, user-friendly interface).

## 1. Encapsulation — Hiding Internal Logic

### Without Encapsulation (Exposed Internals)

```python
class DataProcessor:
    def __init__(self):
        self.raw_data = []
        self.processed_data = []

    def load(self, data):
        self.raw_data = data  # User must remember to call load()

    def validate(self):
        # Validation logic here
        pass

    def transform(self):
        # Transformation logic here
        self.processed_data = [d * 2 for d in self.raw_data]
```

**Problems:**

- User must manually call steps in the right order (`load`, then `validate`, then `transform`).
- Internal state (`raw_data`, `processed_data`) is publicly accessible and modifiable.
- The API exposes implementation details — users might misuse them (e.g. skip `validate()`).

***

### With Encapsulation (Safe Interface)

```python
class DataProcessor:
    def __init__(self):
        self._raw_data = []  # _single underscore means internal use
        self._processed_data = []

    def process(self, data):
        """Public, single-step entrypoint."""
        self._load(data)
        self._validate()
        self._transform()
        return self._processed_data

    # Internal helper methods (using underscore to mark private)
    def _load(self, data):
        self._raw_data = data

    def _validate(self):
        pass

    def _transform(self):
        self._processed_data = [d * 2 for d in self._raw_data]
```

**Notes:**

- `_method` → private **by convention**; signals “for internal use only” (Python doesn’t strictly enforce access).[6][9]
- Hides intermediate steps (`_load`, `_validate`) from API consumers.
- The user only interacts with `process()`, ensuring correct order and context.

***

## 2. Properties for Controlled Attribute Access

### Without Encapsulation

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

**Issues:**

- Direct access means no validation or formatting logic possible.
- Users could set `email = "not-an-email"` without errors.

***

### With Encapsulation Using `@property`

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self._email = email  # protected attribute

    @property
    def email(self):
        """Get email as read-only property."""
        return self._email.lower()  # auto-normalize

    @email.setter
    def email(self, value):
        """Perform validation before assignment."""
        if '@' not in value:
            raise ValueError("Invalid email address")
        self._email = value
```

**Notes:**

- `@property` makes `user.email` look like an attribute while invoking method logic behind the scenes.
- Adds validation, formatting, and control — without changing the external usage syntax.
- Combined with `@<name>.setter`, this supports safe write access.

***

## 3. Context Managers — Managed Resources

### Without Encapsulation

```python
file = open("data.txt", "r")
contents = file.read()
file.close()  # Risky: user might forget to close
```

### With Encapsulation (`__enter__` / `__exit__`)

```python
class FileHandler:
    def __enter__(self):
        self.file = open("data.txt", "r")
        return self.file  # returned object used in 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()  # automatic cleanup


with FileHandler() as f:
    contents = f.read()  # Automatically closed after
```

**Notes:**

- `__enter__` and `__exit__` implement the **Context Manager Protocol**.
- `with` ensures cleanup even if exceptions occur.
- A key part of Pythonic API design — hides resource-management details.

***

## 4. Iterators — Natural Data Access

### Without Encapsulation

```python
class Numbers:
    def __init__(self, n):
        self.values = list(range(n))  # exposed list
```

**Issue:** The user must manage iteration manually:

```python
nums = Numbers(5)
for value in nums.values:
    print(value)
```

### With Encapsulation

```python
class Numbers:
    def __init__(self, n):
        self._values = list(range(n))

    def __iter__(self):  # allows "for x in Numbers(...)"
        for item in self._values:
            yield item
```

**Notes:**

- `__iter__()` turns objects into native iterables.
- No direct data exposure; returns values safely while hiding structure.
- Keeps behavior flexible (e.g., lazy data fetching).

***

## 5. Fluent APIs (Chained Calls)

### Without Encapsulation

```python
class QueryBuilder:
    def __init__(self):
        self.wheres = []
        self.orders = []

    def where(self, field, value):
        self.wheres.append((field, value))

    def order_by(self, field):
        self.orders.append(field)
```

**Problem:**  
You can’t chain calls naturally, so users must call step-by-step.

### With Encapsulation

```python
class QueryBuilder:
    def __init__(self):
        self._wheres = []
        self._orders = []

    def where(self, field, value):
        self._wheres.append((field, value))
        return self  # enables chaining

    def order_by(self, field):
        self._orders.append(field)
        return self
```

**Notes:**

- Returning `self` allows syntax like:  
  `query.where("age", ">18").order_by("created_at")`.
- This makes complex logic expressive and compact — a hallmark of high‑quality APIs.

***

## 6. Facade Pattern — Simplify Complex Systems

### Without Encapsulation

```python
audio = AudioProcessor()
metadata = MetadataExtractor()

decoded = audio.decode("song.mp3")
normalized = audio.normalize(decoded)
processed = audio.apply_effects(normalized, ["reverb"])
encoded = audio.encode(processed, "wav")
metadata.update(encoded)
```

**Problem:** Too many steps for the user — they must understand internal structure.

### With Encapsulation (Using Facade)

```python
class MediaConverter:
    def convert(self, file, fmt):
        """Simple Facade — hides internal complexity."""
        self._decode(file)
        self._normalize()
        self._encode(fmt)
```

**Notes:**

- The **Facade pattern** unifies multiple subsystems into one coherent interface.
- Exposes one public API, wrapping multiple private helpers.

***

## 7. REST Example — Structured Encapsulation

### Without Encapsulation (Tight Coupling)

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if '@' not in data['email']:
        return {"error": "invalid"}, 400
    # direct logic inside route
    return {"ok": True}
```

### With Encapsulation (Service Layer)

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserModel(BaseModel):
    email: EmailStr
    name: str


class UserService:
    """Encapsulates business logic."""

    def create(self, user: UserModel):
        # Implementation hidden from route
        return {"user": user}


service = UserService()


@app.post("/users")
def create_user(user: UserModel):
    return service.create(user)
```

**Notes:**

- Keeps endpoints lightweight — business rules live within `UserService`.
- Makes logic testable and reusable.
- Pydantic handles validation automatically using type annotations.

***

## Comparison Table

| Concept             | Without Encapsulation          | With Encapsulation                      |
|---------------------|--------------------------------|-----------------------------------------|
| Data Access         | Public variables (`obj.value`) | Controlled with `_value` or `@property` |
| Workflow            | Many manual steps              | One intuitive entrypoint (`process()`)  |
| Resource Management | Must manually manage           | Automatic via context managers          |
| Reusability         | Poor                           | Modular and safe                        |
| Code Maintenance    | Tight coupling                 | Clean separation of concerns            |
| API Usability       | Verbose and fragile            | Simple, elegant, and robust             |

***

By contrasting raw and encapsulated implementations, it becomes clear that **encapsulation transforms low-level
operations into approachable, fail-safe APIs**. The goal isn’t to prevent access but to **guide developers toward
correct, intuitive use** — ensuring they spend time *using* your API, not *learning* it.[9][6]

[1](https://auth0.com/blog/developing-restful-apis-with-python-and-flask/)
[2](https://zato.io/en/tutorials/rest-api/python.html)
[3](https://realpython.com/api-integration-in-python/)
[4](https://stackoverflow.com/questions/36008595/how-to-design-a-library-public-api-avoiding-to-expose-internals)
[5](https://www.freecodecamp.org/news/rest-api-design-best-practices-build-a-rest-api/)
[6](https://www.machinelearningplus.com/python/why-python-lacks-traditional-oop-encapsulation/)
[7](https://www.reddit.com/r/learnprogramming/comments/zoegcd/isnt_encapsulation_pointless_because_we_have/)
[8](https://stackoverflow.com/questions/41086827/understanding-data-encapsulation-in-python)
[9](https://breadcrumbscollector.tech/encapsulation-is-your-friend-also-in-python/)