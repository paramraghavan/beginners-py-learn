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

---

*Continued in Part 2 (Chapters 6-19)...*

The remaining chapters continue in the same detailed, example-rich style. See the companion file for the complete guide.
