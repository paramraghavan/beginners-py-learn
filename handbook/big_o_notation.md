#### Big O Notation - Complete Guide

## What is Big O?

Big O describes how an algorithm's performance scales with input size **n**. It measures worst-case time/space
complexity.

---

##### Common Big O Notations (Best to Worst)

### 1. **O(1) - Constant Time**

**Meaning**: Time doesn't depend on input size.

```python
def get_first_element(lst):
    return lst[0]  # Always 1 operation


def check_dict(d, key):
    return key in d  # Dictionary lookup
```

**Real-world**: Array indexing, dictionary lookups, hash table operations.

---

###### 2. **O(log n) - Logarithmic Time**

**Meaning**: Work grows logarithmically with input size. A common pattern is
reducing the remaining problem by a fixed factor each iteration, such as
halving the search space in binary search.

```python
def binary_search(sorted_lst, target):
    left, right = 0, len(sorted_lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_lst[mid] == target:
            return mid
        elif sorted_lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Real-world**: Binary search, balanced tree operations (AVL, Red-Black trees), efficient database queries.

**Why?** For n=1,000,000, only ~20 iterations needed.

**Is `log` always base 2 in Big O?** No. Binary search naturally uses log₂(n)
because each step halves the remaining search space. Dividing the remaining
size by 3 each step would give log₃(n), which is also O(log n).

Any **fixed base greater than 1** gives the same Big O class. Changing the
base only introduces a constant multiplier, and Big O ignores constant factors:

```text
log₂(n) = log₁₀(n) / log₁₀(2) ≈ 3.322 × log₁₀(n)
O(log₂ n) = O(log₁₀ n) = O(log n)
```

The base matters when estimating actual counts: log₂(1000) ≈ 10, while
log₁₀(1000) = 3. For the binary search above, the worst-case loop count is
floor(log₂(n)) + 1 for n ≥ 1, including the final element check.

---

### 3. **O(n) - Linear Time**

**Meaning**: Time grows proportionally with input size.

```python
def find_max(lst):
    max_val = lst[0]
    for num in lst:  # Loop through each element
        if num > max_val:
            max_val = num
    return max_val


def linear_search(lst, target):
    for item in lst:  # Worst case: check all elements
        if item == target:
            return True
    return False
```

**Real-world**: Simple search, array iteration, linear scan operations.

---

### 4. **O(n log n) - Linearithmic Time**

**Meaning**: Linear operations repeated log(n) times.

```python
def merge_sort(lst):
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])  # O(log n) depth
    right = merge_sort(lst[mid:])  # O(log n) depth

    return merge(left, right)  # O(n) at each level
```

**Real-world**: Efficient sorting (Merge Sort, Quick Sort on average), most practical sorting.

**Why?** Best sorting efficiency without additional constraints.

---

### 5. **O(n²) - Quadratic Time**

**Meaning**: Double-nested loops processing all combinations.

```python
def bubble_sort(lst):
    n = len(lst)
    for i in range(n):  # O(n)
        for j in range(n - 1):  # O(n)
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]


def nested_loop_search(lst1, lst2):
    results = []
    for item1 in lst1:  # O(n)
        for item2 in lst2:  # O(n)
            if item1 == item2:
                results.append(item1)
    return results
```

**Real-world**: Naive sorting (Bubble, Insertion), simple nested iterations.

**When acceptable?** Small datasets (<1000 items).

---

### 6. **O(n³) - Cubic Time**

**Meaning**: Work grows in proportion to n × n × n = n³. A common pattern is
three nested loops, each running n times, with constant work in the innermost
loop.

For matrix multiplication, each of the n² output cells needs n
multiply-and-add steps. That gives n² × n = n³ steps in total.

```python
def matrix_multiplication(A, B):
    # Assume A and B are both n×n matrices of numbers.
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):          # n output rows
        for j in range(n):      # n output columns per row
            sum_val = 0
            for k in range(n):  # n terms per output cell
                sum_val += A[i][k] * B[k][j]
            result[i][j] = sum_val
    return result


print(matrix_multiplication([[1, 2], [3, 4]], [[5, 6], [7, 8]]))
# Output: [[19, 22], [43, 50]]
```

**Step-by-step calculation:**

1. The outer loop chooses one of n rows.
2. For each row, the middle loop chooses one of n columns: n² output cells.
3. For each cell, the inner loop performs n multiply-and-add steps: n³ total.


| Matrix size  | Multiply-and-add steps (n³) |
| ------------ | ---------------------------: |
| 2 × 2       |                            8 |
| 10 × 10     |                        1,000 |
| 100 × 100   |                    1,000,000 |
| 1000 × 1000 |                1,000,000,000 |

**Growth rule**: Doubling n multiplies the work by 8, because (2n)³ = 8n³.
Linear work doubles and quadratic work quadruples for the same input increase.

**Space complexity**: O(n²) for the returned matrix and O(1) auxiliary space
beyond that output. The time analysis assumes constant-cost numeric arithmetic.

**Real-world**: Standard square matrix multiplication, processing all cells of
an n × n × n grid, and the Floyd–Warshall algorithm for all-pairs shortest paths.

**When acceptable?** Small inputs or problems where this amount of work is
practical. Cubic growth becomes expensive quickly, so consider a more efficient
algorithm when n is large.

**Watch the loop bounds**: Three nested loops are not automatically cubic.
If their lengths are n, m, and k, the time is O(n × m × k). O(n³) describes
the common case where all three lengths scale proportionally to n.

---

### 7. **O(2ⁿ) - Exponential Time**

````markdown
# Big O: $O(2^n)$ — Exponential Time Complexity

In computer science, **$O(2^n)$** — pronounced **"Big O of 2 to the n"** — represents **exponential time complexity**.

If an algorithm has exponential time complexity, the time it takes to run **doubles** with every additional input item,
where input size is represented by **$n$**.

This type of algorithm is generally considered inefficient and impractical for large datasets.

---

## The Growth Problem

To understand how fast **$O(2^n)$** grows, look at how the number of operations increases as **$n$** becomes larger:

| Input Size | Operations |
|---:|---:|
| $n = 1$ | $2^1 = 2$ |
| $n = 10$ | $2^{10} = 1,024$ |
| $n = 20$ | $2^{20} = 1,048,576$ |
| $n = 50$ | $2^{50} = 1,125,899,906,842,624$ |

An algorithm with this complexity might run in a fraction of a second for **$n = 10$**, but could take **years** to
finish for **$n = 50$**.

---

## Classic Example: Recursive Fibonacci Sequence

A common example of an **$O(2^n)$** algorithm is the naive recursive solution for finding the **n-th Fibonacci number**.

The Fibonacci sequence is:

```text
0, 1, 1, 2, 3, 5, 8, ...
````

