# Function to override `print()`

This function both prints to console and logs to a file:

```python
import logging
import builtins

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output.log'),
        logging.StreamHandler()  # This also prints to console
    ]
)

# Save reference to original print
_original_print = builtins.print


def custom_print(*args, sep=' ', end='\n', file=None, flush=False):
    """
    Custom print function that prints to console and logs to file
    """
    # Convert args to string like print does
    message = sep.join(str(arg) for arg in args)

    # Log to file
    logging.info(message)

    # Also use original print (optional, since StreamHandler already prints)
    # _original_print(*args, sep=sep, end=end, file=file, flush=flush)


# Override built-in print
builtins.print = custom_print

# Test it
print("This will be printed and logged!")
print("Multiple", "arguments", "work", "too")
print("Numbers:", 42, 3.14)
```

**Alternative approach** (if you don't want to override the built-in):

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='output.log',
    filemode='a'
)


def print_and_log(*args, sep=' ', end='\n', **kwargs):
    """
    Print to console and log to file
    """
    message = sep.join(str(arg) for arg in args)

    # Print to console
    print(*args, sep=sep, end=end, **kwargs)

    # Log to file
    logging.info(message)


# Usage
print_and_log("This appears in console and log file")
```

**Key features:**

- Maintains `print()` signature (supports `sep`, `end`, etc.)
- Logs with timestamp automatically
- Can easily restore original `print()` if needed: `builtins.print = _original_print`

# How to make it work with all my libraries/modules
To make this work you override it **before** importing other modules.
Here's why:

```python
import builtins
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='output.log'
)

_original_print = builtins.print


def custom_print(*args, sep=' ', end='\n', file=None, flush=False):
    message = sep.join(str(arg) for arg in args)
    logging.info(message)
    _original_print(*args, sep=sep, end=end, file=file, flush=flush)


# Override BEFORE importing other modules
builtins.print = custom_print

# Now import modules - they will use custom_print
import requests
import pandas as pd
from my_module import some_function

# All print() calls in those modules will now use custom_print
```

**Important timing consideration:**

```python
# ❌ This WON'T work for already-imported modules
import pandas as pd
import builtins

builtins.print = custom_print  # Too late! pandas already imported

# pandas will still use original print
```

**Best practice - put override in a separate file:**

```python
# override_print.py
import builtins
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='output.log'
)

_original_print = builtins.print


def custom_print(*args, sep=' ', end='\n', file=None, flush=False):
    message = sep.join(str(arg) for arg in args)
    logging.info(message)
    _original_print(*args, sep=sep, end=end, file=file, flush=flush)


builtins.print = custom_print
```

Then in your main script:

```python
# main.py
import override_print  # Do this FIRST

import pandas as pd
import requests

# ... other imports

# Now all modules use the custom print
print("This is logged!")
```
This way, the override happens before any other module imports, so all `print()` calls system-wide will use your custom
version.