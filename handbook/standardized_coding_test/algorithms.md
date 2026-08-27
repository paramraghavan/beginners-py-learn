# Core Algorithms

## 0. Understanding Time & Space Complexity

Before diving into algorithms, let's understand HOW to calculate complexity, not just what it means.

### Time Complexity: How to Calculate

**Basic Rule:** Count the number of operations as n grows.

#### Example 1: Single Loop - O(n)
```python
def print_all(arr):
    for i in range(len(arr)):  # Loop runs n times
        print(arr[i])          # 1 operation per iteration

# For arr with n=5 elements: 5 operations
# For arr with n=1000 elements: 1000 operations
# For arr with n elements: n operations
# Complexity: O(n)
```

**Calculation:**
```
Operations count:
n=5:     5 operations
n=10:    10 operations
n=100:   100 operations
n=1000:  1000 operations

Pattern: operations = n
Therefore: O(n)
```

#### Example 2: Nested Loop - O(n²)
```python
def compare_all_pairs(arr):
    count = 0
    for i in range(len(arr)):        # Outer loop: n times
        for j in range(len(arr)):    # Inner loop: n times (for each outer iteration)
            count += 1               # 1 operation per inner iteration

    return count

# Let's trace for n=3: [a, b, c]
# i=0: j loops 3 times (0,1,2) = 3 operations
# i=1: j loops 3 times (0,1,2) = 3 operations
# i=2: j loops 3 times (0,1,2) = 3 operations
# Total: 3 + 3 + 3 = 9 operations = 3 × 3 = 3²

print(compare_all_pairs([1, 2, 3]))  # Output: 9
```

**Calculation:**
```
Operations count:
n=2:     4 operations (2 × 2)
n=3:     9 operations (3 × 3)
n=4:     16 operations (4 × 4)
n=5:     25 operations (5 × 5)
n=10:    100 operations (10 × 10)
n=100:   10,000 operations (100 × 100)
n=1000:  1,000,000 operations (1000 × 1000)

Pattern: operations = n × n = n²
Therefore: O(n²)
```

#### Example 3: Partial Loop - O(n/2) = O(n)
```python
def first_half_only(arr):
    for i in range(len(arr) // 2):  # Only loop through half
        print(arr[i])

# For n=100: 50 operations
# For n=1000: 500 operations

# We ignore constants in Big O!
# O(n/2) = O(n) because:
# As n grows, the /2 becomes insignificant
# 1000 vs 500 operations? Same order of magnitude
# Both are "linear"
```

**Key Insight:** In Big O, we only care about the dominant term and ignore constants!

```
O(n/2)      → O(n)      (ignore constant 1/2)
O(2n)       → O(n)      (ignore constant 2)
O(n² + n)   → O(n²)     (n² dominates n)
O(n³ + n²)  → O(n³)     (n³ dominates n²)
```

#### Example 4: Nested Partial Loop - O(n²/4) = O(n²)
```python
def partial_nested(arr):
    count = 0
    for i in range(len(arr) // 2):      # Half the outer loop
        for j in range(len(arr) // 2):  # Half the inner loop
            count += 1

    return count

# For n=4:   2 × 2 = 4 operations
# For n=8:   4 × 4 = 16 operations
# For n=100: 50 × 50 = 2,500 operations
# Pattern: (n/2) × (n/2) = n²/4

# But O(n²/4) = O(n²)! (ignore constant 1/4)
```

#### Example 5: Sequential Loops (not nested!) - O(n)
```python
def sequential_not_nested(arr):
    # First loop
    for i in range(len(arr)):  # n operations
        print(f"First: {arr[i]}")

    # Second loop
    for i in range(len(arr)):  # n operations
        print(f"Second: {arr[i]}")

# Total: n + n = 2n operations
# For n=100: 200 operations
# For n=1000: 2000 operations

# O(2n) = O(n)! Sequential adds, not multiplies
```

**Key Insight:**
- **Nested loops:** Multiply → O(n × n) = O(n²)
- **Sequential loops:** Add → O(n + n) = O(n)

#### Example 6: Binary Search - O(log n)
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1      # Eliminate right half
        else:
            right = mid - 1     # Eliminate left half

# Each iteration eliminates half the remaining elements
# n=16: iterations = 16 → 8 → 4 → 2 → 1 = 4 iterations
# n=32: iterations = 32 → 16 → 8 → 4 → 2 → 1 = 5 iterations
# n=1000: iterations ≈ 10
```

**Calculation:**
```
How many times can we divide n by 2 until we reach 1?

n=2:    2 → 1            = 1 iteration
n=4:    4 → 2 → 1        = 2 iterations
n=8:    8 → 4 → 2 → 1    = 3 iterations
n=16:   16 → 8 → 4 → 2 → 1 = 4 iterations
n=1000: ≈ 10 iterations

This is logarithm! log₂(n)
n=2:    log₂(2) = 1
n=4:    log₂(4) = 2
n=8:    log₂(8) = 3
n=16:   log₂(16) = 4
n=1000: log₂(1000) ≈ 10

Pattern: iterations = log₂(n)
Therefore: O(log n)
```

#### Common Time Complexities (from fastest to slowest)
```
O(1)        → 1 operation (constant)
O(log n)    → ~10 ops for n=1000 (very fast!)
O(n)        → 1000 ops for n=1000
O(n log n)  → ~10,000 ops for n=1000
O(n²)       → 1,000,000 ops for n=1000 (slow!)
O(n³)       → 1,000,000,000 ops for n=1000 (very slow!)
O(2ⁿ)       → Too many to count! (impossibly slow)
O(n!)       → Even slower than 2ⁿ
```

### Space Complexity: How to Calculate

**Basic Rule:** Count the extra memory used as n grows (NOT including input).

#### Example 1: Constant Space - O(1)
```python
def find_max(arr):
    max_val = float('-inf')  # 1 variable
    for num in arr:
        if num > max_val:
            max_val = num

    return max_val

# No matter how large arr is:
# - max_val always uses same memory
# - loop variable i uses same memory
# - Total extra space: constant

# For n=10:     O(1)
# For n=1000:   O(1)
# For n=1M:     O(1)
# Pattern: Space doesn't grow with n
# Therefore: O(1)
```

#### Example 2: Linear Space - O(n)
```python
def create_new_array(arr):
    new_arr = [x * 2 for x in arr]  # Creates array of size n
    return new_arr

# new_arr uses n elements of memory
# For n=10:     needs 10 spaces
# For n=100:    needs 100 spaces
# For n=1000:   needs 1000 spaces

# Pattern: Space = n
# Therefore: O(n)
```

#### Example 3: Quadratic Space - O(n²)
```python
def create_matrix(n):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(i * j)
        matrix.append(row)

    return matrix

# Creates n × n matrix = n² elements
# For n=10:     100 elements
# For n=100:    10,000 elements
# For n=1000:   1,000,000 elements

# Pattern: Space = n²
# Therefore: O(n²)
```

#### Example 4: Recursion Stack Space - O(n)
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Recursive call

# Call stack grows with n:
# factorial(5):
#   → factorial(4):
#     → factorial(3):
#       → factorial(2):
#         → factorial(1): [depth = 5]

# For n=10:     10 calls on stack = O(10)
# For n=100:    100 calls on stack = O(100)
# For n=1000:   1000 calls on stack = O(1000)

# Pattern: Stack depth = n
# Therefore: O(n)
```

#### Example 5: Recursion with Memoization - O(n)
```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}  # Create dictionary

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Space used:
# - memo dictionary: stores n entries
# - call stack: maximum depth = n
# Total: O(n) + O(n) = O(n)

# For n=100: memo stores 100 values + stack depth 100
# Pattern: Space = n
# Therefore: O(n)
```

