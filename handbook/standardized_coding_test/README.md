# Standardized Online Coding Test Preparation

This folder is for beginners preparing for timed online coding tests. Do not try
to memorize every solution at once. Learn the small set of patterns that keep
appearing, then practice recognizing which pattern a problem is asking for.

## Beginner Mental Model

Every coding-test problem is usually asking one of four questions:

| Problem is asking... | First idea to try |
|---|---|
| "Have I seen this before?" | Hash map or set |
| "Can I shrink the search space?" | Two pointers or binary search |
| "Is this about a connected structure?" | DFS, BFS, or union-find |
| "Am I recomputing the same answer?" | Dynamic programming |

Use this sentence while solving:

```text
I need to know ______ quickly, so I will use ______.
```

Examples:

```text
I need to know whether a complement was seen quickly, so I will use a hash map.
I need to inspect a sorted array from both ends, so I will use two pointers.
I need the shortest number of steps, so I will use BFS.
```

## What Gets Tested

**Most Common Topics:**
- Arrays & Strings (Sliding window, two pointers, hashing)
- Trees & Graphs (DFS/BFS, BST, shortest paths)
- Linked Lists (Reversal, cycle detection)
- Hash Tables (Counting, pattern matching)
- Dynamic Programming (Memoization, optimization)
- Stacks & Queues (Implementation, use cases)
- Heaps (Priority queues, top-k problems)

**Evaluation Criteria:**
1. **Correctness** - Solution produces correct output
2. **Efficiency** - Time/space complexity appropriate
3. **Code Quality** - Clear names, proper structure
4. **Edge Cases** - Handles null, empty, single element, large inputs
5. **Problem Solving** - Shows optimization thinking

---

## Essential Python Patterns

### Collections Module

**Why these matter:** Online tests often reward choosing the right data
structure more than writing many lines of code. `defaultdict`, `Counter`, and
`deque` solve common bookkeeping problems cleanly.

**defaultdict** - Auto-initializing dictionary
```python
from collections import defaultdict

count = defaultdict(int)
for word in ["apple", "apple", "banana"]:
    count[word] += 1  # No KeyError needed!
# Output: {'apple': 2, 'banana': 1}
```

**Counter** - Frequency counting
```python
from collections import Counter

count = Counter([1, 1, 1, 2, 2, 3])
print(count.most_common(2))  # [(1, 3), (2, 2)]
```

**deque** - Double-ended queue (essential for BFS!)
```python
from collections import deque

queue = deque([1, 2, 3])
queue.append(4)        # Add to right: deque([1, 2, 3, 4])
queue.popleft()        # Remove from left: deque([2, 3, 4])
queue.appendleft(0)    # Add to left: deque([0, 2, 3, 4])
```

### ⚠️ CRITICAL: Why deque.popleft() is Essential

Using `list.pop(0)` in BFS causes **O(n²) complexity** instead of O(n):

```
PROBLEM: list.pop(0) shifts all remaining elements left

Before:  [A][B][C][D][E]
After:   [B][C][D][E]  ← Every element moved!

In BFS with n nodes:
pop(0) #1: shift n-1 elements = n operations
pop(0) #2: shift n-2 elements = n-1 operations
...
pop(0) #n: shift 0 elements = 1 operation

Total: n + (n-1) + ... + 1 = n(n+1)/2 = O(n²) ❌
```

**For n=1000:** 500K operations (timeout!)
**For n=10000:** 50M operations (crash!)

**Solution:** Use `deque.popleft()` = O(1) per operation = O(n) total ✓

---

## Algorithm Patterns (8 Essential Types)

### 1. Two Pointers ⭐⭐⭐ (Essential)
**Use for:** Sorted arrays, pairs, palindromes, reversals

**Mental note:** Two pointers means "look from two places at once." Usually the
pointers move toward each other or move together through the input.

**Recognize it when:** The problem mentions a sorted array, a pair, reversing, or
checking from both ends.

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1
    return []

# Input: arr=[1, 2, 3, 5, 8], target=13
# Output: [3, 4]  (5+8=13)
```

### 2. Sliding Window ⭐⭐⭐ (Essential)
**Use for:** Substrings, subarrays, max/min windows

**Mental note:** A sliding window is a moving slice of an array or string. You
add the new right item and remove the old left item instead of recomputing the
whole slice.

**Recognize it when:** The problem asks for a longest, shortest, maximum, or
minimum contiguous subarray/substring.

```python
def max_window_sum(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)
    return max_sum

