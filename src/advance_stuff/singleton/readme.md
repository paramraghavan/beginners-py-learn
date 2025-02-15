**Simple implementation**

```python
class Singleton:
    _instance = None

    def __init__(self):
        if Singleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Singleton._instance = self

    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            Singleton._instance = Singleton()
        return Singleton._instance
```

**Usage**

```python
# Get the singleton instance
first = Singleton.get_instance()
second = Singleton.get_instance()

# Both variables point to the same instance
print(first is second)  # Output: True

# Trying to create a new instance directly will raise an exception
# new_instance = Singleton()  # This would raise an exception
```

**A more modern alternative using Python's built-in metaclass approach:**

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        pass

    @staticmethod
    def some_static_method():
        return "I am a static method in a singleton class"
```

Use the above metaclass approach if you need more flexibility or want to create multiple singleton classes.

**How use the metaclass to create multiple singleton classes**
This is a flexible way to create different singleton classes that each maintain their own single instance:

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Now you can create multiple singleton classes
class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, connection_string="default"):
        self.connection_string = connection_string

    def connect(self):
        return f"Connected to {self.connection_string}"


class LoggerService(metaclass=SingletonMeta):
    def __init__(self, log_level="INFO"):
        self.log_level = log_level

    def log(self, message):
        return f"[{self.log_level}] {message}"


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {}

    def set_config(self, key, value):
        self.settings[key] = value

    def get_config(self, key):
        return self.settings.get(key)
```

**Usage**

```python
# Database usage
db1 = DatabaseConnection("mysql://localhost")
db2 = DatabaseConnection("postgres://localhost")  # This won't change the connection string
print(db1.connection_string)  # Output: "mysql://localhost"
print(db2.connection_string)  # Output: "mysql://localhost"
print(db1 is db2)  # Output: True

# Logger usage
logger1 = LoggerService("DEBUG")
logger2 = LoggerService("ERROR")  # This won't change the log level
print(logger1.log_level)  # Output: "DEBUG"
print(logger2.log_level)  # Output: "DEBUG"
print(logger1 is logger2)  # Output: True

# Config usage
config1 = ConfigManager()
config2 = ConfigManager()
config1.set_config("api_key", "123456")
print(config2.get_config("api_key"))  # Output: "123456"
print(config1 is config2)  # Output: True
```



**Here's a thread-safe version:**

```python
import threading


class ThreadSafeSingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Usage is the same, just change the metaclass
class DatabaseConnection(metaclass=ThreadSafeSingletonMeta):
    # ... same implementation as before
    pass
```

If you need to be able to reset singletons (for testing purposes, for example), you can add a reset method:

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset_instance(cls, target_class):
        if target_class in cls._instances:
            del cls._instances[target_class]


# Example usage of reset
db = DatabaseConnection()
SingletonMeta.reset_instance(DatabaseConnection)  # Now you can create a new instance
```

This pattern is  useful when you need to ensure single instances of multiple different services in your
application, such as database connections, configuration managers, logging services, or cache handlers.