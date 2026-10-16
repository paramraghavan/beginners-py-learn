# 10 Python Features You Should Be Using

Inspired by the ArjanCodes video linked below, this guide explains ten useful Python features with small examples.
**Requires Python 3.10 or later.**

## 1. Cache Repeated Calculations with `@cache`

`functools.cache` remembers a function's return value for each set of arguments. Calling it again with the same arguments reuses that value.

```python
from functools import cache


@cache
def square(number: int) -> int:
    print(f"Calculating {number} squared")
    return number * number


print(square(4))
print(square(4))
print(square(5))
```

Output:

```text
Calculating 4 squared
16
16
Calculating 5 squared
25
```

The second `square(4)` skips the function body. Squaring is cheap; this example makes the reuse visible. Caching is more useful when a calculation is expensive and its result depends only on its arguments.

**Watch out:**

- `@cache` has no size limit. Use `@lru_cache(maxsize=128)` from `functools` to limit the number of stored calls.
- Cached file contents or API results can become stale. The cache does not detect external changes or expire entries automatically.
- Use `square.cache_clear()` to discard its cached results.

### Notes: data types and custom objects

The same rules apply to `@cache` and `@lru_cache`:

| What you pass or return | Rule |
| --- | --- |
| Arguments | Must be hashable: `int`, `float`, `bool`, `str`, `bytes`, and `None` work. |
| Tuple or frozenset arguments | Work if all their contents are hashable. |
| List, dictionary, or set arguments | Not hashable; passing them raises `TypeError`. |
| Return values | Can be any type, including a list or dictionary. Cached calls reuse the same returned object. |

**Mutable results:** Changing a returned list or dictionary changes what later callers receive. Prefer immutable results, or copy the result before modifying it. A shallow copy still shares nested mutable objects.

**Custom objects:** For a value-based cache key, use `@dataclass(frozen=True)` with hashable fields. It generates compatible equality and hashing methods:

```python
from dataclasses import dataclass
from functools import cache


@dataclass(frozen=True)
class Rectangle:
    width: int
    height: int


@cache
def area(rectangle: Rectangle) -> int:
    print("Calculating...")
    return rectangle.width * rectangle.height


print(area(Rectangle(3, 4)))  # Prints Calculating..., then 12.
print(area(Rectangle(3, 4)))  # Prints only 12: equal instance, cached result.
```

Equal objects must have equal hashes, and an object's hash must stay stable throughout its lifetime. For frozen dataclass fields included in the hash, use hashable values such as tuples instead of lists; `frozen=True` does not make nested objects immutable.

Ordinary classes normally use identity-based equality and hashing, so two instances with identical attributes are different cache keys. If you implement `__eq__()` and `__hash__()` yourself, keep them consistent and keep the fields used by them unchanged. Defining `__eq__()` without a suitable `__hash__()` normally makes instances unhashable. Avoid forcing hashing with `unsafe_hash=True` just to bypass an error.