#### Example 6: BFS with Queue - O(n)
```python
from collections import deque

def bfs(graph, start):
    visited = set()           # Can store up to n nodes
    queue = deque([start])    # Can store up to n nodes

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        queue.extend(graph.get(node, []))

    return visited

# Space used:
# - visited set: stores up to n nodes
# - queue: stores up to n nodes
# Total: O(n) + O(n) = O(n) (constants don't matter!)

# For n=1000 nodes: visited could have 1000, queue could have 1000
# Pattern: Space = n
# Therefore: O(n)
```

### Time vs Space Trade-off

Often you can trade time for space or vice versa:

```python
# SPACE-EFFICIENT (O(1) space, O(n²) time)
def find_duplicate_slow(arr):
    for i in range(len(arr)):           # O(n)
        for j in range(i+1, len(arr)):  # O(n)
            if arr[i] == arr[j]:
                return True
    return False

# TIME-EFFICIENT (O(n) space, O(n) time)
def find_duplicate_fast(arr):
    seen = set()  # Extra O(n) space!
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False

# For n=1000000:
# Slow version: 1 trillion operations, minimal memory
# Fast version: 1 million operations, needs 1M memory
# Fast is worth the extra memory!
```

### Calculating Complexity: Step-by-Step Framework

**For Time Complexity:**
1. Count operations in each loop
2. Multiply for nested loops, add for sequential
3. Keep only highest power and ignore constants
4. Examples: O(n+m), O(n²), O(n log n), etc.

**For Space Complexity:**
1. Count variables used
2. Count recursion depth or data structures created
3. Add all sources (ignore constants)
4. Examples: O(1), O(n), O(log n), etc.

### Quick Reference: Complexity Calculations

| Code Pattern | Time | Space | Why? |
|---|---|---|---|
| `for i in range(n):` | O(n) | O(1) | Loop n times |
| `for i in range(n): for j in range(n):` | O(n²) | O(1) | n × n iterations |
| `while n > 1: n = n // 2` | O(log n) | O(1) | Divide by 2 each time |
| `arr = [0] * n` | O(n) | O(n) | Create array of size n |
| `def func(n): func(n-1)` | O(n) | O(n) | n recursive calls = n stack depth |
| `if/else` | O(1) | O(1) | Single check |
| Hash lookup | O(1) | O(n) | For n items in hash |
| Sort | O(n log n) | O(n) | Standard sorting |

---

## 1. Iteration & Loops

### Theory
The foundation of programming. Iteration allows you to repeat operations on collections of data without writing the code multiple times.

### Basic Loop (For Loop)
```python
# Process each element in a sequence
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(num * 2)
# Output: 2, 4, 6, 8, 10
```

**Time Complexity:** O(n) - visits each element once
**Space Complexity:** O(1) - uses constant extra space
**Use Cases:** Array processing, list traversal, simple searches

### Nested Loops
```python
# Compare all pairs
arr = [1, 2, 3]
for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
        print(f"Pair: ({arr[i]}, {arr[j]})")
# Output: (1, 2), (1, 3), (2, 3)
```

**Time Complexity:** O(n²) - visits every combination
**Space Complexity:** O(1)
**Use Cases:** Comparing elements, finding pairs, checking all combinations

### While Loop
```python
# Repeat until condition is false
count = 0
while count < 5:
    print(count)
    count += 1
# Output: 0, 1, 2, 3, 4
```

**Time Complexity:** Depends on condition
**Use Cases:** Unknown iteration count, game loops, input validation

---

## 2. Recursion

### Theory
A function calling itself to solve smaller versions of the same problem. Requires:
1. **Base case** - stop condition
2. **Recursive case** - break problem into smaller piece

### Simple Recursion
```python
def countdown(n):
    """Base case: when n reaches 0, stop"""
    if n == 0:
        return
    print(n)
    countdown(n - 1)  # Recursive call with smaller input

countdown(5)
# Output: 5, 4, 3, 2, 1
```

**Time Complexity:** O(n) - makes n calls
**Space Complexity:** O(n) - call stack depth
**Use Cases:** Tree/graph traversal, divide-and-conquer, backtracking

### Tree Recursion
```python
def sum_array(arr, index=0):
    """Recursive array summation"""
    # Base case: no more elements
    if index == len(arr):
        return 0
    # Recursive case: current + sum of rest
    return arr[index] + sum_array(arr, index + 1)

print(sum_array([1, 2, 3, 4]))  # Output: 10
```

**Time Complexity:** O(n)
**Space Complexity:** O(n) - recursion depth
**Use Cases:** Simple array processing, tree traversals

### Pros and Cons of Recursion

#### ✅ Advantages
1. **Natural for tree/graph problems** - Mirror the problem structure
2. **Clean, readable code** - Mirrors mathematical definitions
3. **Easier to understand** - Less code, more intuitive
4. **Divide-and-conquer** - Naturally expresses problem breakdown
5. **No manual stack** - Python handles call stack automatically

#### ❌ Disadvantages
1. **Stack overflow risk** - Deep recursion uses lots of memory
2. **Slower than iteration** - Function call overhead
3. **Recursion limit** - Python has default limit of ~1000
4. **Debugging harder** - Stack trace gets very long
5. **Memory inefficiency** - Each call stores frame on stack

**When to Avoid Recursion:**
- Large n values (n > 1000)
- Need maximum performance
- Memory is limited
- No natural recursive structure

### Converting Recursion to Iteration

#### Method 1: Using Stack (for DFS-like recursion)

**Recursive Version:**
```python
def traverse_recursive(node):
    """Recursive tree traversal"""
    if not node:
        return []
    result = [node.val]
    result.extend(traverse_recursive(node.left))
    result.extend(traverse_recursive(node.right))
    return result
```

**Iterative Version (using stack):**
```python
def traverse_iterative(root):
    """Convert recursion to iteration using explicit stack"""
    if not root:
        return []

    stack = [root]  # Explicit stack replaces recursion
    result = []

    while stack:
        node = stack.pop()  # Process node
        result.append(node.val)

        # Add children to stack (in reverse order for correct order)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result

# Both produce same output!
# Input: Tree with root=1, left=2, right=3
# Output: [1, 2, 3]
# Time: O(n), Space: O(n)
```

**Key Principle:** Replace recursive calls with explicit stack.push()

#### Method 2: Using Queue (for BFS-like recursion)

**Recursive (level-order):**
```python
def level_order_recursive(root, level=0, result=None):
    """Recursive level-order traversal"""
    if result is None:
        result = []

    if not root:
        return result

    if level == len(result):
        result.append([])

    result[level].append(root.val)
    level_order_recursive(root.left, level + 1, result)
    level_order_recursive(root.right, level + 1, result)

    return result
```

**Iterative (using queue):**
```python
from collections import deque

def level_order_iterative(root):
    """Convert to iteration using queue"""
    if not root:
        return []

    queue = deque([root])  # Queue replaces recursion
    result = []

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result

# Both produce same output!
# Input: Tree with root=1, left=2, right=3
# Output: [[1], [2, 3]]
# Time: O(n), Space: O(n)
```

**Key Principle:** Replace recursion with queue for level-by-level processing.

#### Method 3: Using Memoization (for recursive optimization)

**Inefficient Recursion (recalculates):**
```python
def fib_slow(n):
    """Multiple calls to same n"""
    if n <= 1:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

# fib_slow(5):
#   fib_slow(4) + fib_slow(3)
#   fib_slow(3) + fib_slow(2) + fib_slow(2) + fib_slow(1)
#   Calculates fib(2) THREE times!
```