Each number is the sum of the two numbers before it.

Here is the naive recursive Python implementation:

```python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        # The function calls itself twice
        return fibonacci(n - 1) + fibonacci(n - 2)
```

---

## Why Is This $O(2^n)$?

Every time the function is called, it creates **two more recursive calls**.

This creates a branching tree of calculations.

For example, here is what happens when we calculate `fibonacci(4)`:

```text
                      fib(4)
                     /      \
               fib(3)        fib(2)
              /      \       /     \
          fib(2)   fib(1) fib(1)  fib(0)
          /    \
      fib(1)  fib(0)
```

Notice how the tree splits into two branches at almost every level.

As **$n$** gets larger:

* The tree gets deeper.
* The number of function calls increases rapidly.
* The amount of repeated work grows exponentially.

> **The flaw:**
> This algorithm is slow because it repeats the same calculations many times.
> For example, `fib(2)` is calculated more than once, and `fib(1)` is calculated multiple times.

---

## Real-World Analogy: Password Cracking

Imagine a combination lock.

If the lock has 3 dials and each dial has digits from 0 to 9, adding one more dial does not just add one more
possibility. It multiplies the total number of possibilities.

In a binary scenario, where each position can be either `0` or `1`:


| Password Length | Combinations |
| --------------: | -----------: |
|           1-bit |    $2^1 = 2$ |
|           2-bit |    $2^2 = 4$ |
|           3-bit |    $2^3 = 8$ |

Examples:

```text
1-bit: 0, 1
2-bit: 00, 01, 10, 11
3-bit: 000, 001, 010, 011, 100, 101, 110, 111
```

If someone tries to crack a password by guessing every possible combination, each extra bit or character can greatly
increase the time required.

---

## How to Fix It

Because **$O(2^n)$** algorithms scale poorly, programmers try to avoid them using better techniques.

### 1. Memoization / Dynamic Programming

Store previous results so the same calculation does not need to be repeated.

For Fibonacci, this can improve the algorithm from: O(2^n) to O(n)

```python
# We create a dictionary to store our previously calculated results
memo = {}


def fibonacci_memo(n):
    # 1. Check if we've already solved this specific sub-problem
    if n in memo:
        return memo[n]

    # Base cases
    if n <= 1:
        return n

    # 2. If not solved yet, calculate it and store it in the memo
    memo[n] = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)

    # 3. Return the stored result
    return memo[n]
```

```text
                       fib(4)
                     /      \
               fib(3)        fib(2) -> (Instantly returns cached value!)
              /      \     
          fib(2)   fib(1) -> (Instantly returns cached value!)
          /    \
      fib(1)  fib(0)
```

### 2. Iterative Approach

Fibonacci starts with `0, 1`; each following number is the sum of the previous
two. A loop avoids the repeated calculations of naive recursion.

```python
def fibonacci_iterative(n: int) -> int:
    """Return the Fibonacci number at index n (starting at index 0)."""
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b  # Move forward using the OLD values of a and b.
    return a


assert fibonacci_iterative(0) == 0
assert fibonacci_iterative(1) == 1
assert fibonacci_iterative(6) == 8
```

**How the update works:** `a, b = b, a + b` calculates both right-hand values
before assigning either variable. If `a=2` and `b=3`, they become `a=3` and
`b=5`. After n iterations, `a` holds the Fibonacci number at index n.

```text
Step     a    b
Start    0    1
1        1    1
2        1    2
3        2    3
4        3    5
5        5    8
6        8   13   → return a: 8
```

**Complexity:** O(n) time for n iterations and O(1) auxiliary space for a fixed
number of variables, assuming constant-cost integer arithmetic. Unlike recursion,
there is no growing call stack or memoization table. Python integers grow with
the result: counting individual bits, this implementation uses O(n) space and
O(n²) time for its growing integer additions.

---

## Summary

**$O(2^n)$** means the algorithm’s work doubles as the input size increases by one.

It is commonly seen in:

* naive recursive algorithms
* brute-force search
* generating all subsets
* solving problems by trying every possible combination

For small inputs, it may work fine.
For large inputs, it quickly becomes impractical.

```

```

### 8. **O(n!) - Factorial Time**

**$O(n!)$**—pronounced **"Big O of n factorial"**—represents **Factorial Time Complexity**.

This is the absolute worst common time complexity in computer science. While $O(2^n)$ grows incredibly fast, $O(n!)$
grows so mind-bogglingly fast that it makes exponential growth look slow. If an algorithm is $O(n!)$, it is essentially
useless for anything more than a handful of inputs.

---

## What is a Factorial?

In math, a factorial (written with an exclamation point `!`) means multiplying a number by every whole number below it
down to 1.

* $3! = 3 \times 2 \times 1 = 6$
* $5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$
* $10! = 3,628,800$

