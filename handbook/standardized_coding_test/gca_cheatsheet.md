# CodeSignal GCA Assessment - Quick Cheatsheet

**70 minutes | 2-3 problems | Intermediate to Hard**

**During Preparation:** Use this as quick reference while studying
**During Test:** Quick memory jogger for pattern names and imports

## How Beginners Should Use This Sheet

This sheet is not for memorizing every line. Use it to recognize problem shapes.

Before coding, pause and ask:

```text
1. What is the input shape? array, string, tree, graph, intervals?
2. What do I need quickly? membership, count, min/max, next node?
3. Which pattern gives that quickly?
4. What edge case can break it?
```

Mental shortcut:

```text
Repeated lookup  -> dict or set
Contiguous range -> sliding window
Sorted input     -> two pointers or binary search
Shortest steps   -> BFS
All paths        -> DFS/backtracking
Top K            -> heap or Counter
Repeated states  -> dynamic programming
```

**Difficulty Levels:**
- ⭐ = Essential (appears in 70% of tests)
- ⭐⭐ = Important (appears in 40% of tests)
- ⭐⭐⭐ = Advanced (appears in 20% of tests)

---

## Python Essentials - Quick Conversions

### String <-> List Conversion
```python
s = "hello world"
s.split()                    # ['hello', 'world']
s.split(',')                 # Split by comma
' '.join(['hello', 'world']) # 'hello world'

# Reverse
s[::-1]                      # 'dlrow olleh'
list(reversed(s))            # ['d','l','r','o','w',' ','o','l','l','e','h']
```

### Set Operations
```python
list1 = [1, 2, 3]
list2 = [2, 3, 4]
set(list1) & set(list2)  # {2, 3}  intersection
set(list1) | set(list2)  # {1,2,3,4}  union
set(list1) - set(list2)  # {1}  difference
```

### Sorting & Type Conversion
```python
arr = [3, 1, 4, 1, 5]
sorted(arr)              # [1, 1, 3, 4, 5]
sorted(arr, reverse=True) # [5, 4, 3, 1, 1]

int('123')   # 123
str(123)     # '123'
float('3.14') # 3.14
list('abc')  # ['a', 'b', 'c']
```

### Built-in Functions
```python
len(arr)                # 5
max(arr)                # 5
min(arr)                # 1
sum(arr)                # 14
list(enumerate(arr))    # [(0,3), (1,1), (2,4), (3,1), (4,5)]
list(zip([1,2], [3,4])) # [(1,3), (2,4)]
```

---

## Essential Imports

```python
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop, heapify
import bisect
```

---

## Algorithm Patterns at a Glance

### Two Pointers ⭐⭐⭐
**When:** Sorted arrays, pairs, palindromes
**Template:** Start at edges, move towards center
**Mental note:** Move the pointer that cannot help anymore.
**See:** README.md or common_patterns.py for full implementation

### Sliding Window ⭐⭐⭐
**When:** Substrings, subarrays, max/min windows
**Template:** Expand/contract window, track state in hash map
**Mental note:** Reuse the previous window instead of recomputing from scratch.
**See:** README.md or common_patterns.py for full implementation

### Hash Map Counting ⭐⭐⭐
**When:** Frequencies, anagrams, duplicates, lookups
**Use:** Counter for frequencies, defaultdict for default values
**Mental note:** Spend memory to avoid repeated searching.
**See:** README.md or common_patterns.py for full implementation

### DFS (Depth-First Search) ⭐⭐⭐
**When:** Paths, cycles, backtracking, permutations
**Template:** Recursive or use stack, track visited nodes
**Mental note:** Go deep, then backtrack.
**See:** README.md or common_patterns.py for full implementation

### BFS (Breadth-First Search) ⭐⭐⭐
**When:** Shortest paths, level-order, connected components
**Template:** Use deque (NOT list.pop(0)!), track visited
**Mental note:** BFS explores by distance: 1 step, then 2 steps, then 3.
**See:** README.md or common_patterns.py for full implementation

### Binary Search ⭐⭐
**When:** Sorted arrays, rotated arrays, boundaries
**Template:** left=0, right=len-1, while left<=right, mid=(left+right)//2
**Mental note:** You need a rule that discards half the search space.
**See:** README.md or common_patterns.py for full implementation

### Dynamic Programming (Memoization) ⭐⭐⭐
**When:** Overlapping subproblems, optimization
**Template:** Use dict for memo, check cache first
**Mental note:** If recursion repeats the same state, store the answer.
**See:** README.md or common_patterns.py for full implementation

### Heaps ⭐⭐
**When:** Priority queues, top-k problems, min/max
**Template:** heappush, heappop, heapify
**Mental note:** Keep only the best k items instead of sorting everything.
**See:** README.md or common_patterns.py for full implementation

---

## Time Complexity Quick Reference

| Operation | Complexity |
|-----------|-----------|
| Array access | O(1) |
| Array search | O(n) |
| Binary search | O(log n) |
| Array sort | O(n log n) |
| Hash lookup | O(1) avg |
| Hash insert/delete | O(1) avg |
| Heap insert/extract | O(log n) |
| Tree search (balanced) | O(log n) |
| Tree search (unbalanced) | O(n) |
| Graph DFS/BFS | O(V + E) |
| Two pointers | O(n) |
| Sliding window | O(n) |

---

## Common Data Structures

| Structure | Access | Insert | Delete | Search |
|-----------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(1) | O(1) | O(n) |
| Hash Map | O(1) | O(1) | O(1) | O(1) |
| Stack | - | O(1) | O(1) | - |
| Queue | - | O(1) | O(1) | - |
| Heap | - | O(log n) | O(log n) | O(n) |
| Tree (balanced) | - | O(log n) | O(log n) | O(log n) |

