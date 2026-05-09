# Python Beginner's Cheatsheet — Jupyter-Ready ✅
### For Python Students & Complete Beginners
> Every code cell below runs standalone in a Jupyter notebook. Just copy-paste and run!

---

## 1. Getting Started

### Variables & Assignment

```python
# Variables store data - think of them as labeled boxes
name = "Alice"      # String (text)
age = 25            # Integer (whole number)
height = 5.7        # Float (decimal number)
is_student = True   # Boolean (True/False)

print(name)         # Alice
print(age)          # 25
print(f"{name} is {age} years old")  # Alice is 25 years old
```

### Printing Output

```python
# Print displays text
print("Hello, World!")

# Print multiple things
print("Name:", "Bob", "Age:", 30)

# Print with variables
x = 42
print(f"The answer is {x}")      # f-strings (best way)
print("The answer is " + str(x)) # Manual conversion
```

### Comments

```python
# This is a comment - it's ignored by Python
# Use comments to explain WHY, not WHAT

x = 5  # Single-line comment
# Multi-line comments:
# are just multiple lines of #
```

---

## 2. Core Concepts

### Data Types

```python
# Check the type of any value
print(type(42))             # <class 'int'>
print(type(3.14))           # <class 'float'>
print(type("hello"))        # <class 'str'>
print(type(True))           # <class 'bool'>
print(type(None))           # <class 'NoneType'>

# Everything in Python is an object
# Variables are labels/references pointing to objects
```

### Variables as References (⭐ Important!)

```python
# Variables DON'T hold values, they POINT TO objects
a = [1, 2, 3]
b = a  # Both point to the SAME list

b.append(4)
print(a)  # [1, 2, 3, 4] ← Surprise! 'a' changed!

# To create a separate copy:
c = a.copy()
c.append(5)
print(a)  # [1, 2, 3, 4] ← Unchanged now
print(c)  # [1, 2, 3, 4, 5]

# Check if two variables point to the same object:
print(a is c)  # False - different objects
print(a is b)  # True - same object
```

### Type Conversion

```python
# Convert between types
x = int("42")       # "42" → 42
y = float("3.14")   # "3.14" → 3.14
z = str(100)        # 100 → "100"

print(f"x={x} (type: {type(x).__name__})")
print(f"y={y} (type: {type(y).__name__})")
print(f"z={z} (type: {type(z).__name__})")

# Remember: input() always returns a STRING
age_input = input("Enter age: ")  # User types: 25
age_number = int(age_input)       # Must convert to use as number
print(f"Next year you'll be {age_number + 1}")
```

---

## 3. Operators

### Arithmetic Operators

```python
print(10 + 3)    # 13     Addition
print(10 - 3)    # 7      Subtraction
print(10 * 3)    # 30     Multiplication
print(10 / 3)    # 3.333  Division (returns float)
print(10 // 3)   # 3      Floor division (drops decimal)
print(10 % 3)    # 1      Modulo (remainder)
print(2 ** 3)    # 8      Power (2 to the 3rd)
```

### Comparison Operators

```python
# These return True or False
print(5 == 5)    # True   Equal
print(5 != 3)    # True   Not equal
print(5 > 3)     # True   Greater than
print(5 >= 5)    # True   Greater than or equal
print(5 < 3)     # False  Less than
print(5 <= 5)    # True   Less than or equal
```

### Logical Operators

```python
# Combine conditions
age = 25

# 'and' - both must be true
if age >= 18 and age < 65:
    print("Working age")  # Prints!

# 'or' - at least one must be true
has_car = False
has_bike = True
if has_car or has_bike:
    print("Has transport")  # Prints!

# 'not' - flips the result
is_raining = False
if not is_raining:
    print("Go outside")  # Prints!
```

---

## 4. Strings

### String Basics

```python
s = "Hello, World!"

# Indexing - get single character
print(s[0])      # H (first character)
print(s[-1])     # ! (last character)

# Slicing - get a portion
print(s[0:5])    # Hello
print(s[7:])     # World!
print(s[::-1])   # !dlroW ,olleH (reversed)

# Length
print(len(s))    # 13
```