Now, look at how fast $O(n!)$ explodes compared to $O(2^n)$:


| $n$    | Exponential:$O(2^n)$ | Factorial:$O(n!)$                            |
| ------ | -------------------- | -------------------------------------------- |
| **5**  | 32                   | 120                                          |
| **10** | 1,024                | 3,628,800                                    |
| **15** | 32,768               | 1,307,674,368,000 (1.3 Trillion!)            |
| **20** | ~1 Million           | 2,432,902,008,176,640,000 (2.4 Quintillion!) |

If you tried to run an $O(n!)$ algorithm with $n=20$ on a standard modern computer, it would take **thousands of years**
to finish.

---

## Classic Example: Finding All Permutations

Exploring every possible arrangement of n distinct items produces n! permutations.
The total running time also depends on the work performed for each permutation.

Imagine you have a string of unique characters, like `"abc"`, and you want to write a function that prints every
possible way to arrange those letters.

* For the 1st position, you have **3** choices (`a`, `b`, or `c`).
* For the 2nd position, you only have **2** choices left.
* For the 3rd position, you only have **1** choice left.

Total arrangements = $3 \times 2 \times 1 = 6$.

Here is what the code looks like in Python using recursion:

```python
def get_permutations(string, pocket=""):
    if len(string) == 0:
        print(pocket)
    else:
        for i in range(len(string)):
            letter = string[i]
            remaining = string[:i] + string[i + 1:]
            # The loop spawns recursive calls for every remaining letter
            get_permutations(remaining, pocket + letter)


get_permutations("abc")

```

### Step-by-Step: How the Recursion Works

The function remembers two things:

- **`string`**: characters still available to choose.
- **`pocket`**: characters already chosen, in order.

#### 1. Choose the first character

The first call is `get_permutations("abc", "")`. The loop tries each possible
first character: `"a"`, then `"b"`, then `"c"`. Start with `"a"`:

```text
letter    = "a"
remaining = "bc"
pocket    = "" + "a" = "a"

Next call: get_permutations("bc", "a")
```

#### 2. Choose the second character

Now `"bc"` contains the available characters. Choose `"b"`:

```text
letter    = "b"
remaining = "c"
pocket    = "a" + "b" = "ab"

Next call: get_permutations("c", "ab")
```

#### 3. Choose the last character

Only `"c"` remains:

```text
letter    = "c"
remaining = ""
pocket    = "ab" + "c" = "abc"

Next call: get_permutations("", "abc")
```

#### 4. Reach the base case

The available string is empty, so the arrangement is complete:

```python
if len(string) == 0:
    print(pocket)  # Prints "abc"
```

The call returns to its caller. Once the `"c"` call finishes, execution returns
to the loop that was choosing from `"bc"`.

#### 5. Try the next choice

That loop already tried `"b"`. It now chooses `"c"` as the second character:

```text
get_permutations("bc", "a")
    choose "c"
    → get_permutations("b", "ac")
        choose "b"
        → get_permutations("", "acb")
            print "acb"
```

Both arrangements starting with `"a"` are now complete. The original call
resumes and tries `"b"` first, then `"c"` first:

```text
Start
├── a
│   ├── b → c → print abc
│   └── c → b → print acb
├── b
│   ├── a → c → print bac
│   └── c → a → print bca
└── c
    ├── a → b → print cab
    └── b → a → print cba
```

The output is:

```text
abc
acb
bac
bca
cab
cba
```

### How Does `remaining` Remove a Character?

```python
remaining = string[:i] + string[i + 1:]
```

It joins everything **before** index i with everything **after** it.
For `"abc"` with `i = 1`:

```text
string[:1] = "a"
string[2:] = "c"
remaining  = "ac"  # "b" was removed
```

Each recursive call gets its own string values. Strings are immutable, so
building `remaining` and `pocket + letter` does not change the caller's strings.
Returning from a call lets the previous loop continue with its next choice;
there is no need to explicitly undo a change to a shared list.

### Why Does the Number of Permutations Grow as n!?

The `for` loop runs $n$ times at the top level. Inside that loop, it calls the function recursively, which runs a
loop $n-1$ times, which calls a loop that runs $n-2$ times, and so on. This creates a nested structure that mirrors the
factorial math perfectly: $n \times (n-1) \times (n-2)...$

For `"abc"`, that is 3 × 2 × 1 = 6 permutations. For n distinct characters,
there are n! permutations.

**Why isn't this O(n) just because it has one loop?** The loop body calls
`get_permutations` again. You must count the work of those calls too:
the first call makes n recursive calls, each of those makes n−1 calls, and
so on. A loop with n iterations gives linear time only when the work per
iteration is bounded by a constant. See **How to Recognize an O(n) Function**
below for a step-by-step method.

**Precise time complexity for this implementation:** O(n × n!), including
string copying and printing all n characters of each of the n! permutations.
The factorial counts the arrangements; the extra n accounts for the work
needed to construct and output each full arrangement.

**Space complexity:** The recursion depth is O(n). Because active calls retain
copied strings of different lengths, this implementation uses O(n²) auxiliary
space at its deepest point. It prints results one at a time; collecting all
permutations in a list instead would require O(n × n!) output space.

### What If Characters Repeat? (`"aac"` Instead of `"abc"`)

The current function still prints six results, but some repeat:

```python
get_permutations("aac")
```

```text
aac
aca
aac
aca
caa
caa
```

The function chooses by **position**, so it treats the two `"a"` characters
as separate choices. Imagine labeling them a₁ and a₂ just to track which
position was chosen:

```text
First choice
├── a₁ → a₂c or ca₂ → prints aac, aca
├── a₂ → a₁c or ca₁ → prints aac, aca
└── c  → a₁a₂ or a₂a₁ → prints caa, caa
```