**Optimized Recursion (memoization):**
```python
def fib_memo(n, memo=None):
    """Cache results"""
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]  # Return cached result

    if n <= 1:
        return n

    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# fib_memo(5):
#   Calculates each n only ONCE
#   O(n) instead of O(2^n)!
```

**Key Principle:** Cache results to avoid recalculation.

#### Method 4: Tail Recursion → Iteration

**Tail Recursive (last call is recursive):**
```python
def factorial_tail(n, acc=1):
    """Tail recursion - last operation is recursive call"""
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)  # Recursive call is last

# Can be directly converted to loop
```

**Iterative:**
```python
def factorial_iter(n):
    """Simple loop - no recursion"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial_iter(5))  # Output: 120
# Input: n=5
# Output: 120
# Time: O(n), Space: O(1) - much better!
```

**Key Principle:** Tail recursion can always be converted to simple loop.

#### Method 5: Dynamic Programming (for complex recursion)

**Complex Recursion:**
```python
def coin_change_recursive(coins, amount):
    """Recursive but very slow"""
    if amount == 0:
        return 0

    min_coins = float('inf')
    for coin in coins:
        if coin <= amount:
            min_coins = min(min_coins, 1 + coin_change_recursive(coins, amount - coin))

    return min_coins

# Very slow! Recalculates same amounts repeatedly
```

**DP Solution (bottom-up iteration):**
```python
def coin_change_dp(coins, amount):
    """Iterative DP - replaces complex recursion"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], 1 + dp[i - coin])

    return dp[amount]

print(coin_change_dp([1, 2, 5], 5))
# Input: coins=[1,2,5], amount=5
# Output: 1 (use one 5-coin)
# Time: O(amount * len(coins)), Space: O(amount)
# Much faster than recursive!
```

**Key Principle:** Build solution bottom-up instead of top-down recursion.

### Comparison: Recursive vs Iterative

| Aspect | Recursive | Iterative |
|--------|-----------|-----------|
| **Readability** | Cleaner, more intuitive | More verbose |
| **Speed** | Slower (function overhead) | Faster |
| **Memory** | O(n) stack space | Minimal overhead |
| **Stack Overflow Risk** | YES (deep recursion) | NO |
| **Debugging** | Long stack traces | Easier to trace |
| **Recursion Limit** | ~1000 in Python | No limit |
| **Natural for** | Trees, backtracking | Loops, DP |

### Decision Guide

**Use Recursion When:**
- Problem naturally recursive (trees, graphs)
- Small input size (n < 100)
- Clarity more important than performance
- No risk of stack overflow

**Use Iteration When:**
- Large input size (n > 1000)
- Need maximum performance
- Memory limited
- Risk of deep recursion
- Simple loops or DP

### Real-World Example: Converting DFS to Iterative

**Problem:** Find all paths in graph from start to end

**Recursive (clean but risky):**
```python
def find_paths_recursive(graph, start, end, path=None):
    """Recursive DFS - simple but limited depth"""
    if path is None:
        path = []
    path = path + [start]

    if start == end:
        return [path]

    paths = []
    for neighbor in graph.get(start, []):
        if neighbor not in path:
            new_paths = find_paths_recursive(graph, neighbor, end, path)
            paths.extend(new_paths)

    return paths
```

**Iterative (robust):**
```python
def find_paths_iterative(graph, start, end):
    """Iterative DFS - handles large graphs"""
    stack = [(start, [start])]  # (node, path_to_node)
    all_paths = []

    while stack:
        node, path = stack.pop()

        if node == end:
            all_paths.append(path)
            continue

        for neighbor in graph.get(node, []):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return all_paths

# Test both
graph = {1: [2, 3], 2: [4], 3: [4], 4: []}

print(find_paths_recursive(graph, 1, 4))
# Output: [[1, 2, 4], [1, 3, 4]]

print(find_paths_iterative(graph, 1, 4))
# Output: [[1, 2, 4], [1, 3, 4]]

# Both work! But iterative handles larger graphs safely.
# Time: O(paths found), Space: O(max path length)
```

---

## 3. Fibonacci Sequence

### Theory
Each number is the sum of the two preceding ones: F(n) = F(n-1) + F(n-2)
Classic example of inefficient vs efficient algorithms.

### Naive Recursion (❌ SLOW)
```python
def fib_naive(n):
    """Recalculates same values multiple times"""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# fib_naive(5) = 5
# But recalculates fib(3) multiple times!
```

**Time Complexity:** O(2ⁿ) - exponential! 💥
**Space Complexity:** O(n) - recursion depth
**Problem:** Calculates same values repeatedly

### Memoization (✅ FAST)
```python
def fib_memo(n, memo=None):
    """Cache results to avoid recalculation"""
    if memo is None:
        memo = {}

    # Check if already calculated
    if n in memo:
        return memo[n]

    # Base case
    if n <= 1:
        return n

    # Calculate and store
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print(fib_memo(10))  # Output: 55 (much faster!)
```

**Time Complexity:** O(n) - calculates each once
**Space Complexity:** O(n) - memo dictionary
**Improvement:** 2ⁿ → n (massive speedup!)

### Tabulation (✅ ALTERNATIVE)
```python
def fib_tab(n):
    """Build solution bottom-up"""
    if n <= 1:
        return n

    # Create table
    dp = [0] * (n + 1)
    dp[1] = 1

    # Fill from bottom up
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

print(fib_tab(10))  # Output: 55
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)
**Advantage:** Iterative (no recursion stack)

### Space-Optimized (✅ BEST)
```python
def fib_optimized(n):
    """Only keep last two values"""
    if n <= 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr

print(fib_optimized(10))  # Output: 55
```

**Time Complexity:** O(n)
**Space Complexity:** O(1) - constant space! 🎯
**Best for:** Large n values, interviews

---

## 4. Linked List Operations

### Theory
Sequential data structure where each node contains data and reference to next node.

### Node Structure
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Create linked list: 1 -> 2 -> 3 -> None
head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
```

### List Traversal
```python
def traverse(head):
    """Visit all nodes in order"""
    current = head
    while current:
        print(current.data)
        current = current.next
    # Output: 1, 2, 3

# Time: O(n), Space: O(1)
```

### Reverse Linked List
```python
def reverse(head):
    """Reverse entire linked list"""
    prev = None
    current = head

    while current:
        # Save next node
        next_node = current.next
        # Reverse the link
        current.next = prev
        # Move prev and current forward
        prev = current
        current = next_node

    return prev  # New head

# Input:  1 -> 2 -> 3 -> None
# Output: 3 -> 2 -> 1 -> None
# Time: O(n), Space: O(1)
```

### Find Cycle
```python
def has_cycle(head):
    """Detect if linked list has cycle using two pointers"""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next           # Move 1 step
        fast = fast.next.next      # Move 2 steps

        if slow == fast:
            return True  # Cycle found

    return False  # No cycle

# Time: O(n), Space: O(1)
```

### Merge Sorted Lists
```python
def merge_sorted(l1, l2):
    """Merge two sorted linked lists"""
    dummy = Node(0)
    current = dummy

    while l1 and l2:
        if l1.data < l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Attach remaining nodes
    current.next = l1 if l1 else l2

    return dummy.next

# Time: O(n + m), Space: O(1)
```

### Doubly Linked List

#### Theory
Each node has TWO pointers: one to next node and one to previous node. Allows traversal in both directions.

**Advantages over Singly Linked List:**
- Traverse backwards without reversing
- Delete node directly if you have reference (no need to find previous)
- Better for implementing deque and certain algorithms

**Trade-off:** Requires more memory (two pointers vs one)

