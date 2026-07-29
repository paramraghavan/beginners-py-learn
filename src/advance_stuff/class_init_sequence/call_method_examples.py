"""
Examples demonstrating __call__ method usage
- Instance-level __call__: makes instances callable like functions
- Metaclass-level __call__: customizes class instantiation
"""

print("=" * 80)
print("Example 1: Instance-level __call__")
print("=" * 80)


class Multiplier:
    """A callable class that multiplies input by a factor"""

    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        """Called when instance is used with () syntax"""
        return x * self.factor


# Create instances
double = Multiplier(2)
triple = Multiplier(3)

# Call instances like functions
print(f"double(5) = {double(5)}")  # 10
print(f"triple(5) = {triple(5)}")  # 15

print("\n" + "=" * 80)
print("Example 2: Metaclass-level __call__ (Singleton Pattern)")
print("=" * 80)


class SingletonMeta(type):
    """Metaclass that creates singleton classes"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Override class instantiation to return existing instance"""
        if cls not in cls._instances:
            print(f"Creating new instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            print(f"Returning existing instance of {cls.__name__}")
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """A database connection (singleton)"""

    def __init__(self, connection_string):
        print(f"Initializing Database with: {connection_string}")
        self.connection = connection_string


# Test singleton pattern
print("\nFirst instantiation:")
db1 = Database("localhost:5432")

print("\nSecond instantiation:")
db2 = Database("different_connection")

print(f"\ndb1 is db2: {db1 is db2}")  # True - same instance
print(f"db1.connection: {db1.connection}")  # localhost:5432

print("\n" + "=" * 80)
print("Example 3: Decorator using __call__")
print("=" * 80)


class CountCalls:
    """Callable decorator that counts function calls"""

    def __init__(self, func):
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        """Called when decorated function is invoked"""
        self.call_count += 1
        result = self.func(*args, **kwargs)
        print(f"  [Call #{self.call_count}]")
        return result


@CountCalls
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"


print("Calling greet() three times:")
greet("Alice")
greet("Bob")
greet("Charlie")
print(f"Total calls: {greet.call_count}")

print("\n" + "=" * 80)
print("Example 4: Factory Pattern using __call__")
print("=" * 80)


class Shape:
    """Base shape class"""

    def __init__(self, name):
        self.name = name

    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class ShapeFactory:
    """Factory class that creates shapes"""

    def __init__(self):
        self.shapes = {"circle": Circle, "rectangle": Rectangle}

    def __call__(self, shape_type, *args, **kwargs):
        """Create shape based on type"""
        shape_class = self.shapes.get(shape_type.lower())
        if shape_class:
            return shape_class(*args, **kwargs)
        raise ValueError(f"Unknown shape type: {shape_type}")


# Use factory
factory = ShapeFactory()

circle = factory("circle", radius=5)
rectangle = factory("rectangle", width=4, height=6)

print(f"Circle area: {circle.area()}")  # 78.5
print(f"Rectangle area: {rectangle.area()}")  # 24

print("\n" + "=" * 80)
print("Example 5: Metaclass __call__ with initialization control")
print("=" * 80)


class LoggingMeta(type):
    """Metaclass that logs instance creation"""

    def __call__(cls, *args, **kwargs):
        print(f"[LOG] Creating instance of {cls.__name__} with args={args}, kwargs={kwargs}")
        instance = super().__call__(*args, **kwargs)
        print(f"[LOG] Instance created successfully: {instance}")
        return instance


class User(metaclass=LoggingMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name={self.name}, age={self.age})"


print("\nCreating user:")
user = User("John", 30)
