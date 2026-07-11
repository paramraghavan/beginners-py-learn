# Exception Interception Guide

A comprehensive guide on how to intercept and handle exceptions in Python, with practical examples and the implementation used in `permission_analyzer_runtime.py`.

## Table of Contents
1. [Exception Basics](#exception-basics)
2. [Interception Techniques](#interception-techniques)
3. [Monkey Patching](#monkey-patching)
4. [Context Managers](#context-managers)
5. [Permission Analyzer Example](#permission-analyzer-example)
6. [Real-World Use Cases](#real-world-use-cases)

---

## Exception Basics

### Standard Exception Flow (Without Interception)

```python
def risky_operation():
    # Something goes wrong here
    raise ValueError("Invalid input")

# Exception propagates UP
try:
    risky_operation()  # Throws ValueError
except ValueError as e:
    print(f"Caught: {e}")  # Handled here
```

### Call Stack During Exception

```
main()
  ↓
function_a()
  ↓
function_b()
  ↓
raise Exception  ← Happens here
  ↓
Propagates UP (unwinding stack)
  ↓
function_b() → (not caught, passes up)
  ↓
function_a() → (not caught, passes up)
  ↓
main() → try/except catches it
  ↓
Exception handled ✅
```

---

## Interception Techniques

### Technique 1: Direct Try-Except

**What it is:** Catch exceptions at the call site.

```python
# Simple interception at the point of failure
try:
    risky_operation()
except SpecificException as e:
    print(f"Caught: {e}")
    # Handle it
```

**Pros:** Simple, explicit, easy to understand
**Cons:** Must know where exceptions occur, not reusable

---

### Technique 2: Wrapper Function

**What it is:** Wrap a function to intercept its exceptions.

```python
def safe_wrapper(func, *args, **kwargs):
    """Wrapper that catches exceptions from func."""
    try:
        return func(*args, **kwargs)
    except SpecificException as e:
        print(f"Caught exception: {e}")
        # Handle or suppress
        return None
    except Exception as e:
        # Let other exceptions through
        raise

# Usage
result = safe_wrapper(risky_operation)
```

**Pros:** Reusable, separates error handling from logic
**Cons:** Must manually wrap each call

---

### Technique 3: Decorator

**What it is:** Use a decorator to intercept all calls to a function.

```python
import functools

def catches_exceptions(func):
    """Decorator that catches exceptions from the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SpecificException as e:
            print(f"Caught: {e}")
            return None
        except Exception as e:
            raise
    return wrapper

@catches_exceptions
def my_operation():
    # This function's exceptions are now intercepted
    raise ValueError("Something went wrong")

# Usage - exception is caught!
my_operation()  # Prints "Caught: Something went wrong", returns None
```

**Pros:** Automatic, clean, reusable
**Cons:** Only works for functions you decorate

---

### Technique 4: Context Manager

**What it is:** Use `with` statement to intercept exceptions in a block.

```python
class ExceptionInterceptor:
    def __enter__(self):
        print("Starting operation")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Caught exception: {exc_type.__name__}: {exc_value}")
            # Return True to suppress the exception
            return True  # Suppress
        return False

# Usage
with ExceptionInterceptor():
    raise ValueError("Error in block")  # Caught and suppressed

print("Code continues!")  # This runs!
```

**Pros:** Clean syntax, automatic cleanup, flexible scope
**Cons:** Requires class definition

---

### Technique 5: Monkey Patching (The Permission Analyzer Technique)
[permission_analyzer_runtime.py](permission_analyzer_runtime.py)

**What it is:** Replace a method/function at runtime to intercept calls.

```python
# Original function
def original_function():
    raise ValueError("Original error")

# Save the original
_original = original_function

# Replace with interceptor
def interceptor():
    try:
        return _original()
    except ValueError as e:
        print(f"Intercepted: {e}")
        return None

# Monkey patch
original_function = interceptor

# Now all calls go through interceptor
original_function()  # Prints "Intercepted: Original error"
```

**Pros:** Intercepts ALL calls globally, works without modifying original code
**Cons:** Can be confusing, affects all uses of the function

---

## Monkey Patching

### What is Monkey Patching?

Monkey patching is **replacing/modifying a function or method at runtime** without changing the original code.

### Simple Example

```python
class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
print(calc.add(2, 3))  # Output: 5

# Monkey patch the add method
_original_add = Calculator.add

def patched_add(self, a, b):
    print(f"Adding {a} + {b}")
    return _original_add(self, a, b)

Calculator.add = patched_add

# Now uses patched version
print(calc.add(2, 3))
# Output:
# Adding 2 + 3
# 5
```

### Why Monkey Patch?

✅ **Intercept calls** without modifying source
✅ **Add logging/tracking** globally
✅ **Mock objects** for testing
✅ **Modify behavior** of third-party libraries
✅ **A/B testing** different implementations

### Risks ⚠️

❌ **Global state** - affects everything
❌ **Hard to debug** - behavior changes mysteriously
❌ **Fragile** - breaks if internals change
❌ **Non-obvious** - readers don't expect it

---

## Context Managers

### What is a Context Manager?

A context manager ensures **setup and cleanup** code runs around a block.

### The Protocol

```python
class MyContextManager:
    def __enter__(self):
        """Called when entering 'with' block"""
        print("Setup")
        return self  # What you get in 'as' variable

    def __exit__(self, exc_type, exc_value, traceback):
        """Called when exiting 'with' block (even on exception)"""
        print("Cleanup")

        # Return True to suppress exception
        # Return False (or nothing) to let it propagate
        if exc_type is not None:
            print(f"Exception occurred: {exc_type}")
        return False

# Usage
with MyContextManager() as cm:
    print("Inside block")
    # cm is the object returned by __enter__

print("After block")
```

### Exception Handling in Context Managers

```python
class SafeFile:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

        if exc_type is not None:
            print(f"Exception during file operation: {exc_value}")
            return False  # Don't suppress

        return True

# Usage
with SafeFile('test.txt') as f:
    f.write("Hello")
    # File is automatically closed
```

---

## Permission Analyzer Example

### How permission_analyzer_runtime Uses These Techniques

It combines **monkey patching + context manager + exception interception**.

### The Structure

```python
class PermissionTracker:
    def __enter__(self):
        """Setup: Patch boto3"""
        self._patch_boto3()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup: Restore boto3"""
        self._unpatch_boto3()
        return False

    def _patch_boto3(self):
        """Monkey patch BaseClient._make_request"""
        from botocore.client import BaseClient

        # Save original
        self._original_make_request = BaseClient._make_request

        # Define interceptor
        def tracked_make_request(self, operation_model, request_dict, request_context):
            try:
                # Call real method
                return self._original_make_request(
                    operation_model,
                    request_dict,
                    request_context
                )
            except ClientError as e:
                # Intercept exception
                error_code = e.response['Error']['Code']

                if is_permission_error(error_code):
                    # Track it
                    track_permission(...)
                    # Suppress exception
                    return mock_response
                else:
                    # Let other errors through
                    raise

        # Replace method globally
        BaseClient._make_request = tracked_make_request

    def _unpatch_boto3(self):
        """Restore original"""
        from botocore.client import BaseClient
        BaseClient._make_request = self._original_make_request
```

### Usage Flow

```python
# Step 1: Create tracker
tracker = PermissionTracker(verbose=True)

# Step 2: Enter context (__enter__ called)
with tracker:
    # Step 3: boto3 is now patched
    s3 = boto3.client('s3')

    # Step 4: When s3.put_object() is called:
    # - Interceptor catches it
    # - Tries real AWS call
    # - Catches ClientError
    # - Checks if permission error
    # - Returns mock response or re-raises
    s3.put_object(Bucket='bucket', Key='file', Body=b'data')

# Step 5: Exit context (__exit__ called)
# - boto3 is restored to original state

# Step 6: Report results
tracker.report()
```

---

## Detailed Flow: Permission Analyzer

### Before: Normal AWS Call

```
User Code
  ↓
s3.put_object()
  ↓
boto3 client
  ↓
BaseClient._make_request()
  ↓
botocore sends HTTP request
  ↓
AWS returns: AccessDenied
  ↓
ClientError exception raised
  ↓
Exception bubbles up
  ↓
User code crashes ❌
```

### After: With Permission Tracker

```
User Code
  ↓
with PermissionTracker() as tracker:
  └─→ __enter__() patches boto3

s3.put_object()
  ↓
boto3 client
  ↓
BaseClient._make_request()  ← PATCHED!
  ↓
tracked_make_request() called
  ├─→ Tries: original_make_request()
  │   └─→ AWS returns: AccessDenied
  │   └─→ ClientError raised
  ├─→ Catches: ClientError exception
  ├─→ Checks: is_permission_error? YES
  ├─→ Tracks: s3:PutObject
  ├─→ Returns: mock_response ← NOT AN EXCEPTION
  └─→ Code continues! ✅

exit context
  └─→ __exit__() unpatches boto3

tracker.report()
  └─→ Shows all tracked permissions
```

---

## Real-World Use Cases

### Use Case 1: Logging Interceptor

Automatically log all function calls:

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            print(f"  Returned: {result}")
            return result
        except Exception as e:
            print(f"  Raised: {type(e).__name__}: {e}")
            raise
    return wrapper

@log_calls
def divide(a, b):
    return a / b

divide(10, 2)
divide(10, 0)  # Exception is logged before being raised
```

### Use Case 2: Retry Interceptor

Automatically retry failed operations:

```python
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except TemporaryError as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def unstable_api_call():
    # Might fail, but will retry
    pass
```

### Use Case 3: Permission Tracking (Like permission_analyzer_runtime)

Track specific errors:

```python
class ErrorTracker:
    def __init__(self):
        self.errors = []

    def __enter__(self):
        # Patch the library
        self._patch_library()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._unpatch_library()

    def _patch_library(self):
        # Replace library's error handler
        pass

    def track_error(self, error):
        self.errors.append(error)

    def report(self):
        print(f"Tracked {len(self.errors)} errors")

# Usage
with ErrorTracker() as tracker:
    # Errors are automatically tracked
    do_something()
```

### Use Case 4: Performance Monitoring

Track function execution time:

```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.timings = {}

    def track(self, func_name):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = time.time() - start
                    if func_name not in self.timings:
                        self.timings[func_name] = []
                    self.timings[func_name].append(duration)
            return wrapper
        return decorator

monitor = PerformanceMonitor()

@monitor.track('database_query')
def query_db():
    # Performance tracked
    pass
```

### Use Case 5: Database Transaction Context

Automatic commit/rollback:

```python
class DatabaseTransaction:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        self.db.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.db.commit()
        else:
            self.db.rollback()
            # Suppress or propagate the exception
            return False

# Usage
with DatabaseTransaction(db):
    db.insert(data)
    # If exception occurs here, automatically rollbacks
```

---

## Comparison: When to Use Each Technique

| Technique | Use When | Pros | Cons |
|-----------|----------|------|------|
| **Try-Except** | Exception might occur | Simple, explicit | Limited scope |
| **Wrapper Function** | Want to handle errors | Reusable, flexible | Manual wrapping |
| **Decorator** | Want to decorate functions | Automatic, clean | Only for functions you control |
| **Context Manager** | Need setup/cleanup | Automatic cleanup, clean syntax | Requires class |
| **Monkey Patch** | Need global interception | Intercepts everything | Fragile, confusing |

---

## Best Practices

### ✅ DO

```python
# Use context managers for resource management
with open(file) as f:
    data = f.read()

# Use decorators for reusable error handling
@catches_exceptions
def my_func():
    pass

# Use try-except for expected exceptions
try:
    risky_operation()
except ExpectedException as e:
    handle_error(e)

# Save originals when monkey patching
_original = func
def patched():
    # Use _original
    pass
func = patched
```

### ❌ DON'T

```python
# Don't catch everything silently
try:
    everything()
except:
    pass

# Don't monkey patch without good reason
some_library.function = my_function  # Risky!

# Don't forget to restore after patching
# (Use context managers to ensure this)
```

---

## Summary

**Exception Interception Techniques:**

1. **Try-Except** - Catch at call site
2. **Wrapper** - Manually wrap calls
3. **Decorator** - Auto-wrap functions
4. **Context Manager** - Scope-based interception
5. **Monkey Patch** - Global replacement

**Permission Analyzer Uses:**
- ✅ Monkey patching (global interception of boto3)
- ✅ Context manager (setup/cleanup)
- ✅ Exception handling (catching ClientError)
- ✅ Mock responses (suppressing exceptions)

**Result:** All boto3 calls are intercepted without modifying user code! 🎯