There are only **three unique permutations**: `"aac"`, `"aca"`, and `"caa"`.
To count unique permutations, divide n! by the factorial of each character's
frequency:

```text
Unique permutations = n! / (c₁! × c₂! × ...)

For "aac": n = 3, frequency of a = 2, frequency of c = 1
Unique permutations = 3! / (2! × 1!) = 6 / 2 = 3
```

Dividing by 2! accounts for swapping the two identical `"a"` characters,
which produces the same visible arrangement.

**Complexity stays the same for the current function:** It does not skip
duplicate choices, so it still explores n! completed paths and takes
O(n × n!) time to construct and print the results. Generating only unique
permutations requires skipping duplicate choices during recursion; removing
duplicates after generating them still pays for exploring those paths.

---

## The Real-World Nightmare: The Traveling Salesperson Problem (TSP)

The most famous real-world example of $O(n!)$ is the **Traveling Salesperson Problem**.

Imagine a delivery driver who needs to visit a specific number of cities and then return home. They want to find the *
*absolute shortest route** that visits every city exactly once.

If the driver uses a brute-force approach (checking every single possible route to compare distances):

* With **5 cities**, there are $5! = 120$ possible routes. (Easy, a computer does this instantly).
* With **10 cities**, there are $10! = 3,628,800$ routes. (Takes less than a second).
* With **15 cities**, there are $15! = 1.3$ trillion routes. (Takes minutes/hours).
* With **50 cities**, the number of routes is vastly larger than the total number of atoms in the observable universe.

## Can we optimize $O(n!)$?

Unlike $O(2^n)$, you usually can't just use memoization to make $O(n!)$ completely linear. Because every arrangement is
unique, you actually *have* to look at them all if you want a perfect answer.

To solve problems like the Traveling Salesperson for large datasets, programmers have to abandon looking for a
*perfect* answer and instead use **Heuristics** or **Approximation Algorithms
** (like Genetic Algorithms or Ant Colony Optimization). These give an answer that is 99% perfect in a fraction of a second, rather than waiting a trillion years for the 100% perfect route.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Spotting O(2^n) and O(n!) in Your Code

### Start Here: What Are We Counting?

**n is the input size.** For `"abc"`, n = 3.
**Big O describes how the work grows when n grows.** You do not need to count
seconds or every Python instruction. First count how many times the code
repeats its work.

Use this question while reading code:

> **Does it visit each item once, try two options for each item, or try every
> possible order?**

### 1. Visit Each Item Once → O(n)

```python
def show_letters(word):
    for letter in word:
        print(letter)


show_letters("abc")  # Prints a, b, c on separate lines
```

Trace it:

```text
"abc"   → 3 letters → 3 prints
"abcdef" → 6 letters → 6 prints
```

There is no extra search inside the loop. Each letter needs one print.
Twice as many letters means twice as much work: **O(n), linear time**.

### 2. Try Two Options for Each Item → 2^n Possibilities

Imagine two light switches. Each switch can be OFF (`0`) or ON (`1`).
To try every setting, choose both options for the first switch, then both
options for the second switch **under each earlier choice**:

```text
Start
├── First switch OFF
│   ├── Second OFF → 00
│   └── Second ON  → 01
└── First switch ON
    ├── Second OFF → 10
    └── Second ON  → 11
```

Two switches give 2 × 2 = 4 settings. Add a third switch and every existing
setting gets two endings: 000, 001, 010, 011, 100, 101, 110, 111.
That is 2 × 2 × 2 = 8 settings.

Here is code that does exactly that:

```python
def show_settings(n, chosen=""):
    if n == 0:                    # No switches left to decide
        print(chosen)
        return

    show_settings(n - 1, chosen + "0")  # Try OFF for this switch
    show_settings(n - 1, chosen + "1")  # Also try ON for this switch


show_settings(2)  # Prints 00, 01, 10, 11 on separate lines
```

**What to look for in code:**

- Both recursive calls run. Finishing the first call does not skip the second.
- Each call has one fewer item to decide: `n - 1`.
- Each decision has two options, so multiply 2 by itself n times: **2^n**.

For “include or exclude,” use the same idea: OFF means leave the item out;
ON means put it in. Each item doubles the number of possible selections.

**Use this immediately:** If code explores both choices for every one of n
items, expect exponential growth. Adding just one item doubles the outcomes.

### 3. Try Every Order → n! Possibilities

Now arrange `"abc"`. You cannot reuse a character after choosing it:

```text
Choose the first letter:   a, b, or c → 3 choices
Choose the second letter:  two left  → 2 choices
Choose the third letter:   one left  → 1 choice

Total = 3 × 2 × 1 = 6 orders
```

That multiplication is called **factorial**: 3! = 3 × 2 × 1.
For four different letters, it is 4! = 4 × 3 × 2 × 1 = 24 orders.

Look at these lines inside `get_permutations`:

```python
for i in range(len(string)):                 # Try EVERY remaining letter
    letter = string[i]
    remaining = string[:i] + string[i + 1:]  # Remove that letter
    get_permutations(remaining, pocket + letter)
```

**What to look for in code:**

- The recursive call is **inside the loop**, so it runs for every choice.
- Removing the chosen item leaves one fewer choice for the next call.
- Multiply the choices: **n × (n−1) × ... × 1 = n!**.

**Use this immediately:** If code picks each remaining item in turn and then
repeats that process on the rest, expect factorial growth.

### A Fast Comparison

| Input size n | Visit each item once | Try OFF/ON settings | Try every order of distinct items |
|---|---:|---:|---:|
| 3 | 3 visits | 8 settings | 6 orders |
| 4 | 4 visits | 16 settings | 24 orders |
| 5 | 5 visits | 32 settings | 120 orders |
| 10 | 10 visits | 1,024 settings | 3,628,800 orders |