---

## Problem Categories

### String/Array
- Palindrome: Two pointers or expand-around-center
- Anagram: Counter or sorted comparison
- Substring: Sliding window
- Pattern match: Two pointers or hashing

### Linked List
- Reverse: Three pointers (prev, curr, next)
- Cycle: Fast/slow pointers
- Merge: Dummy node + comparison

### Tree
- Traversal: Recursive or iterative with stack
- Path: DFS with sum tracking
- Level-order: BFS with deque
- Validate: Constraint tracking

### Graph
- Connected: DFS/BFS or Union-Find
- Shortest path: BFS or Dijkstra
- Cycle: DFS or Union-Find
- Topo sort: DFS or Kahn's algorithm

### Dynamic Programming
- Fibonacci: Memoization
- Coin change: DP optimization
- Longest sequence: 2D DP
- Edit distance: String DP

---

## Edge Cases Checklist

- [ ] Empty input (null, empty list/string)
- [ ] Single element
- [ ] Duplicates
- [ ] Negative numbers
- [ ] Very large numbers
- [ ] All same elements
- [ ] Already sorted/reversed
- [ ] No valid solution

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Off-by-one errors | Double-check loop bounds |
| list.pop(0) in BFS | Use deque.popleft() instead |
| Wrong data structure | Choose by access patterns |
| Inefficient nested loops | Use hash maps or two pointers |
| Modifying list while iterating | Iterate in reverse or use copy |
| Not initializing variables | Set defaults before loops |
| Forgetting edge cases | Test empty, null, single |
| Mutable default arguments | Use None and initialize in function |

---

## String Methods

```python
s = "Hello World"
s.lower()                 # 'hello world'
s.upper()                 # 'HELLO WORLD'
s.strip()                 # Remove leading/trailing spaces
s.split()                 # ['Hello', 'World']
s.replace("World", "Python") # 'Hello Python'
s.startswith("Hello")     # True
s.find("World")           # 6 (index)
```

---

## List Methods

```python
arr = [1, 2, 3, 2, 4]
arr.append(5)       # [1, 2, 3, 2, 4, 5]
arr.pop()           # Remove last, returns 5
arr.pop(1)          # Remove at index 1
arr.insert(1, 99)   # Insert at index 1
arr.remove(99)      # Remove first 99
arr.count(2)        # Count occurrences
arr.index(3)        # Find index of 3
arr.reverse()       # Reverse in-place
arr.sort()          # Sort in-place
```

---

## Dictionary Methods

```python
d = {"a": 1, "b": 2, "c": 3}
d.get("a")           # 1
d.get("z", -1)       # -1 (default)
d.keys()             # ['a', 'b', 'c']
d.values()           # [1, 2, 3]
list(d.items())      # [('a',1), ('b',2), ('c',3)]
d.pop("b")           # Remove and return value
```

---

## Debugging Tips

1. **Print intermediate values** - Verify calculations
2. **Test with simple examples** - Before complex cases
3. **Check loop bounds** - Off-by-one is common
4. **Verify base cases** - Critical for recursion
5. **Trace through code** - Manually with examples
6. **Check data types** - int vs string, etc.
7. **Look for null/empty** - Edge case handling

---

## When Stuck on a Problem

1. **Re-read** problem statement carefully
2. **Work through** example by hand
3. **Identify pattern** - Two pointers? Sliding window? DFS?
4. **Write pseudocode** - Before actual code
5. **Try brute force** - Get something working first
6. **Optimize** - If you have working solution
7. **Move on** - If stuck 15+ minutes

---

## Pre-Test Checklist

### Pattern Knowledge
- [ ] Can you code two pointers without help?
- [ ] Do you understand why deque beats list.pop(0)?
- [ ] Can you implement DFS and BFS from memory?
- [ ] Do you know when to use dynamic programming?
- [ ] Can you recognize hash map vs sliding window problems?

### Data Structures
- [ ] Linked list with insert/delete/traverse
- [ ] Binary tree and BST operations
- [ ] Graph with adjacency list
- [ ] Stack, queue, heap basics
- [ ] Trie for string problems

### Problem Solving
- [ ] Estimate time complexity quickly
- [ ] Recognize problem patterns instantly
- [ ] Handle edge cases automatically
- [ ] Code clearly even under pressure
- [ ] Know when to move on (>15 min stuck)

### Test Readiness
- [ ] Practiced 5+ problems with timing
- [ ] Know the 70-minute strategy
- [ ] Comfortable with your IDE
- [ ] Got good sleep before test
- [ ] Know common mistakes to avoid

### Result
- **✓ YES to all?** → You're ready for the test!
- **✗ Some NO?** → Review those weak areas
- **✗ Many NO?** → Spend more time on fundamentals

---

## Test Day Strategy

**0-5 min:** Read all problems, identify patterns, choose order
**5-25 min:** Solve easiest problem (build confidence)
**25-55 min:** Solve medium problem (demonstrate knowledge)
**55-65 min:** Solve hard or polish medium
**65-70 min:** Final review and submit

**Key Rules:**
- Start with easiest (not first)
- Correctness before optimization
- Partial solution > no solution
- Don't spend 30+ min on one problem

---

## Final Tips

✓ **Correctness first** - Optimize after it works
✓ **Test thoroughly** - Edge cases matter
✓ **Partial solutions** - Better than nothing
✓ **Clear code** - Beats clever code
✓ **Manage time** - Don't get stuck
✓ **Stay calm** - You're prepared!

---

*CodeSignal GCA Assessment | Lead Software Engineer*
