"""
Common Python Patterns for CodeSignal GCA Assessment
Ready-to-use implementations for typical algorithm problems

HOW TO USE THIS FILE:
1. Study each pattern to understand the approach
2. Don't just copy-paste - understand WHY it works
3. Try implementing each pattern from scratch first
4. Use this file as reference during practice
5. Run the test section to verify examples work

PATTERNS INCLUDED:
- Two Pointers (5 algorithms)
- Sliding Window (4 algorithms)
- Hash Maps (5 algorithms)
- DFS/Backtracking (2 algorithms)
- BFS (3 algorithms)
- Binary Search (3 algorithms)
- Dynamic Programming (5 algorithms)
- Heaps (3 algorithms)
- Utilities (4 algorithms)

TOTAL: 34 algorithms with working examples + tests

LEARNING APPROACH:
1. Read the docstring
2. Study the algorithm
3. Trace through with example
4. Implement from scratch
5. Run test section to verify
6. Practice variations
"""

from collections import defaultdict, Counter, deque
from typing import List, Optional, Dict, Set, Tuple
import bisect
import heapq


# ============================================================================
# TWO POINTERS PATTERN
# ============================================================================

def two_sum(arr: List[int], target: int) -> List[int]:
    """
    Two pointer approach for sorted array.
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []


def two_sum_unsorted(arr: List[int], target: int) -> List[int]:
    """
    Hash map approach for unsorted array.
    Time: O(n), Space: O(n)
    """
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def reverse_string(s: List[str]) -> None:
    """Two pointer reversal in-place."""
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1


def is_palindrome(s: str) -> bool:
    """Check palindrome using two pointers."""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def container_with_most_water(heights: List[int]) -> int:
    """
    Find maximum area between two lines.
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(heights) - 1
    max_area = 0

    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        max_area = max(max_area, area)

        # Move the pointer pointing to shorter line
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area


# ============================================================================
# SLIDING WINDOW PATTERN
# ============================================================================

def max_window_sum(arr: List[int], k: int) -> int:
    """
    Find maximum sum of k consecutive elements.
    Time: O(n), Space: O(1)
    """
    if k > len(arr):
        return 0

    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)

    return max_sum