#### Node Structure
```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Create doubly linked list: 1 <-> 2 <-> 3
head = DoublyNode(1)
node2 = DoublyNode(2)
node3 = DoublyNode(3)

head.next = node2
node2.prev = head
node2.next = node3
node3.prev = node2

# Now can traverse forward: 1 -> 2 -> 3
# And backward: 3 -> 2 -> 1
```

#### Forward & Backward Traversal
```python
def traverse_forward(head):
    """Traverse from head to tail"""
    current = head
    while current:
        print(current.data)
        current = current.next
    # Output: 1, 2, 3

def traverse_backward(tail):
    """Traverse from tail to head"""
    current = tail
    while current:
        print(current.data)
        current = current.prev
    # Output: 3, 2, 1 (reversed!)

# Time: O(n) for each, Space: O(1)
```

#### Insert at Beginning
```python
def insert_at_beginning(head, data):
    """Add node at front of list"""
    new_node = DoublyNode(data)

    if head:
        new_node.next = head
        head.prev = new_node

    return new_node  # New head

# Input:  1 <-> 2 <-> 3
# After insert_at_beginning(head, 0):
# Output: 0 <-> 1 <-> 2 <-> 3
# Time: O(1), Space: O(1)
```

#### Insert at End
```python
def insert_at_end(head, data):
    """Add node at end of list"""
    new_node = DoublyNode(data)

    if not head:
        return new_node

    current = head
    while current.next:
        current = current.next

    current.next = new_node
    new_node.prev = current

    return head

# Input:  1 <-> 2 <-> 3
# After insert_at_end(head, 4):
# Output: 1 <-> 2 <-> 3 <-> 4
# Time: O(n), Space: O(1)
```

#### Delete Node
```python
def delete_node(node):
    """Delete node from anywhere in list (key advantage!)"""
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev

    # Return new head (if deleting head, return next)
    return node.next

# Input:  1 <-> 2 <-> 3 <-> 4
# After delete_node(node2):  # node2.data = 2
# Output: 1 <-> 3 <-> 4
# Time: O(1) if you have node reference (huge advantage!)
# Space: O(1)
```

#### Find Node
```python
def find_node(head, target):
    """Find first node with given value"""
    current = head
    while current:
        if current.data == target:
            return current
        current = current.next
    return None

# Input:  1 <-> 2 <-> 3
# After find_node(head, 2):
# Output: reference to node with data=2
# Time: O(n), Space: O(1)
```

#### Reverse Doubly Linked List
```python
def reverse_doubly_list(head):
    """Reverse entire doubly linked list"""
    current = head

    while current:
        # Swap prev and next pointers
        current.prev, current.next = current.next, current.prev

        # Move to next (which is now in prev after swap)
        current = current.prev

    # Find new head (last node of original)
    while head.next:
        head = head.next

    return head

# Input:  1 <-> 2 <-> 3
# Output: 3 <-> 2 <-> 1 (both directions reversed)
# Time: O(n), Space: O(1)
```

#### Practical Example: LRU Cache
```python
class LRUCache:
    """Use doubly linked list for efficient access tracking"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = DoublyNode(0)  # Dummy head (least recent)
        self.tail = DoublyNode(0)  # Dummy tail (most recent)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node):
        """Move node to front (most recently used)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        """Remove node from current position"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_head(node)
        return node.data

    def put(self, key, value):
        if key in self.cache:
            self._remove_node(self.cache[key])
        node = DoublyNode(value)
        self.cache[key] = node
        self._add_to_head(node)
        if len(self.cache) > self.capacity:
            del self.cache[self.tail.prev.data]
            self._remove_node(self.tail.prev)

# Time: O(1) for get/put operations!
# Space: O(capacity)
# Use: LRU Cache, undo/redo functionality
```

#### Comparison: Singly vs Doubly Linked List

| Operation | Singly | Doubly |
|-----------|--------|--------|
| Traverse forward | O(n) | O(n) |
| Traverse backward | O(n) or impossible | O(n) ✓ |
| Insert at start | O(1) | O(1) |
| Delete (need prev node) | O(n) | O(1) ✓ |
| Find and delete | O(n) + O(n) | O(n) + O(1) |
| Memory | Less | More (extra pointer) |

**When to use Doubly Linked List:**
- Need backward traversal (undo/redo)
- Frequent deletions from middle
- Implementing deque
- LRU/MRU cache patterns

---

## 5. Binary Search

### Theory
Efficiently find element in **sorted** array by dividing search space in half each time.

### Prerequisite
Array MUST be sorted! Otherwise algorithm fails.

### Implementation
```python
def binary_search(arr, target):
    """Find target index in sorted array"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid  # Found!
        elif arr[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half

    return -1  # Not found

# Input: arr=[1, 3, 5, 7, 9], target=7
# Output: 3
# Time: O(log n) - much faster than linear O(n)!
```

### Find First Position
```python
def find_first(arr, target):
    """Find first occurrence of target"""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

# Input: arr=[1, 2, 2, 2, 3], target=2
# Output: 1 (first position)
# Time: O(log n)
```

### Search in Rotated Array
```python
def search_rotated(arr, target):
    """Search in rotated sorted array"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid

        # Determine which half is sorted
        if arr[left] <= arr[mid]:  # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1  # Search left
            else:
                left = mid + 1  # Search right
        else:  # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1  # Search right
            else:
                right = mid - 1  # Search left

    return -1

# Input: arr=[4, 5, 6, 7, 0, 1, 2], target=0
# Output: 4
# Time: O(log n)
```

---

## 6. Depth-First Search (DFS)

### Theory
Explore as far as possible along each branch before backtracking. Uses stack (implicit in recursion).

### Recursive DFS
```python
def dfs_recursive(graph, node, visited=None):
    """Visit node, then recursively visit unvisited neighbors"""
    if visited is None:
        visited = set()

    visited.add(node)
    print(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

    return visited

# Graph: {1: [2, 3], 2: [4], 3: [5], 4: [], 5: []}
# Output: 1, 2, 4, 3, 5 (depth-first order)
# Time: O(V + E), Space: O(V) - recursion depth
```

### Iterative DFS (Using Stack)
```python
def dfs_iterative(graph, start):
    """Use explicit stack instead of recursion"""
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            # Add neighbors in reverse (to maintain order)
            stack.extend(reversed(graph[node]))

    return result

# Output: [1, 2, 4, 3, 5] (or similar depth-first order)
# Time: O(V + E), Space: O(V)
```

### Find Path Between Nodes
```python
def find_path(graph, start, end, path=None):
    """Find any path from start to end"""
    if path is None:
        path = []

    path = path + [start]

    if start == end:
        return path

    for node in graph[start]:
        if node not in path:  # Avoid cycles
            new_path = find_path(graph, node, end, path)
            if new_path:
                return new_path

    return None

# Graph: {1: [2, 3], 2: [4], 3: [5], 4: [], 5: []}
# find_path(graph, 1, 5) -> [1, 3, 5]
# Time: O(V + E), Space: O(V)
```

### Detect Cycle in Graph
```python
def has_cycle(graph):
    """Detect cycle using DFS with color coding"""
    # 0: white (unvisited), 1: gray (visiting), 2: black (visited)
    color = {node: 0 for node in graph}

    def dfs(node):
        color[node] = 1  # Mark as visiting

        for neighbor in graph[node]:
            if color[neighbor] == 1:  # Back edge = cycle!
                return True
            if color[neighbor] == 0 and dfs(neighbor):
                return True

        color[node] = 2  # Mark as visited
        return False

    for node in graph:
        if color[node] == 0:
            if dfs(node):
                return True
    return False

# Time: O(V + E), Space: O(V)
```

---

## 7. Breadth-First Search (BFS)

