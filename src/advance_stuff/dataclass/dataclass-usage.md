# `@dataclass` decorator

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# Basic dataclass
@dataclass
class Point:
    x: int
    y: int

# Without dataclass, you'd need to write:
class PointWithoutDataclass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"PointWithoutDataclass(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, PointWithoutDataclass):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

# Dataclass with default values
@dataclass
class Person:
    name: str
    age: int = 0  # Default value
    email: Optional[str] = None  # Optional field with default None

# Dataclass with computed fields
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # Not included in __init__
    
    def __post_init__(self):
        # Computed after initialization
        self.area = self.width * self.height

# Dataclass with custom field options
@dataclass
class Student:
    name: str
    # List that defaults to empty list using field()
    grades: List[float] = field(default_factory=list)
    # Private field (not included in repr)
    _id: int = field(default=0, repr=False)
    # Computed property using field
    created_at: datetime = field(
        default_factory=datetime.now,
        repr=True,
        compare=False  # Not used in comparisons
    )

# Frozen (immutable) dataclass
@dataclass(frozen=True)
class Configuration:
    host: str
    port: int = 8080
    
    # Even with frozen=True, you can still have computed properties
    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

# Inheritance with dataclasses
@dataclass
class Animal:
    name: str
    species: str

@dataclass
class Dog(Animal):
    breed: str
    # species will be automatically included from Animal

def demonstrate_dataclass_features():
    # Basic usage
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    print(f"Points: {p1}, {p2}")
    print(f"Points equal? {p1 == p2}")  # True, automatic equality
    
    # Default values
    person = Person("Alice")
    print(f"\nPerson with defaults: {person}")
    
    # Computed fields
    rect = Rectangle(width=5, height=3)
    print(f"\nRectangle: {rect}")
    
    # List field with default_factory
    student = Student("Bob")
    student.grades.append(95.5)
    print(f"\nStudent: {student}")
    
    # Frozen dataclass
    config = Configuration("localhost")
    print(f"\nConfiguration: {config}")
    print(f"Address: {config.address}")
    
    try:
        config.port = 9000  # This will raise FrozenInstanceError
    except Exception as e:
        print(f"Cannot modify frozen dataclass: {str(e)}")
    
    # Inheritance
    dog = Dog("Rex", "Canis lupus", "German Shepherd")
    print(f"\nDog: {dog}")

if __name__ == "__main__":
    demonstrate_dataclass_features()

```

Key features and benefits of `@dataclass`:

1. **Automatic Method Generation**:
   ```python
   @dataclass
   class Point:
       x: int
       y: int
   ```
   Automatically creates:
   - `__init__`
   - `__repr__`
   - `__eq__`
   - `__hash__` (if specified)

2. **Type Hints and Default Values**:
   ```python
   @dataclass
   class Person:
       name: str
       age: int = 0  # Default value
   ```
   - Enforces type hints
   - Supports default values
   - Works well with IDE autocompletion

3. **Computed Fields**:
   ```python
   @dataclass
   class Rectangle:
       width: float
       height: float
       area: float = field(init=False)
       
       def __post_init__(self):
           self.area = self.width * self.height
   ```
   - Use `field(init=False)` for computed values
   - `__post_init__` runs after `__init__`

4. **Field Customization**:
   ```python
   @dataclass
   class Student:
       grades: List[float] = field(
           default_factory=list,
           repr=True,
           compare=False
       )
   ```
   Field options include:
   - `default_factory`: Callable for mutable defaults
   - `repr`: Include in string representation
   - `compare`: Include in comparisons
   - `hash`: Include in hash computation
   - `init`: Include in `__init__`

5. **Dataclass Options**:
   ```python
   @dataclass(frozen=True, order=True)
   class Config:
       host: str
       port: int = 8080
   ```
   Common options:
   - `frozen=True`: Makes instance immutable
   - `order=True`: Adds comparison methods
   - `slots=True`: Uses `__slots__` for memory efficiency
   - `kw_only=True`: Forces keyword-only arguments

6. **Inheritance Support**:
   ```python
   @dataclass
   class Animal:
       name: str
   
   @dataclass
   class Dog(Animal):
       breed: str  # Adds to parent fields
   ```
   - Properly handles inheritance
   - Combines fields from parent classes

Benefits of using dataclasses:
1. Reduces boilerplate code
2. Makes code more readable
3. Provides type safety
4. Automatic method generation
5. Easy to modify and maintain
6. Great for data-oriented programming
