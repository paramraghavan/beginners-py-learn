# Context Manager & __getattr__ - Detailed Explanation

Clear, practical explanations with step-by-step execution and real-world examples.

---

## Part 1: Context Manager Hook (Lifecycle)

### What It Does

A context manager ensures **setup happens before** and **cleanup happens after**, **even if errors occur**.

### The Two Methods

```python
class ResourceManager:
    def __enter__(self):
        """Called when entering 'with' block"""
        print("1. SETUP - Acquiring resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block (even on error!)"""
        print("4. CLEANUP - Releasing resource")
        return False  # False = don't suppress exceptions
```

### Step-by-Step Execution

```python
with ResourceManager() as rm:
    print("2. USING resource")
    print("3. Still using")
    # Exception could happen here

# Output (NO ERROR):
# 1. SETUP - Acquiring resource
# 2. USING resource
# 3. Still using
# 4. CLEANUP - Releasing resource

# Output (WITH ERROR - cleanup still runs!):
# 1. SETUP - Acquiring resource
# 2. USING resource
# 3. Still using
# ERROR HAPPENS HERE
# 4. CLEANUP - Releasing resource  <-- This still runs!
# Then error is raised
```

### Real-World Example 1: File Handling

```python
class SafeFile:
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file  # Return the file object

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing file: {self.filename}")
        if self.file:
            self.file.close()  # Always close, even on error

        if exc_type:
            print(f"Error occurred: {exc_type.__name__}")
        return False  # Don't suppress the error

# Usage
with SafeFile('data.txt', 'w') as f:
    f.write("Hello")
    f.write("World")
    # ERROR could happen here

# Output:
# Opening file: data.txt
# Closing file: data.txt    <-- Always happens!
```

**What it solves:**
- Without context manager: You might forget `f.close()`
- With context manager: Close is **guaranteed** to happen

### Real-World Example 2: Database Transaction

```python
class DatabaseTransaction:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        print("BEGIN TRANSACTION")
        self.db.begin()  # Start transaction
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No error - commit changes
            print("COMMIT - All changes saved")
            self.db.commit()
        else:
            # Error occurred - undo everything
            print(f"ROLLBACK - Error: {exc_type.__name__}")
            self.db.rollback()

        return False  # Don't suppress error

# Usage
class MockDB:
    def begin(self): print("  db.begin()")
    def commit(self): print("  db.commit()")
    def rollback(self): print("  db.rollback()")
    def insert(self, data): print(f"  inserting {data}")

db = MockDB()

print("SCENARIO 1: Success")
with DatabaseTransaction(db) as t:
    db.insert("record1")
    db.insert("record2")
    # Success - commits

# Output:
# BEGIN TRANSACTION
#   db.begin()
#   inserting record1
#   inserting record2
# COMMIT - All changes saved
#   db.commit()

print("\nSCENARIO 2: Error")
try:
    with DatabaseTransaction(db) as t:
        db.insert("record1")
        raise ValueError("Invalid data!")  # ERROR
        db.insert("record2")  # Never reached
except ValueError:
    pass

# Output:
# BEGIN TRANSACTION
#   db.begin()
#   inserting record1
# ROLLBACK - Error: ValueError
#   db.rollback()
```

**What it solves:**
- Ensures database transactions either complete or rollback completely
- No partial updates on error

### Real-World Example 3: Lock/Unlock

```python
import time

class LockManager:
    def __init__(self, resource_name):
        self.resource = resource_name
        self.locked = False

    def __enter__(self):
        print(f"🔒 Locking: {self.resource}")
        self.locked = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"🔓 Unlocking: {self.resource}")
        self.locked = False
        if exc_type:
            print(f"   (After error: {exc_type.__name__})")
        return False

# Usage
print("Using shared resource...")
with LockManager("database"):
    print("  [locked] Making changes...")
    time.sleep(0.5)
    print("  [locked] Still working...")
# [Auto-unlocks here]
print("Resource unlocked")

# Output:
# Using shared resource...
# 🔒 Locking: database
#   [locked] Making changes...
#   [locked] Still working...
# 🔓 Unlocking: database
# Resource unlocked
```

**What it solves:**
- Lock is always released, even if code crashes
- Prevents deadlocks

---

## Part 2: `__getattr__` Hook (Dynamic Attributes)

### What It Does

`__getattr__` is called when you try to access an attribute that **doesn't exist**.

It allows you to **create attributes on the fly** without defining them ahead of time.

