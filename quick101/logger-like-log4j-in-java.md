# logger usage

Also if you're experiencing an issue with Python's logging module where your for example  `logging.info()` calls aren't
showing up,
even though you've set the log level to DEBUG. This is a common problem that occurs when libraries manipulate the
logging configuration.

1. **Check and reset the root logger level:**

```python
import logging

logging.getLogger().setLevel(logging.DEBUG)  # Set root logger level
```

2. **Make sure you're configuring logging before importing other libraries:**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
# Only import other libraries after configuring logging
import your_library
```

3. **Create and use your own logger instead of the root logger:**

```python
import logging

logger = logging.getLogger('my_application')
logger.setLevel(logging.DEBUG)
# Create handler with desired output format
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Then use your logger
logger.info("This should be visible")
```

4. **Check for handlers:**
   Sometimes the issue is that no handlers are configured. Make sure you have a handler set up:

```python
import logging
import sys

# Check if handlers exist, if not create one
if not logging.getLogger().handlers:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
```

5. **Force disable propagation in third-party loggers:**
   If a library is changing logger settings, you can try to reset them:

```python
# Reset all loggers to propagate to parent
for name in logging.root.manager.loggerDict:
    logging.getLogger(name).propagate = True
    logging.getLogger(name).setLevel(logging.NOTSET)  # Use parent's level
```

5.1 Explain in detail
This code resets the behavior of all existing loggers in your Python application to ensure they properly pass messages
up to their parent loggers (ultimately to the root logger). Let me break it down:

```python
# Reset all loggers to propagate to parent
for name in logging.root.manager.loggerDict:
    logging.getLogger(name).propagate = True
    logging.getLogger(name).setLevel(logging.NOTSET)  # Use parent's level
```

1. `logging.root.manager.loggerDict` contains a dictionary of all named loggers that have been created in your
   application. This includes loggers created by your code and by any libraries you're using.

2. For each logger in this dictionary:

    - `logging.getLogger(name).propagate = True` - This ensures that log messages captured by this logger will be passed
      up to its parent logger. When a library sets `propagate = False` on its logger, it prevents messages from being
      seen by parent loggers, effectively trapping them.

    - `logging.getLogger(name).setLevel(logging.NOTSET)` - This resets the logger's level to `NOTSET`, which is a
      special value (0) that tells the logger to use its parent's level instead of having its own filter. This means if
      you set the root logger to `DEBUG`, and a child logger has `NOTSET`, the child will inherit the `DEBUG` level.

This solution works well when:

- You suspect a third-party library is configuring its loggers to not propagate messages
- You want consistent logging behavior where the root logger's level controls all logging
- You need to override logger settings that were established by code you can't modify directly

After running this code, you would typically set your root logger's level:

```python
logging.getLogger().setLevel(logging.DEBUG)  # Set root logger to desired level
```

Now, all loggers will propagate their messages up to the root logger, and will use the root logger's level (DEBUG in
this case), allowing your `logging.info()` calls to be visible.

5.1 By using following steps, your application will gain more control over logging across all libraries in your Python
environment.

```python
# Reset all loggers to propagate to parent
for name in logging.root.manager.loggerDict:
    logging.getLogger(name).propagate = True
    logging.getLogger(name).setLevel(logging.NOTSET)  # Use parent's level

# Set root logger level
logging.getLogger().setLevel(logging.DEBUG)  # Or whatever level you need
```

You're essentially creating a hierarchical override that:

* Forces all existing loggers (including those created by libraries) to propagate their messages up to their parent
  loggers and ultimately to the root logger.
* Makes all loggers defer their level decision to their parent by setting them to NOTSET.
* Establishes a single control point at the root logger where you can set the level that will be inherited by all
  loggers.

This gives you application-wide control because:

- Libraries that would normally suppress their log messages by setting `propagate = False` no longer do so
- Libraries that set restrictive log levels (like ERROR or WARNING) on their loggers now defer to your root logger's
  level
- Any handler you attach to the root logger will receive all log messages that meet or exceed your specified level

If you need even more granular control, you could selectively adjust specific library loggers after the reset:

```python
# After the reset, set specific levels for particular libraries if needed
logging.getLogger('requests').setLevel(logging.WARNING)  # Less verbose for requests
logging.getLogger('your_critical_module').setLevel(logging.DEBUG)  # More verbose for your code
```