### Theory
Explore all nodes at distance k before exploring nodes at distance k+1. Uses queue.

### Basic BFS
```python
from collections import deque

def bfs(graph, start):
    """Visit nodes level by level"""
    visited = {start}
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()  # Remove from front
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Add to back

    return result

# Graph: {1: [2, 3], 2: [4], 3: [5], 4: [], 5: []}
# Output: [1, 2, 3, 4, 5] (level-order)
# Time: O(V + E), Space: O(V)
```

### ⚠️ Critical: Why deque, not list.pop(0)?
```python
# ❌ WRONG - list.pop(0) is O(n²) in BFS!
queue = [start]
queue.pop(0)  # Shifts all remaining elements - SLOW!

# ✅ CORRECT - deque.popleft() is O(1)
from collections import deque
queue = deque([start])
queue.popleft()  # Pointer update - FAST!
```

### Shortest Path
```python
def shortest_path(graph, start, end):
    """Find shortest path using BFS"""
    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

# Graph: {1: [2, 3], 2: [4], 3: [5], 4: [5], 5: []}
# shortest_path(graph, 1, 5) -> [1, 3, 5]
# Time: O(V + E), Space: O(V)
```

### Level-Order Tree Traversal
```python
def level_order(root):
    """Visit tree level by level"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result

# Returns: [[1], [2, 3], [4, 5, 6, 7]]
# Time: O(n), Space: O(n)
```

---

## 8. Sorting Algorithms

### Why NOT Bubble Sort? Performance Analysis

**Problem with Bubble Sort:**
```
For n=10:    100 operations
For n=100:   10,000 operations
For n=1000:  1,000,000 operations
For n=10,000: 100,000,000 operations (SLOW! 10+ seconds)
```

**Why it's slow:** Compares almost every pair repeatedly. Each comparison takes time, and with O(n²) complexity, it gets exponentially worse.

**Merge Sort instead:**
```
For n=10:    40 operations
For n=100:   664 operations
For n=1000:  10,000 operations
For n=10,000: 132,000 operations (FAST! milliseconds)
```

**Performance Comparison with Real Numbers:**
- Sorting 1,000 items:
  - Bubble Sort: ~100 seconds ❌
  - Merge Sort: ~0.01 seconds ✓
  - Speedup: 10,000x faster!

- Sorting 10,000 items:
  - Bubble Sort: ~10,000 seconds (2.7 hours!) ❌
  - Merge Sort: ~0.13 seconds ✓
  - Speedup: 75,000x faster!

### Bubble Sort (❌ Educational only)
```python
def bubble_sort(arr):
    """Compare adjacent pairs, swap if needed"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Example 1: Random array
arr1 = [64, 34, 25, 12, 22, 11, 90]
result1 = bubble_sort(arr1.copy())
print(f"Input:  {arr1}")
print(f"Output: {result1}")
# Output: [11, 12, 22, 25, 34, 64, 90]

# Example 2: Already sorted (best case)
arr2 = [1, 2, 3, 4, 5]
result2 = bubble_sort(arr2.copy())
print(f"Input:  {arr2}")
print(f"Output: {result2}")
# Output: [1, 2, 3, 4, 5]

# Example 3: Reverse sorted (worst case)
arr3 = [90, 64, 34, 25, 22, 12, 11]
result3 = bubble_sort(arr3.copy())
print(f"Input:  {arr3}")
print(f"Output: {result3}")
# Output: [11, 12, 22, 25, 34, 64, 90]

# Time: O(n²), Space: O(1)
# Use: NEVER in production!
```

### Merge Sort (✅ Divide & Conquer - PREFERRED)
```python
def merge_sort(arr):
    """Divide into halves, sort, merge - STABLE SORT"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
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

# Example 1: Random array
arr1 = [64, 34, 25, 12, 22, 11, 90]
result1 = merge_sort(arr1)
print(f"Input:  {arr1}")
print(f"Output: {result1}")
# Output: [11, 12, 22, 25, 34, 64, 90]

# Example 2: Array with duplicates (maintains stable order)
arr2 = [5, 2, 8, 2, 9, 1, 5, 5]
result2 = merge_sort(arr2)
print(f"Input:  {arr2}")
print(f"Output: {result2}")
# Output: [1, 2, 2, 5, 5, 5, 8, 9]

# Example 3: Large array (still fast!)
arr3 = list(range(100, 0, -1))  # 100, 99, 98, ..., 1
result3 = merge_sort(arr3)
print(f"Input:  [100, 99, 98, ..., 2, 1]")
print(f"Output: {result3[:5]}...{result3[-5:]}")
# Output: [1, 2, 3, ..., 98, 99, 100]

# Time: O(n log n) always, Space: O(n)
# Use: When STABILITY matters (duplicates keep relative order)
# Why? 10,000x faster than bubble sort!
```

### Quick Sort (✅ Average case best)
```python
def quick_sort(arr):
    """Partition around pivot, recursively sort"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

# Example 1: Random array
arr1 = [64, 34, 25, 12, 22, 11, 90]
result1 = quick_sort(arr1)
print(f"Input:  {arr1}")
print(f"Output: {result1}")
# Output: [11, 12, 22, 25, 34, 64, 90]

# Example 2: Array with duplicates
arr2 = [5, 2, 8, 2, 9, 1, 5, 5]
result2 = quick_sort(arr2)
print(f"Input:  {arr2}")
print(f"Output: {result2}")
# Output: [1, 2, 2, 5, 5, 5, 8, 9]

# Example 3: Already sorted (worst case for simple pivot)
arr3 = [1, 2, 3, 4, 5, 6, 7, 8]
result3 = quick_sort(arr3)
print(f"Input:  {arr3}")
print(f"Output: {result3}")
# Output: [1, 2, 3, 4, 5, 6, 7, 8]

# Time: O(n log n) avg, O(n²) worst, Space: O(log n)
# Use: DEFAULT choice for most applications
# Why? Fast in practice, less memory than merge sort
```

### Python's Built-in Sort (✅ ALWAYS USE THIS)
```python
# Python uses Timsort - hybrid of merge sort and insertion sort
# ALWAYS FASTER than manual implementation!

# Example 1: Basic sorting
arr1 = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = sorted(arr1)  # Returns new list
print(f"Input:  {arr1}")
print(f"Output: {sorted_arr}")
# Output: [11, 12, 22, 25, 34, 64, 90]

# Example 2: In-place sorting (modifies original)
arr2 = [64, 34, 25, 12, 22, 11, 90]
arr2.sort()  # Sorts in-place
print(f"After arr2.sort(): {arr2}")
# Output: [11, 12, 22, 25, 34, 64, 90]

# Example 3: Sorting with custom key
arr3 = ["apple", "pie", "a", "longer"]
sorted_by_length = sorted(arr3, key=len)
print(f"Input:  {arr3}")
print(f"Sorted by length: {sorted_by_length}")
# Output: ['a', 'pie', 'apple', 'longer']

# Example 4: Reverse sorting
arr4 = [64, 34, 25, 12, 22, 11, 90]
reverse_sorted = sorted(arr4, reverse=True)
print(f"Input:  {arr4}")
print(f"Reverse sorted: {reverse_sorted}")
# Output: [90, 64, 34, 25, 22, 12, 11]

# Time: O(n log n), Space: O(n)
# Use: ALWAYS in production!
# Why? Optimized in C, handles edge cases, guaranteed O(n log n)
```

### Sorting Algorithm Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable | Use Case |
|-----------|------|---------|-------|-------|--------|----------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Teaching only |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Need stable sort |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No | General purpose |
| Python sorted() | O(n) | O(n log n) | O(n log n) | O(n) | Yes | **ALWAYS USE** |