### The Basic Idea

```python
class DynamicObject:
    def __getattr__(self, name):
        # Called ONLY when attribute is missing
        print(f"Someone asked for: {name}")
        return f"<Default value for {name}>"

obj = DynamicObject()

# These don't exist, so __getattr__ is called:
print(obj.username)   # Prints: Someone asked for: username
print(obj.token)      # Prints: Someone asked for: token
print(obj.config)     # Prints: Someone asked for: config

# If we set it, __getattr__ is NOT called:
obj.username = "alice"
print(obj.username)   # No print, just returns "alice"
```

### Real-World Example 1: REST API Client

Problem: An API has hundreds of endpoints. Can't define them all.

```python
class RestAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def __getattr__(self, endpoint_name):
        # Called when you access a non-existent endpoint
        print(f"Creating endpoint handler for: {endpoint_name}")

        def api_call(*args, **kwargs):
            url = f"{self.base_url}/{endpoint_name}"
            print(f"  GET {url}")
            return f"Response from {endpoint_name}"

        return api_call

# Usage
api = RestAPI("https://api.example.com")

# All these dynamically create endpoints:
api.users()           # Creates /users endpoint
api.products()        # Creates /products endpoint
api.orders()          # Creates /orders endpoint
api.inventory()       # Creates /inventory endpoint

# Output:
# Creating endpoint handler for: users
#   GET https://api.example.com/users
# Creating endpoint handler for: products
#   GET https://api.example.com/products
```

### Real-World Example 2: Configuration Object

Problem: Config has many optional properties we don't know in advance.

```python
class Config:
    def __init__(self, defaults):
        self._values = defaults

    def __getattr__(self, key):
        # Return value from dict, or a default
        if key.startswith('_'):
            # Don't intercept private attributes
            raise AttributeError(f"No attribute {key}")

        print(f"Getting config: {key}")
        return self._values.get(key, "NOT_SET")

# Usage
config = Config({
    'database_host': 'localhost',
    'database_port': 5432,
    'api_key': 'secret123'
})

print(config.database_host)   # Gets from dict
print(config.database_port)   # Gets from dict
print(config.timeout)         # Not in dict, returns "NOT_SET"
print(config.max_retries)     # Not in dict, returns "NOT_SET"

# Output:
# Getting config: database_host
# localhost
# Getting config: database_port
# 5432
# Getting config: timeout
# NOT_SET
# Getting config: max_retries
# NOT_SET
```

### Real-World Example 3: Proxy Object

Problem: Need to track all attribute accesses to an object.

```python
class TrackedProxy:
    def __init__(self, obj):
        self._obj = obj
        self._accesses = []

    def __getattr__(self, name):
        # Track that this attribute was accessed
        print(f"✓ Accessed: {name}")
        self._accesses.append(name)

        # Return the actual attribute from wrapped object
        return getattr(self._obj, name)

    def show_accesses(self):
        print(f"Attributes accessed: {self._accesses}")

# Usage
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
tracked = TrackedProxy(person)

# All accesses are tracked:
print(tracked.name)     # Tracked
print(tracked.age)      # Tracked
print(tracked.name)     # Tracked again

tracked.show_accesses()

# Output:
# ✓ Accessed: name
# Alice
# ✓ Accessed: age
# 30
# ✓ Accessed: name
# Alice
# Attributes accessed: ['name', 'age', 'name']
```

---

## Comparison: When to Use Each

### Use `__getattr__` When:
✅ You have **many possible attributes** you can't define ahead of time
✅ You need **dynamic/flexible** behavior
✅ You're building a **proxy** or **wrapper**
✅ Attribute doesn't exist → create it on demand

**Examples:**
- REST API clients
- Configuration objects
- Dynamic proxies
- Attribute forwarding

### Use Context Manager When:
✅ You need **setup and cleanup** logic
✅ You want to ensure **cleanup even on error**
✅ You're managing **resources** (files, connections, locks)
✅ You need **transactional behavior**

**Examples:**
- File handling
- Database transactions
- Lock/unlock
- Memory cleanup

---

## Step-by-Step Detailed Examples

### Context Manager: Detailed Flow