References: [dataclass hashing](https://docs.python.org/3/library/dataclasses.html), [custom object hashing](https://docs.python.org/3/reference/datamodel.html#object.__hash__).

### Related example: limit and inspect an `lru_cache`

LRU means **least recently used**. When the cache is full, it removes the entry that has gone unused the longest. `maxsize` limits entries, not bytes or how long a result stays cached.

```python
from functools import lru_cache


@lru_cache(maxsize=2)
def square(number: int) -> int:
    return number * number


print(square(2))  # 4: miss, calculate and store
print(square(3))  # 9: miss, calculate and store
print(square(2))  # 4: hit, making 2 the most recently used
print(square(4))  # 16: miss, evicts 3
print(square(3))  # 9: miss, must calculate 3 again
print(square.cache_info())  # CacheInfo(hits=1, misses=4, maxsize=2, currsize=2)

square.cache_clear()  # Removes all entries and resets the statistics.
print(square.cache_info())  # CacheInfo(hits=0, misses=0, maxsize=2, currsize=0)
```

A **hit** reuses an entry; a **miss** runs the function. Both `@cache` and `@lru_cache` provide `cache_info()` and `cache_clear()`. Use `@cache` for an unbounded cache or `@lru_cache(maxsize=...)` for a bounded one. Neither provides automatic time-based expiry.

[Reference: `functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)

[Reference: `functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)

## 2. Describe Required Behavior with `Protocol`

A protocol tells a type checker which methods an object must provide. A class can satisfy a protocol without inheriting from it. This is called **structural subtyping**.

```python
from typing import Protocol


class MessageSender(Protocol):
    def send(self, message: str) -> None:
        ...


class ConsoleSender:
    def send(self, message: str) -> None:
        print(f"Console: {message}")


class TestSender:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


def notify(sender: MessageSender, message: str) -> None:
    sender.send(message)


notify(ConsoleSender(), "Hello!")  # Console: Hello!

test_sender = TestSender()
notify(test_sender, "Hello!")
print(test_sender.messages)  # ['Hello!']
```

Both classes have a compatible `send()` method, so a type checker accepts either one in `notify()`. This makes it easy to substitute a test implementation.

Unlike a Java interface that requires `implements`, a Python protocol does not require an explicit declaration on the implementing class.

**Watch out:** Type hints do not enforce this contract at runtime. Tools such as mypy or Pyright check it. Adding `@runtime_checkable` enables `isinstance()` checks, but those checks only inspect member presence; they do not validate method signatures or argument types.

### Related example: runtime checks with `@runtime_checkable`

Decorate the protocol when you need to check an object's available members while the program runs:

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class MessageSender(Protocol):
    def send(self, message: str) -> None:
        ...


class ConsoleSender:
    def send(self, message: str) -> None:
        print(message)


class WrongSignatureSender:
    def send(self) -> None:  # Missing the message parameter.
        print("No message accepted")


print(isinstance(ConsoleSender(), MessageSender))  # True
print(isinstance(object(), MessageSender))  # False: no send member
print(isinstance(WrongSignatureSender(), MessageSender))  # True: signature ignored!
```

The last result shows why a runtime protocol check does not replace a type checker. Calling `WrongSignatureSender().send("Hello")` would raise `TypeError`. Passing that object to a function annotated to accept `MessageSender` should be rejected by a type checker.

Without `@runtime_checkable`, using a protocol in `isinstance()` raises `TypeError`.

[Reference: `typing.runtime_checkable`](https://docs.python.org/3/library/typing.html#typing.runtime_checkable)

[Reference: `typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

## 3. Copy a Dataclass with Changes Using `replace`

`dataclasses.replace()` creates a new instance with selected fields changed. The original instance stays unchanged.

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Settings:
    theme: str = "dark"
    notifications: bool = True


original = Settings()
updated = replace(original, theme="light")

print(original)  # Settings(theme='dark', notifications=True)
print(updated)   # Settings(theme='light', notifications=True)
```

`frozen=True` prevents direct field assignment, such as `original.theme = "light"`. `replace()` is useful for creating a modified version instead. It also works with dataclasses that are not frozen.

**Watch out:** This is a shallow copy. If a field contains a list, both instances share that list unless you explicitly supply a new one. A frozen dataclass does not make objects stored inside its fields immutable.

### Related example: avoid sharing a mutable field

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Team:
    members: list[str]


original = Team(["Alice"])
shared_copy = replace(original)
independent_copy = replace(original, members=original.members.copy())

shared_copy.members.append("Bob")  # A frozen field can still contain a mutable list.
print(original.members)  # ['Alice', 'Bob']
print(independent_copy.members)  # ['Alice']
```

Copying this list is enough because its items are immutable strings. Nested mutable objects would still be shared by a shallow list copy.

[Reference: `dataclasses.replace`](https://docs.python.org/3/library/dataclasses.html#dataclasses.replace)

## 4. Compare Neighbors with `itertools.pairwise`

`pairwise()` yields overlapping pairs: first and second, second and third, and so on.

```python
from itertools import pairwise


readings = [10, 20, 35, 50]

print(list(pairwise(readings)))  # [(10, 20), (20, 35), (35, 50)]

changes = [current - previous for previous, current in pairwise(readings)]
print(changes)  # [10, 15, 15]
```

Use it for changes between measurements, distances between neighboring points, or adjacent duplicate detection.

```python
from itertools import pairwise


values = [1, 1, 2, 3, 3, 3]
duplicates = [left for left, right in pairwise(values) if left == right]

print(duplicates)  # [1, 3, 3]
```

Three consecutive `3`s produce two matching pairs. This finds equal neighbors, not unique duplicated values. An empty iterable or one containing a single item produces no pairs.

[Reference: `itertools.pairwise`](https://docs.python.org/3/library/itertools.html#itertools.pairwise)

## 5. Reuse a Value in a Condition with `:=`

The walrus operator assigns a value inside an expression. It helps when you need to test a result and then use it.

```python
import re


line = "Order number: 1234"

if (match := re.search(r"Order number: ([0-9]+)", line)):
    print(match.group(1))  # 1234
else:
    print("No order number found")
```

`re.search()` returns a match object or `None`. `:=` saves that result in `match`, and the `if` checks whether a match exists.

For ordinary file lines, a `for` loop is usually clearer. A walrus loop is useful when reading fixed-size chunks:

```python
from io import StringIO


with StringIO("abcdefghij") as stream:
    while (chunk := stream.read(4)):
        print(chunk)
```

Output:

```text
abcd
efgh
ij
```

The loop stops when `read()` returns an empty string.

**Watch out:** A truth test also rejects valid values such as `0` and `False`. If only `None` means “missing,” write `if (value := ...) is not None:`. Prefer a separate assignment if combining assignment and testing makes the code harder to read.

### Related example: keep a valid zero

```python
settings = {"retries": 0}

if (retries := settings.get("retries")) is not None:
    print(f"Retries: {retries}")  # Retries: 0
else:
    print("Retries not configured")
```

Using only `if (retries := settings.get("retries")):` would skip the first branch because zero is false in a truth test.

[Reference: assignment expressions](https://docs.python.org/3/reference/expressions.html#assignment-expressions)

## 6. Work with File Paths Using `pathlib`

`Path` objects let you join paths, inspect filenames, and read or write files through one API.

```python
from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as directory:
    folder = Path(directory) / "notes"
    folder.mkdir()

    note = folder / "hello.txt"
    note.write_text("Hello, Python!\n", encoding="utf-8")

    print(note.name)  # hello.txt
    print(note.stem)  # hello
    print(note.suffix)  # .txt
    print(note.read_text(encoding="utf-8").strip())  # Hello, Python!

    for path in sorted(folder.glob("*.txt")):
        print(path.name)  # hello.txt
```

The `/` operator joins path components; it does not create a directory. Use `mkdir(parents=True, exist_ok=True)` when parent directories may need creating.

Use `glob("*.py")` for matching files in one directory and `rglob("*.py")` to search its subdirectories too. `with_suffix(".bak")` returns a different path; it does not copy or rename a file.

**Watch out:** `write_text()` overwrites an existing file. `read_text()` loads the entire file into memory; for large text files, use `with path.open(encoding="utf-8") as file:` and iterate over the lines.

### Related example: nested folders, recursive search, and line reading

```python
from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as directory:
    root = Path(directory)
    nested = root / "notes" / "daily"
    nested.mkdir(parents=True, exist_ok=True)
    note = nested / "tasks.txt"
    note.write_text("Learn paths\nPractice Python\n", encoding="utf-8")

    print(list(root.glob("*.txt")))  # []: no text files directly in root
    print([path.name for path in root.rglob("*.txt")])  # ['tasks.txt']

    backup = note.with_suffix(".bak")
    print(backup.name, backup.exists())  # tasks.bak False: only a path was created

    with note.open(encoding="utf-8") as file:
        for line in file:
            print(line.rstrip())  # Prints each task on its own line.
```

`parents=True` creates missing parents; `exist_ok=True` permits an existing directory. Iterating over the open file reads lines without loading the whole file at once.

[Reference: `pathlib`](https://docs.python.org/3/library/pathlib.html)

## 7. Ignore an Expected Exception with `suppress`

`contextlib.suppress` skips a block's remaining statements if a specified exception occurs. Use it when that failure is expected and needs no further action.

```python
from contextlib import suppress


settings = {"theme": "dark", "debug": True}

with suppress(KeyError):
    del settings["debug"]

with suppress(KeyError):
    del settings["missing"]

print(settings)  # {'theme': 'dark'}
```

Each `with` block is equivalent to a `try` block followed by `except KeyError: pass`.

For this particular task, `settings.pop("missing", None)` is shorter. Likewise, for deleting a file that may be missing, `path.unlink(missing_ok=True)` is usually clearer. Use `suppress` when there is no suitable built-in alternative.

**Watch out:** Keep the block small and name only exceptions you intend to ignore. Suppressing `Exception` or all `OSError`s can hide problems that need attention. Use `try`/`except` when you need to log an error, recover, or return a fallback value.

### Related example: use built-in alternatives for missing items

```python
from pathlib import Path
from tempfile import TemporaryDirectory


settings = {"theme": "dark", "debug": True}
print(settings.pop("debug", None))  # True: removes and returns the value
print(settings.pop("missing", None))  # None: returns the default
print(settings)  # {'theme': 'dark'}

with TemporaryDirectory() as directory:
    path = Path(directory) / "cache.tmp"
    path.write_text("temporary data", encoding="utf-8")
    path.unlink(missing_ok=True)
    path.unlink(missing_ok=True)  # Already gone: no FileNotFoundError.
    print(path.exists())  # False
```

`missing_ok=True` ignores a missing file, but still allows errors such as `PermissionError` to surface.

[Reference: `contextlib.suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress)

## 8. Keep Request Context with `contextvars`

Use a `ContextVar` when helpers need information about the current request, such as a request ID, user ID, or language, without passing it through every function call.

**One `ContextVar` object can have a different value in each async task's context.** When `asyncio` switches tasks, it also switches the active context. `get()` reads from that context.

```python
import asyncio
from contextvars import ContextVar


# Create once, at module level.
request_id = ContextVar("request_id", default="unknown")


def log(message: str) -> None:
    print(f"[{request_id.get()}] {message}")


async def handle_request(identifier: str) -> None:
    token = request_id.set(identifier)  # Set this task's value.
    try:
        await asyncio.sleep(0)  # Let another task run.
        log("Request complete")
    finally:
        request_id.reset(token)  # Restore the previous state, even on failure.


async def main() -> None:
    await asyncio.gather(  # Run each handler as a separate task.
        handle_request("REQ-1"),
        handle_request("REQ-2"),
    )
    log("Outside requests")


asyncio.run(main())
```

Output (the first two lines may appear in either order):

```text
[REQ-1] Request complete
[REQ-2] Request complete
[unknown] Outside requests
```

Both tasks use the same `request_id` object, but each stores its own value. The `log()` helper reads the calling task's ID. Neither task changes `main()`'s value.

- `set(value)` assigns a value in the current context and returns a restoration token.
- `get()` reads the current context's value, falling back to the default if unset.
- `reset(token)` restores the state from before that `set()`.

A normal function call or direct `await` uses the current task's context. A newly created task normally inherits a copy of its creator's context.

> **Be careful with dictionaries:** `ContextVar` stores object references; it does not copy dictionaries or make them thread-safe. If tasks inherit or are assigned the same dictionary, mutations are visible to all of them. For separate request data, create a fresh dictionary inside each handler, pass it to `set()`, and reset in `finally`. Avoid a shared mutable default such as `default={}`. Prefer immutable values, such as strings, when practical.

Use ordinary arguments when only a few functions need the value. In a notebook with an existing event loop, use `await main()` instead of `asyncio.run(main())`.

[Reference: `contextvars`](https://docs.python.org/3/library/contextvars.html)

## 9. Match Structured Data with Guards

`match` checks a value against patterns. A **guard** is an `if` condition that must also be true before a case runs.

```python
def describe_command(command: str) -> str:
    match command.split():
        case ["quit"] | ["exit"]:
            return "Goodbye!"
        case ["repeat", word, count] if count.isdecimal():
            return " ".join([word] * int(count))
        case ["repeat", *_]:
            return "Usage: repeat WORD NONNEGATIVE_INTEGER"
        case ["echo", *words]:
            return " ".join(words)
        case _:
            return "Unknown command"


print(describe_command("repeat hi 3"))  # hi hi hi
print(describe_command("repeat hi no"))  # Usage: repeat WORD NONNEGATIVE_INTEGER
print(describe_command("echo hello world"))  # hello world
print(describe_command("quit"))  # Goodbye!
```

The `repeat` case requires exactly three words. It captures the last two in `word` and `count`, then checks the guard. `*words` captures any remaining words as a list; `_` matches anything without saving it.

**Watch out:** Cases are tried from top to bottom, and only the first match with a true guard runs. Put specific cases before general ones. A bare name such as `case status:` captures a value rather than comparing against an existing variable. Use literals, qualified constants, or guards for comparisons.

For a few simple numeric comparisons, `if`/`elif` is usually easier to read. Pattern matching is most useful when the data's shape matters.

### Related example: compare against a named constant

Use a qualified name such as `Status.OK` when a case should compare a value rather than capture it:

```python
from enum import Enum


class Status(Enum):
    OK = "ok"
    FAILED = "failed"


def describe(status: Status) -> str:
    match status:
        case Status.OK:
            return "Success"
        case Status.FAILED:
            return "Failure"
        case _:
            return "Unknown status"


print(describe(Status.OK))  # Success
print(describe(Status.FAILED))  # Failure
```

[Reference: the `match` statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

## 10. Manage a Variable Number of Resources with `ExitStack`

Use `ExitStack` when the number of context managers is decided at runtime. Each call to `enter_context()` enters a context manager and registers its exit method.

```python
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as directory:
    folder = Path(directory)
    paths = [folder / "first.txt", folder / "second.txt"]
    for path, content in zip(paths, ["Hello", "Python"]):
        path.write_text(content, encoding="utf-8")

    with ExitStack() as stack:
        files = [
            stack.enter_context(path.open(encoding="utf-8"))
            for path in paths
        ]
        for file in files:
            print(file.read())

    print(all(file.closed for file in files))
```

Output:

```text
Hello
Python
True
```

Resources exit in reverse order. If opening a later file fails, previously opened files still close. They also close if an exception leaves the `with` block.

**Watch out:** Use a normal `with` for a fixed, small number of resources. If you only need one file at a time, open it inside a loop to avoid holding many files open. `ExitStack` coordinates cleanup; it does not make multiple database transactions atomic.

### Related example: a normal `with` for fixed resources

When there are exactly two known resources, a regular `with` can manage both:

```python
from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as directory:
    source = Path(directory) / "source.txt"
    target = Path(directory) / "target.txt"
    source.write_text("Hello, Python!\n", encoding="utf-8")

    with (
        source.open(encoding="utf-8") as reader,
        target.open("w", encoding="utf-8") as writer,
    ):
        for line in reader:
            writer.write(line)

    print(reader.closed, writer.closed)  # True True
    print(target.read_text(encoding="utf-8").strip())  # Hello, Python!
```

Both files close on exit, including when an exception occurs. Choose `ExitStack` when the number or selection of resources is determined while the program runs.

[Reference: `contextlib.ExitStack`](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack)

## Quick Reference

| Feature | Use it when you need to... |
| --- | --- |
| `@cache` | Reuse a calculation for repeated arguments |
| `Protocol` | Describe behavior accepted by a typed function |
| `dataclasses.replace` | Create a modified dataclass instance |
| `pairwise` | Compare neighboring items |
| `:=` | Save and test a result in one expression |
| `pathlib` | Build paths and work with files |
| `suppress` | Ignore a specific, expected exception |
| `contextvars` | Make request context available to helper functions |
| `match` with guards | Branch on data structure and conditions |
| `ExitStack` | Manage a variable number of context managers |

**Original video:** [10 Python Features You're Not Using (But Really Should)](https://www.youtube.com/watch?v=cXl-AUXHHZY)