### String Methods

```python
s = "Hello, World!"

print(s.lower())           # hello, world!
print(s.upper())           # HELLO, WORLD!
print(s.replace("World", "Python"))  # Hello, Python!
print(s.split(","))        # ['Hello', ' World!']
print("-".join(["a","b","c"]))  # a-b-c
print(s.startswith("Hello"))    # True
print(s.endswith("!"))         # True
```

### F-Strings (Best Way to Format)

```python
name = "Alice"
age = 30
score = 95.7

# Basic f-string
print(f"Name: {name}, Age: {age}")

# Formatting numbers
print(f"Score: {score:.1f}")       # Score: 95.7
print(f"Score: {score:.0f}")       # Score: 96
print(f"Count: {1000000:,}")       # Count: 1,000,000

# Expressions in f-strings
print(f"Next year: {age + 1}")
print(f"Is adult: {age >= 18}")
```

---

## 5. Control Flow

### If / Elif / Else

```python
score = 85

if score >= 90:
    print("Grade A")
elif score >= 80:
    print("Grade B")      # This runs
elif score >= 70:
    print("Grade C")
else:
    print("Grade F")

# ⭐ Key: elif stops checking once a condition is true!
# Don't use multiple 'if' statements unless conditions are independent
```

### Loops - For

```python
# Loop through numbers
for i in range(5):        # 0, 1, 2, 3, 4
    print(i, end=" ")
print()

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# Loop with index
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")  # 0: apple, 1: banana, 2: cherry
```

### Loops - While

```python
# Repeat while condition is true
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1  # Same as count = count + 1

# Get valid input from user
while True:
    age = input("Enter age (number): ")
    try:
        age = int(age)
        if age >= 0:
            break  # Exit the loop
        else:
            print("Age can't be negative!")
    except ValueError:
        print("That's not a valid number!")
```

### Break & Continue

```python
# break - exit the loop
for i in range(10):
    if i == 5:
        break  # Stop looping
    print(i)  # 0 1 2 3 4

print()

# continue - skip to next iteration
for i in range(5):
    if i == 2:
        continue  # Skip this iteration
    print(i)  # 0 1 3 4 (skipped 2)
```

---

## 6. Data Structures Fundamentals

### Lists

```python
# Lists - ordered, mutable (can change)
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Add items
fruits.append("orange")
print(fruits)  # ['apple', 'banana', 'cherry', 'orange']

# Remove items
fruits.remove("banana")
print(fruits)  # ['apple', 'cherry', 'orange']

# Get item by index
print(fruits[0])  # apple
print(fruits[-1]) # orange (last item)

# Slice
print(fruits[0:2])  # ['apple', 'cherry']

# Length
print(len(fruits))  # 3

# Check if item exists
print("apple" in fruits)  # True
```

### Dictionaries

```python
# Dictionaries - key-value pairs
person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC"
}

# Access by key
print(person["name"])      # Alice
print(person.get("age"))   # 30

# Add/update
person["age"] = 31
person["job"] = "Engineer"
print(person)

# Check if key exists
if "name" in person:
    print("Has name field")

# Loop through
for key, value in person.items():
    print(f"{key}: {value}")
```

### Tuples

```python
# Tuples - ordered, immutable (can't change)
colors = ("red", "green", "blue")

# Access by index
print(colors[0])      # red
print(colors[-1])     # blue

# Can't modify
# colors[0] = "yellow"  # ERROR!

# But you can create a new tuple
colors2 = colors + ("yellow",)
print(colors2)  # ('red', 'green', 'blue', 'yellow')

# Unpacking
r, g, b = colors
print(f"RGB: {r}, {g}, {b}")
```

### Sets

