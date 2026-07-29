# Metaclass Use Cases - Practical Examples

## 1. Singleton Pattern
**Problem**: Need to ensure only one instance of a class exists
**Solution**: Use metaclass to control instance creation

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection = connection_string
        print(f"Connecting to {connection_string}")

# Only one instance created
db1 = Database("localhost:5432")
db2 = Database("localhost:5432")  # Reuses same instance
print(db1 is db2)  # True
```

**Real-world use**: Database connections, logging, cache managers, configuration objects

---

## 2. Auto-Registration Pattern
**Problem**: Keep track of all subclasses automatically
**Solution**: Register classes in metaclass `__new__` method

```python
class PluginMeta(type):
    plugins = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'PluginBase':  # Don't register the base class
            mcs.plugins[name] = cls
        return cls

class PluginBase(metaclass=PluginMeta):
    def execute(self):
        raise NotImplementedError

class EmailPlugin(PluginBase):
    def execute(self):
        print("Sending email...")

class SMSPlugin(PluginBase):
    def execute(self):
        print("Sending SMS...")

class SlackPlugin(PluginBase):
    def execute(self):
        print("Sending Slack message...")

# Access all plugins
print(PluginMeta.plugins)
# {'EmailPlugin': <class 'EmailPlugin'>, 'SMSPlugin': <class 'SMSPlugin'>, 'SlackPlugin': <class 'SlackPlugin'>}

# Dynamically execute plugins
for plugin_name, plugin_class in PluginMeta.plugins.items():
    plugin = plugin_class()
    plugin.execute()
```

**Real-world use**: Plugin systems, driver registration, test frameworks (pytest), ORM models

---

## 3. Validation & Enforcement
**Problem**: Enforce class naming conventions or structure
**Solution**: Validate class definition in metaclass `__new__`

```python
class ValidatedMeta(type):
    """Enforce class naming and required methods"""

    def __new__(mcs, name, bases, namespace):
        # Skip validation for base class
        if bases:
            # Enforce PascalCase naming
            if not name[0].isupper():
                raise ValueError(f"Class name must start with uppercase: {name}")

            # Enforce required methods
            required_methods = {'execute', 'validate'}
            defined_methods = set(namespace.keys())
            missing = required_methods - defined_methods

            if missing and name != 'BaseTask':
                raise TypeError(f"{name} missing required methods: {missing}")

        return super().__new__(mcs, name, bases, namespace)

class BaseTask(metaclass=ValidatedMeta):
    pass

# ✅ Valid
class EmailTask(BaseTask):
    def execute(self):
        pass

    def validate(self):
        pass

# ❌ Invalid - lowercase name
class emailTask(BaseTask):
    def execute(self):
        pass

    def validate(self):
        pass
# ValueError: Class name must start with uppercase: emailTask

# ❌ Invalid - missing execute method
class SMSTask(BaseTask):
    def validate(self):
        pass
# TypeError: SMSTask missing required methods: {'execute'}
```

**Real-world use**: Framework validation, API client libraries, test runners

---

## 4. Attribute Transformation
**Problem**: Automatically transform/validate class attributes
**Solution**: Process attributes in metaclass `__new__`

```python
class DescriptorMeta(type):
    """Auto-create validators for attributes"""

    def __new__(mcs, name, bases, namespace):
        for key, value in list(namespace.items()):
            # Convert type hints to validators
            if hasattr(value, '__class__') and value.__class__.__name__ == 'type':
                namespace[key] = value  # Keep as-is
        return super().__new__(mcs, name, bases, namespace)

class Config(metaclass=DescriptorMeta):
    host: str = "localhost"
    port: int = 5432
    debug: bool = False

config = Config()
print(f"{config.host}:{config.port}")
```

**Real-world use**: ORM models (Django, SQLAlchemy), data validation libraries, configuration management

---

## 5. Method Wrapping/Instrumentation
**Problem**: Add logging, timing, or tracking to all class methods
**Solution**: Wrap methods in metaclass `__new__`

```python
import time
from functools import wraps

