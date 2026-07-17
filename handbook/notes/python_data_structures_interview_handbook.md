# Python Data Structures Interview Handbook

This standalone handbook is a practical Python tutorial, data-structures and algorithms reference, pytest guide, and interview-preparation workbook. It uses Python 3.11+ style and keeps examples concise, runnable, and suitable for daily reference.

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

**Intermediate:** Use sections 20-35 to strengthen OOP, typing, data structures, complexity, algorithms, and interview patterns.

**Advanced:** Use sections 36-56 for pytest, mocking, concurrency, async, profiling, design, scenario interviews, and quick revision.

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

```bash
python3 -m venv .venv
source .venv/bin/activate
which python
python --version
python -m pip --version
```

Install development tools:

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

**Beginner:** A module is a `.py` file. A package is a directory of modules. `__init__.py` marks a directory as a regular package and can expose package-level imports.

**Intermediate:** The `src` layout helps tests import installed package code instead of accidentally importing files from the working directory.

**Production note:** Do not make application logic depend on the current working directory. Pass paths explicitly or derive them from configuration.

## 4. Python Syntax And Execution Model

Python programs are made of statements and expressions. Expressions produce values; statements perform actions.

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

**Interview answer:** Python is dynamically typed because names can refer to different object types over time. It is strongly typed because it does not silently combine incompatible types like `"x" + 1`.

**Common mistake:** Use `is None`, but use `==` for normal value comparison.

## 5. Built-In Python Data Types

| Type | Example | Mutable | Use |
|---|---|---:|---|
| `int` | `42` | No | Whole numbers |
| `float` | `3.14` | No | Approximate decimal values |
| `complex` | `1 + 2j` | No | Scientific/math work |
| `bool` | `True` | No | Conditions |
| `str` | `"text"` | No | Unicode text |
| `bytes` | `b"abc"` | No | Immutable binary data |
| `bytearray` | `bytearray(b"abc")` | Yes | Mutable binary data |
| `None` | `None` | No | Absence of value |

```python
value = 42
print(type(value))
print(isinstance(value, int))
```

**Interview answer:** Prefer `isinstance(value, expected_type)` when checking type relationships because it respects inheritance and can check multiple allowed types.

Floating-point caution:

```python
import math

print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
```

## 6. Strings

Strings are immutable Unicode sequences.

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

Build large strings efficiently:

```python
parts = ["row", ":", "42"]
line = "".join(parts)
```

**Performance note:** Repeated `result += piece` in a loop may allocate many intermediate strings. Use `"".join(parts)` when collecting many pieces.

## 7. Lists

Lists are mutable ordered arrays of object references.

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

| Operation | Complexity |
|---|---:|
| Index lookup | O(1) |
| Membership | O(n) |
| Append | O(1) amortized |
| Insert/delete middle | O(n) |
| Pop end | O(1) |
| Sorting | O(n log n) |
| Slicing length `k` | O(k) |

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

## 8. Tuples

Tuples are immutable ordered containers.

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

## 9. Sets And Frozensets

Sets store unique hashable values and support fast average membership checks.

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

## 10. Dictionaries

Dictionaries map hashable keys to values and preserve insertion order in modern Python.

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

**Interview answer:** Dict lookup is average O(1). Worst case can degrade if many keys collide, but Python's implementation is engineered to make this rare.

## 11. Comparing Core Python Collections

| Collection | Ordered | Mutable | Duplicates | Lookup | Best use |
|---|---:|---:|---:|---:|---|
| `list` | Yes | Yes | Yes | O(n) membership | Ordered mutable sequence |
| `tuple` | Yes | No | Yes | O(n) membership | Fixed records |
| `set` | No | Yes | No | O(1) avg | Unique values |
| `frozenset` | No | No | No | O(1) avg | Immutable set key |
| `dict` | Yes | Yes | Keys no | O(1) avg key | Key-value lookup |
| `deque` | Yes | Yes | Yes | O(n) membership | Fast append/pop both ends |

**Interview answer:** Use the structure that matches the operation you need most often.

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

## 13. Loops And Iteration

Direct iteration is usually clearer than index iteration:

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

## 14. Functions

```python
def add(left: int, right: int) -> int:
    """Return the sum of two integers."""
    return left + right
```

Argument forms:

```python
def describe(name: str, /, role: str = "user", *, active: bool = True) -> str:
    return f"{name}:{role}:{active}"
```

Mutable default problem:

```python
def add_item_bad(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items
```

Correct:

```python
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

Closure:

```python
def multiplier(factor: int):
    def multiply(value: int) -> int:
        return value * factor
    return multiply