The columns count visits or completed outcomes, not exact running times.

### One Final Check: What Does Each Result Cost?

First identify **how many results** the code explores. Then check the work
needed to build or process each result.

- One visit per item, with constant work each time → **O(n)** time.
- Exploring a full binary decision tree with constant work per call →
  **O(2^n)** time. `show_settings` also builds and prints strings of length n,
  so that particular implementation takes **O(n × 2^n)** time.
- Every order of n distinct items → **n! results**. `get_permutations` builds
  and prints n characters per result, so it takes **O(n × n!)** time.

The extra n counts the cost of producing each full result. The 2^n or n!
explains why the number of results grows so quickly.

### Your Checklist When You Open a Function

1. **Find n:** How many input items are there?
2. **Follow the loop body:** Is its work constant, or does it start more work?
3. **For recursion, follow the next calls:** One call? Two calls? A call for
   every remaining item? Check how much input each receives.
4. **Try n = 3 on paper:** Count all branches, not just one path to the end.
5. **Include copying and output costs** before stating the final time complexity.

**Avoid one shortcut:** Two recursive calls alone do not prove O(2^n).
The example above uses `n - 1`; merge sort gives each call roughly **half**
the input and takes O(n log n). Also check whether results are cached or
branches are skipped; the full-search counts above assume every branch runs.

**Quick practice:** “Choose any group of students” gives include/exclude
choices → 2^n groups. “Put all students in a line” gives decreasing choices
→ n! orders. “Check each student's name once” gives one pass → O(n) time,
assuming constant work per name.

---

## Understanding the Exponential vs Factorial Difference

**2^n (Exponential)** = "At each step, 2 choices"

- Binary problems: subset generation, backtracking with 2 branches
- Slower than factorial for small n, but same "explosive" nature

**n! (Factorial)** = "At each step, decreasing choices"

- Permutation problems: "arrange these items"
- Even worse than 2^n because choices don't stay at 2

### Side-by-Side Comparison:

```
        Growth Rate Visualization

n=10    2^10 = 1,024             10! = 3,628,800
        ███ Fast enough           ████████████████████ Already slow

n=15    2^15 = 32,768            15! = 1.3 trillion
        ███████ Okay              ████████████████████████████ Hours

n=20    2^20 = 1 million          20! = 2.4 quintillion
        ███████████ Still okay    ████████████████████████████████
                                  Days or Years

n=25    2^25 = 33 million         25! = 10^25
        ███████████████ Slow      ████████████████████████████████
                                  (More stars than atoms on Earth!)
```

### When You'll Actually Encounter These:


| Scenario                  | Complexity | n=5 | n=10 | n=15 |
| ------------------------- | ---------- | --- | ---- | ---- |
| **Lightbulbs ON/OFF**     | O(2^n)     | 32  | 1K   | 33K  |
| **Coin change ways**      | O(2^n)     | 32  | 1K   | 33K  |
| **Tower of Hanoi**        | O(2^n)     | 31  | 1K   | 33K  |
| **Letter anagrams**       | O(n!)      | 120 | 3.6M | 1.3T |
| **Traveling Salesman**    | O(n!)      | 120 | 3.6M | 1.3T |
| **Password permutations** | O(n!)      | 120 | 3.6M | 1.3T |

### Why 2^n grows faster than n² but slower than n!?

For **n=5**:

- O(n²) = 25 operations
- O(2^n) = 32 operations ← 28% worse
- O(n!) = 120 operations ← 4.8x worse

For **n=10**:

- O(n²) = 100 operations
- O(2^n) = 1,024 operations ← 10x worse
- O(n!) = 3,628,800 operations ← 35,000x worse!

For **n=15**:

- O(n²) = 225 operations
- O(2^n) = 32,768 operations ← 146x worse
- O(n!) = 1,307,674,368,000 operations ← 5.8 million times worse!

**The gap only gets worse** as n increases.

---

## Quick Comparison Table


| Notation   | n=10            | n=20                | n=25           | Verdict                |
| ---------- | --------------- | ------------------- | -------------- | ---------------------- |
| O(1)       | 1               | 1                   | 1              | ✅ Instant             |
| O(log n)   | 3.3             | 4.3                 | 4.6            | ✅ Great               |
| O(n)       | 10              | 20                  | 25             | ✅ Good                |
| O(n log n) | 33              | 86                  | 115            | ✅ Good                |
| O(n²)     | 100             | 400                 | 625            | ⚠️ Caution           |
| O(n³)     | 1K              | 8K                  | 15K            | ❌ Avoid               |
| **O(2ⁿ)** | **1,024**       | **1 million**       | **33 million** | ❌**Exponential Doom** |
| **O(n!)**  | **3.6 million** | **2.4 quintillion** | **10²⁵**     | ❌**Impossible**       |

**Real-world timing** (assuming 1 billion operations/second):

- O(2^10) = 1,024 ops → 0.000001 seconds ✅
- O(2^20) = 1 million ops → 0.001 seconds ✅
- O(2^30) = 1 billion ops → 1 second ⚠️
- O(2^40) = 1 trillion ops → 17 minutes ❌
- O(10!) = 3.6 million ops → 0.0036 seconds ✅
- O(20!) = 2.4 quintillion ops → 77 million years ❌❌❌

---

## How to Analyze Code

Big O is the notation for describing growth; **O(n)** is one particular
growth rate, called linear time. To find a function's complexity, count its
total work, including helper functions and recursive calls.

**Step 1**: Identify loops and recursion depth
**Step 2**: Multiply complexities of nested structures
**Step 3**: Drop constants and lower-order terms
**Step 4**: Focus on worst-case scenario