```python
class DetailedManager:
    def __init__(self, name):
        self.name = name
        print(f"[INIT] Creating {name}")

    def __enter__(self):
        print(f"[ENTER] Starting {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[EXIT] Finishing {self.name}")
        if exc_type:
            print(f"[EXIT] Exception: {exc_type.__name__}: {exc_val}")
        return False

print("=== SCENARIO 1: No Error ===")
with DetailedManager("Operation1"):
    print("  [BODY] Running code")

# Output:
# [INIT] Creating Operation1
# [ENTER] Starting Operation1
#   [BODY] Running code
# [EXIT] Finishing Operation1

print("\n=== SCENARIO 2: With Error ===")
try:
    with DetailedManager("Operation2"):
        print("  [BODY] Running code")
        raise ValueError("Something failed!")
        print("  [BODY] This never runs")
except ValueError:
    print("  [CAUGHT] Error caught outside")

# Output:
# [INIT] Creating Operation2
# [ENTER] Starting Operation2
#   [BODY] Running code
# [EXIT] Finishing Operation2
# [EXIT] Exception: ValueError: Something failed!
#   [CAUGHT] Error caught outside
```

### `__getattr__`: Detailed Flow

```python
class DetailedGetattr:
    def __init__(self):
        self.real_attr = "I exist"
        print("[INIT] Created object")

    def __getattr__(self, name):
        print(f"[GETATTR] Attribute '{name}' not found, creating...")
        return f"Dynamic value for {name}"

obj = DetailedGetattr()

print("\n=== Accessing EXISTING attribute ===")
print(obj.real_attr)  # NO __getattr__ call!
# Output:
# I exist

print("\n=== Accessing MISSING attribute ===")
print(obj.missing)    # __getattr__ IS called!
# Output:
# [GETATTR] Attribute 'missing' not found, creating...
# Dynamic value for missing

print("\n=== Setting attribute ===")
obj.new_attr = "I set this"
print(obj.new_attr)   # NO __getattr__ call (already exists)!
# Output:
# I set this
```

---

## Key Differences Summary

| Feature | Context Manager | `__getattr__` |
|---------|-----------------|--------------|
| **When called** | Entering/exiting `with` block | Accessing missing attribute |
| **Purpose** | Setup/cleanup | Dynamic attributes |
| **Error handling** | Can catch and cleanup | Just returns value |
| **Guarantees** | Exit **always** runs | Only called if missing |
| **Common use** | Files, DB, locks | APIs, proxies, config |

---

## Common Mistakes & Fixes

### Context Manager Mistake 1: Forgetting return value

```python
# ❌ WRONG
def __enter__(self):
    self.resource = acquire()
    # Missing: return self

# ✅ CORRECT
def __enter__(self):
    self.resource = acquire()
    return self  # Return what you want to bind to 'as'
```

### Context Manager Mistake 2: Suppressing errors by mistake

```python
# ❌ WRONG - Error is hidden!
def __exit__(self, exc_type, exc_val, exc_tb):
    self.cleanup()
    return True  # Returns True = suppress exception

# ✅ CORRECT - Error propagates
def __exit__(self, exc_type, exc_val, exc_tb):
    self.cleanup()
    return False  # Returns False = don't suppress
```

### `__getattr__` Mistake 1: Infinite recursion

```python
# ❌ WRONG - Infinite loop!
def __getattr__(self, name):
    return self.name  # Accessing self.name calls __getattr__ again!

# ✅ CORRECT - Use object.__getattribute__
def __getattr__(self, name):
    return object.__getattribute__(self, name)
```

### `__getattr__` Mistake 2: Not checking for private attributes

```python
# ❌ WRONG - Can't use dir() or inspect
class BadAPI:
    def __getattr__(self, name):
        return "something"

obj = BadAPI()
dir(obj)  # Hangs or returns garbage!

# ✅ CORRECT - Block private attributes
def __getattr__(self, name):
    if name.startswith('_'):
        raise AttributeError(f"No {name}")
    return "something"
```

---

## Summary

### Context Manager: **Lifecycle Management**
- ✅ `__enter__` = setup (acquire resources)
- ✅ `__exit__` = cleanup (release resources)
- ✅ Cleanup **always** happens, even on error
- ✅ Use for: files, databases, locks, transactions

```python
with Manager() as m:
    use_resource()
# Cleanup guaranteed here
```

### `__getattr__`: **Dynamic Attributes**
- ✅ Called when attribute **doesn't exist**
- ✅ Returns dynamically generated value
- ✅ Allows flexible/extensible objects
- ✅ Use for: APIs, proxies, configuration

```python
obj.missing_attribute  # __getattr__ creates it dynamically
```

