# Public, Protected and Private
The short answer is: **No, not strictly.** Unlike languages like Java or C++, Python does not have true "private" or "
protected" keywords that physically block access to data. In Python, everything is technically **public**.

Instead, Python relies on **naming conventions** and the "consenting adults" philosophy—the idea that the language won't
stop you from breaking things, but it expects you to follow the rules of the road.

---

### The Three "Levels" of Access

| Level         | Convention | What it tells other programmers                                      |
|:--------------|:-----------|:---------------------------------------------------------------------|
| **Public**    | `name`     | "Go ahead and use this; it's part of the API."                       |
| **Protected** | `_name`    | "This is internal. Don't touch it unless you're a subclass."         |
| **Private**   | `__name`   | "This is super-internal. I'm going to make it hard for you to find." |

---

### 1. Public (Default)

Any variable or method without leading underscores is public.

```python
class Car:
    def __init__(self):
        self.brand = "Tesla"  # Public
```

### 2. Protected (`_single_underscore`)

Adding one underscore is a **hint** to other developers. It doesn't actually change how the code runs, but it serves as
a "Do Not Enter" sign.

* **Behavior:** You can still access it from outside the class (e.g., `my_car._engine_temp`), but it’s considered bad
  practice and "rude."

```python
class Car:
    def __init__(self):
        self._engine_temp = 90  # Protected: Intended for internal/subclass use only
```

### 3. Private (`__double_underscore`)

When you use two underscores, Python performs **Name Mangling**. It doesn't actually make the variable invisible, but it
renames it behind the scenes to prevent accidental overrides in subclasses.

* **Behavior:** If you try to access `my_car.__serial_number`, you will get an `AttributeError`.
* **The "Secret":** You can still access it if you use the mangled name: `_ClassName__variableName` (e.g.,
  `my_car._Car__serial_number`).

---

### Summary Example

```python
class SecretAgent:
    def __init__(self):
        self.name = "Bond"  # Public
        self._id = "007"  # Protected (By convention)
        self.__password = "shaken_not_stirred"  # Private (Name Mangled)


agent = SecretAgent()

print(agent.name)  # Works: Bond
print(agent._id)  # Works: 007 (but your IDE might complain)
# print(agent.__password) # ERROR: AttributeError
print(agent._SecretAgent__password)  # Works: Accessing the "mangled" name
```

### Why does Python do this?

Python values **transparency and debugging** over strict encapsulation. The creator, Guido van Rossum, famously said, *"
We’re all consenting adults here."* If a developer really needs to reach inside an object to fix a bug or monkey-patch a
feature, the language allows it.
