# logger usage

Also if you're experiencing an issue with Python's logging module where your for example  `logging.info()` calls aren't showing up,
even though you've set the log level to DEBUG. This is a common problem that occurs when libraries manipulate the logging configuration.


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

Would you like me to explain any of these approaches in more detail?