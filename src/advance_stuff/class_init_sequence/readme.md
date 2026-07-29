# Python Class and initialization Sequence
In Python, a class is a blueprint for creating objects. It encapsulates data (attributes) and behavior (methods) into a single entity. 


## Class Definition:
- This defines the blueprint for the objects.
- Example:
```python
class MyClass:
    pass
```
## Class Variables:
- These are shared by all instances of the class.
- They are defined within the class but outside any instance methods.
- Example
```python
class MyClass:
    class_variable = "I am a class variable"
```

## Instance Variables:
- These are unique to each instance of the class.
- They are usually defined within the __init__ method
- __init__ is the constructor of the class.
- Example:
```python
class MyClass:
    def __init__(self, instance_variable):
        self.instance_variable = instance_variable
```

## Static Variables (Class Variables):
* These belong to a class and  are  shared by all instances of the class.
* Defined using the @staticmethod decorator if they belong to methods that don't modify class or instance state.
* Example:
```python
class MyClass:
    # This is a CLASS VARIABLE (aka STATIC VARIABLE)
    static_variable = "I am a static variable, Also shared by all instances"  # Same thing!
    class_variable = "I am shared by all instances, I am also  a static variable"
    
    @staticmethod
    def static_method():
        print("I am a static method")
```

## Initialization Sequence
### Class Definition and Class Variables
* When a class is defined, Python sets up the class and its class variables.
* Class variables are initialized once when the class is loaded into memory.
* Which means even before you create first instance of  new instance of this class, the class variable is initialized.

### Instance Creation and __init__
* When you create an instance of the class, Python calls the __init__ method.
* The __init__ method initializes instance variables for that particular object.
* instance variables are set when __init__ is called during object creation
* and this is called for every new onject creation
* Example:
```python
class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, instance_variable):
        self.instance_variable = instance_variable

# Creating an instance of MyClass
obj = MyClass("I am an instance variable")

```

## __call__ Method
- Makes instances of a class callable like functions.
- Can also be defined in a metaclass to make classes callable.
- Called when you use `instance()` or `ClassName()` syntax.

### Instance-level __call__:
- Used to make an instance callable
- Example:
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

# Create an instance
double = Multiplier(2)
# Call the instance like a function
result = double(5)  # Returns 10
```

### Metaclass-level __call__:
- Used to customize class instantiation
- The metaclass's __call__ method is invoked when creating an instance
- Signature: `def __call__(cls, *args, **kwargs):`
- Example:
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

db1 = Database("connection1")
db2 = Database("connection2")
# db1 is db2 == True (same instance)
```