def longest_substring_without_repeating(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    Time: O(n), Space: O(min(n, charset_size))
    """
    char_index = {}
    max_length = 0
    left = 0

    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_length = max(max_length, right - left + 1)

    return max_length


def sliding_window_maximum(arr: List[int], k: int) -> List[int]:
    """
    Find maximum in each sliding window.
    Time: O(n), Space: O(k)

    ⚠️ IMPORTANT: Uses deque as MONOTONIC DEQUE (not simple queue)
    - Maintains indices in decreasing order of values
    - Needs popleft() AND pop() operations
    - Index-based queue won't work here!

    Use deque for:
    • Monotonic stacks/queues
    • Operations from both ends

    Use index-based for:
    • Simple BFS/queue operations
    • Standard FIFO queue
    """
    if k > len(arr) or k == 0:
        return []

    result = []
    window = deque()  # Store indices

    for i in range(len(arr)):
        # Remove indices outside current window
        while window and window[0] < i - k + 1:
            window.popleft()

        # Remove smaller elements
        while window and arr[window[-1]] < arr[i]:
            window.pop()

        window.append(i)

        # Add to result when window is full
        if i >= k - 1:
            result.append(arr[window[0]])

    return result


def min_window_substring(s: str, t: str) -> str:
    """
    Find minimum window substring containing all characters in t.
    Time: O(n + m), Space: O(charset_size)
    """
    if not s or not t or len(t) > len(s):
        return ""

    dict_t = Counter(t)
    required = len(dict_t)

    window_counts = {}
    formed = 0
    left = 0
    result = (float('inf'), 0, 0)

    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1

        while left <= right and formed == required:
            char = s[left]

            if right - left + 1 < result[0]:
                result = (right - left + 1, left, right)

            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1

            left += 1

    return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]


# ============================================================================
# HASH MAP / COUNTER PATTERN
# ============================================================================

def most_common_elements(arr: List[int], k: int) -> List[int]:
    """
    Find k most common elements.
    Time: O(n log k), Space: O(n)
    """
    count = Counter(arr)
    return [num for num, _ in count.most_common(k)]


def group_anagrams(words: List[str]) -> List[List[str]]:
    """
    Group words that are anagrams of each other.
    Time: O(n * k log k), Space: O(n)
    """
    anagram_map = defaultdict(list)
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_map[sorted_word].append(word)

    return list(anagram_map.values())


def contains_duplicate(arr: List[int]) -> bool:
    """Check if array contains duplicates."""
    return len(arr) != len(set(arr))


def valid_anagram(s: str, t: str) -> bool:
    """Check if t is anagram of s."""
    return Counter(s) == Counter(t)


def intersection_of_two_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """Find intersection of two arrays."""
    set1 = set(arr1)
    return list(set(num for num in arr2 if num in set1))


# ============================================================================
# DFS / BACKTRACKING PATTERN
# ============================================================================

def dfs_recursive(node, visited: Set = None) -> None:
    """Generic DFS traversal."""
    if visited is None:
        visited = set()

    if node in visited:
        return

    visited.add(node)

    # Process node
    for neighbor in node.neighbors:
        dfs_recursive(neighbor, visited)


def dfs_with_stack(start_node) -> List:
    """DFS using explicit stack."""
    visited = set()
    stack = [start_node]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in reversed(node.neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

    return result


def permutations(arr: List) -> List[List]:
    """Generate all permutations."""
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return

        for i in range(len(remaining)):
            current.append(remaining[i])
            new_remaining = remaining[:i] + remaining[i+1:]
            backtrack(current, new_remaining)
            current.pop()

    backtrack([], arr)
    return result


def combinations(arr: List, r: int) -> List[List]:
    """Generate combinations of size r."""
    result = []

    def backtrack(start, current):
        if len(current) == r:
            result.append(current[:])
            return

        for i in range(start, len(arr)):
            current.append(arr[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


# ============================================================================
# BFS PATTERN
# ============================================================================

def bfs_traversal(start_node) -> List:
    """
    Generic BFS traversal.
    Time: O(V + E), Space: O(V)

    Uses deque for O(1) queue operations.
    Alternative: Use index-based queue (no imports needed):
        queue = [start_node]
        index = 0
        while index < len(queue):
            node = queue[index]
            index += 1
            # ... process node
    """
    visited = {start_node}
    queue = deque([start_node])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def level_order_traversal(root) -> List[List]:
    """
    Level-order tree traversal (BFS).
    Returns nodes grouped by level.
    Time: O(n), Space: O(w) where w is max width

    Uses deque for O(1) queue operations.
    Alternative: Index-based (no imports):
        queue = [root]
        index = 0
        while index < len(queue):
            level_size = len(queue) - index
            for _ in range(level_size):
                node = queue[index]
                index += 1
                # ... process node
    """
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


def shortest_path(graph: Dict, start, end) -> int:
    """
    Find shortest path using BFS.
    Time: O(V + E), Space: O(V)

    Uses deque for O(1) queue operations.
    Alternative: Index-based (no imports):
        queue = [(start, 0)]
        index = 0
        visited = {start}
        while index < len(queue):
            node, dist = queue[index]
            index += 1
            # ... process
    """
    visited = {start}
    queue = deque([(start, 0)])

    while queue:
        node, dist = queue.popleft()

        if node == end:
            return dist

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1


# ============================================================================
# BINARY SEARCH PATTERN
# ============================================================================

def binary_search(arr: List[int], target: int) -> int:
    """Standard binary search."""
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


def first_occurrence(arr: List[int], target: int) -> int:
    """Find first occurrence of target."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def search_rotated_array(arr: List[int], target: int) -> int:
    """Binary search in rotated sorted array."""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid

        # Determine which half is sorted
        if arr[left] <= arr[mid]:  # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


# ============================================================================
# DYNAMIC PROGRAMMING PATTERN
# ============================================================================

def fibonacci_memo(n: int, memo: Dict = None) -> int:
    """Fibonacci with memoization."""
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_dp(n: int) -> int:
    """Fibonacci with tabulation."""
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def coin_change(coins: List[int], amount: int) -> int:
    """
    Minimum number of coins to make amount.
    Time: O(n * amount), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def max_subarray(arr: List[int]) -> int:
    """Kadane's algorithm for maximum subarray sum."""
    max_sum = current_sum = arr[0]

    for num in arr[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Find length of LCS."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


# ============================================================================
# HEAP / PRIORITY QUEUE PATTERN
# ============================================================================

def kth_largest_element(arr: List[int], k: int) -> int:
    """Find kth largest element using min heap."""
    if k > len(arr):
        return -1

    heap = arr[:k]
    heapq.heapify(heap)

    for num in arr[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]


def top_k_frequent(arr: List[int], k: int) -> List[int]:
    """Find k most frequent elements using heap."""
    count = Counter(arr)
    heap = [(-freq, num) for num, freq in count.items()]
    heapq.heapify(heap)

    return [heapq.heappop(heap)[1] for _ in range(k)]


def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """Merge k sorted lists using min heap."""
    heap = []

    # Add first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from the same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result


# ============================================================================
# UNION-FIND / DISJOINT SET PATTERN
# ============================================================================

class UnionFind:
    """Union-Find (Disjoint Set Union) implementation."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank. Returns True if union happened."""
        root_x, root_y = self.find(x), self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


# ============================================================================
# QUICK UTILITY FUNCTIONS
# ============================================================================

def is_prime(n: int) -> bool:
    """Check if number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple."""
    return a * b // gcd(a, b)


def sieve_of_eratosthenes(n: int) -> List[int]:
    """Find all primes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]


# ============================================================================
# TEST EXAMPLES - Input/Output for all functions
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("COMMON PATTERNS - TEST EXAMPLES")
    print("=" * 80)

    # TWO POINTERS
    print("\n### TWO POINTERS ###")
    print(f"two_sum([1, 2, 3, 5, 8], 13) → {two_sum([1, 2, 3, 5, 8], 13)}")
    print("  Expected: [3, 4]  (arr[3]=5, arr[4]=8)")

    print(f"\ntwo_sum_unsorted([3, 2, 4], 6) → {two_sum_unsorted([3, 2, 4], 6)}")
    print("  Expected: [1, 2]  (arr[1]=2, arr[2]=4)")

    s = ['h', 'e', 'l', 'l', 'o']
    reverse_string(s)
    print(f"\nreverse_string(['h','e','l','l','o']) → {s}")
    print("  Expected: ['o', 'l', 'l', 'e', 'h']")

    print(f"\nis_palindrome('racecar') → {is_palindrome('racecar')}")
    print("  Expected: True")

    print(f"\ncontainer_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) → {container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7])}")
    print("  Expected: 49  (width=8, height=min(8,7)=7, area=56 or 8*7=49)")

    # SLIDING WINDOW
    print("\n### SLIDING WINDOW ###")
    print(f"max_window_sum([1, 3, 2, 6, -1, 4, 1, 8], 3) → {max_window_sum([1, 3, 2, 6, -1, 4, 1, 8], 3)}")
    print("  Expected: 13  (windows: [1,3,2]=6, [3,2,6]=11, [2,6,-1]=7, [6,-1,4]=9, [-1,4,1]=4, [4,1,8]=13)")

    print(f"\nlongest_substring_without_repeating('abcabcbb') → {longest_substring_without_repeating('abcabcbb')}")
    print("  Expected: 3  ('abc')")

    print(f"\nsliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3) → {sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3)}")
    print("  Expected: [3, 3, 5, 5, 6, 7]")

    print(f"\nmin_window_substring('ADOBECODEBANC', 'ABC') → {min_window_substring('ADOBECODEBANC', 'ABC')}")
    print("  Expected: 'BANC'")

    # HASH MAP / COUNTER
    print("\n### HASH MAP / COUNTER ###")
    print(f"most_common_elements([1, 1, 1, 2, 2, 3], 2) → {most_common_elements([1, 1, 1, 2, 2, 3], 2)}")
    print("  Expected: [1, 2]")

    print(f"\ngroup_anagrams(['eat', 'tea', 'ate', 'bat', 'tab']) → {group_anagrams(['eat', 'tea', 'ate', 'bat', 'tab'])}")
    print("  Expected: [['eat', 'tea', 'ate'], ['bat', 'tab']] (grouped by anagrams)")

    print(f"\ncontains_duplicate([1, 2, 3, 1]) → {contains_duplicate([1, 2, 3, 1])}")
    print("  Expected: True")

    print(f"\nvalid_anagram('anagram', 'nagaram') → {valid_anagram('anagram', 'nagaram')}")
    print("  Expected: True")

    print(f"\nintersection_of_two_arrays([1, 2, 2, 1], [2, 2]) → {intersection_of_two_arrays([1, 2, 2, 1], [2, 2])}")
    print("  Expected: [2]")

    # PERMUTATIONS & COMBINATIONS
    print("\n### BACKTRACKING ###")
    print(f"permutations([1, 2, 3]) → {permutations([1, 2, 3])}")
    print("  Expected: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]")

    print(f"\ncombinations([1, 2, 3, 4], 2) → {combinations([1, 2, 3, 4], 2)}")
    print("  Expected: [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]")

    # BINARY SEARCH
    print("\n### BINARY SEARCH ###")
    print(f"binary_search([1, 3, 5, 7, 9, 11], 7) → {binary_search([1, 3, 5, 7, 9, 11], 7)}")
    print("  Expected: 3  (arr[3]=7)")

    print(f"\nfirst_occurrence([5, 7, 7, 8, 8, 10], 8) → {first_occurrence([5, 7, 7, 8, 8, 10], 8)}")
    print("  Expected: 3  (first index of 8)")

    print(f"\nsearch_rotated_array([4, 5, 6, 7, 0, 1, 2], 0) → {search_rotated_array([4, 5, 6, 7, 0, 1, 2], 0)}")
    print("  Expected: 4  (arr[4]=0)")

    # DYNAMIC PROGRAMMING
    print("\n### DYNAMIC PROGRAMMING ###")
    print(f"fibonacci_memo(10) → {fibonacci_memo(10)}")
    print("  Expected: 55  (sequence: 0,1,1,2,3,5,8,13,21,34,55)")

    print(f"\nfibonacci_dp(10) → {fibonacci_dp(10)}")
    print("  Expected: 55")

    print(f"\ncoin_change([1, 2, 5], 5) → {coin_change([1, 2, 5], 5)}")
    print("  Expected: 1  (use one 5-cent coin)")

    print(f"\nmax_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) → {max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])}")
    print("  Expected: 6  (subarray [4, -1, 2, 1])")

    print(f"\nlongest_common_subsequence('abc', 'abc') → {longest_common_subsequence('abc', 'abc')}")
    print("  Expected: 3  (entire string matches)")

    # HEAP
    print("\n### HEAP ###")
    print(f"kth_largest_element([4, 3, 5, 7, 2, 1, 9, 6], 3) → {kth_largest_element([4, 3, 5, 7, 2, 1, 9, 6], 3)}")
    print("  Expected: 6  (3rd largest: 7, 9, 8→6)")

    print(f"\ntop_k_frequent([1, 1, 1, 2, 2, 3], 2) → {top_k_frequent([1, 1, 1, 2, 2, 3], 2)}")
    print("  Expected: [1, 2]")

    print(f"\nmerge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]]) → {merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])}")
    print("  Expected: [1, 1, 2, 3, 4, 4, 5, 6]")

    # UTILITY
    print("\n### UTILITY FUNCTIONS ###")
    print(f"is_prime(17) → {is_prime(17)}")
    print("  Expected: True")

    print(f"\ngcd(48, 18) → {gcd(48, 18)}")
    print("  Expected: 6")

    print(f"\nlcm(12, 18) → {lcm(12, 18)}")
    print("  Expected: 36")

    print(f"\nsieve_of_eratosthenes(20) → {sieve_of_eratosthenes(20)}")
    print("  Expected: [2, 3, 5, 7, 11, 13, 17, 19]")

    print("\n" + "=" * 80)