class TracingMeta(type):
    """Automatically trace method calls"""

    def __new__(mcs, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                namespace[attr_name] = mcs._trace_method(attr_value)
        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _trace_method(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            print(f"[TRACE] Calling {func.__name__}")
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"[TRACE] {func.__name__} took {elapsed:.4f}s")
            return result
        return wrapper

class Calculator(metaclass=TracingMeta):
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

calc = Calculator()
calc.add(5, 3)
calc.multiply(4, 7)

# Output:
# [TRACE] Calling add
# [TRACE] add took 0.0001s
# [TRACE] Calling multiply
# [TRACE] multiply took 0.0001s
```

**Real-world use**: Debugging frameworks, performance monitoring, logging, AOP (aspect-oriented programming)

---

## 6. Abstract Base Class Enforcement
**Problem**: Enforce implementation of abstract methods
**Solution**: Use metaclass to track required implementations

```python
class AbstractMeta(type):
    """Enforce abstract methods are implemented"""

    def __new__(mcs, name, bases, namespace):
        abstract_methods = set()

        # Collect abstract methods from base classes
        for base in bases:
            if hasattr(base, '_abstract_methods'):
                abstract_methods.update(base._abstract_methods)

        # Mark methods with @abstract_method as abstract
        for key, value in namespace.items():
            if hasattr(value, '_is_abstract'):
                abstract_methods.add(key)

        # Remove implemented abstract methods
        for key in namespace:
            abstract_methods.discard(key)

        # Prevent instantiation if abstract methods exist
        if abstract_methods and name != 'AbstractBase':
            raise TypeError(f"{name} cannot be instantiated. "
                          f"Missing abstract methods: {abstract_methods}")

        namespace['_abstract_methods'] = abstract_methods
        return super().__new__(mcs, name, bases, namespace)

def abstract_method(func):
    func._is_abstract = True
    return func

class AbstractBase(metaclass=AbstractMeta):
    @abstract_method
    def connect(self):
        pass

# ❌ Cannot instantiate - missing connect()
class IncompleteDB(AbstractBase):
    pass
# TypeError: IncompleteDB cannot be instantiated. Missing abstract methods: {'connect'}

# ✅ Can instantiate - connect() is implemented
class PostgresDB(AbstractBase):
    def connect(self):
        print("Connecting to PostgreSQL...")

db = PostgresDB()
db.connect()
```

**Real-world use**: Abstract base classes, interface enforcement, framework base classes

---

## 7. Configuration Management
**Problem**: Prevent invalid configuration values
**Solution**: Validate configuration in metaclass

```python
class ConfigMeta(type):
    """Validate configuration values"""

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Validate on class creation
        if hasattr(cls, '_validate_config'):
            cls._validate_config()

        return cls

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        # Validate on instance creation
        if hasattr(instance, '_validate_instance'):
            instance._validate_instance()

        return instance

class AppConfig(metaclass=ConfigMeta):
    DEBUG = True
    MAX_CONNECTIONS = 100
    TIMEOUT = 30

    @classmethod
    def _validate_config(cls):
        if not isinstance(cls.DEBUG, bool):
            raise ValueError("DEBUG must be boolean")
        if cls.MAX_CONNECTIONS < 1:
            raise ValueError("MAX_CONNECTIONS must be > 0")
        if cls.TIMEOUT < 0:
            raise ValueError("TIMEOUT must be >= 0")
        print("Configuration validated ✓")

config = AppConfig()
```

**Real-world use**: Application configuration, environment-specific settings, secrets management

---

## 8. ORM-Style Model Definition
**Problem**: Create models with automatic attribute tracking
**Solution**: Process class attributes in metaclass

```python
class ModelMeta(type):
    """Auto-track model fields"""

    def __new__(mcs, name, bases, namespace):
        fields = {}

        # Extract field definitions
        for key, value in list(namespace.items()):
            if isinstance(value, type) or key.startswith('_'):
                continue
            if not callable(value):
                fields[key] = value
                namespace.pop(key)

        namespace['_fields'] = fields
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    name = "string"
    email = "string"
    age = "integer"
    active = "boolean"

print(User._fields)
# {'name': 'string', 'email': 'string', 'age': 'integer', 'active': 'boolean'}

# Create a table from fields
def create_table(model_class):
    fields = model_class._fields
    columns = ", ".join(f"{name} {type_}" for name, type_ in fields.items())
    return f"CREATE TABLE {model_class.__name__.lower()} ({columns})"

print(create_table(User))
# CREATE TABLE user (name string, email string, age integer, active boolean)
```

**Real-world use**: ORM frameworks (Django, SQLAlchemy), database migrations, data modeling

---

## 9. Caching & Memoization
**Problem**: Cache class instances or method results automatically
**Solution**: Use metaclass to manage cache

```python
class CachingMeta(type):
    """Cache expensive class instantiations"""

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls._cache = {}
        cls._cache_hits = 0
        cls._cache_misses = 0

    def __call__(cls, *args, **kwargs):
        # Convert args to cache key
        cache_key = (args, tuple(sorted(kwargs.items())))

        if cache_key in cls._cache:
            cls._cache_hits += 1
            print(f"Cache hit! (hits: {cls._cache_hits}, misses: {cls._cache_misses})")
            return cls._cache[cache_key]

        cls._cache_misses += 1
        instance = super().__call__(*args, **kwargs)
        cls._cache[cache_key] = instance
        return instance

class ExpensiveObject(metaclass=CachingMeta):
    def __init__(self, value):
        print(f"Creating expensive object with {value}")
        self.value = value

# First call - creates instance
obj1 = ExpensiveObject(42)

# Second call - returns cached instance
obj2 = ExpensiveObject(42)

print(obj1 is obj2)  # True
```

**Real-world use**: Resource pooling, expensive object creation, connection pooling

---

## 10. Test Fixture Management
**Problem**: Auto-discover and register test classes
**Solution**: Metaclass collects test methods

```python
class TestMeta(type):
    """Auto-discover and track test methods"""

    test_registry = []

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Collect test methods
        test_methods = [attr for attr in dir(cls)
                       if attr.startswith('test_') and callable(getattr(cls, attr))]

        if test_methods and name != 'TestBase':
            mcs.test_registry.append({
                'class': cls,
                'methods': test_methods,
                'count': len(test_methods)
            })

        return cls

class TestBase(metaclass=TestMeta):
    pass

class TestMath(TestBase):
    def test_add(self):
        assert 2 + 2 == 4

    def test_multiply(self):
        assert 3 * 4 == 12

class TestString(TestBase):
    def test_upper(self):
        assert "hello".upper() == "HELLO"

    def test_lower(self):
        assert "HELLO".lower() == "hello"

# Run all tests
print(f"Found {len(TestMeta.test_registry)} test classes")
for test_info in TestMeta.test_registry:
    print(f"\n{test_info['class'].__name__}: {test_info['count']} tests")
    for method in test_info['methods']:
        instance = test_info['class']()
        getattr(instance, method)()
        print(f"  ✓ {method}")
```

**Real-world use**: Test frameworks (pytest, unittest), test runners, test discovery

---

## Summary: When to Use Metaclasses

| Use Case | Benefit |
|----------|---------|
| **Singleton** | Guarantee single instance |
| **Auto-Registration** | Track subclasses automatically |
| **Validation** | Enforce constraints on class definition |
| **Attribute Transform** | Process attributes during class creation |
| **Method Wrapping** | Add logging, timing, tracking |
| **Abstract Methods** | Enforce interface contracts |
| **Configuration** | Validate settings |
| **ORM/Models** | Auto-track fields |
| **Caching** | Improve performance |
| **Testing** | Auto-discover tests |

---

## Best Practices

✅ **DO**:
- Use metaclasses for infrastructure/framework code
- Document why a metaclass is needed
- Keep metaclass logic simple and focused
- Use `__new__` for class-time operations
- Use `__call__` for instance-time operations

❌ **DON'T**:
- Use metaclasses for simple functionality (use regular classes instead)
- Over-engineer solutions with metaclasses
- Create metaclass hierarchies (hard to debug)
- Use multiple inheritance with metaclasses (can cause confusion)

---

## Rule of Thumb

> **If you're wondering whether you need a metaclass, you probably don't.**
>
> Use metaclasses only when:
> 1. You need to control class creation itself
> 2. You're building a framework
> 3. Simpler solutions won't work