### How to Recognize an O(n) Function

1. **Define n.** Usually it is the number of input items, such as `len(lst)`.
2. **Choose the case to analyze.** For worst-case time, count the most work
   the function can do on an input of size n, including branches and early returns.
3. **Count repetitions.** How many times does each operation run across the
   entire function, including all helper calls and recursive calls?
4. **Check the cost of the repeated work.** Arithmetic on fixed-size values
   and list indexing are O(1). A slice, sort, search, or recursive call can
   add work that grows with the input.
5. **Combine and simplify.** Add sequential work, multiply nested work when
   appropriate, then drop constant factors and lower-order terms. If the
   work grows proportionally to n, describe it as O(n).

For example:

```python
def count_positive(numbers):
    count = 0                         # Constant setup
    for number in numbers:            # n iterations
        if number > 0:                # Constant work per iteration
            count += 1
    return count                      # Constant final work
```

Under the usual constant-cost arithmetic assumption, this does at most
a constant amount of work per item:

```text
Total work = constant setup + n × constant work + constant return
           = a × n + b, for fixed constants a and b
Time       = O(n)
Extra space = O(1)
```

**Useful patterns:**


| Pattern                                               | Time             | Reason                                      |
| ----------------------------------------------------- | ---------------- | ------------------------------------------- |
| One pass with O(1) work per item                      | O(n)             | n × constant work                          |
| Two sequential passes                                 | O(n)             | n + n = 2n; drop the constant 2             |
| One pass with an O(n) search each iteration           | O(n²)           | n × n work                                 |
| Repeatedly halve the remaining size                   | O(log n)         | Only logarithmically many steps             |
| Recursive calls branching over every remaining choice | Factorial growth | Count all branches, as in`get_permutations` |

**What does “branching over every remaining choice” mean?** Each call tries
every item still available, making a recursive call for each choice. In
`get_permutations("abc")`, the choices unfold as follows:

1. **First position: 3 choices.** Choose `"a"`, `"b"`, or `"c"`. Each choice
   starts a separate recursive call with two characters remaining.
2. **Second position: 2 choices per branch.** After choosing `"a"`, choose
   `"b"` or `"c"`. The other first-choice branches also have two choices.
   There are now 3 × 2 = 6 partial arrangements.
3. **Third position: 1 choice per branch.** Each branch has one character
   left, producing 3 × 2 × 1 = 3! = 6 completed permutations.

```text
Start
├── choose a (remaining: bc)
│   ├── choose b → choose c → abc
│   └── choose c → choose b → acb
├── choose b (remaining: ac)
│   ├── choose a → choose c → bac
│   └── choose c → choose a → bca
└── choose c (remaining: ab)
    ├── choose a → choose b → cab
    └── choose b → choose a → cba
```

With four distinct characters, there are 4 × 3 × 2 × 1 = 4! = 24
permutations. With n distinct characters, there are n! permutations.

**Count all branches, not just the depth:** Each path makes n choices,
but there are n! completed paths. Printing every full permutation adds n
characters of work per path, so the shown `get_permutations` implementation
takes O(n × n!) time.

Recursion can also be linear: a function that makes one call on size n−1
and does O(1) extra work per call has O(n) time. Recursion depth alone does
not determine time; branching can create many more calls than the depth.

**Sanity check:** Doubling the input should roughly double the growing work
of a linear-time algorithm. Timing measurements can support the analysis,
but constants, small inputs, and runtime noise mean they do not prove Big O.

### Example Analysis:

```python
def example(lst):
    for i in lst:  # O(n)
        print(i)

    for i in lst:  # O(n)
        for j in lst:  # O(n)
            print(i, j)

    # Total: O(n) + O(n²) = O(n²)  ← Highest order dominates
```

---

## Space Complexity

Big O also measures **memory usage**:

```python
def space_example(n):
    new_list = [0] * n  # O(n) space - proportional to n


def constant_space(n):
    total = 0
    for i in range(n):  # O(1) space - only one variable
        total += i
    return total
```

---

## Best / Average / Worst Case Analysis

Big O focuses on **worst case**, but real-world performance varies:

```python
def linear_search(lst, target):
    for item in lst:
        if item == target:
            return True
    return False

# Best case: O(1) - target is first element
# Average case: O(n/2) = O(n) - target in middle
# Worst case: O(n) - target not found or at end
```

**When each matters:**

- **Best Case**: Lucky scenario (rare in analysis)
- **Average Case**: Most realistic (what users experience)
- **Worst Case**: Critical for predictability (SLAs, deadlines)

### Quick Sort Example:

```python
# Quick Sort:
# - Best/Average: O(n log n)
# - Worst: O(n²) if pivot always picks smallest/largest
# - Randomized pivot makes worst case extremely unlikely
```

**Application Impact**:

- Payment systems → need worst-case guarantees
- Caching systems → average case more important
- Real-time systems → predictable performance > average speed

---

## Amortized Complexity

Operations that are sometimes slow but average fast over time.

```python
# Python list.append() with dynamic resizing
lst = []
for i in range(1000000):
    lst.append(i)  # Looks O(1), but occasionally O(n)!
# Overall amortized: O(1) per operation
```

**How it works:**

- Most appends: O(1) - just add to end
- Periodic resizes: O(n) - copy entire array to larger array
- Over many operations: average becomes O(1)

```
Operations: [O(1), O(1), O(1), O(n), O(1), O(1), ... O(1), O(n)]
Amortized:  Total cost / Number of operations = O(1)
```

**Real-world**: Dynamic arrays, hash table resizing, garbage collection pauses.

---

## Hidden Costs (Deceptive Operations)

Operations that seem O(1) but aren't:

