# Python Data Structures Interview Handbook

> Python 3.11+. Learn what each structure stores, which operations it supports, and when to choose it. Examples use small inputs and `assert` checks; silence means a check passed.

Use these three documents together:

| Need | Read |
|---|---|
| Python collections, their behavior, and operation costs | This handbook |
| Searching, sorting, BFS/DFS, windows, DP, and worked algorithms | [Python algorithms notebook](../../dsa/python_algorithms_notebook.md) |
| Syntax, functions, files/pickle, testing, concurrency, and application tools | [Python interview reference](python_interview_reference_guide.md) |

Read sections 1–8 first for core collections, then 9–13 for standard-library tools and memory behavior. Section 14 is an optional bridge to custom structures and the algorithms notebook.

## Contents

1. [Choose a structure by its job](#1-choose-a-structure-by-its-job)
2. [Shared rules: references, mutability, equality, and hashing](#2-shared-rules-references-mutability-equality-and-hashing)
3. [Strings and binary sequences](#3-strings-and-binary-sequences)
4. [Lists](#4-lists)
5. [Tuples and named tuples](#5-tuples-and-named-tuples)
6. [Dictionaries](#6-dictionaries)
7. [Sets and frozensets](#7-sets-and-frozensets)
8. [Deques, stacks, and queues](#8-deques-stacks-and-queues)
9. [Counter and defaultdict](#9-counter-and-defaultdict)
10. [Heaps and priority queues](#10-heaps-and-priority-queues)
11. [Records: dataclasses and TypedDict](#11-records-dataclasses-and-typeddict)
12. [Copying and nested containers](#12-copying-and-nested-containers)
13. [Iteration, comprehensions, and lazy values](#13-iteration-comprehensions-and-lazy-values)
14. [Custom structures: what Python gives you](#14-custom-structures-what-python-gives-you)
15. [Quick revision and interview practice](#15-quick-revision-and-interview-practice)

## 1. Choose a structure by its job

Imagine organizing a classroom: a list keeps a seating order, a dictionary finds a student by ID, a set records unique attendees, and a queue handles students in arrival order.

| Structure | Stores | Preserves order? | First choice when you need |
|---|---|---|---|
| `str` | Text characters | Sequence order | Immutable text |
| `list` | A sequence of object references | Yes | Indexing, duplicates, and changes to a sequence |
| `tuple` / `NamedTuple` | A fixed group of references | Yes | A record whose positions should not change |
| `dict` | Unique keys mapped to values | Insertion order | Lookup by a label or ID |
| `set` | Unique hashable elements | No guaranteed iteration order | Membership, uniqueness, set operations |
| `frozenset` | An immutable set | No guaranteed iteration order | A group used as a dict key/set element |
| `deque` | Items in a sequence | Yes | Add/remove at both ends |
| `Counter` | Hashable items mapped to counts | Dict insertion order | Frequencies |
| `defaultdict` | Keys mapped to automatically created defaults | Dict insertion order | Grouping and accumulation |
| A list maintained with `heapq` | Heap-ordered items | Not fully sorted | Repeatedly access the smallest priority |
| `dataclass` | Named fields | Field definition order for generated methods | A readable application record |

**Decision rule:** start with the operations you repeat. Lists make position lookup fast; sets/dicts make average membership/key lookup fast; deques make end operations fast. No structure makes every operation O(1).

**Cost conventions:** `n` is the collection size; `k` is a slice/result size. Hash costs assume O(1) hashing/comparison and ordinary hash distribution. Average O(1) does not mean worst-case O(1). Amortized O(1) spreads occasional expensive resizing across many operations. Space costs describe additional allocations, not the input already stored. The algorithms notebook explains Big O in more detail.

## 2. Shared rules: references, mutability, equality, and hashing

### Names and containers refer to objects

Assignment creates another reference; it does not copy the object.

```python
values = [1, 2]
alias = values
alias.append(3)
assert values == [1, 2, 3]
assert alias is values

separate = [1, 2, 3]
assert separate == values      # Equal contents.
assert separate is not values  # Different list objects.
```

Use `==` for value equality and `is` for identity, especially `value is None`.

### Mutable versus immutable

- Lists, dictionaries, sets, deques, and bytearrays can change after creation.
- Strings, numbers, tuples, bytes, and frozensets are immutable.
- An immutable container can refer to mutable objects. A tuple containing a list cannot replace that list, but the list itself can change.

### Hashable is the requirement for keys and set elements

A dictionary key or set element must have a stable hash; equal objects must have equal hashes. Strings, integers, and tuples of hashable elements work. Lists, dictionaries, and sets do not.

```python
locations = {(2, 3): "desk"}
assert locations[(2, 3)] == "desk"

try:
    locations[[2, 3]] = "desk"  # A list is unhashable.
except TypeError:
    pass
else:
    raise AssertionError("A list must not be accepted as a key")
```

**Immutable does not automatically mean hashable:** `(1, [2])` is a tuple but contains an unhashable list. Some mutable custom objects are hashable; do not change attributes used for hashing/equality while they are keys. Prefer stable IDs or frozen records with hashable fields. Dictionary **values** may be any type.

## 3. Strings and binary sequences

A string is an immutable Unicode sequence. Methods return results; they do not modify the original string.

```python
text = "  Python,Data  "
clean = text.strip()
assert clean == "Python,Data"
assert text == "  Python,Data  "
assert clean.split(",") == ["Python", "Data"]
assert "-".join(["a", "b", "c"]) == "a-b-c"
assert clean.replace("Python", "Modern Python") == "Modern Python,Data"
assert clean[0] == "P"
```

| Operation on a string of length n | Typical time | Allocation |
|---|---|---|
| Index one character | O(1) | A character result |
| Slice/copy k characters | O(k) | O(k) result |
| Search for a single character | O(n) worst | No full result copy needed |
| Join pieces totaling n characters | O(n + number of pieces) | O(n) result |

Build text from pieces and join once when assembling many pieces. Repeated concatenation may repeatedly copy growing strings. String indices refer to Unicode code points, which are not always the same as user-perceived characters such as combined emoji.

`bytes` stores immutable binary data; `bytearray` is its mutable counterpart. Indexing either returns an integer byte value.

```python
raw = b"ABC"
editable = bytearray(raw)
editable[0] = 90
assert raw[0] == 65
assert bytes(editable) == b"ZBC"
```

For palindrome checks, anagrams, and substring algorithms, use the algorithms notebook; this section focuses on how text is stored and accessed.

## 4. Lists

A list is a mutable, ordered sequence of object references. Duplicates are allowed. Think of numbered seats: indexing jumps directly to a position, but inserting a seat in the middle shifts later positions.

```python
numbers = [10, 20, 30]
assert numbers[1] == 20
numbers.append(40)       # Add one item.
numbers.extend([50, 60]) # Add items from an iterable.
assert numbers[-1] == 60
assert numbers[1:3] == [20, 30]  # Stop index is excluded.
assert numbers.pop() == 60      # Remove/return last item.
assert numbers == [10, 20, 30, 40, 50]
```

| Operation | Time | What happens |
|---|---|---|
| `items[i]` / `items[i] = value` | O(1) | Access/replace a reference |
| `items.append(value)` | Amortized O(1) | Occasional resizing copies references |
| `items.pop()` | Amortized O(1) | Remove the last item; resizing can occur |
| `value in items` / `items.index(value)` | O(n) worst | Scan for a value |
| `items.insert(i, value)` / `del items[i]` | O(n) worst | Shift later references |
| `items.remove(value)` | O(n) worst | Find the first equal value, then remove it |
| `items[a:b]` selecting k items | O(k) | Allocate a new, shallow list |
| `items.sort()` | O(n log n) worst | Mutates the list; can use O(n) workspace |

### Why append is amortized O(1)

Most appends fill an available slot. Occasionally Python needs a larger underlying array and copies existing references, costing O(n). Extra capacity makes those resizes infrequent; the average work per append over a long sequence is O(1).

### Middle insertion: does order matter?

Normal insertion keeps the relative order of existing items:

```python
items = [10, 20, 30, 40]
items.insert(1, 99)
assert items == [10, 99, 20, 30, 40]  # Shift 20, 30, and 40 right.
```

If rearranging existing items is allowed, you can put the new item at an existing index by appending and swapping:

```python
items = [10, 20, 30, 40]
items.append(99)
items[1], items[-1] = items[-1], items[1]
assert items == [10, 99, 30, 40, 20]
```

This costs amortized O(1), but changes order. If the new value needs no specific position, just append it. Confirm the ordering requirement in an interview. A deque does not make arbitrary middle insertion O(1).

### Methods that mutate versus methods that return

```python
numbers = [3, 1, 2]
assert numbers.sort() is None
assert numbers == [1, 2, 3]
ordered = sorted([3, 1, 2])
assert ordered == [1, 2, 3]
```

`append()`, `extend()`, and `sort()` mutate the list and return `None`; `pop()` removes and returns an item. `sorted()` returns a new list. Avoid removing items while iterating over the same list; construct a filtered result instead.

### Searching a sorted list with bisect

```python
from bisect import bisect_left, insort

numbers = [1, 3, 5]
assert bisect_left(numbers, 4) == 2  # An insertion position, not a found item.
insort(numbers, 4)
assert numbers == [1, 3, 4, 5]
```

Boundary search takes O(log n); insertion still takes O(n) because references shift. A sorted list and a heap provide different promises: a sorted list orders every item; a heap only makes the minimum easy to access. Manual search/sort implementations belong in the algorithms notebook.

## 5. Tuples and named tuples

A tuple fixes its sequence of references: you cannot append, delete, or assign a position. Use it for a small fixed-shape record; use a list when the sequence itself needs to change.

```python
point = (10, 20)
x, y = point
assert (x, y) == (10, 20)
assert ("only",) == tuple(["only"])  # A one-item tuple needs the comma.

record = ("Ada", ["Python"])
record[1].append("SQL")  # The nested list remains mutable.
assert record == ("Ada", ["Python", "SQL"])
```

Tuple indexing is O(1); membership is O(n); slicing k items is O(k). Tuple immutability does not recursively freeze its contents. A tuple is hashable only when all its elements are hashable.

A `NamedTuple` adds readable field names while retaining tuple behavior:

```python
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


point = Point(10, 20)
assert point.x == 10
assert point[1] == 20
assert tuple(point) == (10, 20)
```

## 6. Dictionaries

A dictionary maps unique hashable keys to values. Keys identify values; they are not positional indices. Lookup, insertion, and deletion by key are average O(1), with O(n) worst cases under heavy collisions. Hashing long keys or expensive custom comparisons can add cost.

```python
user = {"id": 1, "name": "Ada"}
user["role"] = "engineer"
user["name"] = "Grace"  # Update an existing key.
assert user["name"] == "Grace"
assert user.get("missing", "default") == "default"
assert "name" in user       # Membership checks keys.
assert "Grace" not in user  # Not a key, even though it is a value.
assert "Grace" in user.values()  # Value search is O(n).
```

`user["missing"]` raises `KeyError`; `get()` supplies a fallback without inserting the missing key. `pop(key)` removes and returns a value, while `del mapping[key]` removes the entry.

### Insertion order is not sorted order

Since Python 3.7, dictionaries guarantee insertion order. Updating an existing key does not move it; deleting and reinserting it puts it at the end.

```python
scores = {"Bob": 80, "Alice": 95, "Carol": 70}
scores["Bob"] = 90
assert list(scores) == ["Bob", "Alice", "Carol"]
assert sorted(scores) == ["Alice", "Bob", "Carol"]  # New list of keys.
assert sorted(scores.items(), key=lambda pair: pair[1]) == [
    ("Carol", 70), ("Bob", 90), ("Alice", 95)
]
del scores["Bob"]
scores["Bob"] = 91
assert list(scores) == ["Alice", "Carol", "Bob"]
```

### Views, snapshots, and iteration

`keys()`, `values()`, and `items()` return views that reflect later dictionary changes. Use `list(mapping.items())` when you need a snapshot of the entries for iteration; it is shallow, so nested values can still change.

```python
mapping = {"a": 1}
keys = mapping.keys()
snapshot = list(mapping.items())
mapping["b"] = 2
assert list(keys) == ["a", "b"]
assert snapshot == [("a", 1)]
```

Do not add/delete dictionary entries while iterating its live views. An entry snapshot lets you decide removals without changing the collection being iterated.

### Merge and deduplicate

```python
defaults = {"debug": False, "retries": 3}
override = {"debug": True}
assert defaults | override == {"debug": True, "retries": 3}
assert defaults["debug"] is False  # | returns a new dictionary.

names = ["Ada", "Ben", "Ada", "Cy"]
assert list(dict.fromkeys(names)) == ["Ada", "Ben", "Cy"]
```

Dictionary keys are unique, so `dict.fromkeys()` can remove duplicates while preserving first-occurrence order. Elements must be hashable. Avoid `dict.fromkeys(keys, [])` for independent lists: every key would refer to the same list.

## 7. Sets and frozensets

A set stores unique hashable elements. Membership/add/remove are average O(1), O(n) worst under collisions. It has no positional indexing and guarantees neither insertion order nor sorted iteration order.

```python
left = {1, 2, 3}
right = {3, 4}
assert left | right == {1, 2, 3, 4}  # Union.
assert left & right == {3}           # Intersection.
assert left - right == {1, 2}        # Difference.
assert left ^ right == {1, 2, 4}     # Symmetric difference.
assert {1, 2} <= left                # Subset.
assert set([1, 1, 2]) == {1, 2}
```

Use `set()` for an empty set; `{}` creates an empty dictionary. `remove(x)` raises `KeyError` when absent; `discard(x)` does nothing when absent.

### Ordered output from an unordered collection

```python
values = {30, 10, 20}
assert sorted(values) == [10, 20, 30]
assert sorted(values, reverse=True) == [30, 20, 10]
assert isinstance(values, set)  # Sorting did not change the set.
```

`sorted()` returns a **new list**, and its elements need a compatible ordering or an appropriate `key` function. Converting that list back to a set loses the ordering guarantee. To deduplicate while keeping input order, use the dictionary example above.

Set union creates a result in average O(n + m) time; intersection is average O(min(n, m)) for two sets of sizes n and m. These operations can allocate new result sets. Membership is fast only after the set exists: repeatedly rebuilding `set(values)` inside a loop repeats O(n) work.

### Frozenset: an immutable group

```python
permissions = frozenset({"read", "write"})
labels = {permissions: "editor"}
assert labels[frozenset({"write", "read"})] == "editor"
```

A frozenset is immutable and hashable. Its elements must still be hashable; freezing a collection does not convert unhashable elements into hashable ones.

## 8. Deques, stacks, and queues

A **stack** is a rule: last in, first out (LIFO). A **queue** is a rule: first in, first out (FIFO). A **deque** is a double-ended queue that supports both styles. Use a list for a stack or a deque when both ends are important.

```python
from collections import deque

stack = ["A", "B", "C"]
assert stack.pop() == "C"  # Most recently added.

queue = deque(["A", "B", "C"])
queue.append("D")
assert queue.popleft() == "A"  # Earliest added.
queue.appendleft("first")
assert queue.pop() == "D"      # Right end: no popright() method.
assert list(queue) == ["first", "B", "C"]
```

| Deque operation | Time |
|---|---|
| `append`, `appendleft`, `pop`, `popleft` | O(1) |
| Index at either end | O(1) |
| General middle indexing / membership | O(n) worst |

```python
from collections import deque

recent = deque(maxlen=3)
recent.extend([1, 2, 3, 4])
assert list(recent) == [2, 3, 4]  # Oldest item discarded automatically.
```

A bounded deque is useful for recent history, but silently discarding an item is wrong for a queue that must retain every job. Popping an empty list/deque raises `IndexError`. A deque is not a replacement for a list when you need repeated arbitrary indexing.

BFS/DFS, bracket matching, and monotonic stacks are worked through in the algorithms notebook. For coordinating threads with blocking/waiting behavior, see the general reference and `queue.Queue` rather than assuming a deque provides a complete task-coordination protocol.

## 9. Counter and defaultdict

### Counter: a frequency dictionary

```python
from collections import Counter

counts = Counter("banana")
assert counts["a"] == 3
assert counts["z"] == 0
assert "z" not in counts  # Reading a missing count does not insert it.
assert counts.most_common(1) == [("a", 3)]
counts["z"] = 0
assert "z" in counts      # An explicit zero-count entry still exists.
```

Counting n items takes average O(n) time and O(u) space for u distinct items. `most_common()` adds its own selection/sorting cost; it is not a constant-time operation. Counter counts may be zero or negative.

### defaultdict: create a value on a missing-key lookup

```python
from collections import defaultdict

groups = defaultdict(list)
for word in ["apple", "apricot", "banana"]:
    groups[word[0]].append(word)
assert dict(groups) == {"a": ["apple", "apricot"], "b": ["banana"]}
assert groups.get("z") is None
assert "z" not in groups  # get() does not call the default factory.
assert groups["z"] == []
assert "z" in groups      # [] lookup created and inserted the default list.
```

Pass the factory `list`, not `list()`. A new list is created for each missing key. Grouping n items uses average O(n) dictionary operations and O(n) references in the grouped result, assuming constant-time grouping-key calculation. Unlike a normal dict, `groups[missing]` can change the mapping just by being read.

## 10. Heaps and priority queues

A min-heap promises that the smallest item is at index 0. It does **not** promise that the rest of the list is sorted. Python's `heapq` maintains a heap inside an ordinary list.

```python
import heapq

heap = [5, 1, 4, 2]
heapq.heapify(heap)
assert heap[0] == 1
heapq.heappush(heap, 0)
assert heapq.heappop(heap) == 0
assert heapq.heappop(heap) == 1
assert sorted(heap) == [2, 4, 5]
```

| Operation | Time |
|---|---|
| `heap[0]`, peek at minimum | O(1) |
| `heappush` / `heappop` | O(log n), in the usual heap-operation model |
| `heapify` an existing list | O(n) |
| Search for an arbitrary value | O(n) |

Popping an empty heap raises `IndexError`. Do not mutate a priority inside the heap and assume the heap property repairs itself. For equal priorities and non-comparable payloads, include a unique tie-breaker:

```python
import heapq
from itertools import count

sequence = count()
heap = []
heapq.heappush(heap, (1, next(sequence), {"task": "first"}))
heapq.heappush(heap, (1, next(sequence), {"task": "second"}))
assert heapq.heappop(heap)[2] == {"task": "first"}
```

Tuples compare left to right. The sequence number breaks ties before Python tries to compare the dictionaries; it also preserves arrival order among equal priorities in this example. The algorithms notebook shows top-k and Dijkstra applications.

## 11. Records: dataclasses and TypedDict

A dataclass describes a record with named fields and generates methods such as initialization, representation, and equality. It is useful when a dictionary's free-form keys are too loose for the model you want.

```python
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    courses: list[str] = field(default_factory=list)


ada = Student("Ada")
ben = Student("Ben")
ada.courses.append("Python")
assert ben.courses == []  # Each instance gets its own list.
```

### slots=True: fixed attribute storage

Slots usually avoid a per-instance `__dict__`, reducing memory when many instances exist. They also prevent adding undeclared attributes in a class without an inherited instance dictionary.

```python
from dataclasses import dataclass


@dataclass(slots=True)
class SlottedPoint:
    x: int
    y: int


point = SlottedPoint(2, 3)
point.x = 10  # Existing fields remain writable.
try:
    point.color = "red"  # No slot for color.
except AttributeError as error:
    print(f"AttributeError: {error}")
```

Output:

```text
AttributeError: 'SlottedPoint' object has no attribute 'color'
```

`slots=True` controls storage; `frozen=True` blocks normal attribute assignment/deletion after initialization. Frozen records are not deeply immutable: a list stored inside a frozen field can still be changed.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coordinate:
    x: int
    y: int


labels = {Coordinate(2, 3): "desk"}
assert labels[Coordinate(2, 3)] == "desk"
```

A frozen dataclass with default equality normally gets a generated hash, but hashing still fails if one of its hashed fields is unhashable. A typical mutable dataclass with generated equality is unhashable. Avoid `unsafe_hash=True` as a shortcut around fields that can change.

### TypedDict: a dictionary shape for type checkers

```python
from typing import TypedDict


class UserPayload(TypedDict):
    id: int
    name: str


payload: UserPayload = {"id": 1, "name": "Ada"}
assert isinstance(payload, dict)
```

`TypedDict` adds static typing information; it is still a normal mutable dictionary at runtime and does not validate a JSON payload. Choose `NamedTuple` for tuple-style immutable records, dataclasses for modeled objects, and dictionaries/TypedDict for mapping-shaped data.

## 12. Copying and nested containers

Assignment shares an object; a shallow copy duplicates the outer container; a deep copy recursively copies nested content, respecting object-specific copying behavior.

```python
import copy

original = {"items": [1, 2]}
alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

shallow["items"].append(3)
assert original["items"] == [1, 2, 3]
assert alias is original
assert shallow is not original
assert shallow["items"] is original["items"]
deep["items"].append(4)
assert deep["items"] == [1, 2, 4]
assert original["items"] == [1, 2, 3]
```

A shallow copy of n entries is O(n) time/space. Deep-copy cost depends on the reachable object graph and copying hooks; it is not automatically O(n) in just the outer container's length.

### Repeated nested lists share the same row

```python
bad = [[0] * 3] * 3
bad[0][0] = 1
assert bad == [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

good = [[0] * 3 for _ in range(3)]
good[0][0] = 1
assert good == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

`* 3` repeats references to one row; the comprehension creates each row separately. Also be careful with shared mutable defaults: use `default_factory` in dataclasses and create independent values per dictionary key.

## 13. Iteration, comprehensions, and lazy values

An iterable can supply an iterator. The iterator remembers its position; a generator is an iterator that produces values lazily.

```python
values = [10, 20, 30]
iterator = iter(values)
assert next(iterator) == 10
assert list(iterator) == [20, 30]
assert list(iterator) == []  # Exhausted; the original list still exists.
assert list(values) == [10, 20, 30]
```

Lists are reusable; a particular iterator/generator is one-pass. Once exhausted, `next()` raises `StopIteration` unless a default is supplied.

```python
values = [1, 2, 3, 4]
squares = [value * value for value in values]
lookup = {value: value * value for value in values}
parities = {value % 2 for value in values}
lazy_squares = (value * value for value in values)
assert squares == [1, 4, 9, 16]
assert lookup[3] == 9
assert parities == {0, 1}
assert sum(lazy_squares) == 30
assert list(lazy_squares) == []
```

A list comprehension materializes n results in O(n) time and O(n) result memory when each expression is O(1). The generator keeps O(1) internal iteration state for this example, but retains access to its input; it does not make the input list disappear. Consuming all its results still takes O(n) work. Use a normal loop when nested conditions make a comprehension difficult to read.

```python
numbers = range(0, 10, 2)
assert list(numbers) == [0, 2, 4, 6, 8]
assert numbers[2] == 4
```

A `range` stores its start/stop/step, not a list of all represented integers. For ordinary-sized integer bounds its storage is constant; converting it to a list allocates every result. It is reusable and supports indexing, unlike a generator.

## 14. Custom structures: what Python gives you

A **data structure** organizes items and their relationships. An **abstract data type** describes the behavior you need; an implementation chooses how to store it. For example, “newest item first” describes a stack, and a Python list can implement it.

Python gives you lists, dictionaries, sets, and classes as building blocks. It does not provide a general-purpose linked-list, balanced-BST, trie, or union-find class in the standard library. `heapq` provides heap operations on a list. Build a custom structure when its relationships or operations fit your problem; everyday Python code often needs only built-ins.

### Singly linked list: follow the next link

**Picture:** a chain of treasure-hunt clues. Each clue holds a value and points to the next clue. You cannot jump directly to clue 100 without following links.

```text
head
 ↓
[10 | next] → [20 | next] → [30 | None]
```

```python
from dataclasses import dataclass


@dataclass(eq=False)
class ListNode:
    value: int
    next: "ListNode | None" = None


head = ListNode(10, ListNode(20, ListNode(30)))
assert head.value == 10
assert head.next.value == 20
assert head.next.next.value == 30

# Insert 15 immediately after a node we already have: head.
head.next = ListNode(15, head.next)
assert head.next.value == 15
assert head.next.next.value == 20
```

The new node points to the old second node, then the first node points to the new node. The chain becomes `10 → 15 → 20 → 30`. Later nodes do not shift as they would in a list. Each node still occupies its own object; `next` stores a reference, not a copy of the rest of the chain.

**Append 40 after 30:** start with the original three-node chain.

```python
head = ListNode(10, ListNode(20, ListNode(30)))
head.next.next.next = ListNode(40)
```

`head.next.next` is the node containing `30`. Assigning its `.next` attaches
`40`: `10 → 20 → 30 → 40 → None`. This shortcut assumes exactly three nodes;
for a list of any length, walk to the last node instead:

```python
head = ListNode(10, ListNode(20, ListNode(30)))
new_node = ListNode(40)

if head is None:
    head = new_node           # An empty list starts with the new node.
else:
    current = head
    while current.next is not None:
        current = current.next
    current.next = new_node  # Attach 40 after the last node.
```

Walking to the tail takes **O(n) time** and **O(1) extra space**. If you already
keep a reference to the tail, attaching the new node and updating that reference
takes O(1) time.

**Keep a tail reference:** `head` refers to the first node; `tail` refers to
the last node. They are references to existing nodes, not extra nodes.

```text
head        tail
 ↓           ↓
10 → 20 → 30 → None
```

```python
head = ListNode(10, ListNode(20, ListNode(30)))
tail = head.next.next       # Keep a reference to the node containing 30.

tail.next = ListNode(40)   # Attach 40 directly to the last node.
tail = tail.next           # Move tail to the new last node: 40.

assert head.value == 10
assert head.next.next.next is tail
assert tail.value == 40
assert tail.next is None
```

The chain is now `10 → 20 → 30 → 40 → None`. Appending takes **O(1) time**
because no traversal is needed. Update `tail` after every append; otherwise it
still points to the old last node, and the next append could overwrite a link.
Keeping the tail reference uses **O(1) extra space**. Finding the tail of an
existing list first takes O(n) time; `head.next.next` above assumes three nodes.
For an empty list, both `head` and `tail` are `None`; for a one-node list,
both refer to the same node. On the first append to an empty list, set both
references to the new node.

**Why `@dataclass(eq=False)`?** `eq=False` tells the dataclass not to generate an
`__eq__` method for field-by-field equality. These node classes inherit directly
from `object`, so `==` checks whether two references point to the same object.
Two nodes can hold the same value while occupying different positions in a structure.

```python
a = ListNode(10)
b = ListNode(10)
c = a

assert a != b                 # Same value, different node objects.
assert a == c                 # Both references point to the same node.
assert a.value == b.value     # The stored values are equal.
```

The default, `eq=True`, generates field-based equality: these two separate nodes
would compare equal. The same `eq=False` reasoning applies to `TreeNode` below.
If a parent class defines its own `__eq__`, `eq=False` leaves that inherited
behavior in place.

**Useful for:** learning node/reference manipulation and structures that splice around known nodes. Python's built-in list is a dynamic array, not this chain, and is usually a better everyday sequence.

**Costs:** reaching the kth node takes O(k), up to O(n); inserting after a **known** node is O(1). Finding that node first may cost O(n). Storing n nodes takes O(n) space.

### Binary search tree: smaller left, larger right

**Picture:** organize numbered records so each comparison tells you which branch to follow. Every node has at most two children. For this example all values are distinct, and every value in a left subtree is smaller than its parent; every value in a right subtree is larger.

```text
         10
        /  \
       5    15
           /
          12
```

```python
from dataclasses import dataclass


@dataclass(eq=False)
class TreeNode:
    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


root = TreeNode(10, TreeNode(5), TreeNode(15, TreeNode(12)))
assert root.left.value == 5
assert root.right.value == 15
assert root.right.left.value == 12
```

**Find 12 by hand:** compare with 10 → larger, go right. Compare with 15 → smaller, go left. Reach 12 → found. We follow one path; we do not inspect every node. A general binary tree does not promise this ordering.

**What do the references mean?** `root` refers to the first node we examine.
Each node's `left` and `right` refer to child nodes; `None` means that child
is absent. `current = root` gives us another reference to the same node, not a
copy of the tree. Moving `current` to a child does not move `root`.

**Add 13 to this tree:** follow `10 → 15 → 12`. Since 13 is larger than 12,
attach it as 12's right child:

```python
root.right.left.right = TreeNode(13)
assert root.right.left.right.value == 13
```

```text
         10
        /  \
       5    15
           /
          12
            \
             13
```

This shortcut assumes the pictured tree and an empty child slot. Assigning to
an occupied slot would replace that link and could disconnect an entire subtree.
For an arbitrary tree, follow comparisons until an empty slot is found:

```python
def insert(root: TreeNode | None, value: int) -> TreeNode:
    if root is None:
        return TreeNode(value)
    current = root
    while True:
        if value == current.value:
            return root  # This example ignores duplicate values.
        if value < current.value:
            if current.left is None:
                current.left = TreeNode(value)
                return root
            current = current.left
        else:
            if current.right is None:
                current.right = TreeNode(value)
                return root
            current = current.right


root = insert(root, 18)
assert root.right.right.value == 18
empty_tree = insert(None, 7)
assert empty_tree.value == 7
```

Keep the returned `root`, especially when inserting into an empty tree.
Attaching a child at a known empty slot is O(1); finding its correct slot takes
O(h) time. This iterative insertion uses O(1) working space, plus the new node.
It does not rebalance the tree. There is no single tail: a tree can have many leaves.

**Useful for:** ordered lookup, range queries, and keeping keys searchable in sorted order. A self-balancing implementation is needed for reliable logarithmic operation costs. A dict is a hash table: insertion order does not make it a search tree.

**Costs:** search/insert/delete take O(h), where h is tree height. A balanced tree has O(log n) height; a chain-shaped tree can have O(n) height. Node storage is O(n). The insertion above follows this O(h) bound; it does not implement deletion or balancing.

### Graph: a map of connections

**Picture:** rooms joined by corridors. A room can have many neighbors, and routes can form cycles. A dictionary maps each room to a list of adjacent rooms.

```text
Entrance — Library — Lab
```

```python
graph = {
    "Entrance": ["Library"],
    "Library": ["Entrance", "Lab"],
    "Lab": ["Library"],
}

assert graph["Entrance"] == ["Library"]
assert "Lab" in graph["Library"]
assert "Lab" not in graph["Entrance"]  # Not directly connected.
```

Read `graph["Library"]` as “where can I go in one move from Library?” Both directions are stored because these corridors are two-way. In a directed graph, A → B does not automatically imply B → A.

**Add a room and a two-way connection:** create the room's neighbor list,
then record the corridor at both ends.

```python
graph["Cafe"] = []  # A new room with no connections yet.
graph["Lab"].append("Cafe")
graph["Cafe"].append("Lab")

assert graph["Lab"] == ["Library", "Cafe"]
assert graph["Cafe"] == ["Lab"]
```

```text
Entrance — Library — Lab — Cafe
```

`neighbors = graph["Lab"]` refers to the actual stored list. Changing that list through
this reference changes the graph too:

```python
neighbors = graph["Lab"]
assert neighbors is graph["Lab"]

# Remove the same two-way corridor at both ends.
neighbors.remove("Cafe")
graph["Cafe"].remove("Lab")
assert graph["Cafe"] == []  # The room remains, now isolated.
```

Removing only one side would leave inconsistent two-way connections. For a
one-way corridor, store only the outgoing connection. Neighbor lists permit
duplicates, so repeated `append` calls can store the same corridor twice.
Use sets if each connection should occur only once.

Adding a new room is average O(1); each list append is amortized O(1).
Removing a neighbor from a list takes O(d), including finding it and shifting
remaining references. A graph has no universal head or tail; a traversal chooses
its starting room.

**Useful for:** routes, social connections, dependencies, and networks. The structure stores connections; BFS, DFS, and shortest-path algorithms decide how to explore them.

**Costs:** an adjacency list uses O(V + E) space for V rooms and E connections. Retrieving a room's list is average O(1); checking whether a neighbor is in that list takes O(d), where d is the room's number of neighbors. Undirected edges appear twice, which does not change the Big O bound.

If repeated edge-membership checks dominate, a neighbor **set** offers average O(1) membership, but no guaranteed iteration order or duplicate edges. An adjacency matrix offers O(1) edge lookup at O(V²) storage. Representation changes the costs.

### Trie: words share their starting letters

**Picture:** store `car` and `cat` by sharing the path `c → a`, then branching at the final letter. A trie is a prefix tree.

```text
(root)
   c
   a          "ca" is a prefix, not a stored whole word.
  / \
 r   t        "car" and "cat" are complete words.
```

A small trie can be represented with nested dictionaries. Each one-character key leads to a child. The special `_end` key marks a complete word; it is metadata, not a letter to follow.

```python
trie = {
    "c": {
        "a": {
            "r": {"_end": True},
            "t": {"_end": True},
        }
    }
}

prefix_node = trie["c"]["a"]
assert not prefix_node.get("_end", False)  # "ca" is not a complete word.
assert prefix_node["r"]["_end"]           # "car" is stored.
assert prefix_node["t"]["_end"]           # "cat" is stored.
assert "n" not in prefix_node              # No "can" path.
```

**Add the word `can`:** reuse `c → a` and create only the missing `n` branch.

```python
node = trie  # Start at the root dictionary.
for letter in "can":
    node = node.setdefault(letter, {})
node["_end"] = True

assert trie["c"]["a"]["n"]["_end"]
assert prefix_node["n"] is node  # The earlier reference sees the new branch.
```

`setdefault(letter, {})` returns the existing child dictionary if the letter is
present; otherwise it stores and returns a new empty child. Assigning that result
to `node` moves our reference one level down. The root `trie` stays in place.

```text
(root) → c → a
            /|\
           r t n     car, cat, can are complete words.
```

**Store `ca` as a word too:** marking its existing node does not remove children.

```python
prefix_node["_end"] = True
assert trie["c"]["a"]["_end"]        # "ca" is now a complete word.
assert trie["c"]["a"]["r"]["_end"]   # "car" is still stored.

# Stop treating "ca" as a whole word, but keep its longer words.
prefix_node.pop("_end")
assert not prefix_node.get("_end", False)
assert prefix_node["n"]["_end"]        # "can" is still stored.
```

Deleting `trie["c"]["a"]` instead would remove the entire branch containing
`car`, `cat`, and `can`. The end marker is essential: having a path for a prefix
does not by itself mean that the prefix is a stored word.

**Useful for:** autocomplete and prefix queries. To look up the prefix `ca`, follow two letters; its descendants hold possible completions. If you also store the word `ca`, mark `_end` at that node without removing the longer words.

**Costs:** following/inserting a word of k characters takes average O(k) dictionary operations. The insertion loop uses O(1) working space and creates up to O(k) new nodes; an already stored word reuses its path. Locating a prefix is not the same as listing every completion: enumerating them adds work proportional to what is explored and returned. Storage is O(P) for P distinct nonempty prefixes, plus the root; in the worst case P grows with the total characters stored.

### Union-find: keep track of connected groups

**Why do we need it?** Suppose a company keeps connecting offices with cables.
After each new cable, we want to ask: **“Can office A communicate with office D,
even through other offices?”** Union-find remembers which offices belong to the
same connected group, so we can answer without searching the cable network again.
It is also called a **disjoint-set structure**.

**One example, step by step:**

```text
Action             Actual cables       Connected groups
Start              A   B   C   D       {A} {B} {C} {D}
Connect A to B     A — B   C   D       {A, B} {C} {D}
Connect C to D     A — B   C — D       {A, B} {C, D}
Connect B to C     A — B — C — D       {A, B, C, D}
```

Before the last connection, A cannot reach D. After it, A can reach D through
B and C. **A direct-cable check would miss this indirect connection.**

Union-find has two operations:

| Operation | Meaning |
|---|---|
| `union(a, b)` | Merge the groups containing a and b when a connection is added |
| `find(x)` | Return a representative that identifies x's current group |

Compare `find(a) == find(b)` to check whether two offices belong to the same group.

**Runnable Python example:** a dictionary stores parent links using office names.

```python
parent = {office: office for office in "ABCD"}


def find(office: str) -> str:
    while parent[office] != office:
        office = parent[office]
    return office


def union(a: str, b: str) -> None:
    root_a = find(a)
    root_b = find(b)
    if root_a != root_b:
        parent[root_b] = root_a


union("A", "B")              # Groups: {A, B}, {C}, {D}
union("C", "D")              # Groups: {A, B}, {C, D}
assert find("A") != find("D")  # A cannot reach D yet.

union("B", "C")              # Groups: {A, B, C, D}
assert find("A") == find("D")  # A can now reach D.

# Proposed extra cable A—D: are its endpoints already connected?
assert find("A") == find("D")  # Yes: adding it would create a cycle.
```

**How does it remember groups?** Each group has a representative, or **root**.
A root points to itself; other members follow parent links to reach it.
For this code, the dictionary changes as follows:

```text
After A—B and C—D:  {"A": "A", "B": "A", "C": "C", "D": "C"}
After B—C:          {"A": "A", "B": "A", "C": "A", "D": "C"}

find("D") follows D → C → A and returns "A".
find("A") returns "A" too: same representative, same group.
```

During `union("B", "C")`, B's root is A and C's root is C. Setting
`parent["C"] = "A"` joins the entire C/D group to the A/B group. Always link
**roots**, rather than changing an arbitrary member's parent.
These parent links record group membership; they do not record the actual cables.
The representative is just an internal group label and can change after a merge.

**When is it useful?** Many connectivity checks as connections are added, or
checking whether a proposed edge would create a cycle in an undirected graph.
For one small connectivity question, a BFS/DFS graph search may be enough.
Use a graph search to find the actual route. Basic union-find does not efficiently
handle removing connections and splitting groups.

**Costs:** this simple version has O(n) worst-case time per find/union, O(1)
working space per call, and O(n) total storage and initialization time.
With **path compression** (shorten parent paths) and **union by size/rank**
(keep trees shallow), operations take amortized O(α(n)) time—effectively constant
for practical inputs. See the [algorithms notebook](../../dsa/python_algorithms_notebook.md)
for the optimized implementation.

### Choose the relationship before the algorithm

| What you need to represent | Start with |
|---|---|
| A chain of successors | Linked nodes |
| Keys arranged for ordered search | A balanced search tree |
| Arbitrary connections between items | A graph |
| Shared text prefixes | A trie |
| Groups that repeatedly merge | Union-find |

**Practice aloud:** “Can Library connect to several rooms?” Graph. “Can `car` and `cat` share storage for `ca`?” Trie. “Can offices A and D communicate?” Union-find. The question you need to answer guides the structure you choose.

For complete reversal, traversal, union-find, and shortest-path implementations, use the [algorithms notebook](../../dsa/python_algorithms_notebook.md). This section focuses on what is stored and small updates; the notebook develops the complete algorithms.

## 15. Quick revision and interview practice

| Question | Say this, then give an example |
|---|---|
| List or tuple? | List for a changing sequence; tuple for fixed references. Both can contain mutable objects |
| List or set? | List for positions/order/duplicates; set for uniqueness and average O(1) membership |
| Dict order? | Insertion order, not automatic key/value sorting |
| Dict membership? | `key in mapping` checks keys; searching values is generally O(n) |
| Can a tuple be a key? | Only if every contained element is hashable |
| Can a frozen dataclass be a key? | With the normal generated hash, only if all hashed fields are hashable |
| Queue or heap? | Queue serves arrival order; heap serves the smallest priority |
| Does an in-place change mean O(1) memory? | No; list sorting can use O(n) temporary workspace |
| What does a shallow copy share? | The nested objects, not the outer container |
| List or generator? | Reusable indexed results versus one-pass lazy production |

**Practice by choosing and explaining:**

1. Find student records by ID: use a dictionary; keep IDs hashable and stable.
2. Remember unique visitor IDs: use a set; sort a result list only when ordered output is needed.
3. Process every submitted job in arrival order: use an unbounded deque, not a bounded history deque that discards jobs.
4. Keep the most recent ten readings: use `deque(maxlen=10)`.
5. Count events by category: use `Counter`; group actual records using `defaultdict(list)`.
6. Repeatedly process the smallest deadline/priority: use a heap; include a tie-breaker for non-comparable payloads.

For each answer, say what order/duplicates/mutation are allowed, which operation dominates, and its time/memory cost. Use [the algorithms notebook](../../dsa/python_algorithms_notebook.md) to practice combining these structures into solutions.

References: Python's [built-in types](https://docs.python.org/3.11/library/stdtypes.html), [collections](https://docs.python.org/3.11/library/collections.html), [heapq](https://docs.python.org/3.11/library/heapq.html), [bisect](https://docs.python.org/3.11/library/bisect.html), and [dataclasses](https://docs.python.org/3.11/library/dataclasses.html).