# Input: arr=[1,3,2,6,-1,4,1,8], k=3
# Output: 13  (window [4,1,8])
```

### 3. Hash Map Counting ⭐⭐⭐ (Essential)
**Use for:** Frequencies, anagrams, lookups

**Mental note:** A hash map is memory used to avoid scanning again. If the brute
force solution repeatedly searches for something, a dictionary or set may remove
that repeated work.

**Recognize it when:** The problem asks about frequency, duplicates, matching,
anagrams, pairs, or "seen before."

```python
from collections import Counter

def top_k_frequent(arr, k):
    count = Counter(arr)
    return [num for num, _ in count.most_common(k)]

# Input: arr=[1,1,1,2,2,3], k=2
# Output: [1, 2]  (1 appears 3x, 2 appears 2x)
```

### 4. DFS (Depth-First Search) ⭐⭐⭐ (Essential)
**Use for:** Paths, cycles, trees, backtracking

**Mental note:** DFS goes deep before it goes wide. Think "follow one path until
you cannot continue, then back up."

**Recognize it when:** The problem asks about all paths, connected components,
tree recursion, islands, permutations, combinations, or backtracking.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    # Use .get() to handle nodes that don't exist as keys
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

# Input: graph={1:[2,3], 2:[4], 3:[5]}, start=1
# Output: {1, 2, 3, 4, 5}
```

### 5. BFS (Breadth-First Search) ⭐⭐⭐ (Essential)
**Use for:** Shortest paths, level-order traversal

**Mental note:** BFS explores by distance. It visits everything 1 step away,
then 2 steps away, then 3 steps away.

**Recognize it when:** The problem asks for shortest path in an unweighted graph,
minimum moves, level order, or nearest target.

```python
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result

# Input: graph={1:[2,3], 2:[4], 3:[5]}, start=1
# Output: [1, 2, 3, 4, 5]
```

### 6. Binary Search ⭐⭐ (Important)
**Use for:** Sorted arrays, rotated arrays, boundaries

**Mental note:** Binary search works when one answer lets you throw away half of
the remaining search space.

**Recognize it when:** The input is sorted, or the problem asks for the first,
last, minimum valid, maximum valid, or boundary position.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Input: arr=[1,3,5,7,9], target=7
# Output: 3
```

### 7. Dynamic Programming (Memoization) ⭐⭐⭐ (Essential)
**Use for:** Overlapping subproblems, optimization

**Mental note:** Dynamic programming means "do not solve the same smaller problem
again." Store the answer the first time.

**Recognize it when:** Recursive brute force repeats states, or the problem asks
for number of ways, best score, minimum cost, or maximum value.

```python
def fibonacci(n, memo=None):
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]
    if n <= 1:
        return n

    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]

# Input: n=10
# Output: 55
```

### 8. Heaps ⭐⭐ (Important)
**Use for:** Priority queues, top-k problems, min/max

**Mental note:** A heap keeps the next smallest or next largest item easy to
remove. For top-k, keep only k useful items instead of sorting everything.

**Recognize it when:** The problem asks for kth largest, top k, merge k sorted
lists, scheduling by priority, or repeatedly taking the smallest/largest item.

```python
from heapq import heappush, heappop

def kth_largest(arr, k):
    heap = []
    for num in arr:
        heappush(heap, num)
        if len(heap) > k:
            heappop(heap)
    return heap[0]