```python
# ❌ String concatenation (O(n) in Python - strings are immutable)
result = ""
for i in range(10000):
    result += str(i)  # Each += creates new string! Total: O(n²)

# ✅ Use list and join
result = []
for i in range(10000):
    result.append(str(i))  # O(1) append
result = "".join(result)  # O(n) once at end, Total: O(n)
```

```python
# ❌ List slicing copies data - O(k) where k is slice size
large_list = list(range(1000000))
sublist = large_list[500000:]  # O(500000) hidden cost!

# ✅ Use indices or iterators for large data
for item in large_list[500000:]:  # Still O(n) to iterate
    process(item)
```

```python
# ❌ Checking membership in list - O(n)
if item in my_list:  # Linear search
    process(item)

# ✅ Use sets for O(1) lookup
if item in my_set:  # Hash lookup
    process(item)
```

**Common Hidden Costs:**


| Operation               | Apparent | Actual | Solution        |
| ----------------------- | -------- | ------ | --------------- |
| `str += str`            | O(1)     | O(n)   | Use list + join |
| `lst[start:end]`        | O(1)     | O(k)   | Use indices     |
| `item in lst`           | O(1)?    | O(n)   | Use set         |
| `lst.insert(0, x)`      | O(1)?    | O(n)   | Use deque       |
| `dict.values().count()` | O(1)?    | O(n)   | Cache counts    |

---

## Space-Time Tradeoff

Using more memory to reduce time (or vice versa).

### Example 1: Caching Results

```python
# Time: O(n), Space: O(1)
def sum_to_n(n):
    return n * (n + 1) // 2


# Time: O(1), Space: O(n)
results_cache = {}
for n in range(1000000):
    results_cache[n] = n * (n + 1) // 2

value = results_cache[5000]  # Instant lookup
```

### Example 2: HashMap for Fast Lookup

```python
# Time: O(n²), Space: O(n)
def find_pairs_O_n2(lst, target):
    pairs = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] + lst[j] == target:
                pairs.append((lst[i], lst[j]))
    return pairs


# Time: O(n), Space: O(n)
def find_pairs_O_n(lst, target):
    seen = {}
    pairs = []
    for num in lst:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen[num] = True
    return pairs
```

**When to apply:**

- **High traffic APIs**: Cache results, trade memory for latency
- **Mobile apps**: Minimize memory, accept slower processing
- **Data science**: Load entire dataset in memory for fast processing
- **Embedded systems**: Memory limited, can't cache

---

## Practical Performance Profiling

Theory meets reality here. Always measure actual performance:

```python
import time


def slow_function():
    result = ""
    for i in range(100000):
        result += str(i)
    return result


def fast_function():
    result = []
    for i in range(100000):
        result.append(str(i))
    return "".join(result)


# Measure actual performance
start = time.time()
slow_function()
print(f"Slow: {time.time() - start:.4f}s")  # ~2-3 seconds

start = time.time()
fast_function()
print(f"Fast: {time.time() - start:.4f}s")  # ~0.01 seconds
```

**Use Python's tools:**

```python
import cProfile
import pstats

cProfile.run('slow_function()', sort='cumulative')
# Shows actual time spent in each function
```

**Real data matters**: An O(n) algorithm with huge constants can be slower than O(n²) for small datasets.

---

## Data Structure Selection by Big O

Choose data structures based on your access patterns:


| Operation        | List  | Dict | Set  | Deque  | Tuple |
| ---------------- | ----- | ---- | ---- | ------ | ----- |
| Access by index  | O(1)  | -    | -    | O(n)   | O(1)  |
| Search           | O(n)  | -    | O(1) | O(n)   | O(n)  |
| Insert at start  | O(n)  | -    | -    | O(1)   | -     |
| Insert at end    | O(1)* | -    | -    | O(1)   | -     |
| Insert at middle | O(n)  | -    | -    | O(n)   | -     |
| Delete           | O(n)  | -    | O(1) | O(1)** | -     |
| Membership test  | O(n)  | O(1) | O(1) | O(n)   | O(n)  |

*Amortized. **At ends only.

**Selection strategy:**

```python
# Frequent lookups? → Use dict or set
user_ids = {1001, 1002, 1003}  # O(1) membership
if user_id in user_ids:
    process(user_id)

# Need ordered + fast lookup? → Use combination
users = {id: name for id, name in data}  # O(1) lookup

# Frequent insertion at both ends? → Use deque
from collections import deque

queue = deque()
queue.append(item)  # Add to right: O(1)
queue.appendleft(item)  # Add to left: O(1)
queue.popleft()  # Remove from left: O(1)
```

---

## Real-World Application Contexts

Big O impact varies by context:

### Web Applications

```python
# Database query with O(n²) algorithm might still be fast (n=100)
# But in-memory processing of million records with O(n²) is disaster
# Web context: network + DB I/O often > algorithm cost
# BUT: cache n million records, suddenly algorithm complexity matters
```

### Machine Learning

```python
# Training data: 1 million samples × 1000 features
# O(n²) = 1 trillion operations - unusable
# O(n log n) = 20 billion operations - feasible
# Complexity is critical factor in model selection
```

### Databases

```python
# Index: O(log n) lookup vs O(n) table scan
# For 10M rows: log₂(10M) ≈ 23 comparisons vs 10M scans
# Index almost always worth the memory cost
```

### Stream Processing

```python
# Can't load entire stream into memory
# Must use O(1) or O(log n) algorithms
# Windowing, aggregation, sketching techniques required
```

---

## Premature Optimization vs Strategic Optimization

**Premature optimization** (BAD):

```python
# Don't optimize unclear code for marginal gains
# 90% of time spent in 10% of code
result = [x * 2 for x in data]  # Readable, clear
# Don't micro-optimize to result = list(map(lambda x: x*2, data))
```

**Strategic optimization** (GOOD):

