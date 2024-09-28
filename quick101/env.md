## 1. Using os

```python
import os

# Print the list of user's
# environment variables
print("User's Environment variable:")
print(dict(os.environ))

# Get the value of
# 'foo' environment variable
# export foo = bar  # in the Local Operating System
foo = os.environ['foo']
foo = os.environ.get('foo')

# Modify the value of
# 'foo'  environment variable 
os.environ['foo'] = 'tar'

# Add a new environment variable 
os.environ['learnSpark1'] = 'www.learn-spark.info'

# If the key does not exists
# it will produce an error
os.environ['env_does_not_exist']
```

## 2. Using `sys.modules` and `module.__file__`

The `sys.modules` dictionary holds references to all loaded modules. You can access the file path of each module by
using the `__file__` attribute.

```python
import sys

for module_name, module in sys.modules.items():
    try:
        print(f"Module: {module_name}, Path: {module.__file__}")
    except AttributeError:
        # Some modules might not have a __file__ attribute
        print(f"Module: {module_name}, Path: Built-in or C extension")
```

## 3. Using `inspect` to find the path of a specific module

You can also use the `inspect` module to find the location of a particular module that is loaded.

```python
import inspect
import module_name  # Replace with the actual module you want to inspect

print(inspect.getfile(module_name))
```

## 4. Tracking all the paths where Python is searching for modules

If you're interested in knowing where Python is searching for modules, you can use `sys.path`:

```python
import sys

print(sys.path)
```

This will print out a list of directories where Python is looking for modules. You can use this information to determine
the source location for any imported modules.