# Input: arr=[3,2,1,5,6,4], k=2
# Output: 5  (2nd largest)
```

---

## Key Data Structures

### Time Complexity Reference

**How to use this table:** Pick the structure whose common operation is fast.
For example, if you need many membership checks, a hash map or set usually beats
a list.

| Operation | Array | Hash Map | Linked List | Deque | Heap |
|-----------|-------|----------|-------------|-------|------|
| Access | O(1) | O(1) avg | O(n) | O(1) | O(n) |
| Insert | O(n) | O(1) avg | O(1) | O(1) | O(log n) |
| Delete | O(n) | O(1) avg | O(1) | O(1) | O(log n) |
| Search | O(n) | O(1) avg | O(n) | O(n) | O(n) |

### Data Structures to Implement

**From data_structures.py:**
- Linked List (single)
- Binary Tree
- Binary Search Tree
- Graph (adjacency list)
- Stack
- Queue
- Trie (prefix tree)

---

## Index-Based BFS Alternative

**When you can't use deque**, an index-based approach is valid O(n):

```python
def bfs_with_index(graph, start):
    """Same O(n) complexity as deque, no import needed"""
    queue = [start]
    visited = {start}
    result = []
    index = 0  # Pointer to current node

    while index < len(queue):
        node = queue[index]
        index += 1  # Move pointer forward
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result
```

**Comparison:**
| Approach | Time | Space | Pros | Cons |
|----------|------|-------|------|------|
| list.pop(0) | O(n²) ❌ | O(n) | No import | SLOW for large n |
| deque | O(n) ✓ | O(n) | Optimal | Requires import |
| Index-based | O(n) ✓ | O(n) | No import, clear | Less familiar |

**When to use each:**
- **deque**: Standard choice, most familiar, no downside
- **Index-based**: When you want to avoid imports or just list operations
- **list.pop(0)**: NEVER in time-critical code

**Note:** Sliding window maximum uses monotonic deque (requires both ends), so index-based won't work there.

---

## Common Algorithm Mistakes

| Mistake | Fix |
|---------|-----|
| Off-by-one errors | Double-check loop bounds carefully |
| Using list.pop(0) in BFS | Use deque.popleft() instead |
| Wrong data structure choice | Pick based on access patterns |
| Inefficient nested loops | Use hash maps or two pointers |
| Not handling edge cases | Test: empty, null, single, large |
| Forgetting base case in recursion | Verify base cases work |
| Mutating list while iterating | Iterate backwards or use copy |
| Mutable default arguments | Use None and initialize in function |

---

## What To Say In An Interview

For each solution, practice this four-line explanation:

```text
1. Brute force would be ______ and costs ______.
2. I can improve it by using ______ because ______.
3. The algorithm is ______.
4. Time is ______ and space is ______.
```

Example:

```text
Brute force Two Sum checks every pair and costs O(n^2).
I can improve it with a hash map because I need fast complement lookup.
I scan once and store numbers I have already seen.
Time is O(n), space is O(n).
```

## Pre-Test Checklist

**Pattern Knowledge - can you code these without help?**
- [ ] Two pointers (sorted array pairs)
- [ ] Sliding window (subarray max sum)
- [ ] Hash counting (top-k frequent)
- [ ] DFS and BFS from memory
- [ ] Binary search (standard + variants)
- [ ] DP with memoization

**Data Structures - can you implement?**
- [ ] Linked list with all operations
- [ ] Binary tree and BST
- [ ] Graph and adjacency list
- [ ] Stack, queue, trie basics

**Problem Solving - are you ready?**
- [ ] Estimate time complexity quickly
- [ ] Recognize problem patterns instantly
- [ ] Handle edge cases automatically
- [ ] Code clearly even under pressure

**Test Readiness:**
- [ ] Practiced 5+ problems with timing
- [ ] Know when to move on (>15 min stuck)
- [ ] Familiar with your IDE
- [ ] Comfortable with 70-minute strategy

---

## During Test

1. **Read all problems** (5 min) - Identify patterns, choose order
2. **Solve easiest** (15-20 min) - Build confidence
3. **Solve medium** (25-35 min) - Demonstrate skill
4. **Attempt hard** (remaining) - Get partial credit
5. **Final check** (5 min) - Syntax, edge cases, submit

**If stuck on a problem:**
- Spend max 15 minutes understanding
- Try simpler version first
- Partial solution is better than none
- Move to next problem

---

## File Guide

- **README.md** (this file) - Core concepts and patterns
- **gca_cheatsheet.md** - Quick reference with difficulty levels
- **common_patterns.py** - 34 algorithm implementations with examples
- **data_structures.py** - 7 data structures with all operations
- **practice_problems.py** - 18 solved problems (Easy/Medium/Hard)
- **sample_test_walkthrough.md** - Full 70-minute test simulation
- **Outline.md** - Navigation and file descriptions

---

## Success Tips

**Correctness First**
- Make it work before optimizing
- Test thoroughly with examples

**Time Management**
- Don't get stuck on one problem
- Move on if you're not making progress
- Partial solutions count

**Code Quality**
- Clear variable names
- Comments for complex logic
- No unnecessary complexity

**Testing**
- Work through examples manually
- Test edge cases explicitly
- Verify output format

---

*CodeSignal GCA Assessment Guide | Lead Software Engineer Position*