```python
# Fix algorithms with exponential or quadratic complexity
# Profile first to find bottlenecks
# Only optimize the hot path (where time is actually spent)

# BEFORE: Heavy operation called in nested loop
for user in users:  # 1000 users
    for post in user.posts:  # 50 posts each
        if is_spam(post):  # O(n) spam check
            delete(post)  # 50,000 calls * O(n) = disaster

# AFTER: Preprocess spam filter
spam_filter = load_spam_filter()  # O(1) lookup
for user in users:
    for post in user.posts:
        if is_spam_fast(post, spam_filter):  # O(1)
            delete(post)
```

**Rule of thumb:**

- Code readability > premature micro-optimizations
- Always profile before optimizing
- Focus on algorithmic improvements (Big O) first
- Only then optimize implementation constants

---

## Common Mistakes Developers Make

```python
# ❌ Assuming all O(n) algorithms are equivalent
def sort_v1(lst):
    return sorted(lst)  # O(n log n) with optimized C code


def sort_v2(lst):
    for i in range(len(lst)):
        for j in range(len(lst) - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst  # O(n²) with Python overhead

# Both "sort" but vastly different performance

# ❌ Ignoring constants and practical performance
# O(1) doesn't mean instant - could be slow constant
# 1 million hashes per second still counts

# ❌ Assuming worst case always happens
# Quick Sort is O(n²) worst case but O(n log n) average
# Safe to use with randomized pivot

# ❌ Parallelization doesn't fix bad complexity
# O(n²) with 4 cores = O(n²/4), still quadratic
# Must fix algorithm, not just add threads
```

---

## Practical Optimization Checklist

When performance is an issue:

1. **Profile First**

   ```python
   import cProfile
   cProfile.run('main()')
   # Find actual bottleneck
   ```
2. **Identify Complexity**

   - Is it algorithmic? (Big O issue)
   - Is it constant overhead? (implementation issue)
   - Is it I/O? (network, disk)
3. **Choose Optimization Strategy**

   - Algorithm change: Usually biggest impact
   - Data structure change: Often 10-100x improvement
   - Implementation: Usually 2-10x improvement
   - Hardware/parallel: Addresses specific bottlenecks
4. **Measure Impact**

   ```python
   # Before
   time_before = time.time()
   result = old_approach(data)
   time_old = time.time() - time_before

   # After
   time_before = time.time()
   result = new_approach(data)
   time_new = time.time() - time_before

   improvement = (time_old - time_new) / time_old * 100
   print(f"Improved by {improvement:.1f}%")
   ```

---

## Practical Optimization Tips


| Problem                 | Naive              | Optimized              | Improvement  |
| ----------------------- | ------------------ | ---------------------- | ------------ |
| Searching unsorted data | O(n)               | Use hash set: O(1)     | 1000x faster |
| Finding duplicates      | O(n²)             | Hash map: O(n)         | Huge         |
| Retrieving data         | O(n) linear search | Hash/Index: O(1)       | Massive      |
| Sorting                 | O(n²) Bubble      | O(n log n) Merge/Quick | Critical     |

---

## Key Takeaways

**Foundational**
✅ **Always consider Big O** when choosing algorithms
✅ **Focus on worst case** for predictable performance
✅ **Test with large inputs** to reveal complexity issues

**Practical Application**
✅ **Profile first, optimize second** - find actual bottlenecks
✅ **Hidden costs matter** - strings, slicing, type checking
✅ **Choose data structures strategically** - Big O guides selection
✅ **Balance readability vs optimization** - premature optimization is evil

**Advanced Thinking**
✅ **Understand space-time tradeoffs** - memory for speed, or vice versa
✅ **Consider amortized complexity** - occasional slowness averaged out
✅ **Context matters** - web, DB, ML, streaming have different constraints
✅ **Constants and implementation matter** - Big O tells half the story

---

## Decision Tree: When to Optimize

```
Is performance a problem?
├─ No? → Ship it (readability > premature optimization)
└─ Yes?
   ├─ Profile to find bottleneck
   │  ├─ Algorithmic (Big O issue)? → Change algorithm
   │  ├─ Constant overhead? → Optimize implementation
   │  └─ I/O bound? → Caching, parallelization, async
   │
   └─ Impact worth complexity trade-off?
      ├─ Yes → Implement optimization
      └─ No → Document as technical debt
```

---

## Testing Big O Assumptions

```python
import time
import matplotlib.pyplot as plt


def measure_performance(func, sizes):
    """Verify Big O claims with actual measurements"""
    times = []
    for n in sizes:
        data = list(range(n))
        start = time.perf_counter()
        func(data)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return times


# For O(n): time ∝ n
# For O(n²): time ∝ n²
# Plot actual times vs expected curve to verify

sizes = [1000, 5000, 10000, 50000, 100000]
times = measure_performance(my_function, sizes)

# If O(n): times should roughly double when size × 2
# If O(n²): times should roughly quadruple when size × 2
for i in range(1, len(times)):
    ratio = times[i] / times[i - 1]
    size_ratio = sizes[i] / sizes[i - 1]
    print(f"Size ×{size_ratio:.0f} → Time ×{ratio:.1f}")
    # Should see ×2 time for O(n), ×4 for O(n²)
```

---

## Resources for Practice

**Online Judges**

- **LeetCode**: Filter by complexity, see patterns
- **HackerRank**: Tutorials with complexity analysis
- **CodeSignal**: Interactive complexity challenges

**Visualization**

- **VisuAlgo**: Watch algorithms run with Big O visualization
- **Big-O CheatSheet**: Visual reference (bigocheatsheet.com)

**Real Projects**

- Implement your own: dict, list, tree structures
- Read source: Python collections, NumPy, pandas
- Contribute to open source: See optimization in practice