**Key Insight:** Merge Sort guarantees O(n log n) always, while Quick Sort can degrade to O(n²) on bad input. Python's built-in is fastest due to optimizations.

---

## 9. Hash Map / Dictionary Operations

### Theory
Map keys to values for O(1) average lookup, insertion, deletion.

### Basic Counting
```python
def count_frequencies(arr):
    """Count occurrences of each element"""
    count = {}
    for num in arr:
        count[num] = count.get(num, 0) + 1
    return count

print(count_frequencies([1, 2, 2, 3, 3, 3]))
# Output: {1: 1, 2: 2, 3: 3}
# Time: O(n), Space: O(n)
```

### Two Sum Problem
```python
def two_sum(arr, target):
    """Find two numbers that sum to target"""
    seen = {}
    for num in arr:
        complement = target - num
        if complement in seen:
            return [seen[complement], arr.index(num)]
        seen[num] = arr.index(num)
    return None

print(two_sum([2, 7, 11, 15], 9))
# Output: [0, 1] (2 + 7 = 9)
# Time: O(n), Space: O(n)
# Better than O(n²) nested loop approach!
```

### Anagram Detection
```python
def are_anagrams(s1, s2):
    """Check if two strings are anagrams"""
    return sorted(s1) == sorted(s2)

# Alternative: using hash map
def are_anagrams_v2(s1, s2):
    if len(s1) != len(s2):
        return False

    count1 = {}
    for char in s1:
        count1[char] = count1.get(char, 0) + 1

    for char in s2:
        if char not in count1:
            return False
        count1[char] -= 1
        if count1[char] < 0:
            return False

    return True

print(are_anagrams("listen", "silent"))  # True
# Time: O(n), Space: O(1) for second version
```

### Using Collections.Counter
```python
from collections import Counter

def top_k_frequent(arr, k):
    """Find k most common elements"""
    count = Counter(arr)
    return [num for num, _ in count.most_common(k)]

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))
# Output: [1, 2] (1 appears 3x, 2 appears 2x)
# Time: O(n + k log n), Space: O(n)
```

---

## 10. Sliding Window

### Theory
Maintain a window of elements and slide it across the data to find optimal subarray/substring.

### Maximum Sum Subarray
```python
def max_sum_subarray(arr, k):
    """Find maximum sum of k consecutive elements"""
    if k > len(arr):
        return None

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide window
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_sum_subarray([1, 3, 2, 6, -1, 4, 1, 8], 3))
# Output: 13 (window [4, 1, 8])
# Time: O(n), Space: O(1)
# Much better than O(n*k) nested approach!
```

### Longest Substring Without Repeating Characters
```python
def longest_substring(s):
    """Find longest substring with no repeating chars"""
    char_index = {}
    max_length = 0
    start = 0

    for end in range(len(s)):
        if s[end] in char_index and char_index[s[end]] >= start:
            # Shrink window from left
            start = char_index[s[end]] + 1

        # Expand window on right
        char_index[s[end]] = end
        max_length = max(max_length, end - start + 1)

    return max_length

print(longest_substring("abcabcbb"))
# Output: 3 ("abc")
# Time: O(n), Space: O(min(n, alphabet_size))
```

### Minimum Window Substring
```python
def min_window(s, t):
    """Find smallest substring containing all chars from t"""
    if not s or not t:
        return ""

    need = {}
    for char in t:
        need[char] = need.get(char, 0) + 1

    required = len(need)
    formed = 0
    window_counts = {}

    left = right = 0
    min_len = float('inf')
    min_start = 0

    while right < len(s):
        # Add char from right
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in need and window_counts[char] == need[char]:
            formed += 1

        # Contract from left
        while left <= right and formed == required:
            char = s[left]
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left

            window_counts[char] -= 1
            if char in need and window_counts[char] < need[char]:
                formed -= 1

            left += 1

        right += 1

    return s[min_start:min_start + min_len] if min_len != float('inf') else ""

print(min_window("ADOBECODEBANC", "ABC"))
# Output: "BANC"
# Time: O(n), Space: O(alphabet_size)
```

---

## 11. Dynamic Programming

### Theory
Solve complex problems by breaking into overlapping subproblems and storing results.
Two approaches: **Memoization** (top-down) and **Tabulation** (bottom-up).

### Coin Change Problem
```python
# Problem: Minimum coins needed to make amount
def coin_change(coins, amount):
    """Return minimum coins to make amount"""
    # dp[i] = minimum coins to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1, 2, 5], 5))
# Output: 1 (one 5-cent coin)
# Time: O(amount * len(coins)), Space: O(amount)
```

### Longest Increasing Subsequence (LIS)
```python
def lis_length(arr):
    """Length of longest increasing subsequence"""
    n = len(arr)
    if n == 0:
        return 0

    # dp[i] = length of LIS ending at index i
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

print(lis_length([10, 9, 2, 5, 3, 7, 101, 18]))
# Output: 4 ([2, 3, 7, 101])
# Time: O(n²), Space: O(n)
```

### Edit Distance (Levenshtein)
```python
def edit_distance(s1, s2):
    """Minimum operations to transform s1 to s2"""
    m, n = len(s1), len(s2)

    # dp[i][j] = distance between s1[:i] and s2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all chars from s1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all chars to get s2

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )

    return dp[m][n]

print(edit_distance("kitten", "sitting"))
# Output: 3 (k→s, e→i, insert g)
# Time: O(m*n), Space: O(m*n)
```

### House Robber (1D DP)
```python
def rob(houses):
    """Max money robbing non-adjacent houses"""
    if not houses:
        return 0
    if len(houses) == 1:
        return houses[0]

    # dp[i] = max money up to house i
    dp = [0] * len(houses)
    dp[0] = houses[0]
    dp[1] = max(houses[0], houses[1])

    for i in range(2, len(houses)):
        dp[i] = max(
            dp[i - 1],           # Skip this house
            dp[i - 2] + houses[i]  # Rob this house
        )

    return dp[-1]

print(rob([1, 2, 3, 1]))
# Output: 4 (rob house 1 and 3: 1 + 3)
# Time: O(n), Space: O(n)
```

---

## 12. Backtracking

### Theory
Explore all possible solutions by building candidates incrementally and abandoning paths that fail.

### Permutations
```python
def permutations(arr):
    """Generate all permutations of array"""
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current)
            return

        for i in range(len(remaining)):
            # Choose
            backtrack(
                current + [remaining[i]],
                remaining[:i] + remaining[i+1:]
            )

    backtrack([], arr)
    return result

print(permutations([1, 2, 3]))
# Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
# Time: O(n!), Space: O(n)
```

### Combinations
```python
def combinations(arr, k):
    """Generate all combinations of k elements"""
    result = []

    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return

        for i in range(start, len(arr)):
            current.append(arr[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result

print(combinations([1, 2, 3, 4], 2))
# Output: [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
# Time: O(C(n,k)), Space: O(k)
```

### N-Queens Problem
```python
def solve_nqueens(n):
    """Place n queens on n×n board, no conflicts"""
    result = []
    board = [[False] * n for _ in range(n)]

    def is_safe(row, col):
        # Check column
        for i in range(row):
            if board[i][col]:
                return False
        # Check diagonals
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if board[i][j]:
                return False
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
            if board[i][j]:
                return False
        return True

    def backtrack(row):
        if row == n:
            result.append([row[:] for row in board])
            return

        for col in range(n):
            if is_safe(row, col):
                board[row][col] = True
                backtrack(row + 1)
                board[row][col] = False

    backtrack(0)
    return result

# Time: O(n!), Space: O(n)
```

---

## 13. Two Pointers

