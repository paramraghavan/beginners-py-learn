This guide combines how the Python logging hierarchy works with practical functions to silence noisy third-party
libraries while keeping your own application logs clear.

---

## 1. How Python Logging Works

Python logging is built on a **hierarchical, event-driven architecture**. Instead of just printing text, it creates "Log
Records" that travel through a pipeline.

### Core Components

* **Loggers:** The entry point (e.g., `logger.info()`). Organized via dot-notation (e.g., `app.models`).
* **Handlers:** Determine **destination** (Console, File, Email).
* **Formatters:** Define the **layout** (Timestamps, Levels).
* **Propagation:** By default, logs "bubble up" from child loggers to the **Root Logger**.

---

## 2. Managing Third-Party "Noise"

Most libraries (like `requests` or `boto3`) use their own loggers. If your root logger is set to `DEBUG`, these
libraries will flood your console.

### The Override Function

Use this function to target specific libraries and set them to a higher threshold (like `WARNING`) so they only speak up
when something is actually wrong.

```python
import logging


def setup_logging(app_name, lib_level=logging.WARNING):
    # 1. Basic config for your own app output
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 2. List of common noisy libraries to override
    noisy_libs = ['urllib3', 'requests', 'boto3', 'matplotlib', 'asyncio']

    for lib in noisy_libs:
        logger = logging.getLogger(lib)
        logger.setLevel(lib_level)
        # Prevent logs from reaching the root logger if they are still too chatty
        # logger.propagate = False 


setup_logging("my_script")
```

---

## 3. Advanced Strategy: Audit Logs

Sometimes you want to hide library logs from the **console** but keep them in a **file** just in case you need to debug
a connection error later.

### The Quarantine Pattern

```python
def quarantine_libraries(libraries, log_file="library_audit.log"):
    # Create a dedicated file for library noise
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)

    for lib_name in libraries:
        lib_logger = logging.getLogger(lib_name)
        lib_logger.addHandler(handler)

        # KEY: Stop these logs from propagating to your main console logger
        lib_logger.propagate = False
        lib_logger.setLevel(logging.DEBUG)  # Catch everything in the file
```

---

## 4. Summary Table: Levels & Usage

| Level        | Value | Best Use Case                                                |
|:-------------|:------|:-------------------------------------------------------------|
| **DEBUG**    | 10    | Detailed diagnostic info; use for your own app during dev.   |
| **INFO**     | 20    | General confirmation; "Server started", "User logged in".    |
| **WARNING**  | 30    | **Best for libraries.** Shows retries or non-fatal issues.   |
| **ERROR**    | 40    | Fatal to a specific operation; "Database connection failed". |
| **CRITICAL** | 50    | The whole program is crashing.                               |

## Example

To bring it all together, here is a complete, real-world example.

Imagine you are using the **`requests`** library. By default, it can be very chatty at the `DEBUG` level. This script
sets your app to be detailed while forcing `requests` to only alert you if there is a warning or error.

### The Implementation Example

```python
import logging
import requests  # Example of a "noisy" library


def configure_app_logging():
    # 1. Setup the Root Logger (This affects your console output)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s | %(levelname)s | %(message)s'
    )

    # 2. Identify and override specific library loggers
    # We set 'urllib3' to WARNING because 'requests' uses it internally
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


# Run the config
configure_app_logging()
logger = logging.getLogger("MyMainApp")

# This WILL show up (DEBUG level)
logger.debug("Starting the API fetch...")

# This library call normally produces several DEBUG logs about 
# connection pools, but now it will stay silent.
response = requests.get("https://www.google.com")

logger.info(f"Finished! Status code: {response.status_code}")
```

---

### Why this specific example matters

In the code above, if you *didn't* include the override line for `urllib3`, your console would look like this:

> `MyMainApp | DEBUG | Starting the API fetch...`
> `urllib3.connectionpool | DEBUG | Starting new HTTPS connection (1): www.google.com:443`
> `urllib3.connectionpool | DEBUG | https://www.google.com:443 "GET / HTTP/1.1" 200 None`
> `MyMainApp | INFO | Finished! Status code: 200`

**With the override**, you only see your own application logic, keeping your terminal clean and readable.



---

### Pro-Tip: Finding Hidden Logger Names

If you are using a library and aren't sure what its internal logger is named, add this temporary line to your code:

```python
# Print every logger name currently registered in your session
print(logging.root.manager.loggerDict.keys())
```

## Loggings intialized in current python runtime env

To see every logger that has been initialized in your current Python runtime, you can inspect the `manager.loggerDict`
inside the `logging` module. This is incredibly useful for finding the exact name of a "noisy" library logger so you can
silence it.

### Function to List All Active Loggers

This function iterates through the internal registry and prints the logger name along with its current effective level.

```python
import logging


def list_active_loggers():
    """Prints all registered loggers and their current logging levels."""
    # The root logger is not in the loggerDict, so we handle it manually
    root = logging.getLogger()
    print(f"{'LOGGER NAME':<40} | {'LEVEL'}")
    print("-" * 55)
    print(f"{'root':<40} | {logging.getLevelName(root.getEffectiveLevel())}")

    # Access the internal dictionary of all non-root loggers
    loggers = logging.root.manager.loggerDict

    for name, logger in sorted(loggers.items()):
        # Some entries in loggerDict are Placeholders; we only want actual Loggers
        if isinstance(logger, logging.Logger):
            level = logging.getLevelName(logger.getEffectiveLevel())
            print(f"{name:<40} | {level}")


# --- Example Usage ---
# Import a library to see it appear in the list
import requests

list_active_loggers()
```

---

### Understanding the Output

When you run the function above, you will likely see a list similar to this:

| Logger Name                | Level   | Description                                 |
|:---------------------------|:--------|:--------------------------------------------|
| **root**                   | WARNING | The top-level parent of all loggers.        |
| **urllib3.connectionpool** | DEBUG   | Internal logger used by `requests`.         |
| **urllib3.poolmanager**    | DEBUG   | Internal logger used by `requests`.         |
| **requests**               | WARNING | The main logger for the `requests` library. |

> **Note:** Loggers usually only appear in this list **after** the library has been imported or initialized. If you run
> this at the very top of your script, the list might be empty.

---

### Why are some loggers "Placeholders"?

In the `loggerDict`, you might occasionally see `logging.PlaceHolder` objects. These occur when a child logger is
defined before its parent. For example, if a library initializes `alpha.beta.gamma` but hasn't initialized `alpha` yet,
`alpha` exists as a placeholder to maintain the hierarchy.

### Quick Tip: The One-Liner

If you are in a debugging session and just want a quick list without a full function, you can run this in your console:

```python
print(list(logging.root.manager.loggerDict.keys()))
```
