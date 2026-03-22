# Python Exception Suppressor Guide

A modern, comprehensive guide to exception suppression techniques in Python, covering both built-in and custom approaches.

## Table of Contents
1. [Built-in Methods](#built-in-methods)
2. [Custom Suppression](#custom-suppression)
3. [Advanced Patterns](#advanced-patterns)
4. [Comparison Table](#comparison-table)
5. [Best Practices](#best-practices)
6. [Real-World Use Cases](#real-world-use-cases)

---

## Built-in Methods

### Method 1: contextlib.suppress()

The simplest, most Pythonic way to suppress exceptions.

```python
from contextlib import suppress

# Suppress single exception
with suppress(ValueError):
    int("not-a-number")  # Silently suppressed

# Suppress multiple types
with suppress(ValueError, KeyError, TypeError):
    data = {}
    result = int(data['missing'])  # Suppressed
```

**Pros:**
- ✓ Built-in, no custom code needed
- ✓ Clear intent and readable
- ✓ Zero overhead
- ✓ Pythonic

**Cons:**
- ✗ No logging of what was suppressed
- ✗ No callbacks or custom handling
- ✗ Can't distinguish between exception types

**Use Case:** Simple suppression where you don't need logging

---

### Method 2: Try-Except with Pass

The explicit traditional approach.

```python
try:
    risky_operation()
except ValueError:
    pass  # Suppress the error
```

**Pros:**
- ✓ Explicit and obvious
- ✓ Can add logging easily

**Cons:**
- ✗ Less Pythonic than suppress()
- ✗ More verbose
- ✗ Bare `except:` is dangerous

**Use Case:** When you need some handling logic

---

### Method 3: Python 3.11+ ExceptionGroup

Modern exception handling for multiple simultaneous exceptions.

```python
# Python 3.11+
try:
    raise ExceptionGroup("Multiple errors", [
        ValueError("Error 1"),
        TypeError("Error 2"),
        RuntimeError("Error 3"),
    ])
except* ValueError as eg:
    print(f"Caught ValueError: {eg.exceptions}")
except* TypeError as eg:
    print(f"Caught TypeError: {eg.exceptions}")
```

**Pros:**
- ✓ Handles multiple exceptions at once
- ✓ Type-specific handling with except*
- ✓ Modern Python feature

**Cons:**
- ✗ Requires Python 3.11+
- ✗ More complex

**Use Case:** Concurrent operations with multiple errors

---

## Custom Suppression

### Pattern 1: ExceptionSuppressor Context Manager

Full-featured custom suppression with logging.

```python
from exception_suppressor import ExceptionSuppressor

with ExceptionSuppressor(
    suppress_types=(ValueError, TypeError),
    log_exceptions=True,
    name="DataProcessing"
) as suppressor:
    # Code that might raise exceptions
    int("invalid")  # Suppressed and logged

suppressor.report()  # Show what was suppressed
```

**Features:**
- ✓ Suppress specific exception types
- ✓ Automatic logging with timestamps
- ✓ Exception tracking and reporting
- ✓ Callback support (on_suppress)
- ✓ Summary statistics

---

### Pattern 2: suppress_exceptions Decorator

Decorator-based suppression for functions.

```python
from exception_suppressor import suppress_exceptions

@suppress_exceptions(ValueError, TypeError, log=True)
def convert_to_int(value):
    return int(value)

result = convert_to_int("not-a-number")  # Returns None
```

**Features:**
- ✓ Automatic suppression for decorated functions
- ✓ Optional logging
- ✓ Optional callback on error
- ✓ Reusable across functions

---

### Pattern 3: ExceptionHandler with Grouping

Group exceptions by type for analysis.

```python
from exception_suppressor import ExceptionHandler

handler = ExceptionHandler()

for item in items:
    with handler.handle_and_group(ValueError, suppress=True):
        process_item(item)

handler.report_by_type()
stats = handler.get_stats()
```

**Features:**
- ✓ Groups exceptions by type
- ✓ Counts occurrences
- ✓ Generates statistics
- ✓ Detailed reporting

---

### Pattern 4: Retry with Eventual Suppression

Retry logic that eventually suppresses the exception.

```python
from exception_suppressor import suppress_with_retry

@suppress_with_retry(max_retries=3, delay=0.5)
def unstable_api_call():
    return api.request()  # Retries 3 times, then suppresses

result = api_call()  # Returns None if all attempts fail
```

**Features:**
- ✓ Automatic retry on failure
- ✓ Exponential backoff option
- ✓ Eventual suppression
- ✓ Callback on final failure

---

### Pattern 5: Silent Failure Handler

Handle failures silently with logging for debugging.

```python
from exception_suppressor import SilentFailureHandler

handler = SilentFailureHandler("DataProcessor")

for item in items:
    with handler.silent_context():
        process(item)  # Failures are silent

if handler.has_failures():
    print(handler.get_failures())
```

**Features:**
- ✓ Silent error handling
- ✓ Failure logging for debugging
- ✓ Can detect if failures occurred
- ✓ Retrieve failure details later

---

## Advanced Patterns

### Pattern 1: Conditional Suppression

Suppress exceptions only under certain conditions.

```python
def conditional_suppress(exc):
    """Only suppress network errors, not auth errors."""
    network_errors = (ConnectionError, TimeoutError)
    if isinstance(exc, network_errors):
        return True  # Suppress
    return False  # Don't suppress

try:
    api_call()
except Exception as e:
    if not conditional_suppress(e):
        raise
```

### Pattern 2: Suppression with Fallback

Suppress and provide fallback value.

```python
class FallbackSuppressor:
    def __init__(self, fallback_value):
        self.fallback = fallback_value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Suppressed {exc_type}, using fallback")
            return True
        return False

    @property
    def value(self):
        return self.fallback

with FallbackSuppressor(default_data) as fs:
    data = fetch_data()  # Might fail

# Use fallback if fetch failed
result = process(fs.value)
```

### Pattern 3: Suppression with Metrics

Track suppression metrics for monitoring.

```python
class MetricsCollector:
    def __init__(self):
        self.suppressed_count = 0
        self.failed_attempts = []

    def suppress_with_metrics(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.suppressed_count += 1
            self.failed_attempts.append({
                'function': func.__name__,
                'error': str(e),
                'time': datetime.now()
            })
            # Can send to monitoring system
            return None
```

### Pattern 4: Suppression with Compensation

Suppress and perform compensating action.

```python
class CompensatingException:
    def __init__(self, operation_func, compensation_func):
        self.operation = operation_func
        self.compensation = compensation_func

    def __call__(self):
        try:
            return self.operation()
        except Exception as e:
            # Do compensating action
            self.compensation(e)
            return None

def operation():
    raise ValueError("Failed")

def compensate(error):
    print(f"Performing cleanup: {error}")

call = CompensatingException(operation, compensate)
call()  # Performs operation, then compensation on error
```

---

## Comparison Table

| Method | Syntax | Logging | Callbacks | Typing | Python |
|--------|--------|---------|-----------|--------|--------|
| **suppress()** | Context | ✗ | ✗ | ✓ | 3.4+ |
| **Try-Except** | Block | ✓ | ✓ | ✓ | All |
| **ExceptionGroup** | except* | ✓ | ✓ | ✓ | 3.11+ |
| **ExceptionSuppressor** | Context | ✓ | ✓ | ✓ | 3.6+ |
| **Decorator** | @suppress | ✓ | ✓ | ✓ | 3.6+ |
| **ExceptionHandler** | Context | ✓ | ✓ | ✓ | 3.6+ |

---

## Best Practices

### ✅ DO

```python
# 1. Be specific about what you suppress
with suppress(ValueError):
    process()

# 2. Log what you suppress
with ExceptionSuppressor(ValueError, log_exceptions=True):
    process()

# 3. Add callbacks for important errors
def on_error(exc):
    alert_monitoring(exc)

@suppress_exceptions(ConnectionError, on_error=on_error)
def call_api():
    pass

# 4. Use descriptive names
with ExceptionSuppressor(ValueError, name="DataValidation"):
    validate()

# 5. Document why you're suppressing
# Suppress network errors only - they're transient
with suppress(ConnectionError):
    sync_data()

# 6. Provide fallback values when possible
handler = SilentFailureHandler("Operation")
with handler.silent_context():
    result = get_data()
result = result or default_data
```

### ❌ DON'T

```python
# 1. Don't suppress everything
except:
    pass  # NEVER do this!

# 2. Don't suppress without logging critical errors
@suppress_exceptions(RuntimeError)  # Bad for critical errors
def critical_operation():
    pass

# 3. Don't suppress to hide bugs
try:
    code()
except:
    pass  # Might hide actual bugs

# 4. Don't suppress without understanding why
with suppress(ValueError):
    some_code()  # Why was this suppressed?

# 5. Don't suppress broad exception types
with suppress(Exception):  # Too broad!
    process()

# 6. Don't forget to monitor suppressed errors
# Suppressed errors can hide problems
@suppress_exceptions(TimeoutError)  # What if timeouts increase?
def call_api():
    pass
```

---

## Real-World Use Cases

### Use Case 1: Graceful Degradation

Application continues with reduced functionality on error.

```python
@suppress_exceptions(
    ConnectionError,
    TimeoutError,
    on_error=lambda e: log_warning(f"Feature unavailable: {e}")
)
def fetch_recommendations():
    """Optional feature - fail gracefully if unavailable."""
    return api.get_recommendations()

# Main code
user = get_user()
recommendations = fetch_recommendations()  # None if service down
if recommendations:
    display(recommendations)
else:
    show_message("Recommendations unavailable")
```

### Use Case 2: Batch Processing

Process items even when some fail.

```python
handler = ExceptionHandler()

for item in large_dataset:
    with handler.handle_and_group(ValueError, suppress=True):
        process_item(item)

# Report failures at end
handler.report_by_type()
```

### Use Case 3: Retry with Fallback

Network call with retry and fallback.

```python
@suppress_with_retry(max_retries=3, delay=1.0)
def fetch_data_with_retry():
    return api.get_latest_data()

# Try 3 times, then use cached data
result = fetch_data_with_retry()
if result is None:
    result = cache.get_last_known_data()

display(result)
```

### Use Case 4: Cleanup Operations

Ensure cleanup happens even if operation fails.

```python
with suppress(IOError):
    with ExceptionSuppressor(ValueError, name="Cleanup"):
        temp_file = create_temp_file()
        process_file(temp_file)
finally:
    cleanup_temp_file()  # Always runs
```

### Use Case 5: Feature Flag Validation

Suppress validation errors for experimental features.

```python
@suppress_exceptions(ValidationError, log=feature_flag_enabled)
def experimental_feature():
    """Suppress validation for beta feature."""
    return beta_feature()

# Validation suppressed in prod, logged in beta testing
result = experimental_feature()
```

### Use Case 6: Monitoring & Alerting

Suppress errors but track for monitoring.

```python
class MonitoredSuppressor:
    def __init__(self, metric_name):
        self.metric = metric_name
        self.count = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.count += 1
            metrics.increment(f"{self.metric}.suppressed")

            if self.count > THRESHOLD:
                alerts.trigger(f"High suppression rate for {self.metric}")

            return True
        return False

# Usage
with MonitoredSuppressor("api_calls"):
    call_api()
```

---

## When to Suppress vs When to Handle

### Suppress When:
- ✓ Error is transient (network timeout)
- ✓ Error is expected and handled elsewhere
- ✓ Feature is optional and can fail gracefully
- ✓ Error occurs in cleanup code
- ✓ Error is logged and monitored

### Handle When:
- ✗ Error is critical and affects functionality
- ✗ Error needs specific response
- ✗ Error indicates configuration problem
- ✗ Error needs user notification
- ✗ Error affects security

---

## Performance Considerations

| Approach | Overhead | Use When |
|----------|----------|----------|
| `suppress()` | Minimal | Performance critical |
| Decorator | Low | Many calls, same behavior |
| Context Manager | Low | Scoped suppression |
| ExceptionHandler | Medium | Need tracking |
| Custom | Variable | Complex scenarios |

---

## Summary

### Quick Reference

```python
# Simplest
from contextlib import suppress
with suppress(ValueError):
    code()

# With logging
from exception_suppressor import ExceptionSuppressor
with ExceptionSuppressor(ValueError, log_exceptions=True):
    code()

# For functions
@suppress_exceptions(ValueError, log=True)
def my_func():
    code()

# With retry
@suppress_with_retry(max_retries=3, delay=1)
def unstable():
    code()

# With grouping
handler = ExceptionHandler()
with handler.handle_and_group(ValueError, suppress=True):
    code()
handler.report_by_type()
```

### Recommendation Matrix

| Situation | Recommendation |
|-----------|-----------------|
| One-off suppression | `contextlib.suppress()` |
| Repeated pattern | Decorator |
| Scoped operation | Context manager |
| Need logging | ExceptionSuppressor |
| Batch processing | ExceptionHandler |
| Retry logic | suppress_with_retry |

---

## Further Reading

- Python Documentation: [contextlib.suppress](https://docs.python.org/3/library/contextlib.html#contextlib.suppress)
- PEP 654: Exception Groups and except* (Python 3.11+)
- Exception Best Practices
- Error Handling Patterns