### Theory
Use two pointers at different positions to solve problems in linear time instead of O(n²).

### Two Sum (Sorted Array)
```python
def two_sum_sorted(arr, target):
    """Find two numbers that sum to target"""
    left, right = 0, len(arr) - 1

    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum

    return None

print(two_sum_sorted([2, 7, 11, 15], 9))
# Output: [0, 1]
# Time: O(n), Space: O(1)
```

### Container With Most Water
```python
def max_area(heights):
    """Find max water container using heights"""
    left, right = 0, len(heights) - 1
    max_area = 0

    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        max_area = max(max_area, area)

        # Move pointer on shorter side
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area

print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))
# Output: 49
# Time: O(n), Space: O(1)
```

### Palindrome Checker
```python
def is_palindrome(s):
    """Check if string is palindrome (ignore spaces/punctuation)"""
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        # Compare (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True

print(is_palindrome("A man, a plan, a canal: Panama"))
# Output: True
# Time: O(n), Space: O(1)
```

---

## Algorithm Use Cases Guide

### Real-World Applications for Each Algorithm

#### 1. Iteration & Loops
**When to Use:**
- Processing every element in a collection
- Transforming data sets
- Counting or aggregating values
- Validating all elements

**Real-World Examples:**
- **E-commerce:** Loop through shopping cart items to calculate total price
- **Banking:** Iterate through transactions to find fraud patterns
- **Data Analysis:** Loop through dataset rows to calculate statistics
- **Web Scraping:** Iterate through HTML elements to extract data
- **Game Development:** Loop through all game objects to update positions

**Code Example:**
```python
# Calculate average score for all students
scores = [85, 92, 78, 95, 88]
total = 0
for score in scores:
    total += score
average = total / len(scores)  # Average: 87.6
# Use Case: Grading system, performance analytics
```

---

#### 2. Recursion
**When to Use:**
- Problems with natural recursive structure
- Tree/graph traversal
- Divide-and-conquer algorithms
- Backtracking and exploration problems

**Real-World Examples:**
- **File Systems:** Traverse nested folder structures recursively
- **Organization Charts:** Navigate hierarchical employee structures
- **Compilers:** Parse nested expressions and syntax trees
- **DOM Traversal:** Walk through HTML/XML document trees
- **Chess:** Explore possible moves recursively (minimax algorithm)

**Code Example:**
```python
# List all files in directory recursively
import os

def list_files(directory):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            list_files(path)  # Recursive call for subdirectories
        else:
            print(f"File: {path}")

# Use Case: File explorer, backup systems, directory sync
```

---

#### 3. Fibonacci & Dynamic Programming
**When to Use:**
- Overlapping subproblems
- Optimization problems
- Finding minimum/maximum sequences
- Probability calculations

**Real-World Examples:**
- **Rabbits Population:** Model rabbit population growth
- **Stock Trading:** Find best days to buy/sell (max profit)
- **Currency Exchange:** Minimum coins/bills for change
- **Video Games:** Optimal path planning, resource management
- **Finance:** Loan amortization, pension calculations
- **Scheduling:** Optimal task scheduling with constraints

**Code Example:**
```python
# Minimum coins to make change
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    return dp[amount]

print(coin_change([1, 2, 5], 5))  # Output: 1 (one 5-coin)
# Use Case: ATM cash dispensing, vending machines, currency exchange
```

---

#### 4. Linked Lists
**When to Use:**
- Frequent insertions/deletions
- Dynamic size collections
- Memory-efficient storage
- Stack/queue implementation

**Real-World Examples:**
- **Undo/Redo:** Store operations in linked list for undo functionality
- **LRU Cache:** Track recently used items (with doubly linked list)
- **Music Playlists:** Queue of songs with prev/next navigation
- **Browser History:** Navigate forward/backward through history
- **Memory Allocation:** Operating systems use linked lists for heap
- **Polynomial Operations:** Represent polynomials as linked lists

**Code Example:**
```python
# Browser history navigation
class HistoryNode:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

# Navigate forward/backward in history using doubly linked list
# Use Case: Browser back/forward buttons, undo/redo stacks
```

---

#### 5. Binary Search
**When to Use:**
- Searching in sorted data
- Finding boundaries (first/last occurrence)
- Finding elements efficiently
- Rotated array search

**Real-World Examples:**
- **Dictionary Lookup:** Find words in sorted dictionary O(log n)
- **Library Systems:** Find books by ISBN in sorted catalog
- **Database Indexes:** B-tree indexes use binary search principles
- **Auto-complete:** Find matching prefixes in sorted word list
- **Version Control:** Find first bad commit (git bisect)
- **Phone Books:** Quick lookup of phone numbers

**Code Example:**
```python
# Auto-complete: find first word starting with prefix
def find_prefix(words, prefix):
    left, right = 0, len(words) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if words[mid].startswith(prefix):
            result = mid
            right = mid - 1  # Keep searching left for first
        elif words[mid] < prefix:
            left = mid + 1
        else:
            right = mid - 1
    return result

# Use Case: Search engines, IDE auto-complete, database queries
```

---

#### 6. Depth-First Search (DFS)
**When to Use:**
- Finding paths between nodes
- Detecting cycles
- Topological sorting
- Backtracking problems

**Real-World Examples:**
- **Social Networks:** Find all friends of friends (recommendation)
- **Maze Solving:** Find path through maze (backtracking)
- **Compiler:** Detect circular dependencies in code
- **Cycle Detection:** Credit networks (circular debt detection)
- **Puzzle Solving:** N-queens, sudoku solver (backtracking)
- **Spell Checkers:** Generate corrections using trie + DFS
- **Git:** Detect branch conflicts, merge trees

**Code Example:**
```python
# Detect circular dependency in project modules
def has_circular_dependency(modules):
    # modules: {module: [dependencies]}
    visited = set()
    rec_stack = set()

    def dfs(module):
        visited.add(module)
        rec_stack.add(module)

        for dep in modules.get(module, []):
            if dep not in visited:
                if dfs(dep):
                    return True
            elif dep in rec_stack:
                return True  # Cycle found!

        rec_stack.remove(module)
        return False

    for module in modules:
        if module not in visited:
            if dfs(module):
                return True
    return False

# Use Case: Build systems, module loaders, dependency analyzers
```

---

#### 7. Breadth-First Search (BFS)
**When to Use:**
- Finding shortest paths
- Level-order traversal
- Connected components
- Nearest neighbor problems

**Real-World Examples:**
- **GPS Navigation:** Find shortest route between two locations
- **Social Networks:** Find closest connections (degrees of separation)
- **Puzzle Solving:** Minimum moves to solve puzzle (8-puzzle)
- **Network Broadcasting:** Broadcast message to all connected nodes
- **Torrent Networks:** Find nearest peer with file
- **Game AI:** Flood fill, pathfinding in games
- **Web Crawling:** Crawl web pages level by level

**Code Example:**
```python
# GPS: Find shortest path between cities
def shortest_path_gps(graph, start, destination):
    from collections import deque
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        city, path = queue.popleft()
        if city == destination:
            return path

        for neighbor in graph.get(city, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

# Use Case: Route optimization, social recommendations, game pathfinding
```

---

#### 8. Sorting Algorithms
**When to Use:**
- Organizing data
- Preparation for other algorithms
- Displaying ordered results
- Optimization (greedy algorithms need sorted data)

**Real-World Examples:**
- **E-commerce:** Sort products by price, rating, relevance
- **Student Rankings:** Sort by GPA, test scores
- **Leaderboards:** Sort gamers by score
- **Search Results:** Google sorts results by relevance
- **Logistics:** Sort packages by delivery route
- **Database Optimization:** Create indexes on sorted data
- **File Management:** Sort files by name, date, size