```python
# Sets - unique items, unordered
numbers = {1, 2, 3, 3, 2, 1}
print(numbers)  # {1, 2, 3} - duplicates removed

# Add/remove
numbers.add(4)
numbers.remove(1)
print(numbers)  # {2, 3, 4}

# Check if item exists
print(3 in numbers)  # True

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a & b)  # {3, 4} intersection
print(a | b)  # {1, 2, 3, 4, 5, 6} union
print(a - b)  # {1, 2} difference
```

---

## 7. Functions Basics

### Defining Functions

```python
# Simple function
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Hello, Alice!

# Function with default argument
def power(base, exponent=2):
    return base ** exponent

print(power(3))      # 9 (uses default)
print(power(3, 3))   # 27 (uses custom)

# Function with multiple return values
def get_min_max(numbers):
    return min(numbers), max(numbers)

low, high = get_min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {low}, Max: {high}")  # Min: 1, Max: 9
```

### Scope & LEGB Rule (⭐ Important!)

```python
# LEGB = Local, Enclosing, Global, Built-in
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # Prints "local"

    inner()
    print(x)  # Prints "enclosing"

outer()
print(x)  # Prints "global"

# Variables are looked up in this order:
# 1. Local (inside this function)
# 2. Enclosing (in parent functions)
# 3. Global (top of file)
# 4. Built-in (Python's built-ins)
```

### Recursion

```python
# A function calling itself
def countdown(n):
    # BASE CASE - when to stop
    if n == 0:
        print("Blastoff!")
        return

    # RECURSIVE CASE - call self with smaller problem
    print(n)
    countdown(n - 1)

countdown(3)
# Output: 3, 2, 1, Blastoff!

# Factorial example
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
```

### Common Mistakes

```python
# ❌ Mistake 1: Mutable default argument
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] ← Unexpected!

# ✅ Fix: Use None
def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2] ✓

# ❌ Mistake 2: Forgetting return
def bad_double(x):
    x * 2  # This doesn't return anything!

result = bad_double(5)
print(result)  # None ✗

# ✅ Fix: Return the value
def good_double(x):
    return x * 2

result = good_double(5)
print(result)  # 10 ✓

# ❌ Mistake 3: Confusing return vs print
def print_version(x, y):
    print(x + y)  # Prints but returns None

def return_version(x, y):
    return x + y  # Returns the value

a = print_version(2, 3)  # Prints "5" but a=None
b = return_version(2, 3) # b=5 (can use it)
```

---

## 8. Working with Files

### Reading Files

```python
# Read entire file
with open("myfile.txt", "r") as f:
    content = f.read()
    print(content)

# Read line by line
with open("myfile.txt", "r") as f:
    for line in f:
        print(line.strip())  # strip() removes newline

# Read all lines into a list
with open("myfile.txt", "r") as f:
    lines = f.readlines()
    print(f"Total lines: {len(lines)}")
```

### Writing Files

```python
# Write to file (overwrites if exists)
with open("output.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")

# Append to file (adds to end)
with open("output.txt", "a") as f:
    f.write("Line 4\n")
```

### File Safety with 'with'

```python
# ✅ GOOD: Uses 'with' (automatically closes file)
with open("data.txt", "r") as f:
    content = f.read()
print(content)
# File automatically closed

# ❌ BAD: Manual file handling (risky)
f = open("data.txt", "r")
content = f.read()
f.close()  # Easy to forget!
```

---

## 9. Error Handling Basics

### Try / Except

```python
# Handle errors gracefully
try:
    age = int(input("Enter age: "))
    if age < 0:
        print("Age can't be negative")
    else:
        print(f"You are {age} years old")
except ValueError:
    print("That's not a valid number!")

# Multiple except blocks
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero!")
except TypeError:
    print("Type mismatch!")
except Exception as e:
    print(f"Unknown error: {e}")

# Finally - runs no matter what
try:
    data = open("file.txt", "r").read()
except FileNotFoundError:
    print("File not found!")
finally:
    print("Cleanup code runs here")
```

---

## 10. Common Built-in Functions