```

**Interview answer:** Python passes object references by assignment. Mutating a passed mutable object affects the caller's object.

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

**Interview answer:** A list comprehension stores all results. A generator expression produces values lazily and can use much less memory.

**Common mistake:** If the comprehension needs multiple nested conditions, use a normal loop for readability.

## 16. Lambda Functions And Functional Tools

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
```

**Interview answer:** Use lambda for tiny throwaway functions, commonly with `key=`, but prefer named functions for testable business logic.

## 17. Modules, Packages, And Imports

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

| Problem | Likely cause |
|---|---|
| `ModuleNotFoundError` | Wrong environment, missing install, wrong working directory |
| Relative import error | Running a file directly instead of as a module |
| Circular import | Two modules import each other at import time |
| `json.py` shadowing | File named after a standard-library module |

## 18. File Handling And Serialization

Use `pathlib` and context managers.

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

## 19. Exception Handling

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

Custom exception:

```python
class InvalidInputError(ValueError):
    """Raised when input validation fails."""
```

## 20. Object-Oriented Programming

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

| Decorator | Receives | Use |
|---|---|---|
| `@staticmethod` | Neither `self` nor `cls` | Related utility |
| `@classmethod` | `cls` | Alternate constructor or class-level behavior |
| `@property` | `self` | Computed attribute |

**Interview answer:** Prefer composition when an object "has a" dependency; use inheritance for true "is a" relationships.

## 21. Dataclasses And Modern Python Models

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

**Interview answer:** Dataclasses are best for Python objects with named fields and light behavior. `TypedDict` describes dictionary-shaped data for type checkers.

## 22. Iterables, Iterators, And Generators

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

**Interview answer:** `yield` turns a function into a generator. It returns values one at a time and preserves state between iterations.

## 23. Decorators

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

## 24. Context Managers

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

## 25. Type Hints And Static Analysis

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

**Interview answer:** Type hints do not normally enforce runtime behavior. Static tools use annotations to catch errors earlier and improve maintainability.

## 26. Python Memory Model And Copying

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

**Interview answer:** Assignment creates another reference to the same object. A shallow copy copies the outer container; a deep copy recursively copies nested objects.

## 27. Python Internals

```python
import dis


def add(left: int, right: int) -> int:
    return left + right


dis.dis(add)
```

**Interview answer:** CPython compiles source code to bytecode and runs it on the Python virtual machine. The GIL allows one thread at a time to execute Python bytecode in one process.

LEGB name lookup:

1. Local
2. Enclosing
3. Global
4. Built-in

Descriptors define `__get__`, `__set__`, or `__delete__` and power features like properties and methods.

## 28. Standard-Library Collections And Utilities

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

**Interview answer:** `Counter`, `defaultdict`, `deque`, `heapq`, and `bisect` often turn long interview solutions into clean short ones.

## 29. Abstract Data Types And Implementations

Educational implementations help interviews. In production, prefer built-ins unless you need custom behavior.

Stack and queue:

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

| Structure | Main operations |
|---|---|
| Stack | push/pop O(1) |
| Queue/deque | append/popleft O(1) |
| Linked list | insert after node O(1), search O(n) |
| Hash table | average lookup/insert/delete O(1) |
| Heap | push/pop O(log n) |
| Trie | insert/search O(k), k = word length |
| Union-find | near O(1) amortized with path compression |

## 30. Algorithm Complexity

| Class | Example |
|---|---|
| O(1) | Indexing a list |
| O(log n) | Binary search |
| O(n) | Linear scan |
| O(n log n) | Efficient comparison sorting |
| O(n²) | All pairs |
| O(2ⁿ) | Subsets |
| O(n!) | Permutations |

```python
def linear_sum(values: list[int]) -> int:
    total = 0
    for value in values:
        total += value
    return total
```

**Interview answer:** Big O describes how runtime or memory grows as input grows. It ignores constants and lower-order terms.

Recursion stack space counts as space complexity.

## 31. Searching Algorithms

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

## 32. Sorting Algorithms

Built-in sorting:

```python
values = [3, 1, 2]
new_values = sorted(values)
values.sort()
```

`sorted()` returns a new list. `.sort()` mutates the list and returns `None`.

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

| Algorithm | Best | Average | Worst | Stable |
|---|---:|---:|---:|---:|
| Bubble | O(n) | O(n²) | O(n²) | Yes |
| Selection | O(n²) | O(n²) | O(n²) | No |
| Insertion | O(n) | O(n²) | O(n²) | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | Yes |
| Quick | O(n log n) | O(n log n) | O(n²) | Usually no |
| Heap | O(n log n) | O(n log n) | O(n log n) | No |
| Timsort | O(n) | O(n log n) | O(n log n) | Yes |

## 33. Recursion And Backtracking

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

