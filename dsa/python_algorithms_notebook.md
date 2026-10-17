# Python algorithms handbook: learn, explain, and practice

> Examples target **Python 3.11+**. You should be comfortable with lists, dictionaries, loops, functions, and basic classes. Use the [data-structures handbook](../handbook/notes/python_data_structures_interview_handbook.md) for collection behavior and the [Python interview reference](../handbook/notes/python_interview_reference_guide.md) for language fundamentals.

**Indices start at zero:** in `[8, 3, 5]`, values 8, 3, and 5 have indices 0, 1, and 2. A value answers “what?”; an index answers “where?”

**Read the type hints as labels:** `list[int]` means a list of integers, `-> bool` means a Boolean result, and `tuple[int, int] | None` means a pair of indices or no answer. Type hints do not validate inputs automatically.


## Contents

- [Part 1. Understand time and memory](#part-1-understand-time-and-memory)
  - [1. How to report Big O](#1-how-to-report-big-o)
  - [2. Linear search](#2-linear-search)
- [Part 2. Find, count, and order items](#part-2-find-count-and-order-items)
  - [3. Frequency counting](#3-frequency-counting)
  - [4. Hash map: two sum](#4-hash-map-two-sum)
  - [5. Sorting: prefer Python's built-ins](#5-sorting-prefer-pythons-built-ins)
  - [6. Binary search and boundaries](#6-binary-search-and-boundaries)
  - [7. Two pointers on sorted input](#7-two-pointers-on-sorted-input)
- [Part 3. Work with consecutive items and ranges](#part-3-work-with-consecutive-items-and-ranges)
  - [8. Fixed-size sliding window](#8-fixed-size-sliding-window)
  - [9. Variable-size sliding window](#9-variable-size-sliding-window)
  - [10. Prefix sums: repeated range queries](#10-prefix-sums-repeated-range-queries)
  - [11. Kadane's algorithm: maximum contiguous sum](#11-kadanes-algorithm-maximum-contiguous-sum)
  - [12. Merge intervals](#12-merge-intervals)
- [Part 4. Manage pending work and links](#part-4-manage-pending-work-and-links)
  - [13. Stack and queue operations in Python](#13-stack-and-queue-operations-in-python)
  - [14. Stack: balanced brackets](#14-stack-balanced-brackets)
  - [15. Monotonic stack: next greater element](#15-monotonic-stack-next-greater-element)
  - [16. Linked lists: reverse links and detect cycles](#16-linked-lists-reverse-links-and-detect-cycles)
- [Part 5. Explore trees and graph connections](#part-5-explore-trees-and-graph-connections)
  - [17. Binary tree inorder traversal](#17-binary-tree-inorder-traversal)
  - [18. Why a stack gives DFS and a queue gives BFS](#18-why-a-stack-gives-dfs-and-a-queue-gives-bfs)
  - [19. BFS: shortest path in an unweighted graph](#19-bfs-shortest-path-in-an-unweighted-graph)
  - [20. DFS: reachability and components](#20-dfs-reachability-and-components)
  - [21. Topological sort: dependencies](#21-topological-sort-dependencies)
- [Part 6. Prioritize the next choice](#part-6-prioritize-the-next-choice)
  - [22. Heap: retain the largest k items](#22-heap-retain-the-largest-k-items)
  - [23. Dijkstra: shortest paths with nonnegative weights](#23-dijkstra-shortest-paths-with-nonnegative-weights)
  - [24. Greedy: maximum non-overlapping meetings](#24-greedy-maximum-non-overlapping-meetings)
- [Part 7. Reuse answers and explore alternatives](#part-7-reuse-answers-and-explore-alternatives)
  - [25. Dynamic programming: climbing stairs](#25-dynamic-programming-climbing-stairs)
  - [26. Dynamic programming: minimum coins](#26-dynamic-programming-minimum-coins)
  - [27. Backtracking: enumerate subsets](#27-backtracking-enumerate-subsets)
  - [28. Union-find: repeated connectivity checks](#28-union-find-repeated-connectivity-checks)
- [Quick revision](#quick-revision)
- [Additional references](#additional-references)

## Part 1. Understand time and memory

Start by counting work and retained items. A simple scan is the baseline for later improvements.

### 1. How to report Big O

**Start with this question:** “If the list grows from 4 items to 8, what changes?” A scan may inspect twice as many items. Indexing still jumps straight to one position. The amount of work depends on what the algorithm does, not just on the size of the input.

**Two separate questions:** time asks “how much work?”; space asks “how much memory must we keep?” A loop can do lots of work while remembering only one running total.

Define input sizes first: `n` items, `m` items in another collection, `V` graph vertices, `E` edges, `h` tree height, `k` requested results.

**Card-counting experiment:** place 8 numbered cards face up. Reading each card once takes 8 visits; doing it twice takes 16. Both grow linearly, O(n). Checking every pair takes `8 × 7 / 2 = 28` comparisons. At 16 cards, that becomes 120: quadratic growth, O(n²).

Big O describes growth, not a stopwatch reading or a difficulty score. An O(n²) solution can be perfectly adequate for ten items; input limits help decide what improvement is needed.

- **Time** counts work as input grows, not elapsed seconds. Drop constants and lower-order terms: `3n + 10` → O(n); `n² + n` → O(n²).
- **Auxiliary space** here excludes the existing input and returned output. Count temporary collections and recursion frames. State output space separately.
- Report **peak memory alive at once**, not all allocations added over the entire run.
- Bounds are worst-case unless a different kind of bound is named. Keep these meanings separate:

| Term | Question it answers | Example |
| --- | --- | --- |
| Worst case | What is the most work for this input size? | An absent target requires a full linear scan |
| Average / expected | What work do we expect under stated input/randomness assumptions? | Hash lookup is average O(1); collisions can make it slower |
| Amortized | What does each operation cost when we spread occasional expensive work across many operations? | Most list appends are cheap; occasional resizing copies existing references |

An amortized O(1) append does not promise that **every** append takes constant work.
- Assume fixed-size numeric operations/comparisons are O(1). Very large integers or long string comparisons can add costs.

**First pass:** focus on O(1), O(log n), O(n), O(n log n), and O(n²). The last two rows will make more sense when we generate subsets and permutations. In binary search, `log n` counts how many times we can halve the range.


| Growth      | Typical example              | Doubling input                        |
| --- | --- | --- |
| O(1)        | List indexing                | Roughly unchanged                     |
| O(log n)    | Binary search                | About one more halving                |
| O(n)        | One scan                     | About twice the work                  |
| O(n log n)  | Efficient comparison sort    | A little more than twice              |
| O(n²)      | Every pair                   | About four times                      |
| O(n × 2ⁿ) | Materialize all subsets      | Grows rapidly; output itself is large |
| O(n × n!)  | Materialize all permutations | Grows even faster                     |

```python
def total(values: list[int]) -> int:
    result = 0
    for value in values:
        result += value
    return result


assert total([2, 3, 4]) == 9
assert total([]) == 0
```

One scan: **O(n) time, O(1) auxiliary space**. For `[2, 3, 4]`, the running total changes `0 → 2 → 5 → 9`. We keep one total, not a history of all totals. The existing list is input memory; reading it does not copy it.

“Auxiliary” just means **extra working memory**. A function that returns a new list also needs memory for its output. We report that separately so you can see where memory goes.

Compare `[x * x for x in values]`: O(n) time, **O(n) output**, O(1) auxiliary space excluding that output. An O(n) loop does not automatically require O(n) memory.

#### Python costs that hide inside algorithms


| Operation                        | Time                  | Space / caution                                      |
| --- | --- | --- |
| `values[i]`                      | O(1)                  | Direct list access                                   |
| `x in values` for a list         | O(n)                  | Can hide a scan inside another loop                  |
| `list.append(x)`                 | Amortized O(1)        | An occasional resize is O(n)                         |
| `list.pop(0)`                    | O(n)                  | Shifts later items; use `deque.popleft()` for a queue |
| `set` membership / `dict` lookup | Average O(1)          | Keys/elements must be hashable                       |
| `values[a:b]` for `k` items      | O(k)                  | Allocates a new list of O(k) references              |
| `sorted(values)`                 | O(n log n) worst case | New O(n) result; sorting also needs temporary memory |
| `values.sort()`                  | O(n log n) worst case | Mutates input, but can use O(n) temporary memory     |

Two consecutive scans are O(n + n) = O(n). A full scan of `m` items for every one of `n` items is O(n × m). A nested loop can still be O(n) if its pointers only move forward a total of n times, as in a sliding window.

**Teaching check:** “A sum loops over a million items. Why can its extra space still be O(1)?” It retains one running total rather than a million intermediate answers. A returned list of a million squares does grow with the input.

### 2. Linear search

**Use when:** input is unsorted or there are only a few lookups. Check items one at a time; stop at the first match.

**Walk through it:** find 3 in `[8, 3, 5]`. Check 8 (no), then 3 (yes), and return index 1. If the target is absent, every item must be checked. `index` tells us where we are; `value` is the item at that position.

```python
def linear_search(values: list[int], target: int) -> int:
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


assert linear_search([8, 3, 5], 3) == 1
assert linear_search([], 3) == -1
```

**Time:** O(n) worst, O(1) best. **Auxiliary space:** O(1). No sorting prerequisite or preprocessing cost.

#### Pause and predict: Card detective

Find 9 in `[4, 9, 2, 7]`. How many comparisons? How many if the target is 8? Does checking twice as many cards require storing twice as many answers?

<details>
<summary>Open after predicting</summary>

Two comparisons find 9; four prove 8 is absent. A scan only needs its current position, so auxiliary memory can stay O(1).

</details>

## Part 2. Find, count, and order items

First remember values with dictionaries, then use sorted order to guide a search. Sorting appears before binary search and two pointers.

### 3. Frequency counting

**Problem:** decide whether two words have exactly the same characters and counts. Such words are **anagrams**: `"aab"` and `"aba"` match, but `"aab"` and `"abb"` do not.

**Idea:** make a tally sheet. Counting all characters once avoids looking through the word again for every character.

**Walk through it:** `"aab"` gives counts `a: 2, b: 1`; `"aba"` gives the same counts. They are anagrams because rearranging characters changes their positions, not their counts.

First build one tally by hand. `get(character, 0)` starts a character's count at zero if it has not appeared yet.

```python
counts = {}
for character in "aab":
    counts[character] = counts.get(character, 0) + 1
assert counts == {"a": 2, "b": 1}
```

`Counter` performs this counting for us; comparing two counters compares their character counts.

```python
from collections import Counter


def are_anagrams(left: str, right: str) -> bool:
    return Counter(left) == Counter(right)


assert are_anagrams("aab", "aba")  # The walkthrough example.
assert are_anagrams("listen", "silent")
assert not are_anagrams("aab", "abb")
assert not are_anagrams("A", "a")
```

**Time:** O(n + m) average for two strings. **Auxiliary space:** O(u), where `u` is the total number of distinct characters across the counters. Do not claim O(1) space unless the alphabet is explicitly fixed. Case/whitespace normalization changes the problem; only do it if requested.

### 4. Hash map: two sum

**When to use it:** find a pair with a target value. Store previously seen values and ask whether the required complement has appeared.

**Walk through it:** target 9, input `[2, 7, 11]`.


| Current item | Needed partner (`target - value`) | Previously seen | Action                        |
| --- | --- | --- | --- |
| 2 at index 0 | 7                                 | `{}`            | Remember `2: 0`                |
| 7 at index 1 | 2                                 | `{2: 0}`        | Found partner: return `(0, 1)` |

`seen` maps an earlier value to its index. “Complement” simply means the partner needed to reach the target.

```python
def two_sum(values: list[int], target: int) -> tuple[int, int] | None:
    seen = {}
    for index, value in enumerate(values):
        complement = target - value
        if complement in seen:
            return seen[complement], index
        seen[value] = index
    return None


assert two_sum([2, 7, 11], 9) == (0, 1)  # The walkthrough example.
assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 3], 6) == (0, 1)
assert two_sum([3], 6) is None
```

**Why this saves work:** checking every pair repeats comparisons. The dictionary remembers earlier cards, so each new card asks one question: “Have I already seen my missing partner?” It returns **indices**, not the card values.

**Time:** O(n) average. **Auxiliary space:** O(n) because the dictionary can keep one entry per item. Check before inserting so `[5]` cannot match itself for target 10; `[5, 5]` can use two different indices. Returns one pair, not all pairs.

### 5. Sorting: prefer Python's built-ins

**Problem:** arrange quiz results by score, lowest first. For Ana 90, Ben 70, and Cy 90, Ben comes first; Ana stays before Cy because their scores tie. `key=lambda row: row[1]` means “use the score, at position 1, for comparisons.”

```python
records = [("Ana", 90), ("Ben", 70), ("Cy", 90)]
by_score = sorted(records, key=lambda row: row[1])
assert by_score == [("Ben", 70), ("Ana", 90), ("Cy", 90)]
assert records[0] == ("Ana", 90)  # Original unchanged.
```

Python's sort is **stable**: equal sort keys retain their relative input order. `sorted()` returns a new list; `.sort()` mutates a list and returns `None`.

**Time:** O(n log n) worst, O(n) for already ordered runs. **Space:** `sorted()` returns O(n) output and can use O(n) sorting workspace; `.sort()` can also require O(n) workspace despite mutating input. An expensive `key` function adds its own cost.

#### What is Timsort?

Python's built-in sorting belongs to the **Timsort** family: it notices already ordered stretches, called **runs**, and combines them. Short runs can be extended using insertion sort, which places the next item into its correct position among items already ordered.

Think of two sorted piles of cards: `[1, 3, 5]` and `[2, 4, 6]`. To combine them, repeatedly take the smaller front card: 1, 2, 3, 4, 5, 6. Existing order saves work. This illustrates merging; a tiny input may actually be handled by extending a run rather than that exact sequence of merges.

“Adaptive” means existing order can help; “stable” means equal keys keep their relative input order. Built-in sorting has O(n log n) worst-case time and O(n) best-case time on sorted input. Temporary merging storage can be O(n), even for `.sort()`.

#### Selection sort: an easy first manual sort

Imagine arranging numbered cards. Find the smallest card in the unsorted part and move it to the next open position.

```text
Position 0: [3, 1, 2] → smallest remaining is 1 → swap 3 and 1 → [1, 3, 2]
Position 1: [1, 3, 2] → smallest remaining is 2 → swap 3 and 2 → [1, 2, 3]
Finished:    sorted part grows from the left; the rest still needs checking.
```

```python
def selection_sort(values: list[int]) -> None:
    # Mutates the input list; returns None, like list.sort().
    for position in range(len(values) - 1):
        smallest = position
        for candidate in range(position + 1, len(values)):
            if values[candidate] < values[smallest]:
                smallest = candidate
        values[position], values[smallest] = values[smallest], values[position]


cards = [3, 1, 2]
assert selection_sort(cards) is None
assert cards == [1, 2, 3]
assert selection_sort([]) is None
```

**Time:** O(n²), even for sorted input: still search each remaining part. **Auxiliary space:** O(1). A useful teaching algorithm for small inputs; Python's built-in sort is generally the practical choice.

#### Merge sort: understand divide and conquer

Split into halves, sort each half, then merge the sorted results.

**Recursion in three questions:** what is the smaller version of the problem? Sorting a half. When can we stop? A list of zero or one item is already sorted: the **base case**. What happens when the smaller calls return? Merge their sorted answers. Each unfinished call waits on the call stack; recursion does not make its work or memory disappear.

**Walk through every split:** keep dividing until each piece contains one item. A one-item list is already sorted.

```text
                  [4, 1, 3, 2]
                  /          \
              [4, 1]        [3, 2]
              /    \        /    \
            [4]    [1]    [3]    [2]
```

**Now merge upward in sorted order:**

1. Merge `[4]` and `[1]`: compare 4 with 1, take 1, then the remaining 4 → `[1, 4]`.
2. Merge `[3]` and `[2]`: compare 3 with 2, take 2, then the remaining 3 → `[2, 3]`.
3. Merge `[1, 4]` and `[2, 3]`: take 1, then 2, then 3, then the remaining 4 → `[1, 2, 3, 4]`.

```text
            [4]    [1]    [3]    [2]
               \  /         \  /
              [1, 4]        [2, 3]
                  \          /
                  [1, 2, 3, 4]
```

**Merging is not plain concatenation:** `[4] + [1]` gives `[4, 1]`, which is still unsorted. A sorted merge compares the next available items and takes the smaller one first.

The diagram shows the levels of the problem. The recursive Python code actually finishes splitting and sorting the left half before processing the right half; it does not split all branches simultaneously.

Here is the final merge of `[1, 4]` and `[2, 3]`:

| Next unused left | Next unused right | Take | Result so far |
| --- | --- | --- | --- |
| 1 | 2 | 1 | `[1]` |
| 4 | 2 | 2 | `[1, 2]` |
| 4 | 3 | 3 | `[1, 2, 3]` |
| 4 | No items left | Remaining 4 | `[1, 2, 3, 4]` |

`i` and `j` point to those next unused items. After taking an item, advance only its pointer. `extend()` copies in the leftovers when the other side runs out.

```python
def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values.copy()
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
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


assert merge_sort([4, 1, 3, 1]) == [1, 1, 3, 4]
assert merge_sort([]) == []
```

**Why O(n log n)?** With four cards, merging the single-card lists writes four items across two small merges. The final merge writes four items again: two levels of work on four items. With eight cards there are three merge levels. Halving determines the O(log n) number of levels; processing all n items at each level gives O(n log n) time.

**Auxiliary space:** O(n) peak for slices/intermediate lists, including an O(log n) call stack within that overall bound. **Output:** O(n). Peak memory counts what exists at the same time; it does not add every allocation from every completed call.


| Algorithm               | Time                              | Space depends on implementation                                               |
| --- | --- | --- |
| Selection sort above    | O(n²) in all cases               | O(1) auxiliary; mutates input                                                 |
| Merge sort above        | O(n log n)                        | O(n) auxiliary and O(n) output                                                |
| In-place quicksort      | Average O(n log n), worst O(n²)  | Typical recursive version: O(log n) average stack, O(n) worst                 |
| List-building quicksort | Balanced O(n log n), worst O(n²) | O(n) peak auxiliary when balanced, O(n²) worst with retained partition lists |

**Common mistake:** Do not quote an algorithm name's textbook space bound without examining the actual Python code. Comprehensions, slices, concatenation, and recursion all allocate memory.

### 6. Binary search and boundaries

**Problem:** find a target in a list sorted from small to large.

**Idea:** inspect the middle. If it is too small, everything to its left is also too small; discard that entire half. If it is too large, discard the right half. This is why sorted input matters: on an unsorted list such as `[10, 1, 5]`, this rule can miss 10.

The broader term **monotonic condition** means a condition changes in one direction, such as “too small” becoming “large enough” and never switching back. First learn the sorted-list version below.

**Walk through it:** find 7 in `[1, 3, 5, 7, 9]`.


| Remaining indices | Middle value | Decision                              |
| --- | --- | --- |
| 0 through 4       | 5 at index 2 | 7 is larger: keep indices 3 through 4 |
| 3 through 4       | 7 at index 3 | Found: return 3                       |

`left` and `right` mark the part still being searched. Because the input is sorted, everything discarded on the left is too small; it cannot contain the answer. The loop must make progress: use `middle + 1` or `middle - 1` after checking the middle, or the same position may be checked forever.

```python
def binary_search(values: list[int], target: int) -> int:
    left, right = 0, len(values) - 1
    while left <= right:
        middle = (left + right) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


assert binary_search([1, 3, 5, 7], 5) == 2
assert binary_search([1, 3, 5, 7], 4) == -1
assert binary_search([], 4) == -1
```

**Time:** O(log n) worst. For 16 candidates, the range can shrink `16 → 8 → 4 → 2 → 1`: only four halvings, then at most one final candidate check. That is the meaning of logarithmic growth, not an exact promise of four comparisons.

**Auxiliary space:** O(1): a few indices, with no copied halves. With duplicates, this version may return any matching position.

For the first matching position or an insertion boundary, prefer the standard library:

```python
from bisect import bisect_left, bisect_right

values = [1, 2, 2, 4]
assert bisect_left(values, 2) == 1   # First position where 2 could go.
assert bisect_right(values, 2) == 3  # Position after all existing 2s.
assert bisect_left(values, 3) == 3   # Insertion position, even when absent.
```

The search is O(log n), but actually inserting into a Python list still costs O(n). Sorting once costs O(n log n); include that cost if the input was not already sorted. For repeated exact lookups without needing order, a set/dict may be a better choice.

Recursive binary search with index bounds takes O(log n) time and **O(log n) stack space**. A million items require only about 20 halvings. The recursion risk is different from a linear-depth traversal; slicing the list at each recursive step also changes the costs.

### 7. Two pointers on sorted input

**When to use it:** a sorted sequence and a pair condition. Move the endpoint that can improve the answer.

**Walk through it:** target 9, input `[1, 2, 4, 7]`. Start at 1 and 7: sum 8 is too small. Move the left index to 2: `2 + 7 = 9`, so return indices `(1, 3)`. Moving the right index left would only make the first sum smaller.

```python
def sorted_pair(values: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left] + values[right]
        if total == target:
            return left, right
        if total < target:
            left += 1   # Need a larger sum.
        else:
            right -= 1  # Need a smaller sum.
    return None


assert sorted_pair([1, 2, 4, 7], 9) == (1, 3)
assert sorted_pair([], 9) is None
```

**Why is moving a pointer safe?** If `1 + 7` is too small, pairing 1 with any smaller right-hand item is also too small. We can discard 1. If a sum is too large, pairing that right-hand item with any larger left-hand item is also too large, so discard the right-hand item.

**Time:** O(n). **Auxiliary space:** O(1). The pointers only move inward. Input must already be sorted; sorting first costs O(n log n) and changes index positions. Preserve original indices separately if the task asks for them.

#### Pause and predict: One card cannot be two cards

Two sum receives `[5]`, target 10. What should happen? Now try `[5, 5]`. Which line order prevents reusing a card?

<details>
<summary>Open after predicting</summary>

The first input has no pair; the second returns `(0, 1)`. Check for the complement before adding the current value to `seen`.

</details>

## Part 3. Work with consecutive items and ranges

A **subarray** (or a substring of text) is consecutive: it cannot skip positions. In `[2, 1, 5]`, `[2, 1]` is a subarray; picking `[2, 5]` skips an item and forms a subsequence instead. A size-3 window contains exactly three consecutive items.

Reuse overlapping work: slide a window, subtract prefix totals, or keep the best running answer.

### 8. Fixed-size sliding window

**When to use it:** best sum/average over `k` consecutive items. Reuse the previous window instead of recomputing its sum.

**Walk through it:** input `[2, 1, 5, 1]`, window size 3.


| Window      | Calculation                          | Sum |
| --- | --- | --- |
| `[2, 1, 5]` | Add the first three items            | 8   |
| `[1, 5, 1]` | Previous 8 − leaving 2 + entering 1 | 7   |

`current` remembers the latest window sum; `best` remembers the largest seen. The answer is 8. We reuse the overlapping part instead of adding all three items again.

```python
def max_window_sum(values: list[int], k: int) -> int:
    if not 1 <= k <= len(values):
        raise ValueError("k must be between 1 and the input length")
    current = 0
    for i in range(k):
        current += values[i]
    best = current
    for right in range(k, len(values)):
        current += values[right] - values[right - k]
        best = max(best, current)
    return best


assert max_window_sum([2, 1, 5, 1], 3) == 8  # The walkthrough example.
assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9
assert max_window_sum([-5, -2, -3], 2) == -5
```

Windows are `[2,1,5] → [1,5,1] → [5,1,3] → [1,3,2]`. Add the entering item and subtract the leaving item.

**Time:** O(n), not O(n × k). **Auxiliary space:** O(1). Avoid an initial `values[:k]` slice if claiming constant auxiliary space. Initialize `best` from a real window, not zero, because inputs can be negative.

### 9. Variable-size sliding window

**When to use it:** longest contiguous region satisfying a condition. Grow the right boundary; move the left boundary until the window is valid again.

**Walk through it:** `"abba"`. Grow from `"a"` to `"ab"` (best length 2). The next `b` repeats, so remove the leftmost `a`, then the old `b`, before adding the new `b`. The window becomes `"b"`, then `"ba"`.

Watch the second `b` in `"abba"` arrive at index 2:

| Step | Window before adding the new b | What changes? |
| --- | --- | --- |
| A duplicate arrives | `"ab"` | Old b is still inside |
| Move left once | `"b"` | Removing a did not remove the duplicate |
| Move left again | `""` | Old b is now gone |
| Add the new b | `"b"` | The window has no duplicates again |

`left` marks the current window's start. After adding the new character, `right` marks its end and `present` contains exactly its characters. The **while**, rather than a single **if**, removes as many old characters as needed.

```python
def longest_unique_substring(text: str) -> int:
    present = set()
    left = best = 0
    for right, character in enumerate(text):
        while character in present:
            present.remove(text[left])
            left += 1
        present.add(character)
        best = max(best, right - left + 1)
    return best


assert longest_unique_substring("abcabcbb") == 3
assert longest_unique_substring("abba") == 2
assert longest_unique_substring("") == 0
```

**Time:** O(n) average: each character enters and leaves the window at most once. The nested `while` does not restart a scan. **Auxiliary space:** O(min(n, alphabet size)).

Not every condition supports a sliding window. For “longest subarray with sum at most 3,” `[4, -3, 2]` is a valid full-length answer: its sum is 3. A rule that immediately discards 4 when the sum first exceeds 3 loses that answer. Negative values mean a later item can reduce the sum, so that shrinking rule is unsafe.

**Teaching check:** “Why can a sliding window have a `while` inside a `for` and still take O(n) time?” Each boundary only moves forward. Across the whole run, each item enters once and leaves at most once.

### 10. Prefix sums: repeated range queries

**When to use it:** many sums over a fixed input. Let `prefix[i]` be the sum of items before index `i`.

**Walk through it:** `[2, 4, 1, 3]` produces prefix totals `[0, 2, 6, 7, 10]`. To sum indices 1 and 2, take the total before index 3 (7) minus the total before index 1 (2): `7 - 2 = 5`. The initial zero handles ranges starting at index 0.

`[left, right)` means include `left` but stop **before** `right`, like a Python slice.

```python
def build_prefix(values: list[int]) -> list[int]:
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    # Half-open interval [left, right); caller supplies valid bounds.
    return prefix[right] - prefix[left]


prefix = build_prefix([2, 4, 1, 3])  # [0, 2, 6, 7, 10]
assert range_sum(prefix, 1, 3) == 5  # 4 + 1
assert range_sum(prefix, 2, 2) == 0  # Empty range.
```

**Build:** O(n) time, O(n) returned prefix table, O(1) auxiliary space excluding that output. **Each query:** O(1) time/space. When used inside a larger algorithm, the retained table is O(n) working memory. Changing an input item invalidates later prefix entries.

#### Prefix sum + hash map: count subarrays with a target sum

**Start with subtraction:** suppose the total up to here is 7 and we want a subarray totaling 5. We need an earlier prefix totaling 2, because `7 - 2 = 5`. Everything before that earlier prefix cancels out.

In the code, `total` is the current prefix sum. `total - target` is the earlier total we need. `frequencies` remembers how many earlier prefixes have that total; each one identifies a different starting position.

**Walk through it:** `[1, 1, 1]`, target 2. Start with `{0: 1}`: one empty prefix before the first item.

| New item | Running total | Needed earlier total (`total - 2`) | Earlier matches | Answer so far |
| --- | --- | --- | --- | --- |
| First 1 | 1 | -1 | 0 | 0 |
| Second 1 | 2 | 0 | 1: the empty prefix | 1 |
| Third 1 | 3 | 1 | 1: after the first item | 2 |

After each row, record the current total for later items. We count **nonempty** subarrays, so the current prefix must not be treated as an earlier prefix before counting.

```python
def count_target_subarrays(values: list[int], target: int) -> int:
    frequencies = {0: 1}  # Empty prefix allows matches starting at index 0.
    total = matches = 0
    for value in values:
        total += value
        matches += frequencies.get(total - target, 0)
        frequencies[total] = frequencies.get(total, 0) + 1
    return matches


assert count_target_subarrays([1, 1, 1], 2) == 2
assert count_target_subarrays([1, -1, 0], 0) == 3
assert count_target_subarrays([0, 0], 0) == 3  # Two single zeros and the pair.
```

**Why counts rather than a set?** For `[0, 0]`, target 0, the second zero can start a match after either of two earlier zero-total prefixes. A set would lose that multiplicity. There are three matches in total: each single zero and the pair.

**Time:** O(n) average. **Auxiliary space:** O(n). This works with negatives and zero; it does not require the predictable sum changes needed by some sliding-window rules.

### 11. Kadane's algorithm: maximum contiguous sum

**When to use it:** maximum sum over any nonempty contiguous subarray. At each position, either extend the current run or restart there.

**Walk through it:** `[4, -1, 2, -8, 3]`.


| New item | Best sum ending here    | Best sum anywhere so far |
| --- | --- | --- |
| 4        | 4                       | 4                        |
| -1       | 3: extend the run       | 4                        |
| 2        | 5: extend the run       | 5                        |
| -8       | -3: extend the run      | 5                        |
| 3        | 3: restart at this item | 5                        |

`ending_here` must end at the current item; `best` may refer to an earlier run. Answer: 5 from `[4, -1, 2]`.

**Why only two choices?** A subarray ending here either starts here or extends a subarray ending immediately before it. Keep the better of those two. For example, after a running sum of -3, the next item 3 is better alone (3) than attached to that run (0).

```python
def max_subarray_sum(values: list[int]) -> int:
    if not values:
        raise ValueError("A nonempty list is required")
    ending_here = best = values[0]
    for index in range(1, len(values)):
        value = values[index]
        ending_here = max(value, ending_here + value)
        best = max(best, ending_here)
    return best


assert max_subarray_sum([4, -1, 2, -8, 3]) == 5  # The walkthrough example.
assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray_sum([-5, -2, -8]) == -2
```

**Time:** O(n). **Auxiliary space:** O(1). This returns the best sum, not its indices. Initializing to zero would incorrectly allow an empty subarray when all values are negative.

### 12. Merge intervals

**When to use it:** overlapping reservations/ranges. Sort by start, then compare each interval with the last merged one.

**Walk through it:** `[(1, 3), (2, 6), (8, 10)]`. The first two overlap because 2 starts before 3 ends; replace them with `(1, 6)`. The last interval starts after 6, so keep it separate. Answer: `[(1, 6), (8, 10)]`.

```python
def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            previous_start, previous_end = merged[-1]
            merged[-1] = (previous_start, max(previous_end, end))
    return merged


assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]
assert merge_intervals([(1, 2), (2, 3)]) == [(1, 3)]
assert merge_intervals([]) == []
```

Assume valid **closed** intervals with `start <= end`; touching endpoints merge. A closed interval `[1, 2]` includes 2; a half-open interval `[1, 2)` stops before 2. That is why `(1, 2)` and `(2, 3)` merge here, but two meetings can touch at time 2 in the later scheduling example. Choose the boundary rule from the problem statement.

**Time:** O(n log n), dominated by sorting. **Auxiliary space:** O(n) for the sorted copy/workspace. **Output:** O(n). If already sorted, the merging scan alone is O(n).

#### Pause and predict: Slide the frame

Use four cards `[2, 1, 5, 1]` and cover all but three. Slide the frame one card right. Predict the new sum without re-adding the whole window.

<details>
<summary>Open after predicting</summary>

The first sum is 8. Remove the leaving 2 and add the entering 1: `8 - 2 + 1 = 7`. The overlap does not need to be recomputed.

</details>

## Part 4. Manage pending work and links

Learn stack and queue operations first, then use them to remember unfinished work. Linked-list examples introduce the node references used by trees.

### 13. Stack and queue operations in Python

**Act it out:** stack three books and remove the top one: newest first. Now line up three students and serve the person at the front: oldest first. LIFO means *last in, first out*; FIFO means *first in, first out*. Ask the class to predict which name the code removes.


| Behavior                  | Add                           | Remove                | Typical use                      |
| --- | --- | --- | --- |
| Stack: LIFO, newest first | `list.append(x)`              | `list.pop()`          | DFS, matching brackets, undo     |
| Queue: FIFO, oldest first | `deque.append(x)`             | `deque.popleft()`     | BFS, processing in arrival order |
| Deque at either end       | `appendleft(x)` / `append(x)` | `popleft()` / `pop()` | Work at both ends                |

There is no `popright()` method: `deque.pop()` removes from the right. Deque operations at either end are O(1); list append is amortized O(1). List `pop(0)` is O(n) because it shifts items.

```python
from collections import deque

stack = ["A", "B", "C"]
assert stack.pop() == "C"
queue = deque(["A", "B", "C"])
assert queue.popleft() == "A"
assert queue.pop() == "C"
```

Popping an empty list/deque raises `IndexError`. Check emptiness when it is a valid case in the task.

### 14. Stack: balanced brackets

**When to use it:** nested opening/closing symbols. The next closing symbol must match the most recently opened one.

**Walk through it:** `"([])"`. Push `(`, push `[`, then `]` matches the most recent `[`, so pop it. Finally `)` matches `(`. Nothing remains: valid. For `"([)]"`, the first `)` meets `[` on top, so the nesting is wrong.

```python
def balanced_brackets(text: str) -> bool:
    closing_to_opening = {")": "(", "]": "[", "}": "{"}
    openings = set(closing_to_opening.values())
    stack = []
    for character in text:
        if character in openings:
            stack.append(character)
        elif character in closing_to_opening:
            if not stack or stack.pop() != closing_to_opening[character]:
                return False
    return not stack


assert balanced_brackets("{[()]}")
assert not balanced_brackets("([)]")
assert not balanced_brackets("(")
assert balanced_brackets("text")  # This version ignores non-bracket characters.
```

**Time:** O(n). **Auxiliary space:** O(n), for a sequence of unmatched openings. The map/set of three bracket types is constant-sized. State whether ordinary text is ignored or rejected.

### 15. Monotonic stack: next greater element

**When to use it:** next greater/smaller item, stock spans, daily temperatures. Keep indices whose answers are still unknown.

“Monotonic” means the saved values stay in one direction: here, non-increasing from bottom to top.

**Walk through it:** `[2, 1, 3]`. Save indices 0 and 1 because their next greater values are unknown. On seeing 3, it answers both: 3 is greater than 1 and 2, so pop both saved indices and fill their answers. The answer is `[3, 3, None]`.

The stack holds **indices**, so we know which result positions to update. The result holds **values**.

```python
def next_greater(values: list[int]) -> list[int | None]:
    result = [None] * len(values)
    stack = []  # Indices with non-increasing values.
    for index, value in enumerate(values):
        while stack and value > values[stack[-1]]:
            previous = stack.pop()
            result[previous] = value
        stack.append(index)
    return result


assert next_greater([2, 1, 3, 2, 4]) == [3, 3, 4, 4, None]
assert next_greater([2, 2]) == [None, None]  # Strictly greater, not equal.
assert next_greater([]) == []
```

**Time:** O(n): each index is pushed once and popped at most once. **Auxiliary space:** O(n) for the stack. **Output:** O(n). The nested `while` does not imply O(n²), because popped indices never return to the stack.

### 16. Linked lists: reverse links and detect cycles

A singly linked node stores a value and a reference to its successor. There is no O(1) positional indexing: reaching the kth node requires following links.

**Reversal walkthrough:** move one arrow at a time for `1 → 2 → 3 → None`.

| Turn | Save next node | Reverse this link | Reversed part | Still to process |
| --- | --- | --- | --- | --- |
| 1 | Node 2 | `1.next = None` | `1 → None` | `2 → 3 → None` |
| 2 | Node 3 | `2.next = 1` | `2 → 1 → None` | `3 → None` |
| 3 | None | `3.next = 2` | `3 → 2 → 1 → None` | Nothing |

We change links, not the stored numbers. Save the next node first; otherwise overwriting the link can lose your route to the unprocessed part.

- `previous`: the head of the already reversed part.
- `current`: the node whose link we are changing.
- `following`: the saved node to process next.

**Cycle walkthrough:** in `1 → 2 → 3 → 2 → ...`, there is no end. Both pointers start at node 1. After one turn, slow is at 2 and fast at 3. After the second turn, both are at 3. Meeting at the same node proves a cycle.

More generally, once both are inside the loop, the faster pointer gains one position per turn and eventually catches the slower one. If fast reaches `None`, there is an end instead of a cycle.

```python
class Node:
    def __init__(self, value: int, next_node=None):
        self.value = value
        self.next = next_node


def reverse_list(head: Node | None) -> Node | None:
    previous = None
    current = head
    while current is not None:
        following = current.next  # Save before overwriting the link.
        current.next = previous
        previous = current
        current = following
    return previous


def has_cycle(head: Node | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


head = Node(1, Node(2, Node(3)))
reversed_head = reverse_list(head)
assert reversed_head.value == 3
assert reversed_head.next.value == 2
assert reversed_head.next.next.value == 1
assert reversed_head.next.next.next is None
assert reverse_list(None) is None
assert not has_cycle(reversed_head)
loop = Node(9)
loop.next = loop
assert has_cycle(loop)
```

**Reversal:** O(n) time, O(1) auxiliary space; it **mutates** links and assumes an acyclic list. `1 → 2 → 3 → None` becomes `3 → 2 → 1 → None`.

**Floyd's cycle detection:** O(n) time, O(1) auxiliary space. The fast pointer moves twice as quickly; inside a cycle it eventually meets the slow pointer. Compare node identity with `is`, not whether their stored values are equal. Repeated values alone do not imply a cycle.

**Interview habit:** Explain the invariant before coding: what is on the stack, what remains in the queue, or which links have already been reversed?

**Teaching check:** “Does storing the same value twice mean a linked list has a cycle?” No. A cycle is a link that leads back to the same node object; compare identity with `is`.

#### Pause and predict: Bracket referee

Without running Python, judge `"([])"`, `"([)]"`, and `"(()"`. Point to the exact moment a wrong bracket is detected.

<details>
<summary>Open after predicting</summary>

Only `"([])"` is valid. In `"([)]"`, `)` finds `[` on top. In `"(()"`, an opening `(` remains after the last character.

</details>

## Part 5. Explore trees and graph connections

A **node (vertex)** is an item; an **edge** is a connection. A node's **neighbors** are items directly connected to it. A tree connects all its nodes without cycles; exactly one simple path joins each pair when viewing its edges as connections. A general graph may need a visited set.

An **adjacency list** such as `{"A": ["B", "C"]}` records outgoing neighbors. For undirected graphs, store each edge in both directions. `V` is the number of vertices, `E` the edges, `h` a tree's height, and `w` its maximum width. The existing adjacency-list input occupies O(V + E); algorithm workspace is counted separately. The graph time bounds below assume average O(1) dictionary/set operations.

### 17. Binary tree inorder traversal

A **binary tree** gives each node at most two children, left and right. The **root** is the starting node; a **leaf** has no children. A **binary search tree (BST)** additionally orders keys: smaller keys on the left, larger keys on the right (with a stated policy for duplicates). Binary trees are not automatically BSTs.

**When to use it:** visit left subtree, node, then right subtree. For a valid BST, inorder yields sorted keys; arbitrary binary trees do not have this guarantee.

**Walk through it:** for root 2 with left child 1 and right child 3:

| Action | Stack (top on right) | Output |
| --- | --- | --- |
| Save 2 and go left | `[2]` | `[]` |
| Save 1 and go left to None | `[2, 1]` | `[]` |
| Pop and visit 1 | `[2]` | `[1]` |
| 1 has no right child; pop and visit 2 | `[]` | `[1, 2]` |
| Go right, save 3, then pop and visit it | `[]` after the pop | `[1, 2, 3]` |

“Visit” means append the node's value to the result. The stack remembers where to return after finishing a left subtree.

```python
class TreeNode:
    def __init__(self, value: int, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def inorder(root: TreeNode | None) -> list[int]:
    stack = []
    result = []
    current = root
    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.value)
        current = current.right
    return result


root = TreeNode(2, TreeNode(1), TreeNode(3))
assert inorder(root) == [1, 2, 3]
assert inorder(None) == []
```

**Time:** O(n). **Auxiliary space:** O(h), worst O(n) for a skewed tree; O(log n) for a balanced one. **Output:** O(n). Preorder visits node-left-right; postorder visits left-right-node. Tree BFS uses a queue with O(w) auxiliary space. An unbalanced BST does not guarantee logarithmic search.

### 18. Why a stack gives DFS and a queue gives BFS

```text
        A
       / \
      B   C
     / \   \
    D   E   F
```

Explore left to right:


| After visiting | DFS stack (top on right)         | BFS queue (front on left)        |
| --- | --- | --- |
| A              | `[C, B]` (push C before B)       | `[B, C]`                         |
| B              | `[C, E, D]`                      | `[C, D, E]`                      |
| Next node      | D: a newly discovered descendant | C: an earlier-discovered sibling |
| Full order     | A, B, D, E, C, F                 | A, B, C, D, E, F                 |

**Stack / DFS:** newest work first, so descend before returning to siblings. Recursive DFS uses the call stack implicitly. **Queue / BFS:** oldest work first, so finish a level before processing the next one. Neighbor order affects traversal order; using a set for neighbors does not promise a specific order.

### 19. BFS: shortest path in an unweighted graph

**When to use it:** minimum number of edges, fewest moves, level-order exploration. Record parents when a node is first enqueued, then reconstruct one shortest path.

**Walk through it:** to reach F from A in the diagram, discover B and C first, then D, E, and F. Record `parent["C"] = "A"` and `parent["F"] = "C"`. Follow those links backward from F: F → C → A. Reverse that list to get A → C → F.

`queue` holds nodes waiting for their turn. `parent` remembers how we first reached each node and also tells us whether we have already discovered it. “Unweighted” means each edge has the same cost, such as one move.

On the diagram above, processing the queue goes like this:

| Remove from front | Queue afterward, including newly discovered neighbors |
| --- | --- |
| A | `[B, C]` |
| B | `[C, D, E]` |
| C | `[D, E, F]` |
| D | `[E, F]` |
| E | `[F]` |
| F | Goal found; follow parents back to A |

We mark a node discovered when we add it to the queue. If another edge reaches it before its turn, it is not added a second time.

```python
from collections import deque


def bfs_path(graph: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    queue = deque([start])
    parent = {start: None}  # Also serves as the visited map.
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path
        for neighbor in graph.get(node, []):
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    return None


graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]}
assert bfs_path(graph, "A", "F") == ["A", "C", "F"]
assert bfs_path(graph, "A", "A") == ["A"]
assert bfs_path(graph, "F", "A") is None  # Edges here are directed.
```

Assume `start` is a valid vertex; vertices with no outgoing edges may be absent as keys.

**Time:** O(V + E) worst over the reachable component, including reconstruction. **Auxiliary space:** O(V) for parents/queue. **Output:** up to O(V) path vertices. Mark visited **when enqueuing**, not later, to avoid queueing the same vertex repeatedly. For differing edge weights, BFS does not generally find the cheapest path.

**Grid version:** treat each open cell as a vertex and its valid neighboring cells as edges. With four directions and an R × C grid, BFS/DFS take O(R × C) time and up to O(R × C) auxiliary space. Choose explicitly whether to mutate the grid or retain a visited set.

**Teaching check:** “Why does BFS find the fewest edges?” A FIFO queue processes all nodes at distance 1 before distance 2, and so on. A stack does not preserve that level order, so DFS does not generally find a shortest path.

### 20. DFS: reachability and components

**When to use it:** explore branches, flood fill, connected components, cycle reasoning. Start with the recursive version: visit the current node, then fully explore each not-yet-visited neighbor before continuing.

**Walk through it:** visit A, call `visit(B)`, then call `visit(D)`. D has no neighbors, so return to B. Visit E, return to B, then return to A. Now visit C and F. Returning from a call is how DFS goes back up the branch.

```python
def dfs_recursive(graph: dict[str, list[str]], start: str) -> list[str]:
    seen = set()
    order = []

    def visit(node: str) -> None:
        seen.add(node)
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in seen:
                visit(neighbor)

    visit(start)
    return order


graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]}
assert dfs_recursive(graph, "A") == ["A", "B", "D", "E", "C", "F"]
assert dfs_recursive({"A": ["B"], "B": ["A"]}, "A") == ["A", "B"]
```

**Time:** O(V + E): visit each reachable node and inspect its edges. **Auxiliary space:** O(V) for `seen` and the call stack in the worst case. **Output:** O(V). Marking a node in `seen` before exploring its neighbors prevents an endless loop: on A → B → A, the second encounter with A is skipped. Very deep graphs can exceed Python's recursion limit; use an iterative version when depth may be large.

<details>
<summary>Optional follow-up: iterative DFS without recursion</summary>

Each stack entry below remembers which neighbor to try next. `iter()` creates that reminder; `next()` advances it. `StopIteration` means the current node has no more neighbors, so we pop its frame and return to the previous node.

```python
def dfs_order(graph: dict[str, list[str]], start: str) -> list[str]:
    seen = {start}
    order = [start]
    stack = [iter(graph.get(start, []))]
    while stack:
        try:
            neighbor = next(stack[-1])
        except StopIteration:
            stack.pop()  # This branch is finished: backtrack.
            continue
        if neighbor not in seen:
            seen.add(neighbor)
            order.append(neighbor)
            stack.append(iter(graph.get(neighbor, [])))
    return order


graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]}
assert dfs_order(graph, "A") == ["A", "B", "D", "E", "C", "F"]
assert dfs_order({"A": ["B"], "B": ["A"]}, "A") == ["A", "B"]
```

**Time:** O(V + E). **Auxiliary space:** O(V) for the visited set and active DFS frames. **Output:** O(V). This version avoids both Python recursion limits and duplicate pending entries. A simpler stack that pushes all neighbors before checking whether they were visited may retain duplicate entries; account for those when analyzing its memory.

</details>

One traversal only covers nodes reachable from `start`. For all connected components, use an outer loop that starts traversal at each still-unvisited vertex and shares one visited set. The shown functions create their own set for one traversal; adapt that ownership when enumerating components. In an **undirected** graph this finds connected components; directed strong connectivity needs a different algorithm.

**Cycle warning:** merely reaching a visited node does not prove a directed cycle. Directed DFS cycle detection must distinguish nodes currently on the active path from nodes already finished. For an undirected graph, also distinguish the parent edge.

### 21. Topological sort: dependencies

**Problem:** order tasks so each prerequisite finishes before the task that needs it. An edge A → B means “finish A before B.”

**Idea:** keep a ready queue. A task with zero unfinished prerequisites can go next. Completing it removes one prerequisite from each dependent task. This is Kahn's topological-sort algorithm.

**Walk through it:** `plan → build → test`. Plan has zero prerequisites, build has one, and test has one. Process plan; build now has zero prerequisites and becomes ready. Process build; test becomes ready. Output: plan, build, test.

`indegree[node]` counts unfinished prerequisites. The queue contains tasks ready now. A **DAG** is a directed graph with no directed cycle: no dependency chain leads back to itself.

If A needs B and B needs A, neither can become ready. The queue empties before all tasks finish; the final length check detects this cycle. Independent tasks can have several valid orders.

```python
from collections import deque


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    indegree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            indegree[neighbor] = indegree.get(neighbor, 0) + 1
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != len(indegree):
        raise ValueError("Graph contains a directed cycle")
    return order


assert topological_sort({"plan": ["build"], "build": ["test"]}) == ["plan", "build", "test"]
assert topological_sort({}) == []
```

**Time:** O(V + E). **Auxiliary space:** O(V). **Output:** O(V). Works only for a **directed acyclic graph (DAG)**. Multiple valid orders can exist; verify that every dependency comes before its successor rather than expecting one universal order. A cycle causes the explicit error above.

#### Pause and predict: Room explorer

Use the A–F diagram. After A and B have been processed, which node comes next for BFS? Which for left-to-right DFS? Add D → A: why must you remember visited nodes?

<details>
<summary>Open after predicting</summary>

BFS processes C; DFS processes D. Without a visited set, the new edge can send traversal around A → B → D → A repeatedly.

</details>

## Part 6. Prioritize the next choice

Learn the heap before Dijkstra so the priority-queue operations are familiar. Then contrast priority-based processing with a greedy choice that needs a correctness argument.

### 22. Heap: retain the largest k items

**When to use it:** top-k results or a stream where keeping/sorting all values is unnecessary. Maintain a **min-heap of size k**: its smallest item is the threshold a new item must beat.

A **min-heap** keeps its smallest item easy to remove; its other items need not be fully sorted. It follows parent–child ordering inside a tree-shaped structure. `heapq` stores that structure in a regular Python list and restores the ordering after a push or pop. Maintaining a path through the heap takes O(log k) work for k items.

**Walk through it:** keep the largest 2 values from `[3, 1, 5, 2]`.


| New value | Retained values (shown sorted for explanation) | Decision                                              |
| --- | --- | --- |
| 3         | `[3]`                                          | Still have room                                       |
| 1         | `[1, 3]`                                       | Still have room                                       |
| 5         | `[3, 5]`                                       | Replace the smallest retained value, 1                |
| 2         | `[3, 5]`                                       | Ignore: it cannot beat the smallest retained value, 3 |

Return `[5, 3]` in descending order. Keeping the smallest of the selected values at the top lets us decide quickly whether a new value belongs.

```python
import heapq


def largest_k(values: list[int], k: int) -> list[int]:
    if not 1 <= k <= len(values):
        raise ValueError("k must be between 1 and the input length")
    heap = []
    for value in values:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)


assert largest_k([3, 1, 5, 12, 2, 11], 3) == [12, 11, 5]
assert largest_k([4, 4, 1], 2) == [4, 4]  # Duplicates are retained.
```

**Time:** O(n log(k + 1) + k log k), including sorting the returned k items. **Auxiliary space:** O(k). **Output:** O(k). The `+ 1` keeps the bound meaningful when k = 1. A heap is not a fully sorted list; only its smallest item is guaranteed at index 0.

For concise application code, `heapq.nlargest(k, values)` provides this operation. For the single largest item use `max(values)`; for nearly all items, sorting the whole input can be simpler.

### 23. Dijkstra: shortest paths with nonnegative weights

**When to use it:** cheapest route with unequal, nonnegative edge costs. A min-heap always processes the currently cheapest pending distance.

Learn the [min-heap example](#22-heap-retain-the-largest-k-items) first. “Nonnegative” means zero or greater.

**Walk through it:** A → B costs 4, A → C costs 1, and C → B costs 2.


| Process next | New information                                |
| --- | --- |
| A at cost 0  | B can cost 4; C can cost 1                     |
| C at cost 1  | B can cost `1 + 2 = 3`, improving the earlier 4 |
| B at cost 3  | Cheapest route to B is A → C → B             |

`distances` stores the best cost found for each node. `heap` chooses the smallest pending cost. The old entry for B at cost 4 is now out of date (“stale”) and is skipped when it comes out of the heap.

```python
import heapq


def dijkstra(graph: dict[str, list[tuple[str, int]]], start: str) -> dict[str, int]:
    # All edge weights must be nonnegative; labels here are comparable strings.
    distances = {start: 0}
    heap = [(0, start)]
    while heap:
        distance, node = heapq.heappop(heap)
        if distance != distances[node]:
            continue  # An improved distance made this queued entry stale.
        for neighbor, weight in graph.get(node, []):
            if weight < 0:
                raise ValueError("Dijkstra requires nonnegative weights")
            candidate = distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distances


graph = {"A": [("B", 4), ("C", 1)], "C": [("B", 2)], "B": []}
assert dijkstra(graph, "A") == {"A": 0, "C": 1, "B": 3}
```

The route A → C → B costs 3, beating the direct cost 4. BFS would minimize the number of edges and favor the one-edge route; Dijkstra minimizes the **sum of edge costs**. Unreachable vertices are absent from the result.

**Why choose the cheapest pending route?** With nonnegative weights, continuing a route can only keep or increase its cost. Once the cheapest non-stale entry is removed, an as-yet-unexplored route cannot later undercut it. Negative weights would break that reasoning.

**Cost to remember:** on a simple graph, O((V + E) log(V + 1)) time and O(V + E) auxiliary space; the returned distances use up to O(V). We inspect edges and use a heap to keep the cheapest pending route accessible. Old, out-of-date entries can remain in that heap, so it need not contain just one entry per vertex.

<details>
<summary>Precision note: the lazy heap and parallel edges</summary>

Here “simple” excludes parallel copies of an edge. This implementation can push O(E) entries, giving the more general bound O(V + E log(E + 1)). A stale entry is discarded when popped rather than removed at the moment a better distance is found. The worst-case space bound includes these retained entries.

</details>

Negative weights require a suitable different algorithm, such as Bellman–Ford. For non-comparable node objects, heap entries need a unique numeric tie-breaker so equal distances do not trigger object comparisons.

### 24. Greedy: maximum non-overlapping meetings

**When to use it:** select the largest number of non-overlapping intervals. Choose the meeting that **ends earliest**, leaving the most room for the rest.

**Walk through it:** meetings are `(1, 4), (2, 3), (3, 5), (5, 7)`. Sort by finishing time. Choose `(2, 3)`, then `(3, 5)`, then `(5, 7)`: three meetings. Choosing the earliest starting meeting `(1, 4)` would leave room for only one of the later meetings.

`last_end` remembers when the last chosen meeting finishes. Each new meeting must start at or after that time.

```python
def select_meetings(meetings: list[tuple[int, int]]) -> list[tuple[int, int]]:
    selected = []
    last_end = None
    for start, end in sorted(meetings, key=lambda meeting: meeting[1]):
        if last_end is None or start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected


assert select_meetings([(1, 4), (2, 3), (3, 5), (5, 7)]) == [(2, 3), (3, 5), (5, 7)]
assert select_meetings([]) == []
```

Assume valid half-open intervals `[start, end)` with `start < end`, so one meeting may start exactly when another ends. **Time:** O(n log n). **Auxiliary space:** O(n) for sorting. **Output:** O(n).

**Why greedy works here:** replacing the first meeting in an optimal schedule with an earliest-finishing meeting leaves at least as much time for the remaining meetings. Repeat that argument for the rest.

**Common mistake:** a locally attractive choice is not automatically correct. Greedy coin selection fails for coins `[1, 3, 4]` and amount 6: `4 + 1 + 1` uses three coins, while `3 + 3` uses two. Weighted meeting selection also needs a different algorithm.

#### Pause and predict: The tempting first choice

Choose as many meetings as possible from `(1, 10), (2, 3), (3, 4), (4, 5)`. Does choosing the earliest start help? Which sorting key matches the goal?

<details>
<summary>Open after predicting</summary>

Choose the three short meetings by earliest finish. Earliest-start selection takes `(1, 10)` and blocks all three. The goal is maximum count, not maximum time occupied.

</details>

## Part 7. Reuse answers and explore alternatives

Dynamic programming remembers subproblem answers. Backtracking makes a choice, explores it, and undoes it. Union-find is an optional final topic after graph traversal.

### 25. Dynamic programming: climbing stairs

**When to use it:** overlapping subproblems and a recurrence. If each move is one or two steps, ways to reach step `i` equal ways to reach `i - 1` plus ways to reach `i - 2`.

**Walk through it:** how many ways can we climb 5 stairs using moves of 1 or 2?


| Stair | Ways | Why                                       |
| --- | --- | --- |
| 0     | 1    | One way to do nothing                     |
| 1     | 1    | One move of 1                             |
| 2     | 2    | `1 + 1` or `2`                            |
| 3     | 3    | Ways to stair 2 + ways to stair 1: `2 + 1` |
| 4     | 5    | `3 + 2`                                   |
| 5     | 8    | `5 + 3`                                   |

To land on stair 5, the last move must come from stair 4 or stair 3. Those possibilities do not overlap, so add their counts. The table records one answer for each destination stair.

Start with the table version: `ways[step]` is the answer for exactly that stair. Fill it left to right so both smaller answers already exist.

```python
def climb_stairs_table(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n <= 1:
        return 1
    ways = [0] * (n + 1)
    ways[0] = ways[1] = 1
    for step in range(2, n + 1):
        ways[step] = ways[step - 1] + ways[step - 2]
    return ways[n]


assert climb_stairs_table(0) == 1
assert climb_stairs_table(5) == 8
```

**Time:** O(n), one table entry per stair. **Auxiliary space:** O(n), because we retain the whole table; the returned answer is a single count under the fixed-size arithmetic model.

<details>
<summary>After the table makes sense: keep only the previous two answers</summary>

Only the last two entries are needed to calculate the next one. Before each update, `previous` is the answer two stairs back and `current` is the answer one stair back. The version below returns the same answer using O(1) auxiliary space in that arithmetic model.

```python
def climb_stairs(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n <= 1:
        return 1  # One empty sequence reaches step 0.
    previous, current = 1, 1
    for step in range(2, n + 1):
        previous, current = current, previous + current
    return current


assert climb_stairs(0) == 1
assert climb_stairs(5) == 8
```

For the update `previous, current = current, previous + current`, Python calculates both right-hand values before assigning either variable. The old values are not lost halfway through the update.

**Time:** O(n). **Auxiliary space:** O(1) under the fixed-size arithmetic model. Python's very large integer answers eventually require more bits and more expensive arithmetic.

</details>

Naive recursive branching repeats subproblems and takes exponential time. Memoization reduces this to O(n) states but uses O(n) cache and stack space. Bottom-up iteration can avoid recursion and sometimes compress the table, as above.

**DP checklist:** state = what one answer represents; base case = what we already know; recurrence = how smaller answers combine; evaluation order = when those answers become available. Time is usually **number of states × work per state**, not automatically O(n).

For stairs, the state is “ways to reach stair i,” the bases are stairs 0 and 1, and the recurrence adds the previous two answers. For minimum coins below, the state changes to “fewest coins for this amount”; the recurrence must take a minimum instead of adding counts.

### 26. Dynamic programming: minimum coins

**When to use it:** minimum cost to reach an amount with reusable choices. `dp[a]` is the fewest coins needed to make amount `a`.

**Walk through it:** denominations `[1, 3, 4]`, amount 6. Build answers from amount 0 upward:


| Amount       | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fewest coins | 0 | 1 | 2 | 1 | 1 | 2 | 2 |

For amount 6, try each possible last coin:

- Last coin 1: best for amount 5 + one coin = `2 + 1 = 3`.
- Last coin 3: best for amount 3 + one coin = `1 + 1 = 2`.
- Last coin 4: best for amount 2 + one coin = `2 + 1 = 3`.

Choose the smallest count: 2. `dp[subtotal]` stores a **coin count**, not a list of coins. Adding `+ 1` means using the last coin after solving the remaining amount.

The initial `amount + 1` means “not reachable yet.” For amount 6, any real solution uses at most six coins, because each coin is worth at least 1. A stored count of 7 therefore cannot be a valid answer. Set `dp[0] = 0`: making zero needs zero coins.

For coins `[2]` and amount 3, amounts 1 and 3 remain unreachable. The function returns -1, rather than treating the placeholder as a real coin count.

```python
def min_coins(coins: list[int], amount: int) -> int:
    if amount < 0 or not coins or any(coin <= 0 for coin in coins):
        raise ValueError("Use nonnegative amount and nonempty positive denominations")
    dp = [amount + 1] * (amount + 1)  # Sentinel larger than any feasible count.
    dp[0] = 0
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], dp[subtotal - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


assert min_coins([1, 3, 4], 6) == 2
assert min_coins([2], 3) == -1
assert min_coins([2], 0) == 0
```

For positive amount A and c denominations: **O(A × c) time, O(A) auxiliary space**. Validation adds O(c); for amount zero, this implementation still validates the coins. The numeric amount A is not the number of input coins: amount 1,000,000 requires a much larger table than amount 10 even if both use three denominations. The technical term is **pseudo-polynomial**: the cost depends on the numeric amount, which can be large relative to its encoded input length.

This solves the **minimum count with unlimited reuse**, not the number of combinations and not the version where each coin is available once.

### 27. Backtracking: enumerate subsets

**When to use it:** generate all valid selections. Choose an item, recurse, then undo the choice before trying the next option.

**Walk through it:** for `[1, 2]`, save the empty choice `[]`. Choose 1 and save `[1]`; then choose 2 and save `[1, 2]`. Undo 2, then undo 1. Now choose 2 on its own and save `[2]`.

`path` is the current choice. `start` prevents going backward and choosing the same item again. For `[1, 2]`, the calls form this small tree:

```text
visit(0), path []       → save []
  choose 1: path [1]    → save [1]
    choose 2: [1, 2]    → save [1, 2], then undo 2
  undo 1: path []
  choose 2: path [2]    → save [2], then undo 2
```

`append()` makes a choice; `pop()` undoes it. `copy()` saves a snapshot: storing `path` itself would save another reference to the same list, which becomes empty as the recursion undoes its choices.

Say the rhythm aloud: **choose → explore → undo**. Omitting the undo step lets a choice leak into the next branch. Think of trying ingredients in a recipe: remove the trial ingredient before testing a different combination.

```python
def subsets(values: list[int]) -> list[list[int]]:
    result = []
    path = []

    def visit(start: int) -> None:
        result.append(path.copy())
        for index in range(start, len(values)):
            path.append(values[index])
            visit(index + 1)
            path.pop()

    visit(0)
    return result


assert subsets([1, 2]) == [[], [1], [1, 2], [2]]
assert subsets([]) == [[]]
```

Assume distinct input values. **Time:** O(n × 2ⁿ), including copying each subset. **Auxiliary space:** O(n) for path and recursion. **Output:** O(n × 2ⁿ). Store `path.copy()`, not `path`, or every result would reference the same changing list. Duplicate input values require an explicit deduplication strategy.

#### Permutations: order matters

**Walk through it:** `[1, 2]` has two orders: choose 1 then 2, or choose 2 then 1. Unlike subsets, `[1, 2]` and `[2, 1]` are different results. `used[index]` prevents choosing the same input position twice in one order.

```python
def permutations(values: list[int]) -> list[list[int]]:
    result = []
    path = []
    used = [False] * len(values)

    def visit() -> None:
        if len(path) == len(values):
            result.append(path.copy())
            return
        for index, value in enumerate(values):
            if not used[index]:
                used[index] = True
                path.append(value)
                visit()
                path.pop()
                used[index] = False

    visit()
    return result


assert permutations([1, 2]) == [[1, 2], [2, 1]]
assert permutations([]) == [[]]
```

For distinct inputs: **O(n × n!) time and output space**, O(n) auxiliary space including the stack/used flags. Generating all outputs cannot be faster than writing them. A generator reduces retained output memory, not the total work to consume every result.

**Teaching check:** “How is DP different from backtracking?” DP remembers answers to repeated subproblems; backtracking builds a choice, explores it, and undoes it to try another. A problem can sometimes combine both ideas.

### 28. Union-find: repeated connectivity checks

**When to use it:** merging groups and asking “are these nodes connected?” Examples include incremental undirected connectivity, cycle checks, and Kruskal's spanning-tree algorithm.

**Optional advanced topic:** teach after trees and graph traversal.

**Walk through it:** start with groups `{0}, {1}, {2}, {3}`. Joining 0 and 1 gives `{0, 1}`. Joining 1 and 2 gives `{0, 1, 2}`. Now 0 and 2 are connected even without a direct link. Joining them again changes nothing; 3 is still separate.

`parent` links an item toward its group's representative (root). `find()` follows those links. `union()` joins two roots; `size` helps attach the smaller group to the larger one. Path halving shortens links during future lookups.

```python
class DisjointSet:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, node: int) -> int:
        while node != self.parent[node]:
            self.parent[node] = self.parent[self.parent[node]]  # Path halving.
            node = self.parent[node]
        return node

    def union(self, left: int, right: int) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


groups = DisjointSet(4)
assert groups.union(0, 1)
assert groups.union(1, 2)
assert groups.find(0) == groups.find(2)
assert not groups.union(0, 2)  # Already connected.
assert groups.find(0) != groups.find(3)
```

Assume `n >= 0` and node IDs in `0..n-1`. **Initialization:** O(n) time/space. Storage remains O(n). Linking smaller groups under larger ones, and shortening paths during lookup, makes long sequences of find/union operations very efficient.

<details>
<summary>Advanced complexity: why the bound is called amortized O(α(n))</summary>

Path halving plus union by size gives **amortized O(α(n))** per operation, where α is the extremely slowly growing inverse-Ackermann function. This is not a guarantee that each individual operation is worst-case O(1). You can first learn how the structure works without deriving that function.

</details>

Union-find answers connectivity questions; it does not directly support deleting edges or finding a shortest path.

#### Pause and predict: Coins are not stairs

With coins `[1, 3, 4]` and amount 6, are we adding all counts or choosing the smallest count? Then list the subsets of `[1, 2]`: why must each saved path be copied?

<details>
<summary>Open after predicting</summary>

Choose the smallest count: `3 + 3` uses two coins. Stairs adds alternative route counts; minimum coins minimizes a cost. The subsets are `[]`, `[1]`, `[1, 2]`, `[2]`; copying preserves each snapshot before later append/pop changes.

</details>

## Quick revision


| Task clue                         | Pattern              | Typical time                            | Working memory / caveat                         |
| --- | --- | --- | --- |
| Scan unsorted input once          | Linear search        | O(n)                                    | O(1) auxiliary                                  |
| Search sorted/monotonic space     | Binary search        | O(log n)                                | O(1) iterative; preprocessing may cost more     |
| Counts, duplicates, complements   | Hash map/set         | O(n) average                            | Up to O(n) auxiliary                            |
| Pair in sorted input              | Two pointers         | O(n)                                    | O(1) auxiliary; sorting is separate             |
| Consecutive k items               | Fixed sliding window | O(n)                                    | O(1) auxiliary for a running sum                |
| Longest substring without repeats | Variable window      | O(n) average                            | Up to O(n) auxiliary                            |
| Many static range-sum queries     | Prefix sums          | O(n) build; O(1) query                  | O(n) retained table                             |
| Maximum contiguous sum            | Kadane               | O(n)                                    | O(1) auxiliary                                  |
| Nested symbols                    | Stack                | O(n)                                    | Up to O(n) auxiliary                            |
| Next greater/smaller item         | Monotonic stack      | O(n)                                    | Up to O(n) stack plus output                    |
| Fewest edges / grid moves         | BFS                  | O(V + E)                                | O(V) auxiliary on adjacency lists               |
| Reachability / branch exploration | DFS                  | O(V + E)                                | O(V) visited/frames in the shown implementation |
| Dependency order                  | Topological sort     | O(V + E)                                | O(V) auxiliary; directed acyclic graph          |
| Nonnegative weighted paths        | Dijkstra             | O((V + E) log(V + 1)) on a simple graph | Lazy heap can use O(V + E) auxiliary space      |
| Largest k elements                | Bounded heap         | O(n log(k + 1) + k log k)               | O(k) auxiliary and output                       |
| Repeated subproblem answers       | Dynamic programming  | States × work per state                | Depends on retained states                      |
| All subsets / permutations        | Backtracking         | O(n × 2ⁿ) / O(n × n!)                | O(n) auxiliary; output is exponential/factorial |

Here `n` is sequence length, `V` vertices, `E` edges, and `k` requested window/result size. Time bounds are worst-case unless labeled; see each example for prerequisites. Check each topic's conditions before choosing an algorithm.

## Additional references

The main lessons and runnable examples are above. These optional materials provide diagrams, language foundations, or more background:

- [Python data structures interview handbook](../handbook/notes/python_data_structures_interview_handbook.md).
- [Older sorting diagrams](sort/readme.md) and [BST diagrams](binary_search/bst-binary_seatch_tree.md).
- [Native stack background and Python distinction](how-is-stack-managed.md).
- [Courses and books](data-structures-algorithms.md); the PDFs in this folder remain supplementary references.
- Python documentation: [sorting](https://docs.python.org/3.11/howto/sorting.html), [bisect](https://docs.python.org/3.11/library/bisect.html), [Counter](https://docs.python.org/3.11/library/collections.html#collections.Counter), [deque](https://docs.python.org/3.11/library/collections.html#collections.deque), and [heapq](https://docs.python.org/3.11/library/heapq.html).
