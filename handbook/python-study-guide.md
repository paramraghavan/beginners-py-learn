# The Complete Python Study Guide
### From Basics to Advanced | Interview Ready | For Developers, Data Scientists & Data Engineers

> Built from the [beginners-py-learn](https://github.com/paramraghavan/beginners-py-learn) repository.
> Every code example can be run in the sandbox (see Chapter 1).

---

## Table of Contents

- [Chapter 1: Setting Up Your Sandbox](#chapter-1-setting-up-your-sandbox)
- [Chapter 2: Python Basics](#chapter-2-python-basics)
- [Chapter 3: Data Structures](#chapter-3-data-structures)
- [Chapter 4: Functions & Functional Programming](#chapter-4-functions--functional-programming)
- [Chapter 5: Object-Oriented Programming](#chapter-5-object-oriented-programming)
- [Chapter 6: Error Handling & Exceptions](#chapter-6-error-handling--exceptions)
- [Chapter 7: File I/O & Serialization](#chapter-7-file-io--serialization)
- [Chapter 8: Modules, Packages & Imports](#chapter-8-modules-packages--imports)
- [Chapter 9: Python Environment, pip & Dependency Management](#chapter-9-python-environment-pip--dependency-management)
- [Chapter 10: Debugging & Profiling](#chapter-10-debugging--profiling)
- [Chapter 11: Intermediate Python](#chapter-11-intermediate-python)
- [Chapter 12: Advanced Python](#chapter-12-advanced-python)
- [Chapter 13: Concurrency & Parallelism](#chapter-13-concurrency--parallelism)
- [Chapter 14: Design Patterns](#chapter-14-design-patterns)
- [Chapter 15: Data Science with Python](#chapter-15-data-science-with-python)
- [Chapter 16: Data Engineering with Python](#chapter-16-data-engineering-with-python)
- [Chapter 17: Testing & Code Quality](#chapter-17-testing--code-quality)
- [Chapter 18: Data Structures & Algorithms](#chapter-18-data-structures--algorithms)
- [Chapter 19: Interview Questions & Answers](#chapter-19-interview-questions--answers)
- [Appendix A: Quick Reference / Cheatsheet](#appendix-a-quick-reference--cheatsheet)
- [Appendix B: Resources & References](#appendix-b-resources--references)

---

## Chapter 1: Setting Up Your Sandbox

A sandbox is your safe playground to experiment with Python code. You can test examples, break things, and learn without any risk.

### 1.1 What You Need

Before anything, you need Python installed on your machine. Let's check if you already have it:

```bash
# Open Terminal (Mac/Linux) or Command Prompt (Windows)
python --version
# or
python3 --version
```

If you see something like `Python 3.10.x` or higher, you're good. If not, download Python from [python.org](https://python.org).

**Windows users**: During installation, **check the box "Add Python to PATH"**. This is the #1 mistake beginners make. Without this, your terminal won't find Python.

### 1.2 Jupyter Notebook Setup (Recommended Sandbox)

Jupyter Notebook lets you write and run Python code in your browser, one block at a time. It's perfect for learning because you can see results immediately.

**Step 1: Create a virtual environment** (this isolates your project's packages from the system):

```bash
# Navigate to where you want your project
cd ~/my-python-learning

# Create a virtual environment named .venv
python -m venv .venv
```

**Step 2: Activate the virtual environment:**

```bash
# Mac/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# You should see (.venv) at the beginning of your terminal prompt
# That means you're inside the virtual environment
```

**Step 3: Install Jupyter:**

```bash
python -m pip install --upgrade pip
python -m pip install notebook
```

**Step 4: Launch Jupyter:**

```bash
jupyter notebook
```

Your browser will open automatically. You'll see a file browser. Click **New > Python 3** to create a new notebook.

**Step 5: Try it out:**

In the first cell, type:
```python
print("Hello, World!")
```

Press **Shift + Enter** to run the cell. You should see `Hello, World!` printed below.

**Step 6: Try a few more cells:**

```python
# Cell 2: Math
2 + 2
```
(Output: `4`)

```python
# Cell 3: Variables
name = "Alice"
age = 30
print(f"My name is {name} and I am {age} years old.")
```
(Output: `My name is Alice and I am 30 years old.`)

### 1.3 Jupyter Tips

| What you want to do | How |
|---|---|
| Run a cell | **Shift + Enter** |
| Run cell, stay in same cell | **Ctrl + Enter** |
| Add a cell above | Press **A** (when not editing) |
| Add a cell below | Press **B** (when not editing) |
| Delete a cell | Press **DD** (double D, when not editing) |
| Undo delete | **Z** |
| Switch to Markdown | Press **M** |
| Switch to Code | Press **Y** |
| Time an expression | `%timeit [x**2 for x in range(1000)]` |
| Time a whole cell | Put `%%time` as the first line |
| List all variables | `%who` or `%whos` for details |
| Run a shell command | `!pip install pandas` |
| Load a Python file into a cell | `%load filename.py` |

### 1.4 Alternative: Anaconda (Batteries Included)

If you want everything pre-installed (Jupyter, pandas, numpy, matplotlib, etc.):

1. Download Anaconda from [anaconda.com](https://www.anaconda.com/)
2. Install with defaults
3. Open **Anaconda Navigator** or run `jupyter notebook` from Anaconda Prompt

### 1.5 IDE Setup (For Larger Projects)

Once you move beyond experiments, you'll want an IDE:

| IDE | Best For | Cost | Setup |
|---|---|---|---|
| **VS Code** | General Python, lightweight | Free | Install Python extension, Ctrl+Shift+P > "Python: Select Interpreter" |
| **PyCharm CE** | Large projects, great debugger | Free | Community Edition has built-in venv support |
| **Spyder** | Data science (MATLAB-like) | Free | Comes with Anaconda, has variable explorer |

### 1.6 Troubleshooting Common Setup Issues

**"jupyter: command not found":**
```bash
# Use python -m instead:
python -m notebook

# Or for Python 3 specifically:
python3 -m notebook
```

**"python: command not found" on Mac:**
```bash
# macOS often uses python3 instead of python
python3 --version
python3 -m venv .venv
```

**Multiple Python versions causing confusion:**
```bash
# See exactly which Python you're using:
which python       # Mac/Linux
where python       # Windows

# See the full path:
python -c "import sys; print(sys.executable)"
```

### Exercise 1.1: Verify Your Setup
Create a Jupyter notebook and run these cells to verify everything works:

```python
# Cell 1
import sys
print(f"Python version: {sys.version}")
print(f"Python location: {sys.executable}")

# Cell 2
print("Hello from Jupyter!")
2 + 2  # Should show 4

# Cell 3
# Test that you can install packages
!pip install requests
import requests
print(f"Requests version: {requests.__version__}")
```

---

## Chapter 2: Python Basics

### 2.1 Variables and Data Types

In Python, you don't declare variable types. Python figures it out automatically:

```python
# Numbers
age = 25              # This is an integer (int) - whole numbers
price = 19.99         # This is a float - decimal numbers
complex_num = 3 + 4j  # This is a complex number (used in math/engineering)

# Strings - text enclosed in quotes (single or double, both work)
name = "Alice"
greeting = 'Hello'
multiline = """This is a
multi-line string.
It preserves line breaks."""

# Boolean - True or False (note the capital T and F)
is_active = True
is_empty = False

# None - represents "no value" or "nothing"
result = None

# Check what type a variable is:
print(type(age))       # <class 'int'>
print(type(price))     # <class 'float'>
print(type(name))      # <class 'str'>
print(type(is_active)) # <class 'bool'>
print(type(result))    # <class 'NoneType'>
```

**Type conversion** - changing one type to another:

```python
# String to number
x = int("42")       # x is now the integer 42
y = float("3.14")   # y is now the float 3.14

# Number to string
z = str(100)         # z is now the string "100"

# This is important because you can't mix types carelessly:
age = 25
# print("I am " + age + " years old")  # ERROR! Can't add int to str
print("I am " + str(age) + " years old")  # OK: convert int to str first
print(f"I am {age} years old")             # Better: f-strings handle it
```

**Quick reference - Python data types:**

| Type | Mutable? | Ordered? | Duplicates? | Example | When to use |
|---|---|---|---|---|---|
| `int` | N/A | N/A | N/A | `42` | Counting, indexing |
| `float` | N/A | N/A | N/A | `3.14` | Measurements, money |
| `str` | No | Yes | Yes | `"hello"` | Text |
| `list` | Yes | Yes | Yes | `[1, 2, 3]` | Ordered collection that changes |
| `tuple` | No | Yes | Yes | `(1, 2, 3)` | Fixed data (coordinates, records) |
| `set` | Yes | No | No | `{1, 2, 3}` | Unique items, membership testing |
| `dict` | Yes | Yes* | Keys: No | `{"a": 1}` | Key-value mappings |
| `bool` | No | N/A | N/A | `True` | Conditions |

*Dicts are insertion-ordered since Python 3.7

### 2.2 Operators

**Arithmetic operators** - the basics of math:

```python
print(10 + 3)    # 13     Addition
print(10 - 3)    # 7      Subtraction
print(10 * 3)    # 30     Multiplication
print(10 / 3)    # 3.333  Float division (always returns float)
print(10 // 3)   # 3      Floor division (drops the decimal)
print(10 % 3)    # 1      Modulo (remainder after division)
print(10 ** 3)   # 1000   Power (10 to the 3rd)

# Floor division is useful for things like:
total_minutes = 135
hours = total_minutes // 60    # 2 hours
minutes = total_minutes % 60   # 15 minutes
print(f"{hours}h {minutes}m")  # 2h 15m
```

**Comparison operators** - return True or False:

```python
print(5 == 5)    # True   Equal to
print(5 != 3)    # True   Not equal to
print(5 > 3)     # True   Greater than
print(5 >= 5)    # True   Greater than or equal
print(5 < 3)     # False  Less than
print(5 <= 5)    # True   Less than or equal
```

**Logical operators** - combine conditions:

```python
age = 25
income = 50000

# 'and' - BOTH must be true
if age >= 18 and income >= 30000:
    print("Eligible for loan")  # This prints

# 'or' - AT LEAST ONE must be true
has_degree = False
has_experience = True
if has_degree or has_experience:
    print("Can apply for job")  # This prints

# 'not' - flips True to False and vice versa
is_banned = False
if not is_banned:
    print("Welcome!")  # This prints
```

**Identity operators** - `is` vs `==`:

```python
# == checks if VALUES are the same
# is checks if they're the SAME OBJECT in memory

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True  - same values
print(a is b)    # False - different objects (two separate lists)
print(a is c)    # True  - c points to the same list as a

# RULE: Only use 'is' for None, True, False
if result is None:
    print("No result yet")
```

**Membership operators** - check if something is "in" a collection:

```python
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)      # True
print("grape" not in fruits)   # True

message = "Hello, World!"
print("World" in message)      # True
```

**Walrus operator** `:=` (Python 3.8+) - assign and use in one expression:

```python
# Without walrus:
data = [1, 5, 12, 3, 8]
n = len(data)
if n > 3:
    print(f"List has {n} elements")

# With walrus - more concise:
if (n := len(data)) > 3:
    print(f"List has {n} elements")

# Useful in while loops:
while (line := input("Enter text (q to quit): ")) != "q":
    print(f"You typed: {line}")
```

### 2.3 Strings In Depth

Strings are one of the most-used types. Let's cover them thoroughly.

**Indexing and slicing:**

```python
s = "Hello, World!"
#    H e l l o ,   W o r  l  d  !
#    0 1 2 3 4 5 6 7 8 9 10 11 12    <- positive index
#  -13      ...           -2 -1      <- negative index

# Single character
print(s[0])       # 'H' - first character
print(s[-1])      # '!' - last character

# Slicing: s[start:stop]  (start included, stop excluded)
print(s[0:5])     # 'Hello'
print(s[7:12])    # 'World'
print(s[:5])      # 'Hello' (from beginning)
print(s[7:])      # 'World!' (to end)

# Step: s[start:stop:step]
print(s[::2])     # 'Hlo ol!' - every 2nd character
print(s[::-1])    # '!dlroW ,olleH' - reversed
```

**Common string methods:**

```python
s = "  Hello, World!  "

# Cleaning
print(s.strip())          # "Hello, World!" - remove whitespace from both ends
print(s.lstrip())         # "Hello, World!  " - left strip only
print(s.rstrip())         # "  Hello, World!" - right strip only

# Case
print(s.strip().upper())  # "HELLO, WORLD!"
print(s.strip().lower())  # "hello, world!"
print("hello world".title())  # "Hello World"
print("hello world".capitalize())  # "Hello world"

# Searching
print(s.strip().find("World"))    # 7 (index where found)
print(s.strip().find("Python"))   # -1 (not found)
print(s.strip().count("l"))       # 3

# Checking
print("hello123".isalnum())       # True - letters and numbers only
print("hello".isalpha())          # True - letters only
print("123".isdigit())            # True - digits only
print("hello".startswith("hel"))  # True
print("hello".endswith("llo"))    # True

# Splitting and joining
csv_line = "Alice,30,NYC"
parts = csv_line.split(",")       # ['Alice', '30', 'NYC']
print(parts[0])                   # 'Alice'

words = ["Python", "is", "great"]
sentence = " ".join(words)        # "Python is great"
path = "/".join(["home", "user", "docs"])  # "home/user/docs"

# Replacing
text = "Hello, World!"
new_text = text.replace("World", "Python")  # "Hello, Python!"
```

**f-strings** (Python 3.6+) - the best way to format strings:

```python
name = "Alice"
age = 30
salary = 75000.50

# Basic interpolation
print(f"Name: {name}, Age: {age}")

# Expressions inside braces
print(f"Next year: {age + 1}")
print(f"Name in caps: {name.upper()}")

# Number formatting
print(f"Salary: ${salary:,.2f}")       # Salary: $75,000.50
print(f"Big number: {1000000:,}")      # Big number: 1,000,000
print(f"Percentage: {0.856:.1%}")      # Percentage: 85.6%
print(f"Binary: {42:b}")              # Binary: 101010
print(f"Hex: {255:x}")               # Hex: ff

# Alignment and padding
print(f"{'left':<20}|")     # 'left                |'
print(f"{'right':>20}|")    # '               right|'
print(f"{'center':^20}|")   # '       center       |'
print(f"{'padded':*^20}")   # '*******padded*******'

# Multi-line f-strings
message = (
    f"User Report\n"
    f"{'='*30}\n"
    f"Name:   {name}\n"
    f"Age:    {age}\n"
    f"Salary: ${salary:,.2f}\n"
)
print(message)
```

**IMPORTANT: String concatenation performance:**

```python
# BAD - O(n^2) because strings are immutable, each += creates a new string
result = ""
for i in range(10000):
    result += str(i)  # SLOW for large loops

# GOOD - O(n) using join
parts = []
for i in range(10000):
    parts.append(str(i))
result = "".join(parts)  # FAST

# BEST - use list comprehension + join
result = "".join(str(i) for i in range(10000))
```

### 2.4 Control Flow: if/elif/else

```python
# Basic if/elif/else
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")  # Score: 85, Grade: B
```

**Ternary expression** - one-line if/else:

```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # "adult"

# Useful in f-strings
print(f"You are {'old enough' if age >= 21 else 'too young'} to drink")
```

**Match statement** (Python 3.10+) - like switch/case:

```python
command = "start"

match command:
    case "start":
        print("Starting the engine...")
    case "stop" | "quit" | "exit":   # Multiple values
        print("Shutting down...")
    case str(s) if s.startswith("go "):  # Guard clause
        destination = s[3:]
        print(f"Going to {destination}")
    case _:                              # Default (like else)
        print(f"Unknown command: {command}")
```

**Truthy and Falsy values** - what counts as True/False:

```python
# These are all FALSY (treated as False):
# None, False, 0, 0.0, "", [], {}, set(), ()

# Everything else is TRUTHY (treated as True)

# This is useful for checking if something is empty:
my_list = []
if my_list:
    print("List has items")
else:
    print("List is empty")  # This prints

my_name = "Alice"
if my_name:
    print(f"Hello, {my_name}")  # This prints

# Common pattern: use 'or' for defaults
username = ""  # empty string is falsy
display_name = username or "Anonymous"
print(display_name)  # "Anonymous"
```

### 2.5 Loops

**for loops:**

```python
# Loop through a range of numbers
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10):    # 2, 3, 4, 5, 6, 7, 8, 9
    print(i)

for i in range(0, 20, 3): # 0, 3, 6, 9, 12, 15, 18
    print(i)

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# Loop with index using enumerate
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# Output:
# 0: apple
# 1: banana
# 2: cherry

# Start enumerate at 1
for num, fruit in enumerate(fruits, start=1):
    print(f"{num}. {fruit}")
# Output:
# 1. apple
# 2. banana
# 3. cherry

# Loop through two lists simultaneously with zip
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# Loop through dictionary
person = {"name": "Alice", "age": 30, "city": "NYC"}
for key, value in person.items():
    print(f"{key}: {value}")
```

**while loops:**

```python
# Basic while loop
count = 0
while count < 5:
    print(f"Count is {count}")
    count += 1

# While with user input
while True:
    answer = input("Type 'quit' to exit: ")
    if answer.lower() == 'quit':
        break
    print(f"You said: {answer}")
```

**break, continue, and for/else:**

```python
# break - exit the loop immediately
for i in range(10):
    if i == 5:
        print("Found 5, stopping!")
        break
    print(i)
# Output: 0, 1, 2, 3, 4, Found 5, stopping!

# continue - skip the rest of this iteration
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)
# Output: 1, 3, 5, 7, 9

# for/else - the else block runs if the loop completed WITHOUT break
def find_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False  # Not prime, divisible by i
    return True  # No divisor found, it's prime

for n in range(2, 20):
    if find_prime(n):
        print(f"{n} is prime")
```

### 2.6 List Comprehensions

List comprehensions are a concise way to create lists. They're very Pythonic and you'll see them everywhere.

```python
# Instead of this:
squares = []
for x in range(10):
    squares.append(x ** 2)

# Write this:
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With a condition (filter):
# Only even numbers squared
even_squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# With if/else (transform):
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']

# Nested: flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Read as: "for each row, for each num in that row, give me num"

# Dict comprehension
words = ["hello", "world", "python"]
word_lengths = {word: len(word) for word in words}
# {'hello': 5, 'world': 5, 'python': 6}

# Set comprehension (unique values)
numbers = [1, 2, 2, 3, 3, 3, 4]
unique_doubles = {x * 2 for x in numbers}
# {2, 4, 6, 8}

# Generator expression - like list comp but LAZY (memory efficient)
# Use () instead of []
total = sum(x**2 for x in range(1000000))  # Doesn't create a list in memory
```

### Exercise 2.1: Find the Mode
Given a string of space-separated numbers, find the most frequent value:
```python
data = '13 13 13 13 14 16 18 21'
# Your code here...
# Expected output: Mode: 13

# Hint: split the string, count with a dictionary or collections.Counter
```

<details>
<summary>Solution</summary>

```python
from collections import Counter

data = '13 13 13 13 14 16 18 21'
numbers = data.split()  # Split into list of strings
counts = Counter(numbers)
mode = counts.most_common(1)[0][0]
print(f"Mode: {mode}")  # Mode: 13
```
</details>

### Exercise 2.2: FizzBuzz
Print numbers 1-30. For multiples of 3 print "Fizz", multiples of 5 print "Buzz", multiples of both print "FizzBuzz".

<details>
<summary>Solution</summary>

```python
for i in range(1, 31):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```
</details>

### Exercise 2.3: String Processing
Given a sentence, count the number of words, find the longest word, and reverse the word order.

<details>
<summary>Solution</summary>

```python
sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
print(f"Word count: {len(words)}")
print(f"Longest word: {max(words, key=len)}")
print(f"Reversed: {' '.join(reversed(words))}")
```
</details>

---

## Chapter 3: Data Structures

### 3.1 Lists

Lists are the most commonly used data structure. They're ordered, changeable, and allow duplicates.

```python
# Creating lists
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14, None]  # Can mix types
nested = [[1, 2], [3, 4], [5, 6]]       # List of lists

# Accessing elements
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
print(fruits[0])      # "apple" (first item)
print(fruits[-1])     # "elderberry" (last item)
print(fruits[1:3])    # ["banana", "cherry"] (slice: index 1 to 2)
print(fruits[:3])     # ["apple", "banana", "cherry"] (first 3)
print(fruits[2:])     # ["cherry", "date", "elderberry"] (from index 2 onwards)
print(fruits[::2])    # ["apple", "cherry", "elderberry"] (every 2nd)
print(fruits[::-1])   # reversed list
```

**Modifying lists:**

```python
fruits = ["apple", "banana", "cherry"]

# Add items
fruits.append("date")         # Add to end: ["apple","banana","cherry","date"]
fruits.insert(1, "blueberry") # Insert at index 1: ["apple","blueberry","banana","cherry","date"]
fruits.extend(["fig", "grape"])  # Add multiple to end

# Remove items
fruits.remove("banana")       # Remove first occurrence of "banana"
last = fruits.pop()           # Remove and return last item
second = fruits.pop(1)        # Remove and return item at index 1
del fruits[0]                 # Delete item at index 0

# Modify items
fruits[0] = "avocado"         # Replace first item

# Other operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()                 # Sort in place: [1, 1, 2, 3, 4, 5, 6, 9]
numbers.sort(reverse=True)     # Sort descending: [9, 6, 5, 4, 3, 2, 1, 1]
numbers.reverse()              # Reverse in place
print(numbers.count(1))        # 2 (how many times 1 appears)
print(numbers.index(5))        # Index of first 5

# IMPORTANT: sort() vs sorted()
original = [3, 1, 4, 1, 5]
new_sorted = sorted(original)  # Returns NEW sorted list, original unchanged
original.sort()                # Sorts IN PLACE, returns None
```

**Sorting with custom keys:**

```python
# Sort strings by length
words = ["python", "hi", "jupyter", "code"]
print(sorted(words, key=len))
# ['hi', 'code', 'python', 'jupyter']

# Sort list of tuples by second element
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students.sort(key=lambda s: s[1], reverse=True)
# [('Bob', 92), ('Alice', 85), ('Charlie', 78)]

# Sort dicts by a value
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]
by_age = sorted(people, key=lambda p: p["age"])
```

**Useful built-in functions with lists:**

```python
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(len(nums))       # 10 - number of items
print(sum(nums))       # 55 - sum of all items
print(min(nums))       # 1  - smallest
print(max(nums))       # 10 - largest

# any() and all() - super useful with conditions
print(any(x > 8 for x in nums))   # True - at least one is > 8
print(all(x > 0 for x in nums))   # True - ALL are > 0
print(all(x > 5 for x in nums))   # False - not all are > 5
```

### 3.2 Tuples

Tuples are like lists but **immutable** (can't be changed after creation). Use them for data that shouldn't change.

```python
# Creating tuples
point = (3, 4)
rgb = (255, 128, 0)
single = (42,)     # Note: comma is needed for single-element tuple!
empty = ()

# NOT a tuple:
not_a_tuple = (42)  # This is just the integer 42 with parentheses

# Accessing (same as lists)
print(point[0])    # 3
print(point[1])    # 4

# You CANNOT modify tuples:
# point[0] = 5     # TypeError: 'tuple' object does not support item assignment
```

**Tuple unpacking** - very useful!

```python
# Basic unpacking
point = (3, 4)
x, y = point
print(f"x={x}, y={y}")  # x=3, y=4

# Swap variables (Pythonic way)
a, b = 1, 2
a, b = b, a       # Now a=2, b=1

# Unpack in a loop
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
for name, score in students:
    print(f"{name}: {score}")

# Star unpacking
first, *rest = [1, 2, 3, 4, 5]
print(first)   # 1
print(rest)    # [2, 3, 4, 5]

*beginning, last = [1, 2, 3, 4, 5]
print(beginning)  # [1, 2, 3, 4]
print(last)       # 5
```

**Named tuples** - tuples with field names:

```python
from collections import namedtuple

# Define a named tuple type
Point = namedtuple('Point', ['x', 'y'])
Color = namedtuple('Color', ['red', 'green', 'blue'])

p = Point(3, 4)
print(p.x)     # 3 (access by name, much more readable)
print(p[0])    # 3 (also works by index)

c = Color(255, 128, 0)
print(f"Red: {c.red}")

# Why tuples?
# 1. Immutable = safe to use as dict keys or set elements
locations = {(40.7, -74.0): "New York", (34.0, -118.2): "Los Angeles"}

# 2. Slightly faster and less memory than lists
# 3. Signals intent: "this data is fixed"
```

### 3.3 Sets

Sets are **unordered** collections of **unique** elements. They're great for removing duplicates and membership testing (very fast O(1) lookup).

```python
# Creating sets
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 2, 3, 3, 3}   # Duplicates removed: {1, 2, 3}
empty_set = set()                # NOT {} - that creates an empty dict!

# Add and remove
fruits.add("date")
fruits.discard("banana")   # Remove (no error if missing)
# fruits.remove("banana")  # Remove (KeyError if missing!)

# Membership testing (very fast!)
print("apple" in fruits)    # True
print("grape" in fruits)    # False
```

**Set operations** - mathematical set operations:

```python
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# Union - items in EITHER set
print(a | b)        # {1, 2, 3, 4, 5, 6, 7, 8}
print(a.union(b))   # Same thing

# Intersection - items in BOTH sets
print(a & b)             # {4, 5}
print(a.intersection(b)) # Same thing

# Difference - items in a but NOT in b
print(a - b)              # {1, 2, 3}
print(a.difference(b))    # Same thing

# Symmetric difference - items in EITHER but NOT BOTH
print(a ^ b)                       # {1, 2, 3, 6, 7, 8}
print(a.symmetric_difference(b))   # Same thing

# Subset / superset
small = {1, 2}
print(small <= a)    # True - small is a subset of a
print(a >= small)    # True - a is a superset of small
```

**Common use: removing duplicates while preserving order:**

```python
# Method 1: Using dict.fromkeys() (Python 3.7+ preserves insertion order)
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
unique = list(dict.fromkeys(items))
print(unique)  # [3, 1, 4, 5, 9, 2, 6]

# Method 2: Manual with set
seen = set()
unique = []
for item in items:
    if item not in seen:
        seen.add(item)
        unique.append(item)

# Method 3: One-liner (clever but less readable)
seen = set()
unique = [x for x in items if x not in seen and not seen.add(x)]
```

### 3.4 Dictionaries

Dictionaries store **key-value pairs**. They're one of Python's most powerful and frequently used data structures.

```python
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC",
    "hobbies": ["reading", "coding"]
}

# Accessing values
print(person["name"])               # "Alice"
# print(person["phone"])            # KeyError! Key doesn't exist

# Safe access with .get()
print(person.get("phone"))          # None (no error)
print(person.get("phone", "N/A"))   # "N/A" (custom default)

# Adding / updating
person["email"] = "alice@example.com"   # Add new key
person["age"] = 31                      # Update existing key

# Removing
del person["city"]                 # Delete (KeyError if missing)
age = person.pop("age")           # Remove and return value
last = person.popitem()           # Remove and return last key-value pair

# Check if key exists
if "name" in person:
    print(f"Name is {person['name']}")
```

**Iterating over dictionaries:**

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Loop through keys
for key in person:
    print(key)  # name, age, city

# Loop through values
for value in person.values():
    print(value)  # Alice, 30, NYC

# Loop through key-value pairs (most common)
for key, value in person.items():
    print(f"{key}: {value}")
```

**Useful dictionary patterns:**

```python
# Word frequency counter
text = "the cat sat on the mat the cat"
word_count = {}
for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)
# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}

# Merge dictionaries
defaults = {"color": "red", "size": "medium", "shape": "circle"}
custom = {"color": "blue", "weight": 5}

# Method 1: update() (modifies in place)
config = defaults.copy()   # Don't modify original!
config.update(custom)

# Method 2: Merge operator (Python 3.9+)
config = defaults | custom
# {'color': 'blue', 'size': 'medium', 'shape': 'circle', 'weight': 5}

# Method 3: Unpacking (Python 3.5+)
config = {**defaults, **custom}
```

**defaultdict** - auto-creates default values for missing keys:

```python
from collections import defaultdict

# Without defaultdict - tedious
groups = {}
students = [("Alice", "Math"), ("Bob", "Science"), ("Charlie", "Math"), ("Diana", "Science")]
for name, subject in students:
    if subject not in groups:
        groups[subject] = []
    groups[subject].append(name)

# With defaultdict - clean
groups = defaultdict(list)  # Missing keys auto-create empty lists
for name, subject in students:
    groups[subject].append(name)
print(dict(groups))
# {'Math': ['Alice', 'Charlie'], 'Science': ['Bob', 'Diana']}

# Other default types:
counter = defaultdict(int)     # Missing keys default to 0
counter["apples"] += 1
counter["apples"] += 1
counter["bananas"] += 1
print(dict(counter))  # {'apples': 2, 'bananas': 1}
```

**Counter** - count occurrences:

```python
from collections import Counter

# Count anything iterable
words = "the cat sat on the mat the cat".split()
counts = Counter(words)
print(counts)
# Counter({'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1})

print(counts.most_common(2))   # [('the', 3), ('cat', 2)]
print(counts["the"])           # 3
print(counts["dog"])           # 0 (missing keys return 0, not KeyError!)

# You can also count characters in a string
print(Counter("abracadabra"))
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
```

**deque** (double-ended queue) - efficient append/pop from both ends:

```python
from collections import deque

# Lists are slow for insert(0, x) and pop(0) - O(n)
# deque is fast for both ends - O(1)

dq = deque([1, 2, 3])
dq.appendleft(0)     # [0, 1, 2, 3]
dq.append(4)         # [0, 1, 2, 3, 4]
dq.popleft()          # Returns 0, deque is [1, 2, 3, 4]
dq.pop()              # Returns 4, deque is [1, 2, 3]

# Fixed-size deque - automatically drops oldest items
recent_logs = deque(maxlen=5)
for i in range(10):
    recent_logs.append(f"log-{i}")
print(list(recent_logs))
# ['log-5', 'log-6', 'log-7', 'log-8', 'log-9']
```

### Exercise 3.1: Group Students by City

```python
students = [
    {"name": "Alice", "city": "NYC"},
    {"name": "Bob", "city": "LA"},
    {"name": "Charlie", "city": "NYC"},
    {"name": "Diana", "city": "Chicago"},
    {"name": "Eve", "city": "LA"},
]
# Group them by city. Expected output:
# {'NYC': ['Alice', 'Charlie'], 'LA': ['Bob', 'Eve'], 'Chicago': ['Diana']}
```

<details>
<summary>Solution</summary>

```python
from collections import defaultdict

groups = defaultdict(list)
for student in students:
    groups[student["city"]].append(student["name"])
print(dict(groups))
```
</details>

### Exercise 3.2: Sort a Dictionary by Values

```python
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95, "Eve": 88}
# Sort by score descending and print as: "1. Diana: 95", "2. Bob: 92", etc.
```

<details>
<summary>Solution</summary>

```python
sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
for rank, (name, score) in enumerate(sorted_scores, 1):
    print(f"{rank}. {name}: {score}")
```
</details>

---

## Chapter 4: Functions & Functional Programming

### 4.1 Functions

Functions let you organize code into reusable blocks.

```python
# Basic function
def greet(name):
    """Greet a person by name."""  # This is a docstring - documents the function
    return f"Hello, {name}!"

print(greet("Alice"))  # "Hello, Alice!"

# Function with default arguments
def power(base, exponent=2):
    """Raise base to exponent. Defaults to squaring."""
    return base ** exponent

print(power(3))      # 9   (uses default exponent=2)
print(power(3, 3))   # 27  (exponent=3)
print(power(2, 10))  # 1024

# Function with multiple return values
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {low}, Max: {high}")  # Min: 1, Max: 9

# Type hints (optional but recommended for documentation)
def calculate_area(length: float, width: float) -> float:
    """Calculate rectangle area."""
    return length * width
```

**`*args` and `**kwargs`** - accept any number of arguments:

```python
# *args collects extra POSITIONAL arguments as a tuple
def add_all(*args):
    print(f"Received: {args}")  # args is a tuple
    return sum(args)

print(add_all(1, 2, 3))       # Received: (1, 2, 3) -> 6
print(add_all(10, 20, 30, 40)) # Received: (10, 20, 30, 40) -> 100

# **kwargs collects extra KEYWORD arguments as a dictionary
def create_profile(**kwargs):
    print(f"Received: {kwargs}")  # kwargs is a dict
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

create_profile(name="Alice", age=30, city="NYC")
# Received: {'name': 'Alice', 'age': 30, 'city': 'NYC'}
#   name: Alice
#   age: 30
#   city: NYC

# Combining both
def flexible(required, *args, **kwargs):
    print(f"Required: {required}")
    print(f"Extra positional: {args}")
    print(f"Extra keyword: {kwargs}")

flexible("hello", 1, 2, 3, x=10, y=20)
# Required: hello
# Extra positional: (1, 2, 3)
# Extra keyword: {'x': 10, 'y': 20}
```

**Unpacking arguments** - the reverse of *args/**kwargs:

```python
def add(a, b, c):
    return a + b + c

# Unpack a list into positional arguments
numbers = [1, 2, 3]
print(add(*numbers))  # Same as add(1, 2, 3) -> 6

# Unpack a dict into keyword arguments
params = {"a": 10, "b": 20, "c": 30}
print(add(**params))  # Same as add(a=10, b=20, c=30) -> 60
```

**Functions are first-class objects** - you can pass them around like variables:

```python
def apply(func, value):
    """Apply a function to a value."""
    return func(value)

print(apply(str.upper, "hello"))  # "HELLO"
print(apply(len, [1, 2, 3]))     # 3
print(apply(abs, -42))            # 42

# Store functions in a list
operations = [str.upper, str.lower, str.title]
text = "hello world"
for op in operations:
    print(op(text))
# HELLO WORLD
# hello world
# Hello World
```

### 4.2 Lambda Functions

Lambdas are small anonymous functions (one expression only):

```python
# Regular function
def square(x):
    return x ** 2

# Same thing as a lambda
square = lambda x: x ** 2

# Multiple arguments
add = lambda x, y: x + y
print(add(3, 4))  # 7

# Most commonly used with sort, map, filter:

# Sort by second element of tuple
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students.sort(key=lambda s: s[1])
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]

# Sort strings by last character
words = ["banana", "apple", "cherry"]
print(sorted(words, key=lambda w: w[-1]))
# ['banana', 'apple', 'cherry'] (sorted by a, e, y)
```

### 4.3 Map, Filter, Reduce

These are functional programming tools for transforming data:

```python
# map() - apply a function to every element
numbers = [1, 2, 3, 4, 5]

# Square each number
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# Convert all strings to integers
str_numbers = ["1", "2", "3", "4"]
int_numbers = list(map(int, str_numbers))
print(int_numbers)  # [1, 2, 3, 4]

# Clean up a list of strings
names = ["  alice  ", " BOB  ", "  Charlie  "]
cleaned = list(map(str.strip, names))
print(cleaned)  # ['alice', 'BOB', 'Charlie']

# filter() - keep elements that pass a test
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# Keep non-empty strings
strings = ["hello", "", "world", "", "python"]
non_empty = list(filter(None, strings))  # None removes falsy values
print(non_empty)  # ['hello', 'world', 'python']

# reduce() - accumulate a result
from functools import reduce

# Sum all numbers
total = reduce(lambda acc, x: acc + x, numbers)
print(total)  # 55

# Product of all numbers
product = reduce(lambda acc, x: acc * x, numbers)
print(product)  # 3628800

# NOTE: List comprehensions are usually preferred (more Pythonic):
squared = [x**2 for x in numbers]           # Instead of map
evens = [x for x in numbers if x % 2 == 0]  # Instead of filter

# But map/filter are nice when you already have a function:
cleaned = list(map(str.strip, names))  # Cleaner than comprehension
```

### 4.4 Closures

A closure is a function that "remembers" variables from the scope where it was created:

```python
# Basic closure
def make_multiplier(factor):
    """Returns a function that multiplies by factor."""
    def multiply(x):
        return x * factor  # 'factor' is remembered from the outer function
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
print(double(100)) # 200

# Practical example: configurable logger
def make_logger(prefix):
    """Returns a logging function with a fixed prefix."""
    def log(message):
        print(f"[{prefix}] {message}")
    return log

info = make_logger("INFO")
error = make_logger("ERROR")
debug = make_logger("DEBUG")

info("Server started")     # [INFO] Server started
error("Connection lost")   # [ERROR] Connection lost
debug("x = 42")           # [DEBUG] x = 42

# Another example: counter
def make_counter(start=0):
    count = [start]  # Using list because we need to modify it
    def increment():
        count[0] += 1
        return count[0]
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

### 4.5 Generators

Generators produce values **lazily** (one at a time, on demand). They're memory-efficient for large datasets.

```python
# Regular function: creates entire list in memory
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# Generator function: yields one value at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2  # 'yield' instead of 'return'

# Using them looks the same:
for sq in get_squares_gen(5):
    print(sq)  # 0, 1, 4, 9, 16

# But the memory difference is huge:
import sys
list_version = get_squares_list(10000)
gen_version = get_squares_gen(10000)
print(f"List: {sys.getsizeof(list_version):,} bytes")  # ~85,000 bytes
print(f"Generator: {sys.getsizeof(gen_version):,} bytes")  # ~200 bytes

# Real-world example: Fibonacci sequence
def fibonacci():
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:  # Infinite! But only produces values on demand
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")
# 0 1 1 2 3 5 8 13 21 34

# Batch processing - process large data in chunks
def batch_reader(data, batch_size=3):
    """Yield data in batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

data = list(range(10))
for batch in batch_reader(data, 3):
    print(f"Processing batch: {batch}")
# Processing batch: [0, 1, 2]
# Processing batch: [3, 4, 5]
# Processing batch: [6, 7, 8]
# Processing batch: [9]

# Generator expression (like list comprehension but lazy)
gen = (x**2 for x in range(1000000))  # No memory used yet
total = sum(gen)  # Values computed one at a time
```

### Exercise 4.1: Make a Greeting Factory
Write a closure `make_greeter(greeting)` that returns a function which greets people:

```python
hello = make_greeter("Hello")
hi = make_greeter("Hi there")
print(hello("Alice"))   # "Hello, Alice!"
print(hi("Bob"))        # "Hi there, Bob!"
```

<details>
<summary>Solution</summary>

```python
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"
    return greet

hello = make_greeter("Hello")
hi = make_greeter("Hi there")
print(hello("Alice"))   # "Hello, Alice!"
print(hi("Bob"))        # "Hi there, Bob!"
```
</details>

### Exercise 4.2: Process Large Data with a Generator
Write a generator `read_large_file(filepath)` that yields one line at a time. Then use it to count lines and find the longest line without loading the entire file into memory.

<details>
<summary>Solution</summary>

```python
def read_large_file(filepath):
    """Yield lines one at a time - works for any file size."""
    with open(filepath, 'r') as f:
        for line in f:
            yield line.rstrip('\n')

# Usage:
line_count = 0
longest = ""
for line in read_large_file("some_file.txt"):
    line_count += 1
    if len(line) > len(longest):
        longest = line

print(f"Total lines: {line_count}")
print(f"Longest line ({len(longest)} chars): {longest[:50]}...")
```
</details>

---

## Chapter 5: Object-Oriented Programming

### 5.1 Classes and Objects

A **class** is a blueprint. An **object** is an instance of that blueprint.

```python
class Dog:
    # Class variable (shared by ALL dogs)
    species = "Canis familiaris"

    def __init__(self, name, age, breed):
        """Constructor - called when you create a new Dog."""
        # Instance variables (unique to EACH dog)
        self.name = name
        self.age = age
        self.breed = breed

    def bark(self):
        """Instance method - needs self to access instance data."""
        return f"{self.name} says Woof!"

    def description(self):
        return f"{self.name} is a {self.age}-year-old {self.breed}"

    def birthday(self):
        self.age += 1
        return f"Happy birthday {self.name}! Now {self.age} years old."

# Creating objects (instances)
buddy = Dog("Buddy", 5, "Golden Retriever")
max_dog = Dog("Max", 3, "German Shepherd")

print(buddy.bark())           # "Buddy says Woof!"
print(max_dog.description())  # "Max is a 3-year-old German Shepherd"
print(buddy.birthday())       # "Happy birthday Buddy! Now 6 years old."

# Class variable is shared
print(buddy.species)     # "Canis familiaris"
print(max_dog.species)   # "Canis familiaris"
```

### 5.2 The `__init__` Method

`__init__` is Python's constructor. It's called automatically when you create an object:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        """
        Initialize a bank account.

        Args:
            owner: Account owner's name
            balance: Starting balance (default 0)
        """
        self.owner = owner
        self.balance = balance
        self.transactions = []  # Track all transactions

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(f"+${amount:.2f}")
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(f"-${amount:.2f}")
        return self.balance

    def get_statement(self):
        print(f"\nAccount: {self.owner}")
        print(f"Balance: ${self.balance:.2f}")
        print(f"Transactions: {', '.join(self.transactions)}")

# Usage
account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)
account.get_statement()
# Account: Alice
# Balance: $1300.00
# Transactions: +$500.00, -$200.00
```

### 5.3 Inheritance

A class can inherit attributes and methods from another class:

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}!"

    def __str__(self):
        return f"{self.name} the {self.__class__.__name__}"

# Dog inherits from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")  # Call parent's __init__
        self.breed = breed

    def fetch(self, item):
        return f"{self.name} fetches the {item}!"

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, "Meow")
        self.indoor = indoor

    def purr(self):
        return f"{self.name} purrs..."

# Usage
dog = Dog("Rex", "Labrador")
cat = Cat("Whiskers")

print(dog.speak())     # "Rex says Woof!" (inherited from Animal)
print(dog.fetch("ball"))  # "Rex fetches the ball!" (Dog-only method)
print(cat.speak())     # "Whiskers says Meow!"
print(cat.purr())      # "Whiskers purrs..."

# Polymorphism - same method, different behavior
animals = [Dog("Rex", "Lab"), Cat("Whiskers"), Dog("Max", "Poodle")]
for animal in animals:
    print(animal.speak())  # Each animal speaks differently
```

### 5.4 Abstract Base Classes

ABCs define a contract that subclasses must follow:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """All shapes MUST implement area() and perimeter()."""

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def description(self):
        """Concrete method - available to all subclasses."""
        return f"{self.__class__.__name__}: area={self.area():.2f}"

# You CANNOT create a Shape directly:
# shape = Shape()  # TypeError: Can't instantiate abstract class

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# Usage
shapes = [Rectangle(5, 3), Circle(4)]
for shape in shapes:
    print(shape.description())
# Rectangle: area=15.00
# Circle: area=50.27
```

### 5.5 Access Control

Python uses naming conventions (not enforcement) for access control:

```python
class Account:
    def __init__(self, owner, balance):
        self.owner = owner          # Public - access from anywhere
        self._bank = "MyBank"       # Protected - "internal use" convention
        self.__balance = balance    # Private - name mangling makes it harder to access

    def get_balance(self):
        """Public method to access private data."""
        return self.__balance

    def _internal_method(self):
        """Protected method - meant for class and subclasses only."""
        pass

acc = Account("Alice", 1000)
print(acc.owner)            # OK - public
print(acc._bank)            # Works but discouraged - protected
# print(acc.__balance)      # AttributeError! - private (name-mangled)
print(acc._Account__balance)  # Works via name mangling - but DON'T do this
print(acc.get_balance())    # Correct way: use the public method
```

### 5.6 Properties

Properties let you control access to attributes with getter/setter logic:

```python
class Temperature:
    def __init__(self, celsius=0):
        self.celsius = celsius  # This calls the setter!

    @property
    def celsius(self):
        """Getter - called when you read .celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Setter - called when you assign to .celsius"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Read-only computed property."""
        return self._celsius * 9/5 + 32

# Usage - looks like normal attributes, but validation happens automatically
temp = Temperature(100)
print(temp.celsius)      # 100
print(temp.fahrenheit)   # 212.0

temp.celsius = 0
print(temp.fahrenheit)   # 32.0

# temp.celsius = -300    # ValueError: Temperature below absolute zero!
# temp.fahrenheit = 100  # AttributeError: can't set (read-only property)
```

### 5.7 Class Methods vs Static Methods

```python
class DateUtil:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    @classmethod
    def from_string(cls, date_str):
        """Alternative constructor - creates a DateUtil from a string.

        @classmethod receives the CLASS as first argument (cls),
        so it can create new instances.
        """
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)  # Same as DateUtil(year, month, day)

    @classmethod
    def today(cls):
        """Another alternative constructor."""
        from datetime import date
        d = date.today()
        return cls(d.year, d.month, d.day)

    @staticmethod
    def is_valid_date(date_str):
        """Utility function that doesn't need class or instance.

        @staticmethod doesn't receive self or cls.
        It's just a function that lives inside the class namespace.
        """
        try:
            parts = date_str.split("-")
            if len(parts) != 3:
                return False
            y, m, d = map(int, parts)
            return 1 <= m <= 12 and 1 <= d <= 31
        except ValueError:
            return False

# Usage
d1 = DateUtil(2024, 3, 15)            # Normal constructor
d2 = DateUtil.from_string("2024-06-20")  # Alternative constructor
d3 = DateUtil.today()                     # Another alternative

print(d1)  # 2024-03-15
print(d2)  # 2024-06-20

print(DateUtil.is_valid_date("2024-13-01"))  # False (month 13)
print(DateUtil.is_valid_date("2024-06-15"))  # True
```

### 5.8 Dunder (Magic) Methods

Dunder methods (double underscore) let your objects work with Python's built-in operators and functions:

```python
class Vector:
    """A 2D vector that works with +, -, *, abs(), len(), ==, print(), etc."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # String representations
    def __repr__(self):
        """For developers - unambiguous. Called by repr() and in debugger."""
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        """For users - readable. Called by str() and print()."""
        return f"({self.x}, {self.y})"

    # Arithmetic
    def __add__(self, other):
        """Enables: v1 + v2"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Enables: v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Enables: v * 3"""
        return Vector(self.x * scalar, self.y * scalar)

    # Built-in functions
    def __abs__(self):
        """Enables: abs(v) - returns vector magnitude."""
        return (self.x**2 + self.y**2) ** 0.5

    def __len__(self):
        """Enables: len(v) - returns number of dimensions."""
        return 2

    # Comparison
    def __eq__(self, other):
        """Enables: v1 == v2"""
        return self.x == other.x and self.y == other.y

    # Container behavior
    def __getitem__(self, index):
        """Enables: v[0], v[1]"""
        return (self.x, self.y)[index]

    # Boolean
    def __bool__(self):
        """Enables: if v:  (True if non-zero vector)"""
        return self.x != 0 or self.y != 0

# Try it out:
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1)            # (3, 4)           -> __str__
print(repr(v1))      # Vector(3, 4)     -> __repr__
print(v1 + v2)       # (4, 6)           -> __add__
print(v1 - v2)       # (2, 2)           -> __sub__
print(v1 * 3)        # (9, 12)          -> __mul__
print(abs(v1))       # 5.0              -> __abs__
print(len(v1))       # 2                -> __len__
print(v1 == Vector(3, 4))  # True       -> __eq__
print(v1[0])         # 3                -> __getitem__

if v1:               # True (non-zero)  -> __bool__
    print("Non-zero vector")
```

**Key dunder methods reference:**

| Method | Triggered By | What it does |
|---|---|---|
| `__init__(self, ...)` | `obj = Class()` | Constructor |
| `__repr__(self)` | `repr(obj)`, debugger | Developer string |
| `__str__(self)` | `str(obj)`, `print(obj)` | User-friendly string |
| `__len__(self)` | `len(obj)` | Return length |
| `__getitem__(self, key)` | `obj[key]`, `obj[1:3]` | Index/slice access |
| `__setitem__(self, key, val)` | `obj[key] = val` | Set by index |
| `__contains__(self, item)` | `item in obj` | Membership test |
| `__iter__(self)` | `for x in obj` | Make iterable |
| `__next__(self)` | `next(obj)` | Next value in iteration |
| `__add__(self, other)` | `obj + other` | Addition |
| `__sub__(self, other)` | `obj - other` | Subtraction |
| `__mul__(self, other)` | `obj * other` | Multiplication |
| `__eq__(self, other)` | `obj == other` | Equality |
| `__lt__(self, other)` | `obj < other` | Less than |
| `__call__(self, ...)` | `obj()` | Make callable |
| `__enter__`/`__exit__` | `with obj:` | Context manager |
| `__bool__(self)` | `bool(obj)`, `if obj:` | Truthiness |
| `__hash__(self)` | `hash(obj)` | For sets/dict keys |

### Exercise 5.1: Create a Money Class
Create a `Money` class with `amount` and `currency`. Implement `__add__` (raise error if currencies differ), `__str__`, `__repr__`, `__eq__`, and `__lt__`.

<details>
<summary>Solution</summary>

```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = round(amount, 2)
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount < other.amount

m1 = Money(10.50)
m2 = Money(20.75)
print(m1 + m2)      # USD 31.25
print(m1 < m2)      # True
print(m1 == Money(10.50))  # True
```
</details>
## Chapter 6: Error Handling & Exceptions

### 6.1 Why Error Handling Matters

Without error handling, your program crashes the moment something goes wrong. With it, you can gracefully handle problems and keep running.

```python
# Without error handling - program crashes
user_input = "not a number"
number = int(user_input)  # ValueError: invalid literal for int()
print("This never executes")

# With error handling - program continues
try:
    number = int(user_input)
    print(f"You entered: {number}")
except ValueError:
    print("That's not a valid number!")
print("Program continues running...")
```

### 6.2 try / except / else / finally

Here's the full anatomy:

```python
def divide(a, b):
    try:
        # Code that MIGHT raise an exception
        result = a / b

    except ZeroDivisionError:
        # Handle specific exception
        print("Error: Cannot divide by zero!")
        return None

    except TypeError as e:
        # Catch the exception object to see the error message
        print(f"Error: Wrong types - {e}")
        return None

    except (ValueError, ArithmeticError) as e:
        # Catch multiple exception types
        print(f"Math error: {e}")
        return None

    except Exception as e:
        # Catch ANY exception (use as last resort)
        print(f"Unexpected error: {e}")
        return None

    else:
        # Runs ONLY if NO exception occurred
        # This is the "happy path"
        print(f"Success! {a} / {b} = {result}")
        return result

    finally:
        # ALWAYS runs, whether there was an exception or not
        # Use for cleanup (closing files, database connections, etc.)
        print("Division operation complete.")

# Test it:
divide(10, 3)     # Success! 10 / 3 = 3.333... / Division operation complete.
divide(10, 0)     # Error: Cannot divide by zero! / Division operation complete.
divide("10", 3)   # Error: Wrong types... / Division operation complete.
```

**When to use each block:**
- `try`: Code that might fail
- `except`: Handle specific errors
- `else`: Code that should run only on success (keeps try block minimal)
- `finally`: Cleanup that must always happen (closing files, connections)

### 6.3 Common Built-in Exceptions

```python
# ValueError - wrong value for the type
int("hello")              # ValueError

# TypeError - wrong type
"hello" + 42              # TypeError

# KeyError - dict key not found
d = {"a": 1}
d["b"]                    # KeyError

# IndexError - list index out of range
lst = [1, 2, 3]
lst[10]                   # IndexError

# AttributeError - object doesn't have that attribute
"hello".nonexistent()     # AttributeError

# FileNotFoundError - file doesn't exist
open("nonexistent.txt")   # FileNotFoundError

# ImportError - can't import module
import nonexistent_module  # ModuleNotFoundError (subclass of ImportError)

# ZeroDivisionError
10 / 0                    # ZeroDivisionError

# NameError - variable not defined
print(undefined_variable)  # NameError
```

### 6.4 Custom Exceptions

Create your own exceptions for your application's specific errors:

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, field, message, value=None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"Validation failed for '{field}': {message}")

class NotFoundError(Exception):
    """Raised when a resource is not found."""
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} with id '{resource_id}' not found")

class InsufficientFundsError(Exception):
    """Raised when account balance is too low."""
    pass

# Usage
def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("age", "must be an integer", age)
    if age < 0:
        raise ValidationError("age", "cannot be negative", age)
    if age > 150:
        raise ValidationError("age", f"unrealistic value: {age}", age)
    return age

def get_user(user_id):
    users = {"1": "Alice", "2": "Bob"}
    if user_id not in users:
        raise NotFoundError("User", user_id)
    return users[user_id]

# Using them:
try:
    validate_age(-5)
except ValidationError as e:
    print(f"Caught: {e}")
    print(f"  Field: {e.field}")
    print(f"  Value: {e.value}")
# Caught: Validation failed for 'age': cannot be negative
#   Field: age
#   Value: -5

try:
    get_user("999")
except NotFoundError as e:
    print(f"Caught: {e}")
    print(f"  Type: {e.resource_type}, ID: {e.resource_id}")
```

### 6.5 Exception Handling with Logging (Production Pattern)

```python
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(data):
    """Production-grade error handling pattern."""
    try:
        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")

        # Process
        result = transform(data)
        logger.info(f"Successfully processed {len(data)} items")
        return result

    except ValueError as e:
        # Known, expected errors - log as warning
        logger.warning(f"Invalid input: {e}")
        return None

    except ConnectionError as e:
        # Transient errors - might want to retry
        logger.error(f"Connection failed: {e}")
        raise  # Re-raise so caller can decide to retry

    except Exception:
        # Unknown errors - log full traceback for debugging
        logger.error(f"Unexpected error processing data:\n{traceback.format_exc()}")
        raise  # Re-raise unknown errors (don't swallow them!)
```

### 6.6 Exception Handling Decorator (Reusable Pattern)

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Retry decorator - retries function on failure.

    Args:
        max_attempts: Maximum number of tries
        delay: Seconds between retries
        exceptions: Tuple of exception types to catch

    Usage:
        @retry(max_attempts=3, delay=2)
        def flaky_api_call():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                        print(f"  Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print(f"  All {max_attempts} attempts failed!")
            raise last_exception
        return wrapper
    return decorator

# Usage:
import random

@retry(max_attempts=3, delay=1)
def unreliable_api_call():
    """Simulates a flaky API that fails randomly."""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Server unavailable")
    return {"status": "success", "data": [1, 2, 3]}

# This will retry up to 3 times:
try:
    result = unreliable_api_call()
    print(f"Got result: {result}")
except ConnectionError:
    print("API is down, giving up.")
```

### Exercise 6.1: Build a Robust Input Validator
Write a function `get_valid_number()` that keeps asking the user for input until they enter a valid number between 1 and 100.

<details>
<summary>Solution</summary>

```python
def get_valid_number(prompt="Enter a number (1-100): "):
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 100:
                return value
            else:
                print(f"  {value} is out of range. Must be 1-100.")
        except ValueError:
            print("  That's not a valid number. Try again.")
        except KeyboardInterrupt:
            print("\n  Cancelled.")
            return None

number = get_valid_number()
if number:
    print(f"You chose: {number}")
```
</details>

---

## Chapter 7: File I/O & Serialization

### 7.1 Reading and Writing Text Files

```python
# ===== WRITING =====

# Write (creates file or OVERWRITES existing)
with open("output.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")

# Write multiple lines
lines = ["Hello\n", "World\n", "Python\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)

# Append (adds to end of file)
with open("output.txt", "a") as f:
    f.write("Appended line\n")

# ===== READING =====

# Read entire file as one string
with open("output.txt", "r") as f:
    content = f.read()
    print(content)

# Read all lines into a list
with open("output.txt", "r") as f:
    lines = f.readlines()  # Each line includes \n
    for line in lines:
        print(line.strip())  # strip() removes \n

# Read line by line (memory efficient for large files)
with open("output.txt", "r") as f:
    for line in f:  # f is an iterator - reads one line at a time
        print(line.strip())

# Read first N lines
with open("output.txt", "r") as f:
    for i, line in enumerate(f):
        if i >= 5:  # Read only first 5 lines
            break
        print(line.strip())
```

**The `with` statement** - why you should always use it:

```python
# WITHOUT with (bad - you might forget to close)
f = open("file.txt", "r")
content = f.read()
f.close()  # Easy to forget, especially if an error occurs above

# WITH with (good - auto-closes even if error occurs)
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed here, even if an exception happened
```

### 7.2 pathlib - Modern File Operations

`pathlib` is the modern, Pythonic way to work with file paths:

```python
from pathlib import Path

# Create path objects
p = Path("data/output.txt")
home = Path.home()           # /Users/username (Mac) or C:\Users\username (Win)
cwd = Path.cwd()             # Current working directory

# Path properties
print(p.name)       # "output.txt"
print(p.stem)       # "output"
print(p.suffix)     # ".txt"
print(p.parent)     # "data"
print(p.exists())   # True or False
print(p.is_file())  # True if it's a file
print(p.is_dir())   # True if it's a directory

# Create directories
Path("data/processed").mkdir(parents=True, exist_ok=True)
# parents=True: create parent dirs too
# exist_ok=True: don't error if already exists

# Read and write (simple!)
p = Path("data/output.txt")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("Hello from pathlib!")
content = p.read_text()
print(content)

# Find files
for py_file in Path(".").rglob("*.py"):       # Recursive glob
    print(py_file)

for txt_file in Path("data").glob("*.txt"):    # Non-recursive
    print(txt_file)

# Join paths (works across OS)
config_path = Path.home() / ".config" / "myapp" / "settings.json"
```

### 7.3 JSON

JSON is the most common format for data exchange:

```python
import json

# ===== Python dict <-> JSON string =====

data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"],
    "address": {
        "city": "NYC",
        "state": "NY"
    }
}

# Python -> JSON string
json_str = json.dumps(data)
print(json_str)
# {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"], ...}

# Pretty-printed JSON
json_pretty = json.dumps(data, indent=2)
print(json_pretty)

# JSON string -> Python dict
parsed = json.loads(json_str)
print(parsed["name"])   # "Alice"
print(parsed["hobbies"][0])  # "reading"

# ===== JSON files =====

# Write to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read from file
with open("data.json", "r") as f:
    loaded = json.load(f)
```

### 7.4 CSV

```python
import csv

# ===== Writing CSV =====
with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "Grade"])   # Header
    writer.writerow(["Alice", 30, "A"])
    writer.writerow(["Bob", 25, "B"])
    writer.writerow(["Charlie", 35, "A"])

# ===== Reading CSV =====
with open("students.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)     # Read header row
    print(f"Columns: {header}")
    for row in reader:
        print(f"  {row[0]}, age {row[1]}, grade {row[2]}")

# ===== DictReader (much nicer - access by column name) =====
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['Name']}: {row['Grade']}")
```

### 7.5 YAML

```python
# pip install pyyaml
import yaml

# Read YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)  # Always use safe_load!

# Write YAML
with open("output.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False)

# Example YAML file (config.yaml):
# database:
#   host: localhost
#   port: 5432
#   name: mydb
# features:
#   - logging
#   - caching
```

### 7.6 Pickle (Python Object Serialization)

```python
import pickle

# Pickle can serialize ANY Python object
data = {
    "model_weights": [0.5, 0.3, 0.2],
    "metadata": {"version": "1.0", "created": "2024-01-15"},
    "history": [(1, 0.9), (2, 0.95), (3, 0.97)]
}

# Save
with open("model.pkl", "wb") as f:  # 'wb' = write binary
    pickle.dump(data, f)

# Load
with open("model.pkl", "rb") as f:  # 'rb' = read binary
    loaded = pickle.load(f)

print(loaded["model_weights"])  # [0.5, 0.3, 0.2]
```

> **SECURITY WARNING**: Never unpickle data from untrusted sources! Pickle can execute arbitrary code. Use JSON for data exchange between systems.

### Exercise 7.1: CSV to JSON Converter
Read a CSV file, transform the data, and write to JSON:

<details>
<summary>Solution</summary>

```python
import csv
import json

def csv_to_json(csv_path, json_path):
    records = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    with open(json_path, "w") as f:
        json.dump(records, f, indent=2)

    print(f"Converted {len(records)} records from {csv_path} to {json_path}")

csv_to_json("students.csv", "students.json")
```
</details>

---

## Chapter 8: Modules, Packages & Imports

### 8.1 What Are Modules and Packages?

| Term | What it is | Example |
|---|---|---|
| **Module** | A single `.py` file | `math.py`, `utils.py` |
| **Package** | A folder with `__init__.py` containing modules | `requests/`, `pandas/` |
| **Library** | A collection of packages (installed via pip) | `pandas`, `flask` |
| **Framework** | An opinionated library that controls the structure | `Django`, `FastAPI` |

### 8.2 Import Styles

```python
# Import the entire module
import os
print(os.path.exists("/tmp"))

# Import specific things from a module
from pathlib import Path
from collections import defaultdict, Counter

# Import with an alias (common for data science)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import everything (AVOID - clutters namespace)
# from os import *  # Don't do this in production code
```

### 8.3 Creating Your Own Package

```
myproject/
├── mypackage/
│   ├── __init__.py       # Makes this directory a package
│   ├── utils.py
│   ├── models.py
│   └── subpackage/
│       ├── __init__.py
│       └── helpers.py
├── main.py
└── tests/
    └── test_utils.py
```

```python
# mypackage/__init__.py
"""My package - does amazing things."""

# Control what gets imported with "from mypackage import *"
__all__ = ["utils", "models"]

# Convenience imports (so users can do: from mypackage import MyClass)
from .utils import useful_function
from .models import MyModel

__version__ = "1.0.0"
```

```python
# mypackage/utils.py
def useful_function(x):
    return x * 2
```

```python
# main.py
from mypackage import useful_function
from mypackage.models import MyModel
```

### 8.4 `__name__` and `__main__`

Every Python file has a special variable `__name__`:
- When run directly: `__name__` is `"__main__"`
- When imported: `__name__` is the module's name

```python
# mymodule.py
def main():
    print("Running as main program")

def helper():
    print("I'm a helper function")

# This block only runs when the file is executed directly
# NOT when imported by another module
if __name__ == "__main__":
    main()
```

```python
# another_file.py
import mymodule          # Does NOT run main()
mymodule.helper()       # Can use the functions
```

### 8.5 Import Order (PEP 8)

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports (installed via pip)
import pandas as pd
import numpy as np
import requests

# 3. Local application imports
from mypackage import utils
from mypackage.models import UserModel
```

---

## Chapter 9: Python Environment, pip & Dependency Management

### 9.1 Virtual Environments: Why and How

**Why**: Without virtual environments, all projects share the same Python packages. Project A might need `requests==2.28` while Project B needs `requests==2.31`. Virtual environments isolate each project's dependencies.

```bash
# CREATE a virtual environment
python -m venv .venv

# ACTIVATE it
# Mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Your prompt changes to show (.venv):
# (.venv) $ python --version

# INSTALL packages (only affects this virtual environment)
pip install requests pandas

# DEACTIVATE when done
deactivate
```

### 9.2 pip - Python Package Manager

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.28.0

# Install a version range
pip install "requests>=2.28,<3.0"

# pip install vs python -m pip install
# IMPORTANT: Always prefer python -m pip install
# This ensures you're using the pip for YOUR Python, not some other one
python -m pip install requests

# Upgrade a package
pip install --upgrade requests

# See what's installed
pip list
pip show requests    # Detailed info about one package

# Save your project's dependencies
pip freeze > requirements.txt

# Install from requirements file (reproduce environment)
pip install -r requirements.txt

# Uninstall
pip uninstall requests
```

### 9.3 Common pip Issues & How to Fix Them

**Issue: "pip: command not found"**
```bash
# Use python -m pip instead:
python -m pip install package_name
# Or upgrade pip:
python -m pip install --upgrade pip
```

**Issue: Permission denied**
```bash
# Option 1: Use --user (installs just for your user)
pip install --user package_name

# Option 2 (RECOMMENDED): Use a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install package_name
```

**Issue: SSL certificate error (common behind corporate firewalls)**
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org package_name
```

**Issue: Wrong package installed (e.g., `jwt` vs `PyJWT`)**
```bash
# Diagnose: check what you actually have
python -c "import jwt; print(jwt.__file__); print(dir(jwt))"

# Fix: remove wrong package, install correct one
pip uninstall jwt PyJWT
pip install PyJWT
```

**Issue: Dependency conflict**
```bash
# Force reinstall one package (ignoring dependencies)
pip install --force-reinstall --no-deps package_name

# Nuclear option: reinstall everything
pip install --force-reinstall package_name
```

**Issue: "externally-managed-environment" (newer Ubuntu/macOS)**
```bash
# This means your OS protects system Python. ALWAYS use virtual envs:
python -m venv .venv
source .venv/bin/activate
pip install package_name
```

### 9.4 Pipenv (Better Dependency Management)

Pipenv combines `pip` + `virtualenv` into one tool:

```bash
# Install pipenv
pip install pipenv

# Start a new project (creates Pipfile + virtual env)
pipenv install requests

# Install dev-only packages
pipenv install pytest --dev

# Activate the virtual environment
pipenv shell

# Run a command in the virtual env (without activating)
pipenv run python script.py
pipenv run pytest tests/

# Lock dependencies for reproducible builds
pipenv lock

# Install everything from Pipfile.lock
pipenv install

# Convert existing requirements.txt to Pipfile
pipenv install -r requirements.txt

# Remove virtual environment
pipenv --rm
```

---

## Chapter 10: Debugging & Profiling

This is one of the most important skills for any developer. Let's cover every technique from simple to advanced.

### 10.1 Print Debugging (The Basics)

The simplest debugging technique. Good for quick checks, but remove before committing:

```python
def calculate_total(items):
    print(f"DEBUG: items received = {items}")  # What did we get?

    total = 0
    for item in items:
        print(f"DEBUG: processing item = {item}")  # What are we processing?
        price = item["price"] * item["quantity"]
        print(f"DEBUG: price for {item['name']} = {price}")  # Intermediate result
        total += price

    print(f"DEBUG: final total = {total}")  # Final result
    return total

# Better: use f-strings with variable names
x = 42
print(f"{x = }")  # Output: x = 42  (Python 3.8+)

items = [1, 2, 3]
print(f"{len(items) = }")  # Output: len(items) = 3
```

### 10.2 pdb - Python Debugger (Step-by-Step Guide)

pdb lets you pause your program and inspect everything interactively. This is **much more powerful** than print debugging.

**How to start pdb:**

```python
# Method 1: Add breakpoint() where you want to pause (Python 3.7+)
def calculate_discount(price, discount_pct):
    breakpoint()  # Program pauses here
    discount = price * discount_pct / 100
    final_price = price - discount
    return final_price

result = calculate_discount(100, 20)
```

```python
# Method 2: Old style (works on all Python 3 versions)
import pdb

def calculate_discount(price, discount_pct):
    pdb.set_trace()  # Same effect as breakpoint()
    discount = price * discount_pct / 100
    final_price = price - discount
    return final_price
```

**When you run this, you'll see the pdb prompt:**

```
> /path/to/script.py(3)calculate_discount()
-> discount = price * discount_pct / 100
(Pdb)
```

**Now you can type commands. Here's a complete walkthrough:**

```
(Pdb) p price            # PRINT a variable's value
100
(Pdb) p discount_pct     # Print another variable
20
(Pdb) p price * discount_pct / 100    # Print ANY expression
20.0
(Pdb) pp locals()        # PRETTY-PRINT all local variables
{'discount_pct': 20, 'price': 100}

(Pdb) n                  # NEXT - execute current line, move to next
> /path/to/script.py(4)calculate_discount()
-> final_price = price - discount

(Pdb) p discount         # Now 'discount' exists
20.0

(Pdb) n                  # Execute this line too
> /path/to/script.py(5)calculate_discount()
-> return final_price

(Pdb) p final_price      # Check the result
80.0

(Pdb) c                  # CONTINUE - run until next breakpoint or end
```

**Complete pdb command reference:**

| Command | Short | What it does | Example |
|---|---|---|---|
| `print(expr)` | `p expr` | Print a value | `p my_variable` |
| `pp expr` | | Pretty-print (for dicts, lists) | `pp my_dict` |
| `next` | `n` | Execute current line, go to next | |
| `step` | `s` | Step INTO a function call | |
| `continue` | `c` | Run until next breakpoint | |
| `list` | `l` | Show code around current line | `l 1, 20` (lines 1-20) |
| `longlist` | `ll` | Show entire current function | |
| `where` | `w` | Show call stack (who called what) | |
| `up` | `u` | Go UP one level in call stack | |
| `down` | `d` | Go DOWN one level in call stack | |
| `break` | `b` | Set a breakpoint | `b 42` (line 42), `b my_func` |
| `clear` | `cl` | Remove breakpoints | `cl 1` (breakpoint #1) |
| `return` | `r` | Run until current function returns | |
| `quit` | `q` | Quit debugger | |
| `!statement` | | Execute Python statement | `!x = 42` |
| `whatis expr` | | Show type of expression | `whatis my_var` |

**Real debugging session example:**

Say you have a bug - the function returns wrong results:

```python
def find_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    average = total / len(numbers) + 1  # Bug! The +1 is wrong
    return average

# Let's debug:
def find_average(numbers):
    breakpoint()  # ADD THIS
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    average = total / len(numbers) + 1
    return average

result = find_average([10, 20, 30])
print(f"Average: {result}")  # Prints 21.0, but should be 20.0
```

```
# Run the script, pdb starts:

(Pdb) n                    # Skip past total = 0
(Pdb) n                    # Enter the for loop
(Pdb) n                    # Execute total += numbers[i]
(Pdb) p total              # Check total after first iteration
10
(Pdb) c                    # Continue (but we want to see more...)

# Better approach - set a breakpoint AFTER the loop:
(Pdb) b 6                 # Set breakpoint at line 6 (the average line)
(Pdb) c                    # Continue to that breakpoint
(Pdb) p total              # Check total
60
(Pdb) p len(numbers)       # Check count
3
(Pdb) p total / len(numbers)  # What should average be?
20.0
(Pdb) p total / len(numbers) + 1  # What IS the average (with bug)?
21.0
# AHA! The + 1 is the bug!
```

**Step vs Next - the important difference:**

```python
def helper(x):
    return x * 2

def main():
    breakpoint()
    result = helper(5)  # Line we're about to execute
    print(result)
```

```
# At the breakpoint:
(Pdb) n    # NEXT: executes helper(5) completely, stops at print(result)
           # You DON'T go inside helper()

(Pdb) s    # STEP: goes INSIDE helper(5), stops at "return x * 2"
           # You CAN inspect x inside helper
```

**Post-mortem debugging** - debug AFTER a crash:

```bash
# Run with -m pdb to auto-enter debugger on crash:
python -m pdb my_script.py

# When it crashes, you're dropped into pdb at the crash site
# You can inspect all variables to understand what went wrong
```

### 10.3 Logging (Production-Grade Debugging)

Print statements get removed before deployment. Logging is permanent and configurable.

**Basic logging:**

```python
import logging

# Configure logging (do this ONCE, at the top of your main script)
logging.basicConfig(
    level=logging.DEBUG,       # Show all messages DEBUG and above
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Log at different levels:
logger.debug("Detailed info for diagnosing problems")
logger.info("General operational info")
logger.warning("Something unexpected but not fatal")
logger.error("Something failed!")
logger.critical("System is unusable!")

# Output:
# 2024-03-15 14:30:00 [DEBUG] __main__: Detailed info for diagnosing problems
# 2024-03-15 14:30:00 [INFO] __main__: General operational info
# ...
```

**Log levels (from least to most severe):**

| Level | When to use | Example |
|---|---|---|
| `DEBUG` | Detailed diagnostic info | `logger.debug(f"Processing item {i}: {item}")` |
| `INFO` | General operational events | `logger.info("Server started on port 8080")` |
| `WARNING` | Something unexpected | `logger.warning("Disk space below 10%")` |
| `ERROR` | Something failed | `logger.error("Failed to connect to database")` |
| `CRITICAL` | System is unusable | `logger.critical("Out of memory!")` |

**Production logging setup** (log to file + console):

```python
import logging
import logging.handlers

def setup_logging(log_file="app.log", level=logging.INFO):
    """Set up production-grade logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture everything

    # Format
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler - show INFO and above
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler - log EVERYTHING, rotate at 10MB, keep 5 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Usage
logger = setup_logging()
logger.info("Application started")
```

### 10.4 Decorator for Logging and Timing

This is a pattern used extensively in production Python code:

```python
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_calls(func):
    """Decorator that logs function calls, return values, and execution time.

    Usage:
        @log_calls
        def my_function(x, y):
            return x + y

    When you call my_function(3, 4), it logs:
        CALL my_function(args=(3, 4), kwargs={})
        RETURN my_function -> 7 [0.0001s]
    """
    @wraps(func)  # Preserves function name and docstring
    def wrapper(*args, **kwargs):
        # Log the call
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"CALL {func.__name__}({signature})")

        # Execute and time
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.info(f"RETURN {func.__name__} -> {result!r} [{elapsed:.4f}s]")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            logger.error(f"ERROR {func.__name__} raised {type(e).__name__}: {e} [{elapsed:.4f}s]")
            raise

    return wrapper

# Usage:
@log_calls
def calculate_tax(amount, rate=0.08):
    return round(amount * rate, 2)

@log_calls
def process_order(items):
    total = sum(item["price"] for item in items)
    tax = calculate_tax(total)
    return total + tax

# When you call:
result = process_order([{"price": 10}, {"price": 20}])
# You see in the logs:
# CALL process_order([{'price': 10}, {'price': 20}])
# CALL calculate_tax(30, rate=0.08)
# RETURN calculate_tax -> 2.4 [0.0000s]
# RETURN process_order -> 32.4 [0.0001s]
```

### 10.5 Who Called Me? (Call Stack Inspection)

When debugging, it's useful to know WHO called a function:

```python
import inspect

def who_called_me():
    """Print information about the caller."""
    frame = inspect.currentframe().f_back  # Go up one level
    caller_name = frame.f_code.co_name
    caller_file = frame.f_code.co_filename
    caller_line = frame.f_lineno
    print(f"Called by: {caller_name}() at {caller_file}:{caller_line}")

def my_function():
    who_called_me()

def another_function():
    my_function()

# Run it:
another_function()
# Output: Called by: my_function() at script.py:12

# See the full call stack:
def show_call_stack():
    """Print the entire call stack."""
    print("Call stack (most recent call last):")
    for i, frame_info in enumerate(inspect.stack()):
        frame = frame_info[0]
        print(f"  {i}: {frame.f_code.co_name}() "
              f"at {frame.f_code.co_filename}:{frame.f_lineno}")
```

### 10.6 Python trace Module

The `trace` module shows every line of code as it executes:

```bash
# Trace every line executed in your script
python -m trace --trace script.py

# Example output:
#  --- modulename: script, funcname: calculate
# script.py(3):     total = 0
# script.py(4):     for i in range(len(numbers)):
# script.py(5):         total += numbers[i]
# script.py(4):     for i in range(len(numbers)):
# script.py(5):         total += numbers[i]
# ...

# Show which functions were called (less verbose)
python -m trace --listfuncs script.py

# Count how many times each line was executed
python -m trace --count script.py

# Verbose import tracing (see which modules are loaded)
python -v script.py
```

**Using trace programmatically:**

```python
import sys

def trace_calls(frame, event, arg):
    """Custom tracer that shows function calls."""
    if event == 'call':
        filename = frame.f_code.co_filename
        funcname = frame.f_code.co_name
        lineno = frame.f_lineno
        # Only trace our own code (not library code)
        if 'site-packages' not in filename:
            print(f"CALL: {funcname}() at {filename}:{lineno}")
    return trace_calls

# Enable tracing
sys.settrace(trace_calls)

# Your code here...
def hello(name):
    return f"Hello, {name}!"

result = hello("World")

# Disable tracing
sys.settrace(None)
```

### 10.7 strace / dtrace (System-Level Debugging)

When Python-level debugging isn't enough, you can trace system calls (file opens, network connections, etc.):

```bash
# Linux: see what files Python opens
strace -e trace=open,openat python script.py

# Linux: see network activity
strace -e trace=network python script.py

# macOS: use dtruss
sudo dtruss python script.py

# Useful for:
# - "Why can't Python find my module?" -> see which paths it searches
# - "Why is this script slow?" -> see unexpected disk or network I/O
# - "Permission denied errors" -> see which files it's trying to access
```

### 10.8 Visual Code Tracer (From This Repository)

This repository includes a powerful visual tracing tool that shows function calls in a web browser:

```python
# Copy visual_tracer.py from quick101/debugging/visual_code_tracer/
# Then in your code:

from visual_tracer import trace

# Basic - trace everything
trace()

# Now write your code normally:
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(result)

# A browser window opens at http://localhost:5050 showing:
# - Every function call in real-time
# - Call duration (how long each function took)
# - Call depth (how deep in the call stack)
# - Source code viewing (click to see code)
```

**Filtering (so you don't get overwhelmed):**

```python
# Only trace your code (skip third-party libraries)
trace(only_user_code=True)

# Only trace specific modules
trace(include_modules=["myapp.utils", "myapp.api"])

# Trace all modules starting with "myapp"
trace(include_modules=["myapp.*"])

# Skip test modules
trace(exclude_modules=["*.tests", "*.test_*"])

# Only show slow calls (>100ms)
trace(min_duration_ms=100)

# Combine filters
trace(
    include_modules=["myapp.*"],
    exclude_modules=["myapp.tests.*"],
    only_user_code=True,
    min_duration_ms=10
)
```

### 10.9 Profiling (Finding Performance Bottlenecks)

**cProfile** - find which functions are slow:

```python
import cProfile
import pstats

# Method 1: Profile a function call
cProfile.run('my_slow_function()')

# Method 2: Profile a block of code
profiler = cProfile.Profile()
profiler.enable()

# ... your code here ...
result = process_large_dataset(data)

profiler.disable()

# Print the top 10 slowest functions
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')  # Sort by total time
stats.print_stats(10)           # Show top 10

# Output looks like:
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.056    0.056 script.py:28(big_loop)
#    120002    0.039    0.000    0.039    0.000 script.py:33(<genexpr>)
#         2    0.016    0.008    0.055    0.028 {method 'join' of 'str'}
#
# Columns:
#   ncalls:  how many times the function was called
#   tottime: time spent IN this function (not counting sub-calls)
#   cumtime: time spent in this function INCLUDING sub-calls
```

**Command-line profiling:**

```bash
# Save profile data
python -m cProfile -o profile.pstats script.py

# Visualize with snakeviz (interactive browser UI)
pip install snakeviz
snakeviz profile.pstats

# Visualize with gprof2dot (generates an image)
pip install gprof2dot
brew install graphviz  # macOS
gprof2dot -f pstats profile.pstats | dot -Tpng -o profile.png

# Timeline profiling with viztracer
pip install viztracer
viztracer script.py
vizviewer result.json
```

**Quick timing** - measure how long something takes:

```python
from time import perf_counter

# Time a block of code
start = perf_counter()
result = sum(range(1_000_000))
elapsed = perf_counter() - start
print(f"Took {elapsed:.4f} seconds")

# In Jupyter notebooks:
# %timeit [x**2 for x in range(1000)]     # Time one expression (runs many times)
# %%time                                    # Time an entire cell (runs once)
# slow_function()
```

### 10.10 Debugging Cheat Sheet

| Situation | Tool | Command |
|---|---|---|
| Quick value check | Print | `print(f"{var = }")` |
| Step through code | pdb | `breakpoint()` then `n`, `s`, `c` |
| Inspect after crash | pdb post-mortem | `python -m pdb script.py` |
| See every line executed | trace | `python -m trace --trace script.py` |
| Find slow functions | cProfile | `python -m cProfile script.py` |
| Visual slow-function analysis | snakeviz | `snakeviz profile.pstats` |
| See system calls | strace/dtruss | `strace python script.py` |
| Visual live tracing | visual_tracer | `trace(only_user_code=True)` |
| Production debugging | logging | `logger.debug(f"x={x}")` |
| Find who called a function | inspect | `inspect.stack()` |
| Module loading issues | verbose | `python -v script.py` |

### Exercise 10.1: Debug This Function

This function has a bug. Use `breakpoint()` and pdb to find it:

```python
def calculate_average_grade(students):
    """Calculate the average grade for all students."""
    total = 0
    count = 0
    for student in students:
        if student["grade"] is not None:
            total += student["grade"]
    count += 1  # BUG: this is outside the if block!
    return total / count if count > 0 else 0

students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob", "grade": 80},
    {"name": "Charlie", "grade": None},
    {"name": "Diana", "grade": 85},
]

print(calculate_average_grade(students))  # Should be 85, but isn't!
```

<details>
<summary>Solution</summary>

The bug is that `count += 1` is outside the `if` block and outside the `for` loop. It should be inside both:

```python
def calculate_average_grade(students):
    total = 0
    count = 0
    for student in students:
        if student["grade"] is not None:
            total += student["grade"]
            count += 1  # FIXED: now inside the if block AND the for loop
    return total / count if count > 0 else 0
```

Using pdb to find the bug:
1. Add `breakpoint()` before the return
2. Check `total` (255) and `count` (1 - wrong, should be 3!)
3. Realize count is only incremented once because it's outside the loop
</details>

### Exercise 10.2: Profile and Optimize

Profile this code, find the bottleneck, and optimize it:

```python
def slow_search(data, target):
    """Find all indices where target appears."""
    indices = []
    for i in range(len(data)):
        for j in range(len(data)):  # BUG: why are we scanning the whole list again?
            if data[i] == target:
                indices.append(i)
                break
    return indices

import random
data = [random.randint(0, 100) for _ in range(10000)]
result = slow_search(data, 42)
```

<details>
<summary>Solution</summary>

```python
# Optimized: single pass O(n)
def fast_search(data, target):
    return [i for i, val in enumerate(data) if val == target]

# Or even simpler for just counting:
# count = data.count(42)
```
</details>
## Chapter 11: Intermediate Python

### 11.1 Decorators

A decorator is a function that takes another function and extends its behavior without modifying it.

**Step-by-step: How decorators work:**

```python
# Step 1: Functions can be passed as arguments
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def greet(func):
    """Takes a function, calls it, prints result."""
    result = func("Hello, World")
    print(result)

greet(shout)    # HELLO, WORLD
greet(whisper)  # hello, world
```

```python
# Step 2: Functions can return other functions
def create_greeting(style):
    def formal(name):
        return f"Good day, {name}. How do you do?"
    def casual(name):
        return f"Hey {name}! What's up?"

    if style == "formal":
        return formal
    else:
        return casual

greet = create_greeting("casual")
print(greet("Alice"))  # Hey Alice! What's up?
```

```python
# Step 3: A decorator combines both concepts
from functools import wraps

def timer(func):
    """Decorator that measures execution time."""
    @wraps(func)  # Preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)  # Call the original function
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}() took {elapsed:.4f}s")
        return result
    return wrapper

# Using the decorator:
@timer
def slow_function():
    """This function is slow."""
    import time
    time.sleep(1)
    return "done"

result = slow_function()
# Output: slow_function() took 1.0012s

# @timer is syntactic sugar for:
# slow_function = timer(slow_function)
```

**Decorator with parameters:**

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Decorator factory - returns a decorator configured with parameters."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        print(f"All {max_attempts} attempts failed for {func.__name__}")
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Server down")
    return {"data": "success"}

# Stacking decorators (applied bottom to top):
@timer          # 2nd: wraps the retry-wrapped function
@retry(max_attempts=3)  # 1st: wraps fetch_data
def api_call():
    pass
```

### 11.2 Context Managers

Context managers handle setup and cleanup automatically (files, connections, locks, etc.):

```python
# You've already used one:
with open("file.txt") as f:
    content = f.read()
# File is automatically closed here

# Creating your own context manager - Method 1: class-based
class Timer:
    """Context manager that measures execution time."""
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        print("Timer started")
        return self  # This becomes the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"Timer stopped: {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

# Usage:
with Timer() as t:
    total = sum(range(1_000_000))
print(f"Elapsed: {t.elapsed:.4f}s")

# Method 2: contextlib (simpler for most cases)
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.perf_counter()
    yield  # Everything before yield is __enter__, after is __exit__
    elapsed = time.perf_counter() - start
    print(f"Elapsed: {elapsed:.4f}s")

with timer():
    total = sum(range(1_000_000))

# Practical example: temporary directory change
import os
from contextlib import contextmanager

@contextmanager
def change_directory(path):
    """Temporarily change to a directory, then restore."""
    original = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original)

with change_directory("/tmp"):
    print(f"Now in: {os.getcwd()}")  # /tmp
print(f"Back in: {os.getcwd()}")     # original directory
```

### 11.3 Dataclasses

Dataclasses auto-generate `__init__`, `__repr__`, `__eq__`, and more:

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Employee:
    name: str
    age: int
    department: str
    salary: float = 50000.0                    # Default value
    skills: List[str] = field(default_factory=list)  # Mutable default

    @property
    def is_senior(self):
        return self.age >= 40

# Auto-generated __init__:
emp = Employee("Alice", 35, "Engineering", 95000, ["Python", "SQL"])

# Auto-generated __repr__:
print(emp)
# Employee(name='Alice', age=35, department='Engineering', salary=95000, skills=['Python', 'SQL'])

# Auto-generated __eq__:
emp2 = Employee("Alice", 35, "Engineering", 95000, ["Python", "SQL"])
print(emp == emp2)  # True

# Frozen (immutable) dataclass:
@dataclass(frozen=True)
class Point:
    x: float
    y: float
# Can be used as dict key or in sets

# Ordered dataclass (enables sorting):
@dataclass(order=True)
class Priority:
    priority: int
    name: str = field(compare=False)  # Excluded from comparison

tasks = [Priority(3, "low"), Priority(1, "high"), Priority(2, "med")]
print(sorted(tasks))  # Sorted by priority
```

### 11.4 Regular Expressions

```python
import re

text = "Contact alice@example.com or bob@test.org. Call 555-123-4567 on 2024-01-15."

# findall - find ALL matches
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
print(emails)  # ['alice@example.com', 'bob@test.org']

dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
print(dates)  # ['2024-01-15']

phones = re.findall(r'\d{3}-\d{3}-\d{4}', text)
print(phones)  # ['555-123-4567']

# search - find FIRST match
match = re.search(r'(\w+)@([\w.]+)', text)
if match:
    print(match.group(0))  # 'alice@example.com' (full match)
    print(match.group(1))  # 'alice' (first group)
    print(match.group(2))  # 'example.com' (second group)

# sub - replace matches
cleaned = re.sub(r'\d{3}-\d{3}-\d{4}', '[PHONE REDACTED]', text)
print(cleaned)

# compile - pre-compile for reuse (faster in loops)
email_pattern = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')
matches = email_pattern.findall(some_large_text)
```

### 11.5 Date and Time

```python
from datetime import datetime, date, timedelta, timezone

# Current date/time
now = datetime.now()
today = date.today()
utc_now = datetime.now(timezone.utc)

print(now)          # 2024-03-15 14:30:45.123456
print(today)        # 2024-03-15

# Formatting (datetime -> string)
print(now.strftime("%Y-%m-%d"))          # 2024-03-15
print(now.strftime("%B %d, %Y"))         # March 15, 2024
print(now.strftime("%I:%M %p"))          # 02:30 PM

# Parsing (string -> datetime)
dt = datetime.strptime("2024-03-15 14:30:00", "%Y-%m-%d %H:%M:%S")

# Arithmetic
tomorrow = now + timedelta(days=1)
next_week = now + timedelta(weeks=1)
two_hours_later = now + timedelta(hours=2)

# Difference between dates
diff = datetime(2024, 12, 31) - datetime(2024, 1, 1)
print(f"{diff.days} days")  # 365 days

# Timezones (pip install pytz)
import pytz
est = pytz.timezone('US/Eastern')
now_est = datetime.now(est)
print(f"EST: {now_est.strftime('%Y-%m-%d %H:%M %Z')}")
```

---

## Chapter 12: Advanced Python

### 12.1 Metaclasses

A metaclass is a "class of a class" - it controls how classes themselves are created:

```python
# Every class is an instance of 'type':
print(type(int))    # <class 'type'>
print(type(str))    # <class 'type'>

# Custom metaclass for Singleton pattern
class SingletonMeta(type):
    """Metaclass that ensures only one instance of a class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"
        print("Database initialized")

# Usage:
db1 = Database()  # Prints "Database initialized"
db2 = Database()  # Does NOT print again - returns same instance
print(db1 is db2)  # True
```

### 12.2 The GIL (Global Interpreter Lock)

The GIL is a mutex that allows only one thread to execute Python bytecode at a time:

```python
# CPU-bound: GIL is a bottleneck -> use multiprocessing
# I/O-bound: GIL is released during I/O -> threading works fine

# Example: CPU-bound (GIL hurts performance)
import time
from threading import Thread
from multiprocessing import Process

def cpu_heavy(n):
    total = sum(i * i for i in range(n))
    return total

# Threading: NOT faster for CPU work (GIL blocks parallel execution)
start = time.perf_counter()
threads = [Thread(target=cpu_heavy, args=(5_000_000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Threads: {time.perf_counter() - start:.2f}s")  # ~4s (serial!)

# Multiprocessing: FASTER (each process has its own GIL)
start = time.perf_counter()
processes = [Process(target=cpu_heavy, args=(5_000_000,)) for _ in range(4)]
for p in processes: p.start()
for p in processes: p.join()
print(f"Processes: {time.perf_counter() - start:.2f}s")  # ~1s (parallel!)
```

### 12.3 `__slots__` (Memory Optimization)

```python
import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ['x', 'y']  # No __dict__, saves memory
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Memory comparison (for millions of instances, this matters):
regular = RegularPoint(1, 2)
slotted = SlottedPoint(1, 2)
print(sys.getsizeof(regular.__dict__))  # ~104 bytes per instance
# slotted has no __dict__ - saves ~50% memory

# Tradeoff: can't add new attributes
# slotted.z = 3  # AttributeError!
```

### 12.4 Deep Copy vs Shallow Copy

```python
import copy

# Shallow copy: copies the outer object, but inner objects are SHARED
original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)

# They look the same:
print(original)  # [[1, 2, 3], [4, 5, 6]]
print(shallow)   # [[1, 2, 3], [4, 5, 6]]

# But modifying an inner list affects both:
original[0].append(99)
print(original)  # [[1, 2, 3, 99], [4, 5, 6]]
print(shallow)   # [[1, 2, 3, 99], [4, 5, 6]]  <- ALSO CHANGED!

# Deep copy: copies EVERYTHING recursively
original2 = [[1, 2, 3], [4, 5, 6]]
deep = copy.deepcopy(original2)

original2[0].append(99)
print(original2)  # [[1, 2, 3, 99], [4, 5, 6]]
print(deep)       # [[1, 2, 3], [4, 5, 6]]  <- NOT affected
```

---

## Chapter 13: Concurrency & Parallelism

### 13.1 Threading (For I/O-bound Tasks)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def download_page(url):
    """Simulate downloading a web page."""
    time.sleep(1)  # Simulate network I/O
    return f"Content of {url}"

urls = [f"https://example.com/page/{i}" for i in range(10)]

# Sequential: ~10 seconds
start = time.perf_counter()
results = [download_page(url) for url in urls]
print(f"Sequential: {time.perf_counter() - start:.1f}s")

# Parallel with ThreadPoolExecutor: ~2 seconds
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(download_page, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
            print(f"Done: {url}")
        except Exception as e:
            print(f"Failed: {url} - {e}")
print(f"Threaded: {time.perf_counter() - start:.1f}s")
```

### 13.2 Multiprocessing (For CPU-bound Tasks)

```python
from multiprocessing import Pool

def cpu_task(n):
    """CPU-intensive calculation."""
    return sum(i * i for i in range(n))

# Parallel processing
with Pool(processes=4) as pool:
    results = pool.map(cpu_task, [10**6, 10**6, 10**6, 10**6])
    print(f"Total: {sum(results)}")
```

### 13.3 asyncio (Modern Async I/O)

```python
import asyncio

async def fetch_data(name, delay):
    print(f"Starting {name}...")
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(f"Done {name}")
    return f"{name}: {delay}s of data"

async def main():
    # Run all three concurrently
    results = await asyncio.gather(
        fetch_data("users", 2),
        fetch_data("orders", 1),
        fetch_data("products", 1.5),
    )
    for r in results:
        print(r)

asyncio.run(main())
# All three complete in ~2s (the longest), not 4.5s (sequential)
```

### When to Use What

| Task Type | Tool | Example |
|---|---|---|
| Download files, API calls | `ThreadPoolExecutor` | HTTP requests |
| Database queries | `threading` / `asyncio` | SELECT/INSERT |
| Number crunching | `multiprocessing.Pool` | Math, image processing |
| Many concurrent connections | `asyncio` | Web servers, chat |

---

## Chapter 14: Design Patterns

### 14.1 Singleton

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True

s1 = Singleton("first")
s2 = Singleton("second")
print(s1 is s2)      # True - same object
print(s1.value)       # "first" - not overwritten
```

### 14.2 Factory Pattern

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message): pass

class EmailNotification(Notification):
    def send(self, message): print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message): print(f"SMS: {message}")

class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        klass = cls._registry.get(channel)
        if not klass:
            raise ValueError(f"Unknown channel: {channel}")
        return klass()

    @classmethod
    def register(cls, channel: str, klass):
        cls._registry[channel] = klass

# Usage:
notif = NotificationFactory.create("email")
notif.send("Hello!")
```

### 14.3 Observer Pattern

```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

# Usage
bus = EventEmitter()
bus.on("user_created", lambda user: print(f"Welcome {user}!"))
bus.on("user_created", lambda user: print(f"Sending email to {user}"))
bus.emit("user_created", "Alice")
# Welcome Alice!
# Sending email to Alice
```

---

## Chapter 15: Data Science with Python

Data science in Python revolves around three core libraries: **NumPy** for numerical computation, **Pandas** for data manipulation, and **Matplotlib/Seaborn** for visualization. Together with **scikit-learn** for machine learning, they form the standard data science toolkit.

### 15.1 NumPy - Numerical Computing

NumPy arrays are the foundation of scientific computing in Python. They're **up to 100x faster** than Python lists for math because they use contiguous memory and C-optimized operations.

```python
import numpy as np

# Creating arrays
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros(5)                    # [0. 0. 0. 0. 0.]
ones = np.ones((3, 3))                 # 3x3 matrix of 1s
range_arr = np.arange(0, 10, 2)        # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)        # [0.  0.25 0.5  0.75 1. ]
random_arr = np.random.rand(5)         # 5 random floats [0, 1)
random_int = np.random.randint(1, 100, size=10)  # 10 random ints

# Element-wise operations (no loops needed!)
arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)       # [ 2  4  6  8 10]
print(arr ** 2)      # [ 1  4  9 16 25]
print(arr + 10)      # [11 12 13 14 15]
print(np.sqrt(arr))  # [1.   1.41 1.73 2.   2.24]

# Aggregation
print(np.mean(arr))   # 3.0
print(np.std(arr))    # 1.414
print(np.median(arr)) # 3.0
print(np.sum(arr))    # 15
print(np.min(arr), np.max(arr))  # 1 5
```

**2D arrays (matrices) - the bread and butter of data science:**

```python
# 2D arrays
matrix = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])

# Indexing and slicing
print(matrix[0, :])        # First row: [1, 2, 3]
print(matrix[:, 0])        # First column: [1, 4, 7]
print(matrix[0:2, 1:3])    # Sub-matrix: [[2, 3], [5, 6]]
print(matrix.shape)        # (3, 3)

# Boolean indexing (very powerful!)
print(matrix[matrix > 5])  # [6, 7, 8, 9]
print(matrix[matrix % 2 == 0])  # [2, 4, 6, 8]

# Reshape
flat = np.arange(12)             # [0,1,2,...,11]
reshaped = flat.reshape(3, 4)    # 3x4 matrix
print(reshaped)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Matrix operations
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(a @ b)           # Matrix multiplication (dot product)
print(a * b)           # Element-wise multiplication
print(a.T)             # Transpose
print(np.linalg.inv(a))  # Inverse
print(np.linalg.det(a))  # Determinant: -2.0
```

**Why NumPy over lists - a speed comparison:**

```python
import time

size = 1_000_000

# Python list
py_list = list(range(size))
start = time.perf_counter()
result = [x * 2 for x in py_list]
print(f"List: {time.perf_counter() - start:.4f}s")

# NumPy array
np_arr = np.arange(size)
start = time.perf_counter()
result = np_arr * 2
print(f"NumPy: {time.perf_counter() - start:.4f}s")
# NumPy is typically 50-100x faster!
```

### 15.2 Pandas - Data Manipulation

Pandas is *the* tool for working with tabular data (think spreadsheets, CSV files, database tables).

**Creating DataFrames:**

```python
import pandas as pd

# From a dictionary
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [30, 25, 35, 28, 32],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
    "salary": [95000, 72000, 88000, 78000, 105000],
    "department": ["Eng", "Sales", "Eng", "HR", "Eng"]
})

# From CSV file
# df = pd.read_csv("employees.csv")

# From JSON
# df = pd.read_json("data.json")
```

**Exploring your data (always do this first!):**

```python
print(df.head())       # First 5 rows
print(df.tail(3))      # Last 3 rows
print(df.shape)        # (5, 5) = 5 rows, 5 columns
print(df.dtypes)       # Data type of each column
print(df.info())       # Summary: types, non-null counts, memory
print(df.describe())   # Statistics: mean, std, min, max, percentiles
print(df.columns.tolist())  # Column names as a list
print(df.nunique())    # Number of unique values per column
```

**Selecting and filtering:**

```python
# Select columns
print(df["name"])              # Single column (Series)
print(df[["name", "salary"]]) # Multiple columns (DataFrame)

# Filter rows
nyc = df[df["city"] == "NYC"]
high_salary = df[df["salary"] > 80000]

# Multiple conditions (use & for AND, | for OR, ~ for NOT)
eng_nyc = df[(df["department"] == "Eng") & (df["city"] == "NYC")]
not_sales = df[~(df["department"] == "Sales")]

# .query() - more readable for complex filters
result = df.query("salary > 80000 and city == 'NYC'")

# .loc (label-based) and .iloc (position-based)
print(df.loc[0, "name"])      # "Alice" (by label)
print(df.iloc[0, 0])          # "Alice" (by position)
print(df.loc[0:2, ["name", "salary"]])  # Rows 0-2, specific columns
```

**Transforming data:**

```python
# Add new columns
df["bonus"] = df["salary"] * 0.1
df["tax_bracket"] = df["salary"].apply(
    lambda s: "high" if s > 90000 else "medium" if s > 75000 else "low"
)

# Rename columns
df = df.rename(columns={"name": "employee_name"})

# Sort
df_sorted = df.sort_values("salary", ascending=False)
df_multi_sort = df.sort_values(["city", "salary"], ascending=[True, False])

# Drop columns or rows
df_slim = df.drop(columns=["bonus"])
df_no_dupes = df.drop_duplicates(subset=["city"])
```

**GroupBy - split-apply-combine (most powerful Pandas feature):**

```python
# Average salary by city
print(df.groupby("city")["salary"].mean())
# Chicago    78000.0
# LA         88500.0
# NYC        91500.0

# Multiple aggregations
summary = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    headcount=("name", "count"),
    avg_age=("age", "mean")
).round(0)
print(summary)

# Pivot tables (like Excel pivot tables)
pivot = df.pivot_table(
    values="salary",
    index="department",
    columns="city",
    aggfunc="mean",
    fill_value=0
)
print(pivot)
```

**Handling missing data (critical for real-world data):**

```python
df_dirty = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Diana"],
    "age": [30, None, 35, 28],
    "salary": [95000, 72000, None, 78000]
})

# Detect missing data
print(df_dirty.isnull())           # Boolean mask
print(df_dirty.isnull().sum())     # Count per column
print(df_dirty.isnull().sum().sum())  # Total missing

# Handle missing data
df_clean = df_dirty.dropna()                    # Remove rows with ANY NaN
df_clean = df_dirty.dropna(subset=["name"])     # Remove only if name is NaN
df_filled = df_dirty.fillna({"age": df_dirty["age"].median(), "salary": 0})
df_interpolated = df_dirty.interpolate()        # Fill with interpolated values
df_forward = df_dirty.fillna(method="ffill")    # Forward fill
```

**Merging DataFrames (like SQL JOINs):**

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer": ["Alice", "Bob", "Alice", "Charlie"],
    "amount": [100, 200, 150, 300]
})

customers = pd.DataFrame({
    "name": ["Alice", "Bob", "Diana"],
    "city": ["NYC", "LA", "Chicago"]
})

# Inner join (only matching rows)
merged = orders.merge(customers, left_on="customer", right_on="name", how="inner")

# Left join (keep all orders, even if customer not found)
merged_left = orders.merge(customers, left_on="customer", right_on="name", how="left")

# Concatenate (stack DataFrames)
df_all = pd.concat([df_part1, df_part2], ignore_index=True)
```

### 15.3 Visualization with Matplotlib and Seaborn

```python
import matplotlib.pyplot as plt
import numpy as np

# Line plot
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), 'b-', label="sin(x)", linewidth=2)
plt.plot(x, np.cos(x), 'r--', label="cos(x)", linewidth=2)
plt.xlabel("X axis", fontsize=12)
plt.ylabel("Y axis", fontsize=12)
plt.title("Trigonometric Functions", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("plot.png", dpi=150)  # Save to file
plt.show()
```

```python
# Multiple plot types in subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Bar chart
categories = ["Eng", "Sales", "HR", "Marketing"]
values = [45, 30, 15, 25]
axes[0, 0].bar(categories, values, color=['#5b9cf5', '#50d890', '#f5a623', '#e878a0'])
axes[0, 0].set_title("Headcount by Department")

# Scatter plot
np.random.seed(42)
x = np.random.randn(100)
y = x * 2 + np.random.randn(100) * 0.5
axes[0, 1].scatter(x, y, alpha=0.6, c=y, cmap='viridis')
axes[0, 1].set_title("Correlation Plot")

# Histogram
data = np.random.normal(70000, 15000, 1000)
axes[1, 0].hist(data, bins=30, color='#a78bfa', edgecolor='black', alpha=0.7)
axes[1, 0].set_title("Salary Distribution")

# Pie chart
sizes = [45, 30, 15, 10]
axes[1, 1].pie(sizes, labels=categories, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title("Department Share")

plt.tight_layout()
plt.show()
```

```python
# Seaborn - statistical visualizations (prettier defaults)
# pip install seaborn
import seaborn as sns

# Use a built-in dataset for demonstration
tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Box plot - shows distribution, outliers, median
sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0])
axes[0].set_title("Bill by Day")

# Violin plot - box plot + kernel density
sns.violinplot(data=tips, x="day", y="tip", ax=axes[1])
axes[1].set_title("Tips by Day")

# Heatmap - correlation matrix
numeric_tips = tips.select_dtypes(include='number')
sns.heatmap(numeric_tips.corr(), annot=True, cmap="coolwarm", ax=axes[2])
axes[2].set_title("Correlation Heatmap")

plt.tight_layout()
plt.show()
```

### 15.4 scikit-learn - Machine Learning Basics

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import numpy as np
import pandas as pd

# --- Regression example: Predict house prices ---
np.random.seed(42)
n = 200
sqft = np.random.uniform(800, 3000, n)
bedrooms = np.random.randint(1, 6, n)
price = sqft * 150 + bedrooms * 20000 + np.random.normal(0, 15000, n)

df = pd.DataFrame({"sqft": sqft, "bedrooms": bedrooms, "price": price})

# Step 1: Split into features (X) and target (y)
X = df[["sqft", "bedrooms"]]
y = df["price"]

# Step 2: Train/test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Scale features (important for many algorithms)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaler!

# Step 4: Train model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Step 5: Evaluate
predictions = model.predict(X_test_scaled)
rmse = mean_squared_error(y_test, predictions, squared=False)
print(f"RMSE: ${rmse:,.0f}")
print(f"R² score: {model.score(X_test_scaled, y_test):.3f}")
```

```python
# --- Classification example: Predict customer churn ---
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Simulated data
np.random.seed(42)
n = 500
data = pd.DataFrame({
    "tenure_months": np.random.randint(1, 72, n),
    "monthly_charge": np.random.uniform(20, 100, n),
    "support_calls": np.random.randint(0, 10, n),
})
# Churn more likely with short tenure, high charges, many support calls
data["churned"] = (
    (data["tenure_months"] < 12) &
    (data["monthly_charge"] > 60) |
    (data["support_calls"] > 7)
).astype(int)

X = data[["tenure_months", "monthly_charge", "support_calls"]]
y = data["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))

# Feature importance (which features matter most)
for name, importance in zip(X.columns, clf.feature_importances_):
    print(f"  {name}: {importance:.3f}")
```

### Exercise 15.1: Data Analysis Challenge

Using pandas, analyze this sales dataset:

```python
sales = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=100, freq="D"),
    "product": np.random.choice(["Widget", "Gadget", "Doohickey"], 100),
    "quantity": np.random.randint(1, 50, 100),
    "unit_price": np.random.choice([9.99, 24.99, 49.99], 100),
    "region": np.random.choice(["North", "South", "East", "West"], 100)
})
sales["revenue"] = sales["quantity"] * sales["unit_price"]
```

Tasks:
1. What's the total revenue by product?
2. Which region has the highest average order value?
3. What's the weekly revenue trend?
4. Create a bar chart of revenue by product and a line chart of weekly revenue.

<details>
<summary>Solution</summary>

```python
# 1. Revenue by product
print(sales.groupby("product")["revenue"].sum().sort_values(ascending=False))

# 2. Highest avg order by region
print(sales.groupby("region")["revenue"].mean().sort_values(ascending=False))

# 3. Weekly revenue trend
sales["week"] = sales["date"].dt.isocalendar().week
weekly = sales.groupby("week")["revenue"].sum()

# 4. Visualize
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

sales.groupby("product")["revenue"].sum().plot(kind="bar", ax=ax1, color=['#5b9cf5', '#50d890', '#f5a623'])
ax1.set_title("Revenue by Product")
ax1.set_ylabel("Revenue ($)")

weekly.plot(ax=ax2, marker='o', color='#a78bfa')
ax2.set_title("Weekly Revenue Trend")
ax2.set_ylabel("Revenue ($)")

plt.tight_layout()
plt.show()
```
</details>

---

## Chapter 16: Data Engineering with Python

Data engineering is about building reliable pipelines to move and transform data. Python is the dominant language in this space, especially with tools like Apache Spark (PySpark), Airflow, and boto3.

### 16.1 Database Operations

**SQLite (built-in, great for prototyping):**

```python
import sqlite3

# Connect (creates file if it doesn't exist)
conn = sqlite3.connect("local.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert data - ALWAYS use parameterized queries to prevent SQL injection!
cursor.execute(
    "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Alice", "alice@example.com", 30)
)

# Insert many rows at once (much faster than individual inserts)
users = [
    ("Bob", "bob@example.com", 25),
    ("Charlie", "charlie@example.com", 35),
    ("Diana", "diana@example.com", 28),
]
cursor.executemany(
    "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)
conn.commit()

# Query
cursor.execute("SELECT name, age FROM users WHERE age > ? ORDER BY age", (26,))
for row in cursor.fetchall():
    print(row)  # ('Alice', 30), ('Diana', 28), ('Charlie', 35)

# Use context manager for automatic cleanup
conn.close()
```

**Using Pandas with databases (recommended for data work):**

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect("local.db")

# Read SQL query into DataFrame (much easier than manual iteration)
df = pd.read_sql_query("SELECT * FROM users WHERE age > 25", conn)
print(df)

# Write DataFrame to SQL table
new_users = pd.DataFrame({
    "name": ["Eve", "Frank"],
    "email": ["eve@example.com", "frank@example.com"],
    "age": [29, 33]
})
new_users.to_sql("users", conn, if_exists="append", index=False)

conn.close()
```

**PostgreSQL with psycopg2 (production databases):**

```python
# pip install psycopg2-binary
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="password"  # In production: use env vars!
    )
    try:
        yield conn
    finally:
        conn.close()

# Usage
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users LIMIT 10")
        rows = cur.fetchall()
        for row in rows:
            print(row)
```

### 16.2 Processing Large Files

When files don't fit in memory, you need streaming/chunked approaches:

```python
# Chunked CSV processing (for files too large for memory)
import pandas as pd

total_revenue = 0
row_count = 0

for chunk in pd.read_csv("huge_file.csv", chunksize=50_000):
    # Process each chunk (50,000 rows at a time)
    filtered = chunk[chunk["amount"] > 100]
    total_revenue += filtered["amount"].sum()
    row_count += len(filtered)
    print(f"Processed chunk: {row_count} qualifying rows so far")

print(f"Total revenue: ${total_revenue:,.2f} from {row_count} rows")
```

```python
# Line-by-line processing (for non-CSV or custom formats)
import json

def process_jsonl(filepath):
    """Process a JSON Lines file (one JSON object per line)."""
    results = []
    errors = 0
    with open(filepath) as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line.strip())
                if record.get("status") == "active":
                    results.append(record)
            except json.JSONDecodeError:
                errors += 1
            if line_num % 100_000 == 0:
                print(f"Processed {line_num:,} lines...")
    print(f"Done: {len(results)} active records, {errors} errors")
    return results
```

```python
# Generator-based pipeline (memory-efficient chaining)
def read_lines(filepath):
    """Generator: yields lines from file."""
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def parse_csv_lines(lines):
    """Generator: parse CSV lines into dicts."""
    headers = next(lines).split(",")
    for line in lines:
        values = line.split(",")
        yield dict(zip(headers, values))

def filter_records(records, min_amount=100):
    """Generator: filter by amount."""
    for record in records:
        if float(record.get("amount", 0)) > min_amount:
            yield record

# Chain generators - processes one record at a time, any file size!
pipeline = filter_records(parse_csv_lines(read_lines("sales.csv")))
for record in pipeline:
    print(record)
```

### 16.3 AWS S3 with boto3

```python
# pip install boto3
import boto3
import json

s3 = boto3.client("s3")

# Upload a file
s3.upload_file("local_data.csv", "my-bucket", "data/2024/sales.csv")

# Download a file
s3.download_file("my-bucket", "data/2024/sales.csv", "downloaded.csv")

# List objects in a bucket
response = s3.list_objects_v2(Bucket="my-bucket", Prefix="data/2024/")
for obj in response.get("Contents", []):
    print(f"{obj['Key']}: {obj['Size']} bytes")

# Read file directly into pandas (without downloading)
import io
obj = s3.get_object(Bucket="my-bucket", Key="data/sales.csv")
df = pd.read_csv(io.BytesIO(obj["Body"].read()))
```

### 16.4 Simple ETL Pipeline

```python
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract(source_path: str) -> pd.DataFrame:
    """Extract: read raw data from source."""
    logger.info(f"Extracting from {source_path}")
    df = pd.read_csv(source_path)
    logger.info(f"Extracted {len(df)} rows")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform: clean and reshape data."""
    logger.info("Transforming data...")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {before - len(df)} duplicates")

    # Clean column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Handle missing values
    df["amount"] = df["amount"].fillna(0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Add derived columns
    df["year_month"] = df["date"].dt.to_period("M")
    df["amount_category"] = pd.cut(df["amount"], bins=[0, 100, 500, float("inf")],
                                     labels=["small", "medium", "large"])
    logger.info(f"Transformed: {len(df)} rows")
    return df

def load(df: pd.DataFrame, dest_path: str):
    """Load: write processed data to destination."""
    logger.info(f"Loading {len(df)} rows to {dest_path}")
    df.to_parquet(dest_path, index=False)
    logger.info("Load complete")

# Run the ETL pipeline
if __name__ == "__main__":
    raw = extract("raw_sales.csv")
    clean = transform(raw)
    load(clean, f"processed/sales_{datetime.now():%Y%m%d}.parquet")
```

### Exercise 16.1: Build a Data Pipeline

Write a pipeline that:
1. Reads a CSV file with columns: `date, product, quantity, price`
2. Removes rows where quantity <= 0
3. Adds a `revenue` column (quantity * price)
4. Groups by product and month, summing revenue
5. Saves the result to a new CSV

<details>
<summary>Solution</summary>

```python
import pandas as pd

# Extract
df = pd.read_csv("sales_raw.csv")

# Transform
df = df[df["quantity"] > 0]
df["revenue"] = df["quantity"] * df["price"]
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly = df.groupby(["month", "product"])["revenue"].sum().reset_index()
monthly = monthly.sort_values(["month", "revenue"], ascending=[True, False])

# Load
monthly.to_csv("monthly_revenue.csv", index=False)
print(f"Saved {len(monthly)} rows")
print(monthly.head(10))
```
</details>

---

## Chapter 17: Testing & Code Quality

Testing isn't optional - it's what separates professional code from scripts that break. Python's testing ecosystem is excellent, with **pytest** as the de facto standard.

### 17.1 pytest - The Testing Framework

**Installation and basic setup:**

```bash
pip install pytest
```

**Your first tests:**

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# test_calculator.py
import pytest
from calculator import add, divide

# Basic tests - function names must start with test_
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0

# Testing exceptions
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_normal():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5
```

```bash
# Run tests
pytest                          # Run all tests
pytest test_calculator.py       # Run specific file
pytest -v                       # Verbose output (shows each test name)
pytest -v -k "test_add"         # Run only tests matching pattern
pytest --tb=short               # Shorter traceback on failure
pytest -x                       # Stop on first failure
```

**Parametrize - test many inputs without writing many functions:**

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
    (0.1, 0.2, pytest.approx(0.3)),  # Floating point comparison!
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

**Fixtures - reusable test setup:**

```python
import pytest
import sqlite3

@pytest.fixture
def db_connection():
    """Create a test database, yield it, then clean up."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice', 30)")
    conn.execute("INSERT INTO users VALUES (2, 'Bob', 25)")
    conn.commit()
    yield conn  # Test runs here
    conn.close()  # Cleanup after test

def test_query_users(db_connection):
    cursor = db_connection.execute("SELECT * FROM users")
    users = cursor.fetchall()
    assert len(users) == 2

def test_query_by_age(db_connection):
    cursor = db_connection.execute("SELECT name FROM users WHERE age > 27")
    names = [row[0] for row in cursor.fetchall()]
    assert names == ["Alice"]

@pytest.fixture
def sample_data():
    """Reusable test data."""
    return {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
    }

def test_user_count(sample_data):
    assert len(sample_data["users"]) == 2
```

### 17.2 Mocking - Testing Without External Dependencies

Mocking replaces real objects with fake ones. Use it to test code that calls APIs, databases, or other external services.

```python
from unittest.mock import Mock, patch, MagicMock

# Mock a function
@patch("requests.get")
def test_fetch_user(mock_get):
    # Configure the mock to return a specific response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Alice", "age": 30}
    mock_get.return_value = mock_response

    # Now test YOUR code that calls requests.get
    import requests
    response = requests.get("https://api.example.com/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

    # Verify the mock was called correctly
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

```python
# Mock for testing email sending
class NotificationService:
    def __init__(self, email_client):
        self.email_client = email_client

    def notify_user(self, user_email, message):
        if not user_email:
            raise ValueError("Email required")
        self.email_client.send(to=user_email, body=message)
        return True

def test_notify_user():
    # Create a mock email client (no real emails sent!)
    mock_client = Mock()
    service = NotificationService(mock_client)

    result = service.notify_user("alice@test.com", "Hello!")

    assert result is True
    mock_client.send.assert_called_once_with(to="alice@test.com", body="Hello!")

def test_notify_no_email():
    mock_client = Mock()
    service = NotificationService(mock_client)

    with pytest.raises(ValueError):
        service.notify_user("", "Hello!")

    mock_client.send.assert_not_called()  # Email should NOT be sent
```

### 17.3 Test Organization Best Practices

```
my_project/
    src/
        __init__.py
        calculator.py
        user_service.py
    tests/
        __init__.py
        test_calculator.py
        test_user_service.py
        conftest.py          # Shared fixtures go here
```

```python
# conftest.py - shared fixtures available to ALL test files
import pytest

@pytest.fixture
def api_url():
    return "https://api.example.com"

@pytest.fixture(autouse=True)
def reset_env(monkeypatch):
    """Automatically reset environment for every test."""
    monkeypatch.setenv("ENV", "test")
```

### 17.4 Code Quality Tools

```bash
# Formatting
black src/               # Auto-format code (opinionated, consistent)
black --check src/       # Check without changing (for CI)

# Linting
ruff check src/          # Fast linter (replaces flake8, isort, etc.)
ruff check --fix src/    # Auto-fix what it can
pylint src/              # More thorough (but slower) linting

# Type checking
mypy src/                # Static type checker
mypy src/ --strict       # Strict mode (catches more issues)

# Security
bandit -r src/           # Find security issues
pip-audit                # Check dependencies for vulnerabilities

# Import sorting
isort src/               # Sort imports consistently

# All at once in CI:
# black --check src/ && ruff check src/ && mypy src/ && pytest tests/ -v
```

### Exercise 17.1: Write Tests

Given this function, write at least 5 tests:

```python
def validate_password(password: str) -> tuple[bool, str]:
    """Validate password. Returns (is_valid, message)."""
    if len(password) < 8:
        return False, "Must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Must contain uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Must contain a digit"
    return True, "Valid"
```

<details>
<summary>Solution</summary>

```python
import pytest

@pytest.mark.parametrize("password, expected_valid, expected_msg", [
    ("Ab1defgh", True, "Valid"),
    ("short1A", False, "Must be at least 8 characters"),
    ("alllowercase1", False, "Must contain uppercase letter"),
    ("ALLUPPERcase", False, "Must contain a digit"),
    ("", False, "Must be at least 8 characters"),
    ("A1bcdefg", True, "Valid"),
    ("12345678A", True, "Valid"),
])
def test_validate_password(password, expected_valid, expected_msg):
    is_valid, msg = validate_password(password)
    assert is_valid == expected_valid
    assert msg == expected_msg
```
</details>

---

## Chapter 18: Data Structures & Algorithms

Understanding DSA helps you write efficient code and is essential for technical interviews. Python's built-in data structures are highly optimized, but knowing *when* to use each one matters.

### 18.1 Big-O Notation

Big-O describes how an algorithm's runtime grows as input size grows. It's about the **worst case** scaling pattern, not the exact time.

| Notation | Name | Example | For n=1000 |
|---|---|---|---|
| O(1) | Constant | Dict lookup, array index | 1 operation |
| O(log n) | Logarithmic | Binary search | ~10 operations |
| O(n) | Linear | List scan, linear search | 1,000 operations |
| O(n log n) | Linearithmic | Merge sort, Python's `sorted()` | ~10,000 operations |
| O(n^2) | Quadratic | Nested loops, bubble sort | 1,000,000 operations |
| O(2^n) | Exponential | Recursive fibonacci (naive) | 10^301 operations! |

**Python built-in data structure complexity:**

| Operation | list | dict | set |
|---|---|---|---|
| Access by index | O(1) | N/A | N/A |
| Search (in) | O(n) | **O(1)** | **O(1)** |
| Insert/append | O(1)* | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) |
| Sort | O(n log n) | N/A | N/A |

*O(1) amortized for list.append()

**Key takeaway:** If you're doing lots of membership checks (`if x in collection`), use a `set` or `dict`, not a `list`!

```python
# Bad: O(n) per lookup * O(n) items = O(n^2)
large_list = list(range(100_000))
for item in items_to_check:
    if item in large_list:  # O(n) each time!
        process(item)

# Good: O(1) per lookup * O(n) items = O(n)
large_set = set(range(100_000))   # One-time O(n) conversion
for item in items_to_check:
    if item in large_set:  # O(1) each time!
        process(item)
```

### 18.2 Binary Search

Binary search finds an element in a **sorted** array in O(log n) time by repeatedly halving the search space.

```python
def binary_search(arr, target):
    """
    Find target in sorted array. Returns index or -1.

    How it works:
    - Look at the middle element
    - If it's the target, we're done
    - If target is smaller, search the left half
    - If target is larger, search the right half
    - Repeat until found or search space is empty
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1    # Target is in right half
        else:
            high = mid - 1   # Target is in left half

    return -1  # Not found

# Example
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(arr, 23))   # 5 (index of 23)
print(binary_search(arr, 50))   # -1 (not found)

# Python's built-in: bisect module
import bisect
arr = [1, 3, 5, 7, 9, 11]
idx = bisect.bisect_left(arr, 5)     # 2 (insertion point for 5)
bisect.insort(arr, 6)                # Insert 6 in sorted position
print(arr)                           # [1, 3, 5, 6, 7, 9, 11]
```

### 18.3 Common Algorithm Patterns

**Two Pointers - efficient for sorted arrays:**

```python
def two_sum_sorted(nums, target):
    """Find two numbers in SORTED array that sum to target. O(n)."""
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

print(two_sum_sorted([1, 3, 5, 7, 11], 12))  # [1, 4] (3 + 11 = 14? No, 1+11=12)
# Actually: [0, 4] -> 1 + 11 = 12
```

**Hash Map pattern - O(1) lookups:**

```python
def two_sum(nums, target):
    """Find two numbers that add up to target. Return their indices. O(n)."""
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1] (2 + 7 = 9)
```

**Sliding Window - subarray problems:**

```python
def max_subarray_sum(arr, k):
    """Find maximum sum of subarray of size k. O(n)."""
    if len(arr) < k:
        return None

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window: add new element, remove old element
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_subarray_sum([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))  # 39 (2+10+23+3... no, 10+23+3+1=37? Let me check: [2,10,23,3]=38)
```

**Memoization / Dynamic Programming:**

```python
from functools import lru_cache

# Fibonacci - naive recursive: O(2^n), with memoization: O(n)
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Climbing stairs: how many ways to reach step n (1 or 2 steps at a time)?
@lru_cache(maxsize=None)
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)

print(climb_stairs(5))  # 8 ways
```

**Sorting - Python's built-in is excellent:**

```python
# sorted() returns a NEW list, .sort() modifies in place
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))              # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(nums, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]

# Sort by custom key
words = ["banana", "pie", "Washington", "a"]
print(sorted(words, key=len))    # ['a', 'pie', 'banana', 'Washington']

# Sort objects by attribute
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    grade: float

students = [Student("Alice", 92), Student("Bob", 88), Student("Charlie", 95)]
print(sorted(students, key=lambda s: s.grade, reverse=True))
# [Student(name='Charlie', grade=95), Student(name='Alice', grade=92), ...]

# Sort dict by value
scores = {"Alice": 92, "Bob": 88, "Charlie": 95}
sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
print(sorted_scores)  # {'Charlie': 95, 'Alice': 92, 'Bob': 88}
```

### 18.4 Python collections Module

```python
from collections import Counter, defaultdict, deque, OrderedDict

# Counter - count things
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
freq = Counter(words)
print(freq)                    # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(freq.most_common(2))    # [('apple', 3), ('banana', 2)]

# defaultdict - dict with default values (no KeyError!)
graph = defaultdict(list)
graph["A"].append("B")  # No need to check if "A" exists
graph["A"].append("C")
graph["B"].append("C")
print(dict(graph))  # {'A': ['B', 'C'], 'B': ['C']}

word_count = defaultdict(int)
for word in "the cat sat on the mat".split():
    word_count[word] += 1  # No need for .get() or if-check
print(dict(word_count))

# deque - double-ended queue (O(1) append/pop from both ends)
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)    # [0, 1, 2, 3]
dq.append(4)        # [0, 1, 2, 3, 4]
dq.popleft()        # 0  (O(1) vs list.pop(0) which is O(n)!)
dq.rotate(1)        # [4, 1, 2, 3]

# Use deque as a fixed-size buffer
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
print(list(recent))  # [2, 3, 4] - oldest items dropped automatically
```

### Exercise 18.1: Algorithm Challenges

1. **Valid Anagram**: Write a function to check if two strings are anagrams (same letters, different order).
2. **Find Duplicates**: Given a list with duplicates, return all duplicate values.
3. **Merge Sorted Lists**: Merge two sorted lists into one sorted list.

<details>
<summary>Solutions</summary>

```python
# 1. Valid Anagram - O(n)
def is_anagram(s1, s2):
    from collections import Counter
    return Counter(s1.lower()) == Counter(s2.lower())

print(is_anagram("listen", "silent"))  # True
print(is_anagram("hello", "world"))    # False

# 2. Find Duplicates - O(n)
def find_duplicates(lst):
    from collections import Counter
    return [item for item, count in Counter(lst).items() if count > 1]

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # [2, 3]

# 3. Merge Sorted Lists - O(n+m)
def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]
```
</details>

---

## Chapter 19: Interview Questions & Answers

These are commonly asked Python interview questions with detailed answers and code examples. Understanding *why* is more important than memorizing answers.

### Q1: What's the difference between list, tuple, and set?

| Feature | List | Tuple | Set |
|---|---|---|---|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` | `{1, 2, 3}` |
| Mutable? | Yes | No | Yes |
| Ordered? | Yes | Yes | No |
| Duplicates? | Yes | Yes | No |
| Hashable? | No | Yes | No |
| Lookup speed | O(n) | O(n) | O(1) |

```python
# Use list when you need to modify the collection
shopping = ["milk", "bread", "eggs"]
shopping.append("butter")

# Use tuple for fixed data (coordinates, DB rows, dict keys)
point = (3, 4)
config = ("localhost", 5432, "mydb")  # Won't accidentally change

# Use set for unique items and fast membership testing
seen_ids = {101, 102, 103}
print(104 in seen_ids)  # O(1) lookup - much faster than list for large data
```

### Q2: Explain deep copy vs shallow copy with an example.

```python
import copy

original = {"name": "Alice", "scores": [90, 85, 95]}

# Assignment: NO copy - same object
ref = original
ref["name"] = "Bob"
print(original["name"])  # "Bob" - original changed!

# Shallow copy: new outer dict, but inner list is shared
shallow = copy.copy(original)
shallow["name"] = "Charlie"      # Doesn't affect original
shallow["scores"].append(100)    # DOES affect original!
print(original["scores"])        # [90, 85, 95, 100]

# Deep copy: completely independent copy
deep = copy.deepcopy(original)
deep["scores"].append(200)
print(original["scores"])        # [90, 85, 95, 100] - NOT affected
```

### Q3: What is the GIL and how does it affect your code?

The **Global Interpreter Lock (GIL)** is a mutex in CPython that allows only one thread to execute Python bytecode at a time, even on multi-core machines.

**Impact:**
- **CPU-bound tasks**: Threading gives NO speedup. Use `multiprocessing` instead.
- **I/O-bound tasks**: Threading works fine because the GIL is released during I/O (file reads, network calls, database queries).

```python
# CPU-bound: use multiprocessing
from multiprocessing import Pool
with Pool(4) as p:
    results = p.map(heavy_computation, data)

# I/O-bound: use threading or asyncio
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
```

### Q4: How do decorators work? Write one.

A decorator is a function that wraps another function to extend its behavior. When you write `@decorator`, Python does `func = decorator(func)`.

```python
from functools import wraps
import time

def timer(func):
    @wraps(func)  # Preserves func.__name__ and func.__doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_func():
    time.sleep(1)

slow_func()  # "slow_func took 1.0012s"
```

### Q5: Explain `*args` and `**kwargs` with examples.

```python
def example(*args, **kwargs):
    print(f"args (tuple): {args}")
    print(f"kwargs (dict): {kwargs}")

example(1, 2, 3, name="Alice", age=30)
# args (tuple): (1, 2, 3)
# kwargs (dict): {'name': 'Alice', 'age': 30}

# Real-world use: flexible wrapper functions
def log_call(func):
    def wrapper(*args, **kwargs):  # Accept ANY arguments
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)  # Pass them through
    return wrapper
```

### Q6: What is a generator and when would you use one?

Generators produce values **lazily** - one at a time, on demand. They use `yield` instead of `return` and are memory-efficient for large datasets.

```python
# List: creates ALL items in memory immediately
def get_squares_list(n):
    return [x**2 for x in range(n)]  # 10M items = ~85MB RAM

# Generator: produces ONE item at a time
def get_squares_gen(n):
    for x in range(n):
        yield x**2  # ~200 bytes regardless of n!

# Use generator for large/infinite sequences
for square in get_squares_gen(10_000_000):
    if square > 1000:
        break  # Only computed ~32 values, not 10M!
```

### Q7: What's the mutable default argument trap?

```python
# BUG: The default list is shared across ALL calls!
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] ← Expected [2]!
print(bad_append(3))  # [1, 2, 3] ← Expected [3]!

# FIX: Use None as default, create new list inside
def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2] ✓
```

### Q8: What's the difference between `==` and `is`?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  (same VALUE)
print(a is b)   # False (different OBJECTS in memory)
print(a is c)   # True  (same OBJECT - c points to a)

# Rule: use 'is' ONLY for None, True, False
if result is None:     # Correct
    pass
if result == None:     # Works but not Pythonic
    pass
```

### Q9: Explain `if __name__ == "__main__"`.

```python
# utils.py
def helper():
    return "I'm a helper"

if __name__ == "__main__":
    # This block runs ONLY when you execute: python utils.py
    # It does NOT run when someone does: import utils
    print(helper())
    print("Running as main script")
```

**Why it matters:** Without this guard, any code at the module level runs on import, which can cause unexpected side effects (tests running, servers starting, etc.).

### Q10: How do you handle missing data in Pandas?

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Diana"],
    "age": [30, None, 35, 28],
    "salary": [95000, 72000, None, 78000]
})

# Detect
print(df.isnull().sum())       # Count missing per column
print(df.isnull().any())       # Which columns have missing?

# Strategy 1: Remove rows
df.dropna()                     # Remove rows with ANY NaN
df.dropna(subset=["name"])      # Remove only if name is NaN

# Strategy 2: Fill with values
df.fillna(0)                    # Fill all with 0
df["age"].fillna(df["age"].median(), inplace=True)  # Fill with median

# Strategy 3: Interpolate (for time series)
df["salary"].interpolate()

# Strategy 4: Forward/backward fill
df.fillna(method="ffill")       # Use previous row's value
df.fillna(method="bfill")       # Use next row's value
```

### Q11: What is MRO (Method Resolution Order)?

MRO determines the order Python searches for methods in a class hierarchy with multiple inheritance. Python uses **C3 linearization**.

```python
class A:
    def greet(self): print("A")

class B(A):
    def greet(self): print("B")

class C(A):
    def greet(self): print("C")

class D(B, C):
    pass

d = D()
d.greet()  # "B" - follows MRO: D -> B -> C -> A
print(D.__mro__)
# (D, B, C, A, object)
```

### Q12: What are context managers and why use them?

Context managers ensure **cleanup happens even if exceptions occur**. They implement `__enter__` and `__exit__` (or use `@contextmanager`).

```python
# Without context manager (bug if exception before close):
f = open("file.txt")
data = f.read()       # What if this raises an exception?
f.close()             # This line might never execute!

# With context manager (always cleaned up):
with open("file.txt") as f:
    data = f.read()   # Even if this fails, file is closed

# Common uses: files, database connections, locks, temporary changes
```

### Q13: Explain the bias-variance tradeoff.

**Bias** = error from wrong assumptions (underfitting). Model is too simple, misses patterns.
**Variance** = error from sensitivity to training data (overfitting). Model memorizes noise.

```python
# High bias (underfitting): linear model for non-linear data
from sklearn.linear_model import LinearRegression
# Fits a straight line through curved data - too simple

# High variance (overfitting): very deep decision tree
from sklearn.tree import DecisionTreeClassifier
# model = DecisionTreeClassifier(max_depth=None)  # Memorizes training data

# Sweet spot: tune complexity
# model = DecisionTreeClassifier(max_depth=5)  # Regularized
# Use cross-validation to find optimal complexity
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)  # 5-fold CV
print(f"Mean accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

### Q14: How does Python memory management work?

Python uses **reference counting** + **garbage collection** (cycle detector).

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount's own reference)

b = a          # refcount = 3
del b          # refcount = 2
# When refcount reaches 0, memory is freed immediately

# Circular references: garbage collector handles these
class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b
b.ref = a  # Circular reference!
del a, b   # Refcount never reaches 0, but GC detects and collects the cycle

import gc
gc.collect()  # Force garbage collection
```

### Q15: What are Python's magic/dunder methods?

Dunder (double underscore) methods let you customize how your objects behave with built-in operations:

```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self):
        return f"${self.amount:.2f} {self.currency}"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        return self.amount < other.amount

    def __len__(self):
        return int(self.amount * 100)  # cents

m1 = Money(10.50)
m2 = Money(5.25)
print(m1 + m2)       # $15.75 USD  (uses __add__)
print(m1 == m2)       # False       (uses __eq__)
print(m1 > m2)        # True        (uses __lt__ via @total_ordering)
print(repr(m1))       # Money(10.5, 'USD')
```

---

## Appendix A: Quick Reference

### Common One-Liners

```python
# Flatten nested list
flat = [x for sub in nested for x in sub]

# Remove duplicates, preserve order
unique = list(dict.fromkeys(items))

# Merge dicts (3.9+)
merged = d1 | d2

# Safe nested dict access
val = d.get("a", {}).get("b", {}).get("c")

# Transpose matrix
transposed = list(zip(*matrix))

# Frequency count
from collections import Counter
freq = Counter(items)

# Invert a dictionary
inverted = {v: k for k, v in d.items()}

# Chunk a list into groups of n
def chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

# Read entire file as string
content = open("file.txt").read()

# Flatten dict to query string
params = {"page": 1, "sort": "name", "order": "asc"}
query = "&".join(f"{k}={v}" for k, v in params.items())
# "page=1&sort=name&order=asc"
```

### Built-in Functions You Should Know

| Category | Functions | Example |
|---|---|---|
| Iteration | `enumerate, zip, reversed, sorted, range` | `for i, x in enumerate(lst)` |
| Aggregation | `len, sum, min, max, any, all` | `any(x > 0 for x in lst)` |
| Types | `int, float, str, bool, list, tuple, set, dict` | `int("42")` |
| Functional | `map, filter, isinstance, getattr, hasattr` | `list(map(str, [1,2,3]))` |
| I/O | `print, input, open` | `open("f.txt")` |
| Introspection | `type, dir, help, vars, id` | `dir(object)` |
| Math | `abs, round, divmod, pow` | `divmod(17, 5)` -> `(3, 2)` |

### String Format Cheatsheet

```python
name = "Alice"
pi = 3.14159
big = 1000000

f"{name:>20}"       # Right-align in 20 chars
f"{name:<20}"       # Left-align
f"{name:^20}"       # Center
f"{pi:.2f}"          # "3.14"
f"{pi:.5f}"          # "3.14159"
f"{big:,}"           # "1,000,000"
f"{big:_}"           # "1_000_000"
f"{0.856:.1%}"       # "85.6%"
f"{42:08d}"          # "00000042"
f"{255:#x}"          # "0xff"
f"{255:#b}"          # "0b11111111"
```

---

## Appendix B: Resources & References

**Official:**
- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

**Learning:**
- [Google's Python Class](https://developers.google.com/edu/python)
- [Real Python](https://realpython.com/) - In-depth tutorials
- [Python Cookbook (O'Reilly)](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)

**Practice:**
- [LeetCode](https://leetcode.com/) - Algorithm problems with Python solutions
- [Project Euler](https://projecteuler.net/) - Math + programming challenges
- [HackerRank Python Track](https://www.hackerrank.com/domains/python)

**Data Science:**
- [Kaggle Learn](https://www.kaggle.com/learn) - Free micro-courses
- [D-Tale](https://pypi.org/project/dtale/) - Interactive DataFrame exploration
- [Pandas Documentation](https://pandas.pydata.org/docs/)

**Tools:**
- [PyPI](https://pypi.org/) - Python Package Index
- [Awesome Python](https://github.com/vinta/awesome-python) - Curated list of libraries

---

*Created from the [beginners-py-learn](https://github.com/paramraghavan/beginners-py-learn) repository.*