## 34. Common Coding-Interview Patterns

| Pattern | Recognize it by | Main structure |
|---|---|---|
| Frequency map | Count occurrences | `Counter`, dict |
| Hash-set lookup | Need fast membership | set |
| Two pointers | Sorted array or pair scan | two indexes |
| Sliding window | Contiguous substring/subarray | two indexes + map |
| Fast/slow pointers | Cycle or midpoint | two pointers |
| Prefix sums | Range sums | list of sums |
| Monotonic stack | Next greater/smaller | stack |
| Heap | Top-K or priority | `heapq` |
| Intervals | Merge/overlap | sorting |
| Topological sort | Prerequisites | graph + indegree |
| Union-find | Connectivity groups | parent/rank |
| Dynamic programming | Overlapping subproblems | table/cache |

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

## 35. Common Coding-Interview Problems

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

pytest example:

```python
def test_two_sum() -> None:
    assert two_sum([2, 7, 11], 9) == (0, 1)


def test_product_except_self() -> None:
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
```

For each problem, explain brute force first, then optimize with a stronger data structure.

## 36. pytest Fundamentals

Test discovery finds files named `test_*.py` or `*_test.py` and functions named `test_*`.

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

**Testing note:** Plain `assert` is preferred in pytest because pytest rewrites assertions to show useful failure details.

## 37. pytest Fixtures

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

## 38. pytest Parameterization And Markers

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

## 39. Mocking And Patching

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

**Testing note:** Prefer dependency injection over excessive patching. Do not mock simple value objects or the function under test.

## 40. Testing Exceptions, Files, Classes, And APIs

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

## 41. Test Design And Quality

| Test type | Purpose |
|---|---|
| Unit | Small isolated behavior |
| Integration | Multiple components working together |
| End-to-end | User-level workflow |
| Regression | Prevent a bug from returning |
| Negative | Invalid/error behavior |

Arrange-Act-Assert:

```python
def test_discount() -> None:
    price = 100.0
    discounted = price * 0.9
    assert discounted == 90.0
```

**Testing note:** High coverage does not guarantee good tests. Tests must assert meaningful behavior and edge cases.

## 42. Debugging

```python
def divide(left: int, right: int) -> float:
    breakpoint()
    return left / right
```

Troubleshooting:

| Error | Check |
|---|---|
| `NameError` | Spelling and scope |
| `TypeError` | Types and function signature |
| `ValueError` | Input value assumptions |
| `KeyError` | Dict key existence |
| `IndexError` | Sequence length |
| `AttributeError` | Object type and attributes |
| `ModuleNotFoundError` | Environment and package layout |
| `RecursionError` | Missing base case or excessive depth |

**Interview answer:** Reproduce, minimize, inspect state, fix root cause, add a regression test.

## 43. Logging

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

## 44. Concurrency And Parallelism

| Workload | Tool |
|---|---|
| I/O-bound blocking calls | `ThreadPoolExecutor` |
| CPU-bound work | `ProcessPoolExecutor` |
| Many async I/O tasks | `asyncio` |
| Shared mutable state | Locks or queues |

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def square(value: int) -> int:
    return value * value


with ThreadPoolExecutor(max_workers=4) as executor:
    thread_results = list(executor.map(square, [1, 2, 3]))

with ProcessPoolExecutor() as executor:
    process_results = list(executor.map(square, [1, 2, 3]))
```

**Interview answer:** Concurrency is overlapping tasks. Parallelism is simultaneous execution. The GIL limits CPU-bound Python threads but not processes.

## 45. Async Programming

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

## 46. Performance And Profiling

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

## 47. Clean Python And Design Principles

| Principle | Practice |
|---|---|
| DRY | Remove meaningful duplication |
| KISS | Prefer simple functions |
| YAGNI | Do not overbuild |
| SOLID | Keep responsibilities focused |
| Composition | Inject dependencies instead of hard-coding them |
| Defensive programming | Validate boundaries |

```python
def total_active_scores(records: list[dict[str, object]]) -> int:
    total = 0
    for record in records:
        if record.get("active") is True:
            total += int(record.get("score", 0))
    return total
```

**Production note:** Clean code is testable, observable, explicit, and boring in the best possible way.

## 48. Common Python Design Patterns

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

## 49. Common Python Mistakes

| Mistake | Correct approach |
|---|---|
| Mutable defaults | Use `None` sentinel |
| Modifying collection while iterating | Build a new collection |
| `is` vs `==` | Use `is` only for identity checks like `None` |
| Shadowing built-ins | Avoid names like `list`, `dict`, `file` |
| Broad ignored exceptions | Catch specific exceptions |
| Late-binding closures | Bind values at definition time |
| Shallow copy surprises | Use `deepcopy` when nested data must be independent |
| Direct float equality | Use `math.isclose` |
| Threads for CPU-heavy work | Use processes or native/vectorized libraries |
| Blocking async code | Use async clients or executors |

Late-binding fix:

```python
functions = [lambda value=value: value for value in range(3)]
print([function() for function in functions])
```

## 50. Frequently Used Python Snippets

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

pytest parameterization:

```python
import pytest


