# Python Data Structures Interview Handbook

This standalone handbook is a practical Python tutorial, data-structures and algorithms reference, pytest guide, and
interview-preparation workbook. It uses Python 3.11+ style and keeps examples concise, runnable, and suitable for daily
reference.

## Table Of Contents

1. [How To Use This Handbook](#1-how-to-use-this-handbook)
2. [macOS Python Development Environment](#2-macos-python-development-environment)
3. [Recommended Python Project Structure](#3-recommended-python-project-structure)
4. [Python Syntax And Execution Model](#4-python-syntax-and-execution-model)
5. [Built-In Python Data Types](#5-built-in-python-data-types)
6. [Strings](#6-strings)
7. [Lists](#7-lists)
8. [Tuples](#8-tuples)
9. [Sets And Frozensets](#9-sets-and-frozensets)
10. [Dictionaries](#10-dictionaries)
11. [Comparing Core Python Collections](#11-comparing-core-python-collections)
12. [Conditions And Control Flow](#12-conditions-and-control-flow)
13. [Loops And Iteration](#13-loops-and-iteration)
14. [Functions](#14-functions)
15. [Comprehensions And Generator Expressions](#15-comprehensions-and-generator-expressions)
16. [Lambda Functions And Functional Tools](#16-lambda-functions-and-functional-tools)
17. [Modules, Packages, And Imports](#17-modules-packages-and-imports)
18. [File Handling And Serialization](#18-file-handling-and-serialization)
19. [Exception Handling](#19-exception-handling)
20. [Object-Oriented Programming](#20-object-oriented-programming)
21. [Dataclasses And Modern Python Models](#21-dataclasses-and-modern-python-models)
22. [Iterables, Iterators, And Generators](#22-iterables-iterators-and-generators)
23. [Decorators](#23-decorators)
24. [Context Managers](#24-context-managers)
25. [Type Hints And Static Analysis](#25-type-hints-and-static-analysis)
26. [Python Memory Model And Copying](#26-python-memory-model-and-copying)
27. [Python Internals](#27-python-internals)
28. [Standard-Library Collections And Utilities](#28-standard-library-collections-and-utilities)
29. [Abstract Data Types And Implementations](#29-abstract-data-types-and-implementations)
30. [Algorithm Complexity](#30-algorithm-complexity)
31. [Searching Algorithms](#31-searching-algorithms)
32. [Sorting Algorithms](#32-sorting-algorithms)
33. [Recursion And Backtracking](#33-recursion-and-backtracking)
34. [Common Coding-Interview Patterns](#34-common-coding-interview-patterns)
35. [Common Coding-Interview Problems](#35-common-coding-interview-problems)
36. [pytest Fundamentals](#36-pytest-fundamentals)
37. [pytest Fixtures](#37-pytest-fixtures)
38. [pytest Parameterization And Markers](#38-pytest-parameterization-and-markers)
39. [Mocking And Patching](#39-mocking-and-patching)
40. [Testing Exceptions, Files, Classes, And APIs](#40-testing-exceptions-files-classes-and-apis)
41. [Test Design And Quality](#41-test-design-and-quality)
42. [Debugging](#42-debugging)
43. [Logging](#43-logging)
44. [Concurrency And Parallelism](#44-concurrency-and-parallelism)
45. [Async Programming](#45-async-programming)
46. [Performance And Profiling](#46-performance-and-profiling)
47. [Clean Python And Design Principles](#47-clean-python-and-design-principles)
48. [Common Python Design Patterns](#48-common-python-design-patterns)
49. [Common Python Mistakes](#49-common-python-mistakes)
50. [Frequently Used Python Snippets](#50-frequently-used-python-snippets)
51. [Python Interview Questions And Answers](#51-python-interview-questions-and-answers)
52. [Data-Structure And Algorithm Interview Questions](#52-data-structure-and-algorithm-interview-questions)
53. [pytest Interview Questions](#53-pytest-interview-questions)
54. [Scenario-Based Interview Preparation](#54-scenario-based-interview-preparation)
55. [Runnable Practice Projects](#55-runnable-practice-projects)
56. [Quick-Revision Sheets](#56-quick-revision-sheets)

## 1. How To Use This Handbook

**Beginner:** Read sections 1-19 in order. Type the examples, run them, change inputs, and explain the output aloud.

**Intermediate:** Use sections 20-35 to strengthen OOP, typing, data structures, complexity, algorithms, and interview
patterns.

**Advanced:** Use sections 36-56 for pytest, mocking, concurrency, async, profiling, design, scenario interviews, and
quick revision.

Run examples:

```bash
python example.py
python -m pytest
python -m pytest -v
```

Use coding problems by following this loop:

1. Restate the problem.
2. Ask clarifying questions.
3. Give a brute-force idea.
4. Improve the data structure or algorithm.
5. Write code.
6. Test edge cases.
7. State time and space complexity.

**Interview answer:** A strong Python interview answer explains the trade-off, not just the syntax.

## 2. macOS Python Development Environment

Install Homebrew if needed, then install Python and Git:

```bash
brew install python
brew install git
python3 --version
git --version
```

Apple Silicon notes:

- Homebrew usually lives under `/opt/homebrew`.
- Intel Homebrew usually lives under `/usr/local`.
- If commands fail, check `echo $PATH` and `which brew`.

Create and activate a virtual environment:

**Why this matters:** A virtual environment gives each project its own installed
packages. Without it, one project's dependency upgrade can accidentally break
another project.

```bash
python3 -m venv .venv
source .venv/bin/activate
which python
python --version
python -m pip --version
```

Install development tools:

**Why this matters:** These tools catch different classes of mistakes. `pytest`
checks behavior, `ruff` catches common code issues, `black` formats consistently,
`mypy` checks type hints, and `pre-commit` runs checks before code is committed.

```bash
python -m pip install --upgrade pip
python -m pip install pytest pytest-cov ruff black mypy pre-commit
```

Deactivate:

```bash
deactivate
```

Create dependency files:

```bash
python -m pip freeze > requirements.txt
```

Minimal `pyproject.toml`:

**Why this matters:** `pyproject.toml` is the modern place to store project and
tool configuration. Keeping settings in one file makes the project easier for
another developer, teammate, or interviewer to run.

```toml
[project]
name = "python-handbook-examples"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100

[tool.black]
line-length = 100
```

Run scripts, modules, and tests:

```bash
python script.py
python -m package.module
pytest
pytest -v
pytest --cov=src
```

**Production note:** Virtual environments isolate dependencies so one project does not break another.

**Common mistake:** Calling `pip` directly can install into a different Python. Prefer `python -m pip`.

## 3. Recommended Python Project Structure

**Why this matters:** A consistent project layout makes imports, tests, and
packaging predictable. Beginners often lose time because code works from one
folder but fails from another; a clear layout prevents that.

```text
python-handbook-examples/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── python_examples/
│       ├── __init__.py
│       ├── collections_examples.py
│       ├── algorithms.py
│       ├── models.py
│       └── main.py
└── tests/
    ├── conftest.py
    ├── test_collections.py
    └── test_algorithms.py
```

**Beginner:** A module is a `.py` file. A package is a directory of modules. `__init__.py` marks a directory as a
regular package and can expose package-level imports.

**Intermediate:** The `src` layout helps tests import installed package code instead of accidentally importing files
from the working directory.

**Production note:** Do not make application logic depend on the current working directory. Pass paths explicitly or
derive them from configuration.

## 4. Python Syntax And Execution Model

Python programs are made of statements and expressions. Expressions produce values; statements perform actions.

**Mental model:** Python runs a file from top to bottom. A name is not a box that
contains a value; it is a label that points to an object. This matters when two
names point to the same mutable object.

```python
name = "Ada"
score = 95

if score >= 90:
    print(f"{name} passed")
```

Names refer to objects:

```python
values = [1, 2]
alias = values
alias.append(3)
print(values)
```

`==` compares values. `is` compares object identity.

```python
left = [1, 2]
right = [1, 2]
same_object = left

print(left == right)
print(left is right)
print(left is same_object)
```

**Interview answer:** Python is dynamically typed because names can refer to different object types over time. It is
strongly typed because it does not silently combine incompatible types like `"x" + 1`.

**When explaining in an interview:** Say both parts. "Dynamic" means the type is
checked while the program runs. "Strong" means Python will not guess a conversion
when the operation is unsafe.

**Common mistake:** Use `is None`, but use `==` for normal value comparison.

## 5. Built-In Python Data Types

| Type        | Example             | Mutable | Use                        |
|-------------|---------------------|--------:|----------------------------|
| `int`       | `42`                |      No | Whole numbers              |
| `float`     | `3.14`              |      No | Approximate decimal values |
| `complex`   | `1 + 2j`            |      No | Scientific/math work       |
| `bool`      | `True`              |      No | Conditions                 |
| `str`       | `"text"`            |      No | Unicode text               |
| `bytes`     | `b"abc"`            |      No | Immutable binary data      |
| `bytearray` | `bytearray(b"abc")` |     Yes | Mutable binary data        |
| `None`      | `None`              |      No | Absence of value           |

**Mental model:** Choose a type by the promise you want to make. Use immutable
types when a value should not change, and mutable containers when the program
needs to add, remove, or update items.

```python
value = 42
print(type(value))
print(isinstance(value, int))
```

**Interview answer:** Prefer `isinstance(value, expected_type)` when checking type relationships because it respects
inheritance and can check multiple allowed types.

**Common mistake:** Do not compare exact types with `type(value) == SomeClass`
unless you intentionally want to reject subclasses.

Floating-point caution:

```python
import math

print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
```

## 6. Strings

Strings are immutable Unicode sequences.

**Mental model:** Every string operation returns a new string. Methods like
`strip`, `lower`, and `replace` do not modify the original text.

```python
text = "  Python,Data,Engineering  "
print(text.strip())
print(text.lower())
print(text.split(","))
print("-".join(["a", "b", "c"]))
print(text.replace("Python", "Modern Python"))
```

Runnable interview helpers:

```python
from collections import Counter


def reverse_string(text: str) -> str:
    return text[::-1]


def is_palindrome(text: str) -> bool:
    cleaned = "".join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def character_frequency(text: str) -> Counter[str]:
    return Counter(text)


def first_non_repeating(text: str) -> str | None:
    counts = Counter(text)
    for char in text:
        if counts[char] == 1:
            return char
    return None


def remove_duplicate_characters(text: str) -> str:
    return "".join(dict.fromkeys(text))


def are_anagrams(left: str, right: str) -> bool:
    return Counter(left) == Counter(right)


def longest_unique_substring(text: str) -> int:
    seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, char in enumerate(text):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        best = max(best, right - left + 1)
    return best
```

Why `is_palindrome` uses `char.isalnum()`:

Many interview palindrome questions say to ignore spaces, punctuation, and
capitalization. `isalnum()` keeps only letters and numbers.

```python
text = "A man, a plan, a canal: Panama"
cleaned = "".join(char.lower() for char in text if char.isalnum())
print(cleaned)  # amanaplanacanalpanama
```

Without `isalnum()`, the comma, spaces, and colon would be compared too, and the
phrase would look like it is not a palindrome. `char.lower()` handles uppercase
and lowercase letters consistently.

```python
return cleaned == cleaned[::-1]
```

This compares the cleaned string with its reverse:

```text
amanaplanacanalpanama
amanaplanacanalpanama
```

Build large strings efficiently:

```python
parts = ["row", ":", "42"]
line = "".join(parts)
```

**Performance note:** Repeated `result += piece` in a loop may allocate many intermediate strings. Use `"".join(parts)`
when collecting many pieces.

**Interview answer:** Strings are immutable, so algorithms that repeatedly build
text should collect pieces in a list and join once. For character counting,
anagrams, and first-non-repeating-character problems, `Counter` is often the
clearest tool.

## 7. Lists

Lists are mutable ordered arrays of object references.

**Mental model:** A list is best when order matters and you need to change the
sequence. It is excellent for appending and indexing, but not ideal for repeated
membership checks on large data.

```python
numbers = [3, 1, 2]
numbers.append(4)
numbers.extend([5, 6])
numbers.insert(0, 0)
numbers.remove(3)
last = numbers.pop()
numbers.sort()
copy_of_numbers = numbers.copy()
```

Complexity:

| Operation            |     Complexity |
|----------------------|---------------:|
| Index lookup         |           O(1) |
| Membership           |           O(n) |
| Append               | O(1) amortized |
| Insert/delete middle |           O(n) |
| Pop end              |           O(1) |
| Sorting              |     O(n log n) |
| Slicing length `k`   |           O(k) |

Bad nested-list initialization:

```python
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)
```

Correct:

```python
matrix = [[0 for _ in range(3)] for _ in range(3)]
```

**Common mistake:** Do not remove from a list while iterating over the same list. Build a new filtered list.

```python
numbers = [1, 2, 3, 4]
evens = [number for number in numbers if number % 2 == 0]
```

**Interview answer:** Lists give O(1) indexing and amortized O(1) append. Middle
insertions, middle deletions, and membership checks are O(n), so switch to a set,
dict, or deque when those operations dominate.

## 8. Tuples

Tuples are immutable ordered containers.

**Mental model:** Use a tuple when the position has meaning and the group should
not change, such as `(x, y)` or `(status_code, message)`.

```python
point = (10, 20)
x, y = point
```

Multiple return values are usually tuples:

```python
def min_max(values: list[int]) -> tuple[int, int]:
    return min(values), max(values)
```

Named tuple:

```python
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
```

**Interview answer:** Use tuples for fixed-shape values and lists for mutable sequences.

**Common mistake:** A tuple can contain mutable objects. The tuple cannot be
resized, but a list inside the tuple can still be mutated.

## 9. Sets And Frozensets

Sets store unique hashable values and support fast average membership checks.

**Mental model:** A set answers the question "Have I seen this before?" quickly.
It is the right default for deduplication and repeated membership tests.

```python
values = {1, 2, 3}
other = {3, 4}

print(values | other)
print(values & other)
print(values - other)
print(values ^ other)
```

Practical examples:

```python
def has_duplicates(values: list[int]) -> bool:
    return len(values) != len(set(values))


def common_values(left: list[int], right: list[int]) -> set[int]:
    return set(left) & set(right)
```

`frozenset` is immutable and hashable:

```python
key = frozenset({"read", "write"})
permissions = {key: "editor"}
```

**Performance note:** Set membership is average O(1), but values must be hashable.

**Interview answer:** Use a set when uniqueness or fast membership is more
important than order or duplicates. Convert a list to a set only if losing
duplicates is acceptable.

## 10. Dictionaries

Dictionaries map hashable keys to values and preserve insertion order in modern Python.

**Mental model:** A dictionary is a labeled lookup table. Use it when you want to
find information by a key instead of scanning a whole list.

```python
user = {"id": 1, "name": "Ada"}
user["role"] = "engineer"
print(user.get("missing", "default"))
```

Frequency map:

```python
from collections import Counter, defaultdict


def count_words(words: list[str]) -> Counter[str]:
    return Counter(words)


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    return dict(groups)
```

Merge configurations:

```python
defaults = {"debug": False, "retries": 3}
override = {"debug": True}
config = defaults | override
```

**Interview answer:** Dict lookup is average O(1). Worst case can degrade if many keys collide, but Python's
implementation is engineered to make this rare.

**Common mistake:** Accessing `mapping[key]` raises `KeyError` if the key is
missing. Use `get`, `setdefault`, `defaultdict`, or an explicit `if key in
mapping` depending on the intent.

## 11. Comparing Core Python Collections

| Collection  | Ordered | Mutable | Duplicates |          Lookup | Best use                  |
|-------------|--------:|--------:|-----------:|----------------:|---------------------------|
| `list`      |     Yes |     Yes |        Yes | O(n) membership | Ordered mutable sequence  |
| `tuple`     |     Yes |      No |        Yes | O(n) membership | Fixed records             |
| `set`       |      No |     Yes |         No |        O(1) avg | Unique values             |
| `frozenset` |      No |      No |         No |        O(1) avg | Immutable set key         |
| `dict`      |     Yes |     Yes |    Keys no |    O(1) avg key | Key-value lookup          |
| `deque`     |     Yes |     Yes |        Yes | O(n) membership | Fast append/pop both ends |

**Interview answer:** Use the structure that matches the operation you need most often.

**Decision rule:** If you need order and mutation, start with `list`. If you need
fast lookup by key, use `dict`. If you need unique values or repeated membership
tests, use `set`. If you need a fixed record, use `tuple`.

## 12. Conditions And Control Flow

```python
status = "ready"

if status == "ready":
    print("start")
elif status == "paused":
    print("wait")
else:
    print("stop")
```

**Mental model:** Conditions should read like business rules. Put unusual or
invalid cases early as guard clauses so the normal path is easy to follow.

Guard clause:

```python
def discount(price: float, active: bool) -> float:
    if price < 0:
        raise ValueError("price must be non-negative")
    if not active:
        return price
    return price * 0.9
```

Pattern matching is Python 3.10+:

```python
def describe(command: str) -> str:
    match command:
        case "start":
            return "starting"
        case "stop":
            return "stopping"
        case _:
            return "unknown"
```

**Common mistake:** Avoid `if value == True:`. Prefer `if value:`.

**Interview answer:** Python uses truthiness. Empty containers, `0`, `0.0`, `""`,
`False`, and `None` are falsey; most other objects are truthy.

## 13. Loops And Iteration

Direct iteration is usually clearer than index iteration:

**Mental model:** In Python, loop over the thing itself unless you truly need the
index. This makes code shorter and avoids off-by-one errors.

```python
values = ["a", "b", "c"]

for value in values:
    print(value)

for index, value in enumerate(values):
    print(index, value)
```

Avoid this unless the index is required:

```python
for index in range(len(values)):
    print(values[index])
```

Nested loops are often O(n²):

```python
def all_pairs(values: list[int]) -> list[tuple[int, int]]:
    pairs = []
    for left in values:
        for right in values:
            pairs.append((left, right))
    return pairs
```

Loop `else` runs if no `break` occurs:

```python
for number in [1, 3, 5]:
    if number % 2 == 0:
        break
else:
    print("no even number")
```

**Interview answer:** Prefer direct iteration, `enumerate` when you need indexes,
and `zip` when walking multiple iterables together. Always be ready to state
whether a nested loop is O(n²).

## 14. Functions

```python
def add(left: int, right: int) -> int:
    """Return the sum of two integers."""
    return left + right
```

**Mental model:** A function should do one clear job, name its inputs, return a
result, and avoid surprising changes to external state unless mutation is the
point of the function.

Argument forms:

```python
def describe(name: str, /, role: str = "user", *, active: bool = True) -> str:
    return f"{name}:{role}:{active}"
```

Closure:

```python
def multiplier(factor: int):
    def multiply(value: int) -> int:
        return value * factor

    return multiply
```

**Interview answer:** Python does not pass variables by value or by reference in
the C++ sense. Python passes object references by assignment.

That means a function parameter becomes another name for the same object the
caller passed in.

If the object is mutable and the function changes it, the caller sees the
change:

```python
def add_score(scores: list[int]) -> None:
    scores.append(100)


exam_scores = [80, 90]
add_score(exam_scores)
print(exam_scores)  # [80, 90, 100]
```

The function did not receive a copy of the list. `scores` and `exam_scores`
pointed to the same list object.

But assigning the parameter to a new object does not change the caller's name:

```python
def replace_scores(scores: list[int]) -> None:
    scores = [100]


exam_scores = [80, 90]
replace_scores(exam_scores)
print(exam_scores)  # [80, 90]
```

`scores = [100]` only makes the local name `scores` point to a new list. It does
not reassign `exam_scores` in the caller.

**Common mistake:** Default argument values are created once when Python defines
the function, not every time the function is called.

Bad:

```python
def add_item_bad(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items


print(add_item_bad("a"))  # ['a']
print(add_item_bad("b"))  # ['a', 'b'] surprise: same default list
```

Good:

```python
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

Use `None` as the default, then create a fresh list inside the function.

## 15. Comprehensions And Generator Expressions

```python
numbers = [1, 2, 3, 4]
squares = [number * number for number in numbers]
lookup = {number: number * number for number in numbers}
unique_parity = {number % 2 for number in numbers}
```

Generator expression:

```python
squares = (number * number for number in range(1_000_000))
```

The syntax looks similar, but the result is different:

```python
numbers = range(1_000_000)

all_squares = [number * number for number in numbers]
lazy_squares = (number * number for number in numbers)
```

`all_squares` is a list. Python calculates every square immediately and stores all
1,000,000 results in memory.

`lazy_squares` is a generator expression. Python does not calculate all results
up front. It produces one value at a time when you iterate over it:

```python
for square in lazy_squares:
    print(square)
    if square > 100:
        break
```

Use a list comprehension when you need the whole result now, need to reuse it,
need its length, or need indexing:

```python
squares = [number * number for number in range(10)]
print(len(squares))
print(squares[0])
```

Use a generator expression when you only need to loop once, stream values, or
feed another function:

```python
total = sum(number * number for number in range(1_000_000))
```

This avoids building a large temporary list.

**Interview answer:** A list comprehension eagerly builds and stores a full list.
A generator expression lazily produces one value at a time, so it can use much
less memory. The trade-off is that a generator is one-pass: after it is consumed,
you must create it again if you want to iterate over the values again.

**Common mistake:** If the comprehension needs multiple nested conditions, use a normal loop for readability.

## 16. Lambda Functions And Functional Tools

**Mental model:** `lambda` creates a small anonymous function. It is useful when
the function is short and local to one expression, but it should not hide logic
that deserves a name.

```python
from functools import partial, reduce

numbers = [1, 2, 3, 4]
squares = list(map(lambda number: number * number, numbers))
evens = list(filter(lambda number: number % 2 == 0, numbers))
total = reduce(lambda left, right: left + right, numbers, 0)
```

Often clearer:

```python
squares = [number * number for number in numbers]
evens = [number for number in numbers if number % 2 == 0]
```

Partial function:

```python
def power(base: int, exponent: int) -> int:
    return base ** exponent


square = partial(power, exponent=2)
print(square(5))  # 25
```

`partial` creates a new function by pre-filling some arguments of an existing
function.

Here, `power` normally needs two arguments:

```python
power(5, 2)
```

`partial(power, exponent=2)` creates a new function where `exponent` is already
set to `2`. So this:

```python
square(5)
```

means:

```python
power(5, exponent=2)
```

It is similar to writing this manually:

```python
def square(base: int) -> int:
    return power(base, exponent=2)
```

Use `partial` when you already have a general function and want to create a more
specific version of it.

`key=` is another common place where small functions are useful. Functions such
as `sorted`, `min`, and `max` can receive a `key` function. Python calls that
function for each item and sorts or compares by the returned value.

```python
names = ["Grace", "Ada", "Katherine"]

by_length = sorted(names, key=lambda name: len(name))
print(by_length)  # ['Ada', 'Grace', 'Katherine']
```

The lambda says: "For each name, use `len(name)` as the value to sort by."

For a dictionary or object-like record:

```python
students = [
    {"name": "Ada", "score": 95},
    {"name": "Grace", "score": 99},
    {"name": "Katherine", "score": 97},
]

by_score = sorted(students, key=lambda student: student["score"])
```

Here, Python sorts the dictionaries by each student's `score`.

**Interview answer:** Use lambda for tiny throwaway functions, commonly with `key=`, but prefer named functions for
testable business logic.

**Common mistake:** Do not use `lambda` to show off. A named function is easier
to test, document, reuse, and debug.

## 17. Modules, Packages, And Imports

**Mental model:** A module is one `.py` file. A package is a directory of modules.
Imports are how Python code shares names across files.

```python
import json
from pathlib import Path
from collections import Counter as FrequencyCounter
```

Script entry point:

```python
def main() -> int:
    print("running")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Troubleshooting:

| Problem               | Likely cause                                                |
|-----------------------|-------------------------------------------------------------|
| `ModuleNotFoundError` | Wrong environment, missing install, wrong working directory |
| Relative import error | Running a file directly instead of as a module              |
| Circular import       | Two modules import each other at import time                |
| `json.py` shadowing   | File named after a standard-library module                  |

**Interview answer:** Imports execute module top-level code once, then cache the
module in `sys.modules`. Keep top-level code lightweight and put runnable script
behavior behind `if __name__ == "__main__":`.

**Common mistake:** Naming your file `json.py`, `typing.py`, `collections.py`, or
`pytest.py` can shadow real packages and create confusing import errors.

## 18. File Handling And Serialization

Use `pathlib` and context managers.

**Mental model:** Opening a file creates an external resource. A context manager
closes it reliably, even if an exception happens while reading or writing.

```python
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
```

JSON:

```python
import json
from pathlib import Path


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
```

Usage example:

```python
import json
from pathlib import Path


def save_tasks(path: Path, tasks: list[dict[str, object]]) -> None:
    text = json.dumps(tasks, indent=2)
    path.write_text(text, encoding="utf-8")


def load_tasks(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("tasks file must contain a JSON list")
    return data


tasks_file = Path("tasks.json")

save_tasks(
    tasks_file,
    [
        {"title": "review notes", "done": False},
        {"title": "practice pytest", "done": True},
    ],
)

tasks = load_tasks(tasks_file)
print(tasks[0]["title"])  # review notes
```

This pattern is useful for beginner projects such as contact managers, todo
lists, small settings files, and command-line tools. JSON is readable by humans
and can be shared with many other languages.

CSV:

```python
import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file_obj:
        return list(csv.DictReader(file_obj))
```

Large file:

```python
from pathlib import Path
from collections.abc import Iterator


def lines_containing(path: Path, marker: str) -> Iterator[str]:
    with path.open(encoding="utf-8") as file_obj:
        for line in file_obj:
            if marker in line:
                yield line.rstrip()
```

**Production note:** Do not unpickle untrusted data. Pickle can execute code during loading.

**Interview answer:** For text files, always be explicit about encoding. For
large files, stream line by line instead of calling `read_text()` on the whole
file. For portable structured data, prefer JSON or CSV before pickle.

## 19. Exception Handling

**Mental model:** Exceptions separate the normal path from failure paths. Catch an
exception only when you can add context, recover, retry, or convert it into a
clearer domain-specific error.

```python
from pathlib import Path


def read_required(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"missing required file: {path}") from exc
```

Unsafe:

```python
try:
    risky_operation()
except Exception:
    pass
```

**Interview answer:** `except Exception: pass` hides failures, makes debugging harder, and can leave data inconsistent.

**Common mistake:** Catching too broadly and continuing can make the program look
successful after it has already failed. Catch specific exceptions and preserve
the original cause with `raise ... from exc`.

Custom exception:

```python
class InvalidInputError(ValueError):
    """Raised when input validation fails."""
```

## 20. Object-Oriented Programming

**Mental model:** Use a class when data and behavior naturally belong together.
Do not create classes only to hold unrelated functions.

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @property
    def is_square(self) -> bool:
        return self.width == self.height

    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def square(cls, side: float) -> "Rectangle":
        return cls(side, side)

    @staticmethod
    def is_valid_side(side: float) -> bool:
        return side > 0
```

| Decorator       | Receives                 | Use                                           |
|-----------------|--------------------------|-----------------------------------------------|
| `@staticmethod` | Neither `self` nor `cls` | Related utility                               |
| `@classmethod`  | `cls`                    | Alternate constructor or class-level behavior |
| `@property`     | `self`                   | Computed attribute                            |

**Interview answer:** Prefer composition when an object "has a" dependency; use inheritance for true "is a"
relationships.

**Decision rule:** If you can describe the relationship as "uses a" or "has a",
prefer composition. If every subclass truly satisfies the parent contract, then
inheritance may be appropriate.

## 21. Dataclasses And Modern Python Models

**Mental model:** A dataclass removes boilerplate for objects that mostly store
named fields. It is a good fit for application data, configuration, and small
domain records.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple, TypedDict


class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass(frozen=True, slots=True)
class Ticket:
    ticket_id: int
    title: str
    status: Status = Status.OPEN
    tags: tuple[str, ...] = field(default_factory=tuple)


class Point(NamedTuple):
    x: int
    y: int


class UserPayload(TypedDict):
    id: int
    name: str
```

**Interview answer:** Dataclasses are best for Python objects with named fields and light behavior. `TypedDict`
describes dictionary-shaped data for type checkers.

**Common mistake:** Use `field(default_factory=list)` for mutable defaults in a
dataclass. Do not write `tags: list[str] = []`.

## 22. Iterables, Iterators, And Generators

**Mental model:** An iterable can be looped over. An iterator remembers where it
is during iteration. A generator is a convenient way to write an iterator.

Custom iterator:

```python
class CountUp:
    def __init__(self, stop: int) -> None:
        self.current = 0
        self.stop = stop

    def __iter__(self) -> "CountUp":
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        self.current += 1
        return self.current
```

Generator pipeline:

```python
from collections.abc import Iterable, Iterator


def only_even(values: Iterable[int]) -> Iterator[int]:
    for value in values:
        if value % 2 == 0:
            yield value


def squared(values: Iterable[int]) -> Iterator[int]:
    for value in values:
        yield value * value
```

Paginated producer:

```python
from collections.abc import Iterator


def pages(total: int, page_size: int) -> Iterator[range]:
    for start in range(0, total, page_size):
        yield range(start, min(start + page_size, total))
```

**Interview answer:** `yield` turns a function into a generator. It returns values one at a time and preserves state
between iterations.

**When to use generators:** Use them for streaming data, large files, pipelines,
or early stopping. Convert to a list only when you truly need all values at once.

## 23. Decorators

**Mental model:** A decorator takes a function and returns a new function, usually
adding behavior before or after the original call.

```python
from functools import lru_cache, wraps
from time import perf_counter, sleep


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {perf_counter() - started:.3f}s")

    return wrapper


def retry(times: int, delay: float):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except TimeoutError as exc:
                    last_error = exc
                    sleep(delay)
            raise RuntimeError("retries exhausted") from last_error

        return wrapper

    return decorate


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

**Decorator order:** In `@a @b def f`, Python applies `f = a(b(f))`.

**Interview answer:** Decorators are useful for cross-cutting behavior such as
timing, logging, caching, authorization, retry, or validation. Use
`functools.wraps` so the wrapper keeps the original function metadata.

## 24. Context Managers

**Mental model:** A context manager wraps setup and cleanup around a block. It is
the pattern behind `with open(...) as file_obj:`.

```python
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from collections.abc import Iterator


@contextmanager
def timer(label: str) -> Iterator[None]:
    started = perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {perf_counter() - started:.3f}s")


with TemporaryDirectory() as directory:
    path = Path(directory) / "example.txt"
    path.write_text("hello", encoding="utf-8")
```

**Interview answer:** Context managers guarantee cleanup even when exceptions occur.

**Common mistake:** Manually opening files without closing them is fragile. Use
`with` for files, locks, temporary directories, database sessions, and timers.

## 25. Type Hints And Static Analysis

**Mental model:** Type hints are notes for humans and tools. They make contracts
visible without changing normal Python runtime behavior.

```python
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Any, Literal, Protocol, TypeVar, TypedDict


class User(TypedDict):
    id: int
    name: str


class SupportsSave(Protocol):
    def save(self) -> None:
        ...


T = TypeVar("T")


def find_user(user_id: int) -> User | None:
    return {"id": user_id, "name": "Ada"} if user_id > 0 else None


def first(values: Sequence[T]) -> T:
    return values[0]
```

**Interview answer:** Type hints do not normally enforce runtime behavior. Static tools use annotations to catch errors
earlier and improve maintainability.

**Decision rule:** Prefer `Sequence[T]` for read-only ordered inputs,
`Iterable[T]` when you only loop, `Mapping[K, V]` for read-only dictionaries, and
concrete `list` or `dict` when the function mutates the object.

## 26. Python Memory Model And Copying

**Mental model:** Assignment gives another name to the same object. Copying makes
a new object, but shallow copy does not recursively copy nested objects.

```python
import copy

original = {"items": [1, 2]}
alias = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow["items"].append(3)
print(original["items"])

deep["items"].append(4)
print(original["items"])
```

**Interview answer:** Assignment creates another reference to the same object. A shallow copy copies the outer
container; a deep copy recursively copies nested objects.

**Common mistake:** Shallow copying a list of lists copies the outer list only.
The inner lists are still shared.

## 27. Python Internals

**Mental model:** Python source code is compiled to bytecode, and CPython runs
that bytecode on a virtual machine.

```python
import dis


def add(left: int, right: int) -> int:
    return left + right


dis.dis(add)
```

**Interview answer:** CPython compiles source code to bytecode and runs it on the Python virtual machine. The GIL allows
one thread at a time to execute Python bytecode in one process.

**Interview caveat:** The GIL does not make your whole program thread-safe. It
does not prevent race conditions on shared state, and it does not block I/O-bound
concurrency from being useful.

LEGB name lookup:

1. Local
2. Enclosing
3. Global
4. Built-in

Descriptors define `__get__`, `__set__`, or `__delete__` and power features like properties and methods.

## 28. Standard-Library Collections And Utilities

**Mental model:** The standard library often contains the data structure an
interview problem is asking you to rediscover. Knowing the right tool can make a
solution shorter and clearer.

```python
from collections import ChainMap, Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass
from enum import Enum
from functools import cache
from heapq import heappop, heappush
from itertools import combinations
from operator import itemgetter
import bisect
```

```python
counts = Counter("banana")
groups: dict[str, list[str]] = defaultdict(list)
queue = deque(["a", "b"])
queue.appendleft("start")

heap: list[int] = []
heappush(heap, 3)
heappush(heap, 1)
smallest = heappop(heap)
```

**Interview answer:** `Counter`, `defaultdict`, `deque`, `heapq`, and `bisect` often turn long interview solutions into
clean short ones.

**Decision rule:** Use `Counter` for frequencies, `defaultdict` for grouping,
`deque` for queues, `heapq` for top-K or priority queues, and `bisect` for
searching insertion positions in sorted lists.

## 29. Abstract Data Types And Implementations

Educational implementations help interviews. In production, prefer built-ins unless you need custom behavior.

**Mental model:** An abstract data type describes behavior, not implementation.
A stack means last-in, first-out. A queue means first-in, first-out. Many
different internal structures can provide the same behavior.

**Why this matters:** Interviewers often ask you to implement a structure to see
whether you understand its operations and trade-offs. In production, the same
knowledge helps you choose Python's built-in `list`, `deque`, `dict`, `set`,
`heapq`, or another library structure wisely.

Stack and queue:

Use a stack when the most recent item should be handled first, such as undo,
backtracking, depth-first search, or matching parentheses. Use a queue when the
oldest item should be handled first, such as breadth-first search, task queues,
or level-order traversal.

```python
from collections import deque


class Stack:
    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, value: int) -> None:
        self._items.append(value)

    def pop(self) -> int:
        return self._items.pop()


class Queue:
    def __init__(self) -> None:
        self._items: deque[int] = deque()

    def enqueue(self, value: int) -> None:
        self._items.append(value)

    def dequeue(self) -> int:
        return self._items.popleft()
```

Linked list:

Linked lists are less common in everyday Python because `list` is highly
optimized. They are still useful for interviews because they test pointer-style
reasoning: changing `next` links without losing the rest of the chain.

```python
from dataclasses import dataclass


@dataclass
class ListNode:
    value: int
    next: "ListNode | None" = None


def reverse_linked_list(head: ListNode | None) -> ListNode | None:
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous
```

Trie:

A trie is useful when many strings share prefixes. It avoids repeatedly scanning
whole words for prefix lookup, autocomplete, spell-checking, and dictionary-word
search problems.

```python
class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_word = True
```

Union-find:

Union-find is useful when the problem asks whether items belong to the same
group. It appears in connectivity, network, friend-circle, island-merging, and
minimum-spanning-tree problems.

```python
class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.rank[root_left] < self.rank[root_right]:
            self.parent[root_left] = root_right
        elif self.rank[root_left] > self.rank[root_right]:
            self.parent[root_right] = root_left
        else:
            self.parent[root_right] = root_left
            self.rank[root_left] += 1
```

Complexity summary:

**Why this matters:** Complexity tells you when a data structure will still work
as input grows. A solution that is clear for 10 items may be unusable for
1,000,000 items if the main operation is too slow.

| Structure   | Main operations                           |
|-------------|-------------------------------------------|
| Stack       | push/pop O(1)                             |
| Queue/deque | append/popleft O(1)                       |
| Linked list | insert after node O(1), search O(n)       |
| Hash table  | average lookup/insert/delete O(1)         |
| Heap        | push/pop O(log n)                         |
| Trie        | insert/search O(k), k = word length       |
| Union-find  | near O(1) amortized with path compression |

## 30. Algorithm Complexity

**Mental model:** Big O is about growth. Ask: "If input doubles, does the work
stay constant, grow a little, grow linearly, or explode?"

| Class      | Example                      |
|------------|------------------------------|
| O(1)       | Indexing a list              |
| O(log n)   | Binary search                |
| O(n)       | Linear scan                  |
| O(n log n) | Efficient comparison sorting |
| O(n²)      | All pairs                    |
| O(2ⁿ)      | Subsets                      |
| O(n!)      | Permutations                 |

```python
def linear_sum(values: list[int]) -> int:
    total = 0
    for value in values:
        total += value
    return total
```

**Interview answer:** Big O describes how runtime or memory grows as input grows. It ignores constants and lower-order
terms.

Recursion stack space counts as space complexity.

**Common mistake:** Do not say an algorithm is O(1) space if recursion can go
O(n) deep. The call stack is memory too.

## 31. Searching Algorithms

**Mental model:** Linear search works on any sequence. Binary search is faster,
but only when the search space is sorted or has a monotonic true/false pattern.

Linear search:

```python
def linear_search(values: list[int], target: int) -> int:
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1
```

Binary search:

```python
def binary_search(values: list[int], target: int) -> int:
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Rotated sorted array:

```python
def search_rotated(values: list[int], target: int) -> int:
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[left] <= values[mid]:
            if values[left] <= target < values[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if values[mid] < target <= values[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

pytest tests:

```python
def test_binary_search_found() -> None:
    assert binary_search([1, 3, 5], 3) == 1


def test_binary_search_missing() -> None:
    assert binary_search([1, 3, 5], 2) == -1
```

Complexity: binary search is O(log n) time and O(1) space.

**Interview answer:** Binary search repeatedly discards half of the remaining
search space. The key requirement is not merely "an array"; it is an ordered or
monotonic condition that tells you which half can be ignored.

## 32. Sorting Algorithms

**Mental model:** In real Python code, use `sorted()` or `.sort()` first. Learn
manual sorts to understand complexity, stability, and interview trade-offs.

Built-in sorting:

```python
values = [3, 1, 2]
new_values = sorted(values)
values.sort()
```

`sorted()` returns a new list. `.sort()` mutates the list and returns `None`.

Picture:

```text
Original list:
values = [3, 1, 2]

Using sorted(values):
Step 1: Python reads values
Step 2: Python creates a new sorted list
Step 3: values is unchanged

values             -> [3, 1, 2]
new_values         -> [1, 2, 3]

Using values.sort():
Step 1: Python sorts the same list object in place
Step 2: values itself changes

values before      -> [3, 1, 2]
values after       -> [1, 2, 3]
```

Python's built-in sort uses Timsort. It is the best default in real Python code
because it is stable and performs very well on partially sorted data.

Big O:

```text
Best time:    O(n)        when data is already mostly sorted
Average time: O(n log n)
Worst time:   O(n log n)
Extra space:  O(n)        worst case for merging runs
```

Insertion sort:

```python
def insertion_sort(values: list[int]) -> list[int]:
    result = values.copy()
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result
```

Picture:

```text
Start: [5, 2, 4, 1]

The left side is the sorted side.

Pass 1: take 2
[5 | 2, 4, 1]
 2 is smaller than 5, so shift 5 right
[_, 5 | 4, 1]
 insert 2
[2, 5 | 4, 1]

Pass 2: take 4
[2, 5 | 4, 1]
 4 is smaller than 5, so shift 5 right
[2, _, 5 | 1]
 insert 4
[2, 4, 5 | 1]

Pass 3: take 1
[2, 4, 5 | 1]
 1 is smaller than 5, shift 5 right
[2, 4, _, 5]
 1 is smaller than 4, shift 4 right
[2, _, 4, 5]
 1 is smaller than 2, shift 2 right
[_, 2, 4, 5]
 insert 1
[1, 2, 4, 5]
```

Why it works: everything left of the divider is already sorted. Each new value is
moved left until it lands in the correct position.

Big O:

```text
Best time:    O(n)        when the list is already sorted
Average time: O(n²)
Worst time:   O(n²)       when the list is reversed
Extra space:  O(n)        in this implementation because it copies the list
```

Merge sort:

```python
def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values.copy()
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

Picture:

```text
Start:
[5, 2, 4, 1]

Split phase:
Level 0: [5, 2, 4, 1]
Level 1: [5, 2]        [4, 1]
Level 2: [5] [2]       [4] [1]

Merge phase:
Merge [5] and [2]:
compare 5 vs 2 -> take 2
remaining 5    -> take 5
result         -> [2, 5]

Merge [4] and [1]:
compare 4 vs 1 -> take 1
remaining 4    -> take 4
result         -> [1, 4]

Merge [2, 5] and [1, 4]:
compare 2 vs 1 -> take 1
compare 2 vs 4 -> take 2
compare 5 vs 4 -> take 4
remaining 5    -> take 5
result         -> [1, 2, 4, 5]
```

Why it works: single-item lists are already sorted. Merge sort repeatedly merges
two sorted lists into one bigger sorted list.

Big O:

```text
Best time:    O(n log n)
Average time: O(n log n)
Worst time:   O(n log n)
Extra space:  O(n)        needs temporary lists while merging
```

Quick sort educational version:

```python
def quick_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values.copy()
    pivot = values[len(values) // 2]
    left = [value for value in values if value < pivot]
    middle = [value for value in values if value == pivot]
    right = [value for value in values if value > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

Picture:

```text
Start: [5, 2, 4, 1, 3]

Call 1:
pivot = 4
less than 4:    [2, 1, 3]
equal to 4:     [4]
greater than 4: [5]

Now sort the left side [2, 1, 3]:
pivot = 1
less than 1:    []
equal to 1:     [1]
greater than 1: [2, 3]

Now sort [2, 3]:
pivot = 3
less than 3:    [2]
equal to 3:     [3]
greater than 3: []

Build result back up:
[2] + [3]       -> [2, 3]
[1] + [2, 3]    -> [1, 2, 3]
[1, 2, 3] + [4] + [5] -> [1, 2, 3, 4, 5]
```

Why it works: after partitioning, every value on the left belongs before the
pivot, and every value on the right belongs after the pivot.

Big O:

```text
Best time:    O(n log n)
Average time: O(n log n)
Worst time:   O(n²)       bad pivots create very uneven splits
Extra space:  O(n)        this educational version builds left/middle/right lists
```

Other common sorting pictures:

Bubble sort:

```text
Start: [4, 2, 3, 1]

Pass 1:
compare 4 and 2 -> swap    [2, 4, 3, 1]
compare 4 and 3 -> swap    [2, 3, 4, 1]
compare 4 and 1 -> swap    [2, 3, 1, 4]
4 is now fixed at the end.

Pass 2:
compare 2 and 3 -> keep    [2, 3, 1, 4]
compare 3 and 1 -> swap    [2, 1, 3, 4]
3 is now fixed.

Pass 3:
compare 2 and 1 -> swap    [1, 2, 3, 4]
Sorted.
```

Big O:

```text
Best time:    O(n)        if optimized to stop when no swaps happen
Average time: O(n²)
Worst time:   O(n²)
Extra space:  O(1)        in-place
```

Selection sort:

```text
Start: [4, 2, 3, 1]

Pass 1:
unsorted part: [4, 2, 3, 1]
smallest value is 1
swap 1 with first unsorted value 4
[1 | 2, 3, 4]

Pass 2:
unsorted part: [2, 3, 4]
smallest value is 2
2 is already in the correct place
[1, 2 | 3, 4]

Pass 3:
unsorted part: [3, 4]
smallest value is 3
3 is already in the correct place
[1, 2, 3 | 4]

Sorted: [1, 2, 3, 4]
```

Big O:

```text
Best time:    O(n²)       still scans for the smallest each pass
Average time: O(n²)
Worst time:   O(n²)
Extra space:  O(1)        in-place
```

Heap sort:

```text
Start: [4, 2, 3, 1]

Build a max heap:
        4
      /   \
     2     3
    /
   1

Remove largest 4 and place it at the end:
heap left: [3, 2, 1]     sorted end: [4]

Remove largest 3:
heap left: [2, 1]        sorted end: [3, 4]

Remove largest 2:
heap left: [1]           sorted end: [2, 3, 4]

Remove largest 1:
heap left: []            sorted end: [1, 2, 3, 4]
```

Big O:

```text
Best time:    O(n log n)
Average time: O(n log n)
Worst time:   O(n log n)
Extra space:  O(1)        for classic in-place heap sort
```

Timsort:

```text
Real data often has sorted runs:
[1, 2, 5] [3, 4, 8] [6, 7]

Step 1: detect existing sorted runs
Run A: [1, 2, 5]
Run B: [3, 4, 8]
Run C: [6, 7]

Step 2: sort small messy pieces if needed
In this example, each run is already sorted.

Step 3: merge runs
Merge A and B:
[1, 2, 5] + [3, 4, 8] -> [1, 2, 3, 4, 5, 8]

Merge with C:
[1, 2, 3, 4, 5, 8] + [6, 7] -> [1, 2, 3, 4, 5, 6, 7, 8]
```

Big O:

```text
Best time:    O(n)        when existing runs are already ordered
Average time: O(n log n)
Worst time:   O(n log n)
Extra space:  O(n)        worst case
```

| Algorithm |       Best |    Average |      Worst |     Stable |
|-----------|-----------:|-----------:|-----------:|-----------:|
| Bubble    |       O(n) |      O(n²) |      O(n²) |        Yes |
| Selection |      O(n²) |      O(n²) |      O(n²) |         No |
| Insertion |       O(n) |      O(n²) |      O(n²) |        Yes |
| Merge     | O(n log n) | O(n log n) | O(n log n) |        Yes |
| Quick     | O(n log n) | O(n log n) |      O(n²) | Usually no |
| Heap      | O(n log n) | O(n log n) | O(n log n) |         No |
| Timsort   |       O(n) | O(n log n) | O(n log n) |        Yes |

**Interview answer:** Python's built-in sort is Timsort, stable, and optimized
for partially sorted real-world data. In interviews, explain whether your chosen
sort is stable, in-place, and what its worst-case runtime is.

## 33. Recursion And Backtracking

**Mental model:** Recursion solves a problem by solving a smaller version of the
same problem. Backtracking explores choices, then undoes a choice before trying
the next one.

Factorial:

```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)
```

Memoized Fibonacci:

```python
from functools import cache


@cache
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Subsets:

```python
def subsets(values: list[int]) -> list[list[int]]:
    result: list[list[int]] = []

    def backtrack(index: int, path: list[int]) -> None:
        if index == len(values):
            result.append(path.copy())
            return
        backtrack(index + 1, path)
        path.append(values[index])
        backtrack(index + 1, path)
        path.pop()

    backtrack(0, [])
    return result
```

Permutations:

```python
def permutations(values: list[int]) -> list[list[int]]:
    result: list[list[int]] = []

    def backtrack(path: list[int], remaining: list[int]) -> None:
        if not remaining:
            result.append(path.copy())
            return
        for index, value in enumerate(remaining):
            backtrack(path + [value], remaining[:index] + remaining[index + 1:])

    backtrack([], values)
    return result
```

**Common mistake:** Forgetting to restore state after recursive exploration.

**Interview answer:** A recursive solution needs a base case, progress toward the
base case, and a clear definition of what each call returns or contributes.
Backtracking usually has choose, explore, unchoose.

## 34. Common Coding-Interview Patterns

**Mental model:** Patterns are shortcuts for recognizing the shape of a problem.
They do not replace reasoning, but they help you choose the first useful data
structure.

| Pattern             | Recognize it by               | Main structure    |
|---------------------|-------------------------------|-------------------|
| Frequency map       | Count occurrences             | `Counter`, dict   |
| Hash-set lookup     | Need fast membership          | set               |
| Two pointers        | Sorted array or pair scan     | two indexes       |
| Sliding window      | Contiguous substring/subarray | two indexes + map |
| Fast/slow pointers  | Cycle or midpoint             | two pointers      |
| Prefix sums         | Range sums                    | list of sums      |
| Monotonic stack     | Next greater/smaller          | stack             |
| Heap                | Top-K or priority             | `heapq`           |
| Intervals           | Merge/overlap                 | sorting           |
| Topological sort    | Prerequisites                 | graph + indegree  |
| Union-find          | Connectivity groups           | parent/rank       |
| Dynamic programming | Overlapping subproblems       | table/cache       |

Sliding window example:

```python
def longest_unique_substring_length(text: str) -> int:
    seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, char in enumerate(text):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        best = max(best, right - left + 1)
    return best
```

Topological sort:

```python
from collections import deque


def can_finish_courses(count: int, prerequisites: list[tuple[int, int]]) -> bool:
    graph = {course: [] for course in range(count)}
    indegree = [0] * count
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        indegree[course] += 1
    queue = deque([course for course in range(count) if indegree[course] == 0])
    visited = 0
    while queue:
        course = queue.popleft()
        visited += 1
        for neighbor in graph[course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return visited == count
```

**Interview answer:** Name the pattern, explain why it fits, then state the data
structure and complexity. For example: "This is a sliding window because we need
the best contiguous substring while moving through the string once."

## 35. Common Coding-Interview Problems

**How to study these:** For each problem, say the brute-force approach first,
identify the repeated work, then introduce the data structure or pattern that
removes that repeated work.

Two Sum:

```python
def two_sum(values: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for index, value in enumerate(values):
        needed = target - value
        if needed in seen:
            return seen[needed], index
        seen[value] = index
    return None
```

Two Sum uses a hash map so each previous value can be checked in O(1) average
time instead of scanning all previous values again.

Three Sum:

```python
def three_sum(values: list[int]) -> list[tuple[int, int, int]]:
    values = sorted(values)
    result: list[tuple[int, int, int]] = []
    for index, value in enumerate(values):
        if index > 0 and value == values[index - 1]:
            continue
        left, right = index + 1, len(values) - 1
        while left < right:
            total = value + values[left] + values[right]
            if total == 0:
                result.append((value, values[left], values[right]))
                left += 1
                right -= 1
                while left < right and values[left] == values[left - 1]:
                    left += 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result
```

Three Sum sorts first so the inner search can use two pointers. Sorting costs
O(n log n), and the two-pointer scan across each fixed value gives O(n²) total
time.

Product except self:

```python
def product_except_self(values: list[int]) -> list[int]:
    result = [1] * len(values)
    prefix = 1
    for index, value in enumerate(values):
        result[index] = prefix
        prefix *= value
    suffix = 1
    for index in range(len(values) - 1, -1, -1):
        result[index] *= suffix
        suffix *= values[index]
    return result
```

Product Except Self uses prefix and suffix products to avoid division and handle
zeros correctly.

Number of islands:

```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(row: int, col: int) -> None:
        if row < 0 or col < 0 or row >= rows or col >= cols or grid[row][col] != "1":
            return
        grid[row][col] = "0"
        sink(row + 1, col)
        sink(row - 1, col)
        sink(row, col + 1)
        sink(row, col - 1)

    count = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1":
                count += 1
                sink(row, col)
    return count
```

Number of Islands treats the grid as a graph. Each land cell is a node connected
to neighboring land cells. DFS "sinks" one island so it is counted once.

Climbing stairs:

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    previous, current = 1, 2
    for _ in range(3, n + 1):
        previous, current = current, previous + current
    return current
```

Climbing Stairs is Fibonacci in disguise: ways to reach step `n` equals ways to
reach `n - 1` plus ways to reach `n - 2`.

pytest example:

```python
def test_two_sum() -> None:
    assert two_sum([2, 7, 11], 9) == (0, 1)


def test_product_except_self() -> None:
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
```

For each problem, explain brute force first, then optimize with a stronger data structure.

**Interview checklist:** Clarify input size, handle empty input, state complexity,
and test at least one normal case plus one edge case before calling the solution
done.

## 36. pytest Fundamentals

Test discovery finds files named `test_*.py` or `*_test.py` and functions named `test_*`.

**Mental model:** A test is executable documentation. It should show what the
code promises to do.

```python
def add(left: int, right: int) -> int:
    return left + right


def test_add() -> None:
    assert add(2, 3) == 5
```

Commands:

```bash
pytest
pytest -v
pytest tests/test_algorithms.py
pytest -k "binary_search"
pytest -m "slow"
```

**Testing note:** Plain `assert` is preferred in pytest because pytest rewrites assertions to show useful failure
details.

**Common mistake:** Testing only the happy path. Add edge cases, invalid input,
and regression cases for bugs you fixed.

## 37. pytest Fixtures

**Mental model:** A fixture is reusable setup. pytest injects it into a test by
matching the fixture name to a test parameter.

```python
from pathlib import Path
import pytest


@pytest.fixture
def sample_numbers() -> list[int]:
    return [1, 2, 3]


def test_sum(sample_numbers: list[int]) -> None:
    assert sum(sample_numbers) == 6


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    path = tmp_path / "data.txt"
    path.write_text("hello", encoding="utf-8")
    return path
```

Yield fixture:

```python
import pytest


@pytest.fixture
def resource():
    value = {"open": True}
    yield value
    value["open"] = False
```

Fixture scopes include `function`, `class`, `module`, `package`, and `session`.

**Decision rule:** Keep fixture scope as small as practical. Wider scopes can
speed up tests but make shared-state bugs easier to create.

## 38. pytest Parameterization And Markers

**Mental model:** Parameterization lets one test body cover many examples. This
keeps test logic in one place while making cases explicit.

```python
import sys
import pytest


@pytest.mark.parametrize(
    "value,expected",
    [(1, False), (2, True), (3, False)],
    ids=["one", "two", "three"],
)
def test_even(value: int, expected: bool) -> None:
    assert (value % 2 == 0) is expected


@pytest.mark.skip(reason="example skip")
def test_skipped() -> None:
    assert False


@pytest.mark.skipif(sys.platform == "win32", reason="not for Windows")
def test_non_windows() -> None:
    assert True


@pytest.mark.xfail(reason="known bug being fixed")
def test_expected_failure() -> None:
    assert False
```

**Testing note:** Use `xfail` for known, tracked defects. Do not use it to hide unexplained failures.

**Interview answer:** Use parameterization when behavior should be the same shape
across many inputs. Use markers to select, skip, or label tests intentionally.

## 39. Mocking And Patching

**Mental model:** Mock external behavior, not the logic you are trying to test.
Good mocks isolate slow, random, expensive, or network-dependent boundaries.

```python
from unittest.mock import Mock, patch


def send_message(client, text: str) -> bool:
    response = client.send(text)
    return response == "ok"


def test_send_message() -> None:
    client = Mock()
    client.send.return_value = "ok"
    assert send_message(client, "hello") is True
    client.send.assert_called_once_with("hello")
```

Patch where dependency is looked up:

```python
from unittest.mock import patch


def get_username() -> str:
    import os
    return os.getenv("USER", "unknown")


def test_get_username() -> None:
    with patch("os.getenv", return_value="Ada"):
        assert get_username() == "Ada"
```

**Testing note:** Prefer dependency injection over excessive patching. Do not mock simple value objects or the function
under test.

**Common mistake:** Patch where the dependency is imported or looked up by the
code under test, not necessarily where it was originally defined.

## 40. Testing Exceptions, Files, Classes, And APIs

**Mental model:** A good test checks both success and failure contracts. If your
function promises to reject invalid input, that rejection deserves a test.

```python
import os
from pathlib import Path
import pytest


def parse_positive(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise ValueError("must be positive")
    return value


def test_parse_positive_error() -> None:
    with pytest.raises(ValueError, match="positive"):
        parse_positive("-1")


def test_tmp_path(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("hello", encoding="utf-8")
    assert path.read_text(encoding="utf-8") == "hello"


def test_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    assert os.getenv("APP_ENV") == "test"
```

Capture output:

```python
def greet() -> None:
    print("hello")


def test_greet(capsys) -> None:
    greet()
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
```

**Testing note:** `tmp_path`, `monkeypatch`, `capsys`, and `pytest.raises` cover
many real-world tests without touching the user's machine or global environment.

## 41. Test Design And Quality

**Mental model:** Tests should fail for the reason a user would care about. Avoid
tests that simply repeat implementation details.

| Test type   | Purpose                              |
|-------------|--------------------------------------|
| Unit        | Small isolated behavior              |
| Integration | Multiple components working together |
| End-to-end  | User-level workflow                  |
| Regression  | Prevent a bug from returning         |
| Negative    | Invalid/error behavior               |

Arrange-Act-Assert:

```python
def test_discount() -> None:
    price = 100.0
    discounted = price * 0.9
    assert discounted == 90.0
```

**Testing note:** High coverage does not guarantee good tests. Tests must assert meaningful behavior and edge cases.

**Interview answer:** A strong test suite includes normal cases, boundaries,
invalid inputs, and regression tests. It avoids depending on test order or shared
mutable state.

## 42. Debugging

**Mental model:** Debugging is narrowing. First reproduce the problem, then make
the failing example smaller until the cause is visible.

```python
def divide(left: int, right: int) -> float:
    breakpoint()
    return left / right
```

Troubleshooting:

| Error                 | Check                                |
|-----------------------|--------------------------------------|
| `NameError`           | Spelling and scope                   |
| `TypeError`           | Types and function signature         |
| `ValueError`          | Input value assumptions              |
| `KeyError`            | Dict key existence                   |
| `IndexError`          | Sequence length                      |
| `AttributeError`      | Object type and attributes           |
| `ModuleNotFoundError` | Environment and package layout       |
| `RecursionError`      | Missing base case or excessive depth |

**Interview answer:** Reproduce, minimize, inspect state, fix root cause, add a regression test.

**Common mistake:** Changing several things at once can hide the real fix. Make
one hypothesis, test it, then move to the next.

## 43. Logging

**Mental model:** Logging is for future you. A useful log says what happened,
where it happened, and includes identifiers needed to trace the event.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


def process(order_id: int) -> None:
    try:
        logger.info("processing order_id=%s", order_id)
    except Exception:
        logger.exception("processing failed")
        raise
```

Test logs:

```python
import logging


def test_logging(caplog) -> None:
    logger = logging.getLogger("example")
    with caplog.at_level(logging.INFO):
        logger.info("ready")
    assert "ready" in caplog.text
```

**Production note:** Never log passwords, tokens, or sensitive personal data.

**Interview answer:** Use logging instead of `print` in applications because it
supports levels, formatting, destinations, and structured operational debugging.

## 44. Concurrency And Parallelism

**Mental model:** Concurrency is about managing many tasks in progress.
Parallelism is about doing work at the exact same time on multiple CPU cores.

| Workload                 | Tool                  |
|--------------------------|-----------------------|
| I/O-bound blocking calls | `ThreadPoolExecutor`  |
| CPU-bound work           | `ProcessPoolExecutor` |
| Many async I/O tasks     | `asyncio`             |
| Shared mutable state     | Locks or queues       |

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def square(value: int) -> int:
    return value * value


with ThreadPoolExecutor(max_workers=4) as executor:
    thread_results = list(executor.map(square, [1, 2, 3]))

with ProcessPoolExecutor() as executor:
    process_results = list(executor.map(square, [1, 2, 3]))
```

**Interview answer:** Concurrency is overlapping tasks. Parallelism is simultaneous execution. The GIL limits CPU-bound
Python threads but not processes.

**Decision rule:** Use threads for blocking I/O, processes for CPU-heavy pure
Python work, and async when you have many cooperative I/O tasks and async-capable
libraries.

## 45. Async Programming

**Mental model:** Async code runs on an event loop. A coroutine gives control
back to the loop at `await`, allowing other tasks to make progress.

```python
import asyncio


async def fetch(identifier: int) -> str:
    await asyncio.sleep(0.1)
    return f"item-{identifier}"


async def main() -> None:
    results = await asyncio.gather(fetch(1), fetch(2))
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

Timeout:

```python
import asyncio


async def work() -> str:
    await asyncio.sleep(0.1)
    return "done"


async def run_with_timeout() -> str:
    return await asyncio.wait_for(work(), timeout=1.0)
```

**Common mistake:** Calling blocking functions inside async code blocks the event loop.

**Interview answer:** Async improves throughput for many I/O-bound tasks. It does
not make CPU-heavy Python code faster by itself.

## 46. Performance And Profiling

**Mental model:** Measure before optimizing. Guessing often improves code that
was not the bottleneck.

```python
from functools import lru_cache
from timeit import timeit
import cProfile
import pstats
import tracemalloc


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(timeit("sum(range(1000))", number=1000))
```

Profile command:

```bash
python -m cProfile -s cumulative script.py
```

Memory example:

```python
import tracemalloc

tracemalloc.start()
values = [number for number in range(1000)]
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
```

**Performance note:** Algorithm choice usually matters more than micro-optimizations.

**Interview answer:** Start with complexity, then profile real workloads, then
optimize the hot path. Keep benchmark inputs realistic and add regression tests
so performance fixes do not break correctness.

## 47. Clean Python And Design Principles

**Mental model:** Clean code is code another person can safely change. Names,
small functions, explicit inputs, and tests matter more than cleverness.

| Principle             | Practice                                        |
|-----------------------|-------------------------------------------------|
| DRY                   | Remove meaningful duplication                   |
| KISS                  | Prefer simple functions                         |
| YAGNI                 | Do not overbuild                                |
| SOLID                 | Keep responsibilities focused                   |
| Composition           | Inject dependencies instead of hard-coding them |
| Defensive programming | Validate boundaries                             |

```python
def total_active_scores(records: list[dict[str, object]]) -> int:
    total = 0
    for record in records:
        if record.get("active") is True:
            total += int(record.get("score", 0))
    return total
```

**Production note:** Clean code is testable, observable, explicit, and boring in the best possible way.

**Common mistake:** Over-abstracting too early. Add an abstraction when it removes
real duplication or clarifies a stable concept, not because two lines look
similar today.

## 48. Common Python Design Patterns

**Mental model:** A pattern is a reusable solution shape. Python often expresses
patterns with plain functions, protocols, context managers, decorators, or small
classes.

Factory:

```python
class JsonExporter:
    def export(self) -> str:
        return "{}"


class CsvExporter:
    def export(self) -> str:
        return ""


def create_exporter(kind: str) -> JsonExporter | CsvExporter:
    if kind == "json":
        return JsonExporter()
    if kind == "csv":
        return CsvExporter()
    raise ValueError(f"unknown kind: {kind}")
```

Strategy:

```python
from collections.abc import Callable


def apply_discount(price: float, strategy: Callable[[float], float]) -> float:
    return strategy(price)
```

**Interview answer:** Patterns are tools, not trophies. Prefer simple Python unless a pattern removes real complexity.

**Decision rule:** If a simple function solves the problem, use a function. Reach
for a class or formal pattern only when state, interchangeable behavior, or
lifecycle management is becoming hard to manage.

## 49. Common Python Mistakes

**How to use this section:** Each mistake is a signal to slow down and ask,
"What object is being shared? What is being mutated? What is Python comparing?"

| Mistake                              | Correct approach                                    |
|--------------------------------------|-----------------------------------------------------|
| Mutable defaults                     | Use `None` sentinel                                 |
| Modifying collection while iterating | Build a new collection                              |
| `is` vs `==`                         | Use `is` only for identity checks like `None`       |
| Shadowing built-ins                  | Avoid names like `list`, `dict`, `file`             |
| Broad ignored exceptions             | Catch specific exceptions                           |
| Late-binding closures                | Bind values at definition time                      |
| Shallow copy surprises               | Use `deepcopy` when nested data must be independent |
| Direct float equality                | Use `math.isclose`                                  |
| Threads for CPU-heavy work           | Use processes or native/vectorized libraries        |
| Blocking async code                  | Use async clients or executors                      |

Late-binding fix:

```python
functions = [lambda value=value: value for value in range(3)]
print([function() for function in functions])
```

**Interview answer:** Many Python bugs come from misunderstanding names,
mutability, scope, and iteration. Explain the underlying rule, not just the fix.

## 50. Frequently Used Python Snippets

Use these snippets as starting points, not magic spells. In an interview, explain
why the snippet fits the problem before writing it.

**Why this matters:** Snippets reduce typing and recall pressure, but they should
not replace reasoning. Before using one, identify the input, output, failure
cases, and the data structure that makes it appropriate.

```python
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import json
import logging
import re


def read_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected JSON object")
    return data


def group_by_key(records: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records:
        groups[record[key]].append(record)
    return dict(groups)


@dataclass
class User:
    user_id: int
    name: str


logger = logging.getLogger(__name__)
numbers = re.findall(r"\d+", "a1 b2")
counts = Counter("banana")
```

| Snippet                       | Why it is useful                                                      |
|-------------------------------|-----------------------------------------------------------------------|
| `read_json`                   | Validates file data before the rest of the program trusts it.         |
| `group_by_key`                | Uses `defaultdict` to group records without repetitive key checks.    |
| `@dataclass`                  | Creates a small named data object with less boilerplate.              |
| `logging.getLogger(__name__)` | Gives each module a logger that can be configured by the application. |
| `re.findall`                  | Extracts repeated text patterns such as numbers, IDs, or tokens.      |
| `Counter`                     | Turns frequency counting into one clear line.                         |

pytest parameterization:

Why this snippet exists: parameterization turns several nearly identical tests
into one test definition with multiple cases. That makes edge cases easy to add
without duplicating test logic.

```python
import pytest


@pytest.mark.parametrize("value,expected", [(1, False), (2, True)])
def test_even(value: int, expected: bool) -> None:
    assert (value % 2 == 0) is expected
```

## 51. Python Interview Questions And Answers

Use the table for quick review. In a real interview, expand each concise answer
with one example and one trade-off.

**Why this matters:** Short answers prove vocabulary. Expanded answers prove
understanding. A strong candidate can define a term, show where it appears in
code, and explain the trade-off.

| Level        | Question                        | Concise answer                                                |
|--------------|---------------------------------|---------------------------------------------------------------|
| Beginner     | List vs tuple?                  | Lists are mutable; tuples are immutable.                      |
| Beginner     | `is` vs `==`?                   | `is` checks identity; `==` checks equality.                   |
| Beginner     | What is `None`?                 | A singleton object representing no value.                     |
| Intermediate | What is a generator?            | A lazy iterator created by `yield` or a generator expression. |
| Intermediate | What is a decorator?            | A callable that wraps another callable.                       |
| Intermediate | What does a context manager do? | It guarantees setup and cleanup around `with`.                |
| Advanced     | What is the GIL?                | CPython lock around bytecode execution.                       |
| Advanced     | What is MRO?                    | The order Python uses to resolve attributes in inheritance.   |
| Advanced     | What is a descriptor?           | Object controlling attribute access with descriptor methods.  |

**Common incorrect answer:** "Python is never compiled." Better: source is compiled to bytecode, then executed by the
VM.

**Interview habit:** After a short definition, add a practical consequence. For
example: "A generator is lazy, so it saves memory, but it is consumed after one
pass."

## 52. Data-Structure And Algorithm Interview Questions

For each answer, be ready to draw the state change for a small input. Interviewers
often care more about reasoning than memorized labels.

| Topic       | Question                      | Strong answer                                          |
|-------------|-------------------------------|--------------------------------------------------------|
| Arrays      | Why use two pointers?         | To scan from both ends or maintain a window in O(n).   |
| Hash tables | Why are dict lookups fast?    | Hashing maps keys to table positions, average O(1).    |
| Stacks      | When use a stack?             | Matching parentheses, DFS, undo, monotonic problems.   |
| Queues      | When use BFS?                 | Shortest path in unweighted graphs or level traversal. |
| Heaps       | Top-K complexity?             | O(n log k) with a size-k heap.                         |
| Tries       | Prefix search complexity?     | O(k), where k is prefix length.                        |
| Graphs      | DFS vs BFS?                   | DFS explores depth; BFS explores levels.               |
| DP          | When use dynamic programming? | Overlapping subproblems plus optimal substructure.     |

**Interview habit:** State time and space complexity after the algorithm, and
include what `n`, `k`, `V`, or `E` means.

## 53. pytest Interview Questions

pytest interview answers should connect testing tools to risk reduction: clearer
failures, repeatable setup, edge cases, and regression protection.

| Question                        | Interview answer                                                                  |
|---------------------------------|-----------------------------------------------------------------------------------|
| How does pytest discover tests? | It finds `test_*.py` files and `test_*` functions/classes by convention.          |
| What is a fixture?              | A reusable setup object injected into tests by name.                              |
| What is `conftest.py`?          | A place for shared fixtures and pytest hooks.                                     |
| Why parameterize?               | To run the same test logic over many cases.                                       |
| What is monkeypatch for?        | Safely changing attributes, dicts, environment variables, or paths during a test. |
| What should not be mocked?      | The function under test, simple data objects, or behavior better tested directly. |
| Why can coverage mislead?       | Lines can execute without meaningful assertions.                                  |

**Interview habit:** When asked about testing, include one example of a bad test
and how you would improve it.

## 54. Scenario-Based Interview Preparation

Scenario questions test diagnosis. A strong answer gives an immediate mitigation,
a root-cause investigation plan, and a prevention step.

| Scenario                             | Strong response                                                              |
|--------------------------------------|------------------------------------------------------------------------------|
| Program slows as data grows          | Identify complexity, profile, replace O(n²) patterns, add benchmarks.        |
| Memory keeps increasing              | Use `tracemalloc`, check caches/globals/open resources/reference cycles.     |
| Large file cannot fit memory         | Stream line by line or chunk data.                                           |
| Dict key raises `TypeError`          | Key is unhashable, such as list or dict. Use tuple/frozenset or a stable ID. |
| List modification skips elements     | Do not mutate during iteration; build a filtered list.                       |
| Mock not intercepting call           | Patch where the dependency is looked up.                                     |
| Async app is blocked                 | Locate blocking calls in event loop. Use async client or executor.           |
| Threads produce inconsistent results | Shared state race; use locks, queues, or immutable messages.                 |
| Recursion limit exceeded             | Check base case, convert to iterative, or use explicit stack.                |
| Tests pass alone but fail together   | Shared state, order dependency, time, temp files, or global mocks.           |

**Answer pattern:** "First I would reproduce it, then isolate the smallest case,
then inspect the likely state/resource boundary, then add a regression test after
the fix."

## 55. Runnable Practice Projects

Each project below is intentionally small but complete enough to build and test.

**How to practice:** Build each project in small commits. Write one failing test,
make it pass, then refactor. Keep a short README explaining how to run it.

### Project 1: Command-Line Contact Manager

Structure:

```text
contact_manager/
├── contacts.py
└── test_contacts.py
```

Source:

```python
import json
from pathlib import Path


def load_contacts(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contacts must be a JSON object")
    return {str(key): str(value) for key, value in data.items()}


def save_contacts(path: Path, contacts: dict[str, str]) -> None:
    path.write_text(json.dumps(contacts, indent=2), encoding="utf-8")


def add_contact(contacts: dict[str, str], name: str, email: str) -> dict[str, str]:
    updated = contacts.copy()
    updated[name] = email
    return updated
```

Tests:

```python
from pathlib import Path


def test_add_contact() -> None:
    assert add_contact({}, "Ada", "ada@example.com") == {"Ada": "ada@example.com"}


def test_save_and_load(tmp_path: Path) -> None:
    path = tmp_path / "contacts.json"
    save_contacts(path, {"Ada": "ada@example.com"})
    assert load_contacts(path) == {"Ada": "ada@example.com"}
```

Run:

```bash
pytest
```

### Project 2: Log-File Analyzer

```python
from collections import Counter
from pathlib import Path
from collections.abc import Iterator


def log_levels(path: Path) -> Iterator[str]:
    with path.open(encoding="utf-8") as file_obj:
        for line in file_obj:
            if "ERROR" in line:
                yield "ERROR"
            elif "WARN" in line:
                yield "WARN"
            elif "INFO" in line:
                yield "INFO"


def summarize_logs(path: Path) -> Counter[str]:
    return Counter(log_levels(path))
```

```python
from pathlib import Path


def test_summarize_logs(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    path.write_text("INFO start\nERROR fail\nERROR fail2\n", encoding="utf-8")
    assert summarize_logs(path)["ERROR"] == 2
```

### Project 3: Data-Structure Library

Implement `Stack`, `Queue`, linked list reversal, heap helper, and graph BFS from sections 29 and 31. Test each
operation with empty, one-item, and many-item inputs.

Learning goal: explain each data structure by its operations and complexity, not
by its implementation details alone.

### Project 4: Algorithm-Practice Package

Implement binary search, merge sort, two sum, sliding window, top-K frequent values, tree traversal, graph traversal,
and dynamic programming problems. Use `pytest.mark.parametrize` for edge cases.

Learning goal: practice recognizing problem patterns and stating brute force,
optimized approach, time complexity, and space complexity.

### Project 5: Concurrent File Processor

Use `ThreadPoolExecutor` for I/O-bound file reads, log failures, and compare runtime with sequential processing. Add
tests with `tmp_path`.

Learning goal: understand why threads help blocking I/O, how to collect results,
and how to report partial failures safely.

## 56. Quick-Revision Sheets

Use this section the day before an interview. If any line feels unfamiliar, jump
back to the full section and run the example.

**Why this matters:** Quick revision should trigger memory, not replace learning.
If a quick note feels vague, that is a signal to practice the full example again.

Core syntax:

```python
name = "Ada"
values = [1, 2, 3]
result = [value * 2 for value in values if value > 1]
```

Collections:

```text
list: ordered, mutable, duplicates
tuple: ordered, immutable, duplicates
set: unordered, mutable, unique
dict: insertion-ordered mapping
deque: fast both-end operations
```

Complexities:

```text
dict/set lookup: O(1) average
list membership: O(n)
sort: O(n log n)
binary search: O(log n)
BFS/DFS: O(V + E)
```

pytest:

```bash
pytest
pytest -v
pytest -k "name"
pytest --cov=src
```

Top interview traps:

1. Mutable default arguments.
2. `is` vs `==`.
3. Modifying a list while iterating.
4. Forgetting `return`.
5. Overusing broad exceptions.
6. Using list membership for repeated lookups.
7. Blocking inside async code.
8. Shallow-copy surprises.
9. Timezone-naive datetimes.
10. Over-mocking tests.
