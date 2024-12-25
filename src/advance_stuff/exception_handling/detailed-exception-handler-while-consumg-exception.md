# How to catch an exception while still printing its detailed stack trace.

**Some of the commonn ways to do it:**

```python
# Method 1: Using traceback module (Most detailed)
import traceback

try:
    # Your code that might raise an exception
    1 / 0  # Example exception
except Exception as e:
    print(f"Error occurred: {str(e)}")
    print("Full stack trace:")
    traceback.print_exc()
    # Continue with your error handling logic
```

```python
# Method 2: Using exc_info from sys
import sys

try:
    1 / 0
except Exception as e:
    print(f"Error occurred: {str(e)}")
    print("Stack trace:", file=sys.stderr)
    print(sys.exc_info()[2].format_exc())
```

```python
# Method 3: Using the exception's built-in __traceback__
try:
    1 / 0
except Exception as e:
    print(f"Error occurred: {str(e)}")
    print("Stack trace:")
    print(''.join(traceback.format_tb(e.__traceback__)))
```

The first method using `traceback.print_exc()` is generally the most recommended as it:

- Provides the most detailed stack trace
- Maintains proper formatting
- Is easier to read
- Includes line numbers and file names