@pytest.mark.parametrize("value,expected", [(1, False), (2, True)])
def test_even(value: int, expected: bool) -> None:
    assert (value % 2 == 0) is expected
```

## 51. Python Interview Questions And Answers

| Level | Question | Concise answer |
|---|---|---|
| Beginner | List vs tuple? | Lists are mutable; tuples are immutable. |
| Beginner | `is` vs `==`? | `is` checks identity; `==` checks equality. |
| Beginner | What is `None`? | A singleton object representing no value. |
| Intermediate | What is a generator? | A lazy iterator created by `yield` or a generator expression. |
| Intermediate | What is a decorator? | A callable that wraps another callable. |
| Intermediate | What does a context manager do? | It guarantees setup and cleanup around `with`. |
| Advanced | What is the GIL? | CPython lock around bytecode execution. |
| Advanced | What is MRO? | The order Python uses to resolve attributes in inheritance. |
| Advanced | What is a descriptor? | Object controlling attribute access with descriptor methods. |

**Common incorrect answer:** "Python is never compiled." Better: source is compiled to bytecode, then executed by the VM.

## 52. Data-Structure And Algorithm Interview Questions

| Topic | Question | Strong answer |
|---|---|---|
| Arrays | Why use two pointers? | To scan from both ends or maintain a window in O(n). |
| Hash tables | Why are dict lookups fast? | Hashing maps keys to table positions, average O(1). |
| Stacks | When use a stack? | Matching parentheses, DFS, undo, monotonic problems. |
| Queues | When use BFS? | Shortest path in unweighted graphs or level traversal. |
| Heaps | Top-K complexity? | O(n log k) with a size-k heap. |
| Tries | Prefix search complexity? | O(k), where k is prefix length. |
| Graphs | DFS vs BFS? | DFS explores depth; BFS explores levels. |
| DP | When use dynamic programming? | Overlapping subproblems plus optimal substructure. |

## 53. pytest Interview Questions

| Question | Interview answer |
|---|---|
| How does pytest discover tests? | It finds `test_*.py` files and `test_*` functions/classes by convention. |
| What is a fixture? | A reusable setup object injected into tests by name. |
| What is `conftest.py`? | A place for shared fixtures and pytest hooks. |
| Why parameterize? | To run the same test logic over many cases. |
| What is monkeypatch for? | Safely changing attributes, dicts, environment variables, or paths during a test. |
| What should not be mocked? | The function under test, simple data objects, or behavior better tested directly. |
| Why can coverage mislead? | Lines can execute without meaningful assertions. |

## 54. Scenario-Based Interview Preparation

| Scenario | Strong response |
|---|---|
| Program slows as data grows | Identify complexity, profile, replace O(n²) patterns, add benchmarks. |
| Memory keeps increasing | Use `tracemalloc`, check caches/globals/open resources/reference cycles. |
| Large file cannot fit memory | Stream line by line or chunk data. |
| Dict key raises `TypeError` | Key is unhashable, such as list or dict. Use tuple/frozenset or a stable ID. |
| List modification skips elements | Do not mutate during iteration; build a filtered list. |
| Mock not intercepting call | Patch where the dependency is looked up. |
| Async app is blocked | Locate blocking calls in event loop. Use async client or executor. |
| Threads produce inconsistent results | Shared state race; use locks, queues, or immutable messages. |
| Recursion limit exceeded | Check base case, convert to iterative, or use explicit stack. |
| Tests pass alone but fail together | Shared state, order dependency, time, temp files, or global mocks. |

## 55. Runnable Practice Projects

Each project below is intentionally small but complete enough to build and test.

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

Implement `Stack`, `Queue`, linked list reversal, heap helper, and graph BFS from sections 29 and 31. Test each operation with empty, one-item, and many-item inputs.

### Project 4: Algorithm-Practice Package

Implement binary search, merge sort, two sum, sliding window, top-K frequent values, tree traversal, graph traversal, and dynamic programming problems. Use `pytest.mark.parametrize` for edge cases.

### Project 5: Concurrent File Processor

Use `ThreadPoolExecutor` for I/O-bound file reads, log failures, and compare runtime with sequential processing. Add tests with `tmp_path`.

## 56. Quick-Revision Sheets

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