**Code Example:**
```python
# Sort e-commerce products by multiple criteria
products = [
    {"name": "Laptop", "price": 1200, "rating": 4.5},
    {"name": "Phone", "price": 800, "rating": 4.8},
    {"name": "Tablet", "price": 400, "rating": 4.2},
]

# Sort by rating (descending), then price (ascending)
sorted_products = sorted(products, key=lambda p: (-p['rating'], p['price']))

# Use Case: E-commerce, content delivery, database optimization
```

---

#### 9. Hash Maps / Dictionary
**When to Use:**
- Fast lookups
- Counting frequencies
- Caching results
- Pattern matching

**Real-World Examples:**
- **Caching:** Cache computation results to avoid recalculation
- **Spell Checking:** Hash set of valid words for O(1) lookup
- **Database Indexing:** Index data by primary key
- **Compiler Symbol Tables:** Map variable names to memory addresses
- **HTTP Caching:** Cache responses by URL
- **Rate Limiting:** Count API calls per user
- **Analytics:** Count event frequencies

**Code Example:**
```python
# Rate limiting: count API calls per user
from collections import defaultdict
import time

call_count = defaultdict(list)  # user_id -> [timestamps]

def is_rate_limited(user_id, max_calls=100, time_window=60):
    now = time.time()
    # Remove old calls outside time window
    call_count[user_id] = [t for t in call_count[user_id]
                           if now - t < time_window]

    if len(call_count[user_id]) >= max_calls:
        return True  # Rate limited

    call_count[user_id].append(now)
    return False

# Use Case: API rate limiting, caching, frequency analysis
```

---

#### 10. Sliding Window
**When to Use:**
- Finding subarrays/substrings with properties
- Optimization of nested loops
- Stream processing

**Real-World Examples:**
- **Video Buffering:** Maintain sliding window of buffered frames
- **Stock Analysis:** Calculate moving average over time
- **Network Traffic:** Monitor bytes transferred in time windows
- **String Matching:** Find pattern in text efficiently
- **Data Compression:** Sliding window for LZ77 compression
- **Fraud Detection:** Monitor transaction patterns in time windows
- **Speech Recognition:** Process audio in overlapping windows

**Code Example:**
```python
# Stock analysis: moving average
def moving_average(prices, window_size):
    averages = []
    window_sum = sum(prices[:window_size])

    for i in range(window_size, len(prices)):
        averages.append(window_sum / window_size)
        window_sum = window_sum - prices[i - window_size] + prices[i]

    return averages

prices = [10, 20, 30, 40, 50, 60]
print(moving_average(prices, 3))  # [20, 30, 40, 50]
# Use Case: Financial analysis, video streaming, network monitoring
```

---

#### 11. Backtracking
**When to Use:**
- Finding all solutions
- Constraint satisfaction
- Exploration with pruning
- Permutations/combinations

**Real-World Examples:**
- **Sudoku Solver:** Place numbers following constraints
- **N-Queens:** Place queens on chessboard without conflicts
- **Puzzle Solvers:** Rubik's cube, crosswords (constraint satisfaction)
- **Travel Planning:** Find all possible routes with constraints
- **Phone Dialpad Words:** Find all possible words for digit sequence
- **Text Correction:** Generate similar words within edit distance
- **Maze Generation:** Generate mazes using backtracking

**Code Example:**
```python
# Sudoku solver
def solve_sudoku(board):
    def is_valid(row, col, num):
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        # Check 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(i, j, num):
                            board[i][j] = num
                            if backtrack():
                                return True
                            board[i][j] = 0
                    return False
        return True

    backtrack()
    return board

# Use Case: Puzzle solvers, constraint satisfaction, game AI
```

---

#### 12. Two Pointers
**When to Use:**
- Sorted array problems
- Palindrome checking
- Pairing elements
- Partition problems

**Real-World Examples:**
- **Merge Sorted Arrays:** Combine two sorted lists efficiently
- **Palindrome Validation:** Check if string is palindrome
- **Container Capacity:** Find two lines holding most water (stock price)
- **3Sum Problem:** Find triplets summing to target
- **Partition Arrays:** Partition array into categories
- **Remove Duplicates:** Remove duplicates from sorted array
- **String Reversal:** Reverse string in-place

**Code Example:**
```python
# Container with most water
def max_water_container(heights):
    left, right = 0, len(heights) - 1
    max_area = 0

    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        max_area = max(max_area, area)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area

# Use Case: Container capacity problems, stock trading, data partitioning
```

---

#### 13. Heaps / Priority Queues
**When to Use:**
- Finding min/max elements
- Top-k problems
- Task scheduling by priority
- Dijkstra's algorithm

**Real-World Examples:**
- **OS Task Scheduling:** Schedule processes by priority
- **Huffman Coding:** Build optimal encoding tree
- **Dijkstra's Algorithm:** Find shortest path in weighted graph
- **Event Processing:** Process events in priority order
- **Max Heap:** Find k largest elements
- **Min Heap:** Find k smallest elements
- **Load Balancing:** Distribute tasks to least-busy servers

**Code Example:**
```python
import heapq

# K most common words in document
def top_k_words(words, k):
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

    # Min heap of size k (keep k largest)
    heap = []
    for word, count in word_count.items():
        heapq.heappush(heap, (count, word))
        if len(heap) > k:
            heapq.heappop(heap)

    return [word for count, word in heap]

# Use Case: Search results, OS scheduling, network optimization
```

---

#### 14. Doubly Linked List
**When to Use:**
- Bidirectional traversal
- LRU/MRU caching
- Efficient deletions
- Undo/redo operations

**Real-World Examples:**
- **LRU Cache:** Remove least recently used item efficiently
- **Browser History:** Navigate forward and backward
- **Text Editors:** Undo/redo with doubly linked operations
- **Music Players:** Previous/next song navigation
- **MRU Lists:** Most recently used files in editors
- **Deque Operations:** Double-ended queue for queues and stacks
- **Photo Gallery:** Swipe left/right through photos

**Code Example:**
```python
# LRU Cache implementation
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> value
        # Use doubly linked list to track order
        # Most recent at head, least recent at tail

    def get(self, key):
        if key not in self.cache:
            return -1
        # Move to front (most recently used)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        # Remove least recently used if over capacity

# Use Case: Browser caching, CPU caching, database optimization
```

---

## Complexity Comparison

| Algorithm | Best Case | Average | Worst Case | Space | Use |
|-----------|-----------|---------|-----------|-------|-----|
| Iteration | O(n) | O(n) | O(n) | O(1) | Basic loops |
| Recursion | O(n) | O(n) | O(n) | O(n) | Trees, divide-conquer |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) | Sorted arrays |
| DFS | O(1) | O(V+E) | O(V+E) | O(V) | Paths, cycles |
| BFS | O(1) | O(V+E) | O(V+E) | O(V) | Shortest path |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Stable sort |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | Average best |
| Fibonacci (Memo) | O(n) | O(n) | O(n) | O(n) | DP |
| Two Sum (Hash) | O(n) | O(n) | O(n) | O(n) | Pair finding |
| Sliding Window | O(n) | O(n) | O(n) | O(k) | Substrings |

---

## Interview Tips

1. **Start Simple** - Brute force first, then optimize
2. **Complexity Matters** - Know time/space for each algorithm
3. **Edge Cases** - Empty input, single element, large numbers
4. **Code Clearly** - Variable names matter in interviews
5. **Explain Trade-offs** - Why one algorithm over another
6. **Practice** - Implement each algorithm multiple times

---

*Core Algorithms Reference | Python Implementation Focus*
