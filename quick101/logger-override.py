# main.py
import logging
import sys

# Configure logging before importing other modules
# Reset all loggers to propagate to parent
for name in logging.root.manager.loggerDict:
    logging.getLogger(name).propagate = True
    logging.getLogger(name).setLevel(logging.NOTSET)  # Use parent's level

# DEBUG and INFO messages will go only to stdout
# WARNING, ERROR, and CRITICAL messages will go to both stdout and stderr
# Set root logger level
logging.getLogger().setLevel(logging.DEBUG)  # Or whatever level you need

# Add a handler if you haven't already
if not logging.getLogger().handlers:
    # Create stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)  # Send INFO and above to stdout
    stdout_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Create stderr handler
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)  # Send WARNING, ERROR, CRITICAL to stderr
    stderr_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Add both handlers to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(stderr_handler)

# Module specific logger
# Now import other modules
import your_other_module
# ...rest of your application...

## end main.py

# my_module.py
## How do I log im other modules
# In a file like my_module.py
import logging

# Get a logger specific to this module
logger = logging.getLogger(__name__)


def some_function():
    logger.debug("Debug message from some_function")
    logger.info("Info message from some_function")

    # Do something...

    logger.warning("Warning message from some_function")

"""   
Yes, the module-specific loggers will still use the stderr and stdout handlers you set up in your main.py.

This works because:

1. You've configured your module loggers to propagate=True (in your main.py reset code)
2. The logger hierarchy in Python passes messages up the chain
3. Your handlers are attached to the root logger

When you call `logger.info()` in a module:
1. The module's logger receives the message
2. Since propagate=True, it passes the message up to its parent
3. This continues until it reaches the root logger
4. The root logger applies its handlers (your stdout and stderr handlers)

The full chain looks like this:
my_package.my_module logger → parent loggers → root logger → your stdout/stderr handlers

As long as you run the reset code in main.py before importing your other modules, all your module loggers
will inherit and use the handlers you've attached to the root logger. 
You don't need to add any handlers in your individual modules.
"""

