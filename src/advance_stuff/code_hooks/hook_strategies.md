# Python Hook Strategies - Concise Guide

Simple, practical techniques to intercept and modify Python code behavior without changing the source.

---

## 1. Decorator Hook (Most Common)

**What:** Wrap a function to add behavior before/after execution

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"← Returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)
# Output:
# → Calling add
# ← Returned 5
```

**Use Case:** Logging, timing, caching, error handling
**Scope:** Single function

---

## 2. Monkey Patching Hook (Global)

**What:** Replace a function/method at runtime to intercept all calls

```python
class Calculator:
    def add(self, a, b):
        return a + b

# Save original
_original_add = Calculator.add

# Create interceptor
def tracked_add(self, a, b):
    print(f"Adding {a} + {b}")
    result = _original_add(self, a, b)
    print(f"Result: {result}")
    return result

# Replace globally
Calculator.add = tracked_add

calc = Calculator()
calc.add(2, 3)  # Prints tracking info
```

**Use Case:** Library interception (like permission_analyzer_runtime with boto3)
**Scope:** All instances globally

**⚠️ Important:** Always save the original and restore when done:
```python
Calculator.add = _original_add  # Restore
```

---

## 3. Property Hook (Attribute Access)

**What:** Intercept getting/setting attributes with validation or logging

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        print(f"Reading balance: {self._balance}")
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        print(f"Setting balance to {value}")
        self._balance = value

account = BankAccount(1000)
print(account.balance)      # Triggers getter
account.balance = 2000      # Triggers setter
account.balance = -100      # Raises error
```

**Use Case:** Validation, computed properties, lazy loading
**Scope:** Single property

---

## 4. Context Manager Hook (Lifecycle)

**What:** Execute setup/cleanup code around a block, even on exceptions

```python
class ResourceTracker:
    def __enter__(self):
        print("✓ Acquiring resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("✓ Releasing resource")
        if exc_type:
            print(f"  Exception occurred: {exc_type.__name__}")
        return False  # Don't suppress exception

    def use(self):
        print("Using resource")

with ResourceTracker() as rt:
    rt.use()
    # Exception here?

# Output:
# ✓ Acquiring resource
# Using resource
# ✓ Releasing resource
```

**Use Case:** Resource management, transaction handling, tracking
**Scope:** Code block within `with` statement
**Benefit:** Cleanup guaranteed even if exception occurs

---

## 5. `__getattr__` Hook (Dynamic Attributes)

**What:** Create attributes on-the-fly when they're accessed

```python
class API:
    def __getattr__(self, name):
        # Called only for missing attributes
        print(f"Accessing missing: {name}")
        return f"<Value for {name}>"

api = API()
print(api.username)   # Prints: Accessing missing: username
print(api.token)      # Prints: Accessing missing: token
print(api.config)     # Prints: Accessing missing: config
```

**Use Case:** Dynamic REST APIs, proxies, flexible objects
**Scope:** Missing attributes only (not found ones)
**Note:** Only called if attribute doesn't exist

---

## Quick Comparison

| Hook | How | Best For | Performance |
|------|-----|----------|-------------|
| **Decorator** | Wrap function | Single function logging/caching | Fast ⚡ |
| **Monkey Patch** | Replace globally | Library interception | Fast ⚡ |
| **Property** | Intercept attribute | Validation/computed fields | Fast ⚡ |
| **Context Manager** | Setup/cleanup | Resource lifecycle | Fast ⚡ |
| **`__getattr__`** | Dynamic attributes | REST APIs, proxies | Fast ⚡ |

---

## Real-World Examples

### Example 1: Function Timer (Decorator)
```python
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_operation():
    time.sleep(1)

slow_operation()
# Output: slow_operation took 1.0042s
```

### Example 2: Permission Tracking (Monkey Patch)
```python
# Same pattern used in permission_analyzer_runtime!

_original_make_request = boto3.BaseClient._make_request

def tracked_make_request(self, operation_model, request_dict, request_context):
    try:
        return _original_make_request(self, operation_model, request_dict, request_context)
    except ClientError as e:
        if is_permission_error(e):
            print(f"Permission denied: {operation_model.name}")
            return mock_response
        raise

boto3.BaseClient._make_request = tracked_make_request
```

### Example 3: Database Transaction (Context Manager)
```python
class Transaction:
    def __enter__(self):
        self.db.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        return False

# Usage
with Transaction(db) as t:
    t.db.insert(record1)
    t.db.insert(record2)
    # Auto-commits if no error, auto-rollbacks on error
```

---

## When to Use What

**Decorator:** "I want to modify one function"
```python
@log_calls
def my_func():
    pass
```

**Monkey Patch:** "I want to intercept ALL calls to a library"
```python
library.function = my_interceptor
```

**Property:** "I want to validate/control one attribute"
```python
@property
def value(self):
    return self._value
```

**Context Manager:** "I need setup and cleanup"
```python
with Manager():
    code_here()
```

**`__getattr__`:** "I want dynamic/flexible attributes"
```python
def __getattr__(self, name):
    return something
```

---

## Anti-Patterns (What NOT to Do)

❌ **Don't** use monkey patching without restoring:
```python
lib.function = new_function  # NO CLEANUP!
```

✅ **DO** use context manager for cleanup:
```python
with PatchContext():
    # Patched here
    code()
# Automatically restored
```

❌ **Don't** mix too many hooks - too confusing:
```python
@decorator1
@decorator2
@monkey_patch
@context_manager
def function():  # Too much!
    pass
```

✅ **DO** keep it simple - one hook per concern:
```python
@timer
def function():
    pass
```

---

## Summary

**5 Essential Hooks:**

1. **Decorator** - Wrap functions → Logging, timing, caching
2. **Monkey Patch** - Replace globally → Library interception
3. **Property** - Control attributes → Validation, computed fields
4. **Context Manager** - Lifecycle management → Resource cleanup
5. **`__getattr__`** - Dynamic attributes → Flexible APIs

**Choose based on scope:**
- Function level? → Decorator
- Library level? → Monkey patch
- Attribute level? → Property
- Block level? → Context manager
- Missing attributes? → `__getattr__`

**Remember:** The simpler, the better. Use the least invasive technique that solves your problem.