```python
# Useful functions everyone should know
numbers = [5, 2, 8, 1, 9]

print(len(numbers))      # 5 - length
print(sum(numbers))      # 25 - sum
print(min(numbers))      # 1 - minimum
print(max(numbers))      # 9 - maximum
print(sorted(numbers))   # [1, 2, 5, 8, 9] - sorted

# range - create sequence of numbers
for i in range(3):
    print(i)  # 0, 1, 2

# enumerate - get index and value
for i, num in enumerate(numbers):
    print(f"{i}: {num}")

# zip - combine two lists
letters = ["a", "b", "c"]
for letter, number in zip(letters, numbers):
    print(f"{letter}: {number}")
```

---

## 11. Common Pitfalls

### ⚠️ Modifying List During Iteration

```python
# ❌ WRONG - skips items!
numbers = [1, 2, 3, 4, 5, 6]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)
print(numbers)  # [1, 3, 5] - missing 6!

# ✅ RIGHT - iterate over a copy
numbers = [1, 2, 3, 4, 5, 6]
for num in numbers[:]:  # Use [:] to copy
    if num % 2 == 0:
        numbers.remove(num)
print(numbers)  # [1, 3, 5] ✓

# ✅ BETTER - use list comprehension
numbers = [num for num in numbers if num % 2 != 0]
```

### ⚠️ Mutable vs Immutable

```python
# MUTABLE (can be changed in-place)
lst = [1, 2, 3]
lst2 = lst
lst.append(4)
print(lst2)  # [1, 2, 3, 4] ← Changed!

# IMMUTABLE (creates new object)
s = "hello"
s2 = s
s = s.upper()
print(s2)  # "hello" ← Unchanged ✓
```

### ⚠️ `==` vs `is`

```python
# == checks VALUE
# is checks IDENTITY (same object)

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - same content
print(a is b)  # False - different objects

print(a == c)  # True - same content
print(a is c)  # True - same object

# Use 'is' for None, True, False
if result is None:
    print("No result yet")
```

### ⚠️ Integer vs Float Division

```python
# / always returns float
print(10 / 2)   # 5.0 (float, not 5!)
print(type(10 / 2))  # <class 'float'>

# // returns integer (floor division)
print(10 // 2)  # 5 (int)
print(10 // 3)  # 3 (drops decimal)
```

---

## 12. Best Practices

### Naming Conventions

```python
# Use descriptive names!
# ❌ Bad
x = 25
fn = lambda n: n * 2
l = [1, 2, 3]

# ✅ Good
user_age = 25
double = lambda n: n * 2
numbers = [1, 2, 3]
```

### Commenting & Documentation

```python
def calculate_area(length, width):
    """Calculate the area of a rectangle.

    Args:
        length: The length in meters
        width: The width in meters

    Returns:
        The area in square meters
    """
    return length * width

# Comments explain WHY, not WHAT
# ❌ Bad: x = x + 1  # Add 1 to x
# ✅ Good: score += 1  # Increment score for correct answer
```

### PEP 8 Style Basics

```python
# Use 4 spaces for indentation (not tabs)
# Keep lines under 79 characters
# Use lowercase with underscores for variables: user_age
# Use UPPERCASE for constants: MAX_SIZE = 100
# Add spaces around operators: x = 5 + 3 (not x=5+3)

# Good example:
MAX_ATTEMPTS = 3

def check_password(attempt):
    if len(attempt) < 8:
        return False
    return True
```

---

## 13. Next Steps

### Where to Go From Here

- **Data Structures**: Learn about advanced dict/list operations
- **Object-Oriented Programming**: Classes, inheritance, composition
- **Error Handling**: Exception handling, custom exceptions
- **File I/O**: Working with JSON, CSV, and other formats
- **Modules & Libraries**: Use external packages from PyPI

### Useful Built-in Modules

```python
import math
print(math.sqrt(16))  # 4.0

import random
print(random.choice([1, 2, 3]))  # Random element

import datetime
print(datetime.date.today())  # Current date
```

---

**Python Beginner's Cheatsheet — Jupyter-Ready ✅**

Every code example above can be copied and pasted into a Jupyter notebook. Try modifying them!
