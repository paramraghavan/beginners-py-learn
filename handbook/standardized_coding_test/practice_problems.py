"""
Practice Problems for CodeSignal GCA Assessment
Organized by difficulty level with explanations

HOW TO USE THIS FILE:
1. Try to solve each problem WITHOUT looking at the solution
2. Work through the examples manually on paper first
3. Then code your solution
4. Compare with the provided solution
5. Understand the approach and why it works
6. Note the time/space complexity

DIFFICULTY PROGRESSION:
- Easy: 15-20 minutes per problem (warm-up)
- Medium: 25-35 minutes per problem (main test content)
- Hard: 35-50+ minutes per problem (if time permits)

PRACTICE TIP:
Solve each problem twice:
- First: Try to solve without hints
- Second: Solve by referencing the pattern only (no full code)

BEGINNER SOLVING SCRIPT:
Before writing code, fill in these blanks:
1. Input type: ______
2. Output type: ______
3. Brute force idea: ______
4. Pattern I recognize: ______
5. Data structure I need: ______
6. Edge cases: empty, one item, duplicates, negatives, no answer

MENTAL NOTE:
Most mistakes happen before coding starts. If you cannot say the pattern in one
sentence, slow down and trace the sample input by hand.
"""

from typing import List, Optional, Dict
from collections import defaultdict, Counter, deque


# ============================================================================
# EASY PROBLEMS (15-20 minutes)
# ============================================================================

def remove_duplicates_from_sorted_array(nums: List[int]) -> int:
    """
    Remove duplicates in-place from sorted array.
    Return the length of the array without duplicates.

    Example:
    Input: nums = [1,1,2]
    Output: 2, nums = [1,2,_]

    Approach: Two pointers - maintain pointer for insertion position.
    Why this works: the array is sorted, so duplicates are next to each other.
    When a new value appears, copy it to the next safe position.
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0

    insert_pos = 0

    for i in range(1, len(nums)):
        if nums[i] != nums[insert_pos]:
            insert_pos += 1
            nums[insert_pos] = nums[i]

    return insert_pos + 1


def single_number(nums: List[int]) -> int:
    """
    Find the single number that appears once.
    All other numbers appear twice.

    Example:
    Input: nums = [2,2,1]
    Output: 1

    Approach: XOR all numbers (a ^ a = 0, a ^ 0 = a).
    Why this works: paired values cancel out, leaving the unpaired value.
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def majority_element(nums: List[int]) -> int:
    """
    Find element that appears more than n/2 times.
    Guaranteed to exist.

    Example:
    Input: nums = [3,2,3]
    Output: 3

    Approach: Boyer-Moore voting algorithm.
    Why this works: the majority value appears more than all other values
    combined, so pairwise cancellation cannot fully remove it.
    Time: O(n), Space: O(1)
    """
    count = 0
    candidate = None

    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)

    return candidate


def rotate_array(nums: List[int], k: int) -> None:
    """
    Rotate array to the right by k steps in-place.

    Example:
    Input: nums = [1,2,3,4,5], k = 2
    Output: [4,5,1,2,3]

    Approach: Reverse sections - reverse all, reverse first k, reverse last n-k.
    Why this works: reversing all moves the right block to the front but also
    reverses both blocks internally; the next two reversals fix each block.
    Time: O(n), Space: O(1)
    """
    k = k % len(nums)
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])


def contains_duplicate(nums: List[int]) -> bool:
    """
    Check if array contains duplicates.

    Example:
    Input: nums = [1,2,3,1]
    Output: True

    Approach: Use set
    Time: O(n), Space: O(n)
    """
    return len(nums) != len(set(nums))


def valid_anagram(s: str, t: str) -> bool:
    """
    Check if t is anagram of s.

    Example:
    Input: s = "anagram", t = "nagaram"
    Output: True

    Approach: Count characters
    Time: O(n), Space: O(1) [fixed charset]
    """
    return sorted(s) == sorted(t)
    # or: return Counter(s) == Counter(t)


def first_unique_character(s: str) -> int:
    """
    Find index of first non-repeating character.
    Return -1 if all characters repeat.

    Example:
    Input: s = "leetcode"
    Output: 0

    Approach: Count characters, then find first with count 1
    Time: O(n), Space: O(n)
    """
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1


def is_palindrome_string(s: str) -> bool:
    """
    Check if string is palindrome (alphanumeric only, case-insensitive).

    Example:
    Input: s = "A man, a plan, a canal: Panama"
    Output: True

    Approach: Two pointers, skip non-alphanumeric
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


# ============================================================================
# MEDIUM PROBLEMS (25-35 minutes)
# ============================================================================

def longest_substring_without_repeating(s: str) -> int:
    """
    Find length of longest substring without repeating characters.

    Example:
    Input: s = "abcabcbb"
    Output: 3 ("abc")

    Approach: Sliding window with hash map
    Time: O(n), Space: O(min(n, charset))
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


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Find all unique triplets that sum to zero.

    Example:
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2],[-1,0,1]]

    Approach: Sort, then use two pointers for each element
    Time: O(n^2), Space: O(1) [excluding output]
    """
    if not nums or len(nums) < 3:
        return []

    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        if nums[i] > 0:  # Optimization: positive can't sum to 0
            break
        if i > 0 and nums[i] == nums[i - 1]:  # Skip duplicates
            continue

        left, right = i + 1, len(nums) - 1

        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]

            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicate elements
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1

    return result


def set_matrix_zeroes(matrix: List[List[int]]) -> None:
    """
    Set entire row and column to 0 if element is 0.
    Do it in-place.

    Approach: Use first row/column as markers
    Time: O(m*n), Space: O(1)
    """
    m, n = len(matrix), len(matrix[0])
    first_row_zero = False
    first_col_zero = False

    # Check if first row/column should be zero
    for i in range(m):
        if matrix[i][0] == 0:
            first_col_zero = True
            break

    for j in range(n):
        if matrix[0][j] == 0:
            first_row_zero = True
            break

    # Use first row/column as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Set rows and columns to 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Handle first row and column
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0

    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge overlapping intervals.

    Example:
    Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]

    Approach: Sort by start, then merge
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []

    intervals.sort()
    result = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= result[-1][1]:
            # Overlapping: merge
            result[-1][1] = max(result[-1][1], end)
        else:
            # Non-overlapping: add new interval
            result.append([start, end])

    return result


def word_break(s: str, word_dict: List[str]) -> bool:
    """
    Check if string can be segmented using words in dictionary.

    Example:
    Input: s = "leetcode", word_dict = ["leet", "code"]
    Output: True

    Approach: Dynamic programming
    Time: O(n^2), Space: O(n)
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[len(s)]


def course_schedule(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """
    Determine if all courses can be completed (no cycles in dependency graph).

    Example:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: True

    Approach: Topological sort / cycle detection
    Time: O(V + E), Space: O(V + E)
    """
    # Build graph
    graph = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Topological sort using Kahn's algorithm
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    courses_completed = 0

    while queue:
        course = queue.popleft()
        courses_completed += 1

        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return courses_completed == num_courses


def word_ladder(begin_word: str, end_word: str, word_list: List[str]) -> int:
    """
    Find shortest transformation sequence from begin_word to end_word.
    Each intermediate word must be in word_list, and differ by one letter.

    Example:
    Input: beginWord = "hit", endWord = "cog",
           wordList = ["hot","dot","dog","lot","log","cog"]
    Output: 5 (hit -> hot -> dot -> dog -> cog)

    Approach: BFS with word transformation
    Time: O(n * l^2), Space: O(n * l)
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    def get_neighbors(word):
        neighbors = []
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in word_set:
                        neighbors.append(new_word)
        return neighbors

    while queue:
        word, dist = queue.popleft()

        if word == end_word:
            return dist

        for neighbor in get_neighbors(word):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return 0


# ============================================================================
# HARD PROBLEMS (35-50+ minutes)
# ============================================================================

def median_of_two_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    """
    Find median of two sorted arrays.

    Example:
    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.0

    Approach: Binary search on shorter array
    Time: O(log(min(n, m))), Space: O(1)
    """
    if len(nums1) > len(nums2):
        return median_of_two_sorted_arrays(nums2, nums1)

    low, high = 0, len(nums1)

    while low <= high:
        cut1 = (low + high) // 2
        cut2 = (len(nums1) + len(nums2) + 1) // 2 - cut1

        left1 = float('-inf') if cut1 == 0 else nums1[cut1 - 1]
        left2 = float('-inf') if cut2 == 0 else nums2[cut2 - 1]
        right1 = float('inf') if cut1 == len(nums1) else nums1[cut1]
        right2 = float('inf') if cut2 == len(nums2) else nums2[cut2]

        if left1 <= right2 and left2 <= right1:
            if (len(nums1) + len(nums2)) % 2 == 0:
                return (max(left1, left2) + min(right1, right2)) / 2
            else:
                return max(left1, left2)

        elif left1 > right2:
            high = cut1 - 1
        else:
            low = cut1 + 1

    return -1


def trapping_rain_water(height: List[int]) -> int:
    """
    Calculate water trapped between elevations.

    Example:
    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6

    Approach: Two pointers
    Time: O(n), Space: O(1)
    """
    if not height or len(height) < 3:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    trapped = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                trapped += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                trapped += right_max - height[right]
            right -= 1

    return trapped


def longest_valid_parentheses(s: str) -> int:
    """
    Find length of longest valid parentheses substring.

    Example:
    Input: s = ")()())"
    Output: 4 ("()()")

    Approach: Dynamic programming or stack
    Time: O(n), Space: O(n)
    """
    dp = [0] * len(s)
    max_len = 0

    for i in range(1, len(s)):
        if s[i] == ')':
            if s[i - 1] == '(':
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif dp[i - 1] > 0:
                # s[i-1] == ')' and s[i - dp[i-1] - 1] == '('
                if i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == '(':
                    dp[i] = dp[i - 1] + 2
                    if i - dp[i - 1] - 2 >= 0:
                        dp[i] += dp[i - dp[i - 1] - 2]

            max_len = max(max_len, dp[i])

    return max_len


def max_rectangle_in_histogram(heights: List[int]) -> int:
    """
    Find largest rectangle area in histogram.

    Example:
    Input: heights = [2,1,5,6,2,3]
    Output: 10

    Approach: Stack with indices
    Time: O(n), Space: O(n)
    """
    stack = []
    max_area = 0

    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            index, height = stack.pop()
            area = height * (i - index)
            max_area = max(max_area, area)
            start = index

        if h > 0:
            stack.append((start, h))

    for index, height in stack:
        area = height * (len(heights) - index)
        max_area = max(max_area, area)

    return max_area


def serialize_deserialize_tree(root) -> tuple:
    """
    Serialize and deserialize binary tree.

    Approach: Level-order traversal with null markers
    Time: O(n), Space: O(n)
    """
    def serialize(root):
        if not root:
            return "None"

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if not node:
                result.append("None")
            else:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)

        return ",".join(result)

    def deserialize(data):
        if data == "None":
            return None

        from data_structures import TreeNode

        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1

        while queue and i < len(vals):
            node = queue.popleft()

            if vals[i] != "None":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1

            if i < len(vals) and vals[i] != "None":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1

        return root

    return serialize, deserialize


# ============================================================================
# QUICK REFERENCE: PROBLEM SOLVING CHECKLIST
# ============================================================================

"""
For each problem:

1. READ & UNDERSTAND
   - What is input? What is output?
   - What are constraints?
   - Are there edge cases?

2. EXAMPLES
   - Work through given examples
   - Create own examples

3. APPROACH
   - What algorithm/data structure?
   - Brute force first, then optimize
   - Pseudocode before coding

4. IMPLEMENT
   - Write clean code
   - Use clear variable names
   - Add comments for complex logic

5. TEST
   - Test with provided examples
   - Test edge cases (empty, single, large)
   - Check time/space complexity

6. OPTIMIZE
   - Can we reduce time complexity?
   - Can we reduce space complexity?
   - Is code readable?

Remember: Correct > Fast > Elegant
"""


# ============================================================================
# TEST EXAMPLES - Input/Output for all practice problems
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PRACTICE PROBLEMS - TEST EXAMPLES")
    print("=" * 80)

    # EASY PROBLEMS
    print("\n### EASY PROBLEMS ###")

    nums = [1, 1, 2]
    length = remove_duplicates_from_sorted_array(nums)
    print(f"remove_duplicates_from_sorted_array([1,1,2]) → length={length}, array={nums[:length]}")
    print("  Expected: length=2, array=[1, 2]")

    print(f"single_number([2, 2, 1]) → {single_number([2, 2, 1])}")
    print("  Expected: 1")

    print(f"majority_element([3, 2, 3]) → {majority_element([3, 2, 3])}")
    print("  Expected: 3  (appears more than n/2 times)")

    nums = [1, 2, 3]
    rotate_array(nums, 2)
    print(f"rotate_array([1,2,3], k=2) → {nums}")
    print("  Expected: [2, 3, 1]  (rotated right by 2)")

    print(f"contains_duplicate([1, 2, 3, 1]) → {contains_duplicate([1, 2, 3, 1])}")
    print("  Expected: True")

    print(f"valid_anagram('anagram', 'nagaram') → {valid_anagram('anagram', 'nagaram')}")
    print("  Expected: True")

    print(f"first_unique_character('leetcode') → {first_unique_character('leetcode')}")
    print("  Expected: 0  (l at index 0 appears once)")

    print(f"is_palindrome_string('A man, a plan, a canal: Panama') → {is_palindrome_string('A man, a plan, a canal: Panama')}")
    print("  Expected: True  (ignoring spaces, punctuation, case)")

    # MEDIUM PROBLEMS
    print("\n### MEDIUM PROBLEMS ###")

    print(f"longest_substring_without_repeating('abcabcbb') → {longest_substring_without_repeating('abcabcbb')}")
    print("  Expected: 3  ('abc')")

    print(f"three_sum([-1, 0, 1, 2, -1, -4]) → {three_sum([-1, 0, 1, 2, -1, -4])}")
    print("  Expected: [[-1, -1, 2], [-1, 0, 1]]  (unique triplets summing to 0)")

    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    set_matrix_zeroes(matrix)
    print(f"set_matrix_zeroes with 0 at [1,1] → {matrix}")
    print("  Expected: row 1 and col 1 become 0")

    print(f"merge_intervals([[1,3],[2,6],[8,10],[15,18]]) → {merge_intervals([[1,3],[2,6],[8,10],[15,18]])}")
    print("  Expected: [[1, 6], [8, 10], [15, 18]]")

    print(f"word_break('leetcode', ['leet','code']) → {word_break('leetcode', ['leet','code'])}")
    print("  Expected: True  (can be segmented)")

    print(f"course_schedule(2, [[1,0]]) → {course_schedule(2, [[1,0]])}")
    print("  Expected: True  (no circular dependency)")

    # HARD PROBLEMS
    print("\n### HARD PROBLEMS ###")

    print(f"word_ladder('hit', 'cog', ['hot','dot','dog','lot','log','cog']) → {word_ladder('hit', 'cog', ['hot','dot','dog','lot','log','cog'])}")
    print("  Expected: 5  (hit→hot→dot→dog→cog)")

    print(f"median_of_two_sorted_arrays([1,3], [2]) → {median_of_two_sorted_arrays([1, 3], [2])}")
    print("  Expected: 2.0  (sorted: [1,2,3], median is 2)")

    print(f"trapping_rain_water([0,1,0,2,1,0,1,3,2,1,2,1]) → {trapping_rain_water([0,1,0,2,1,0,1,3,2,1,2,1])}")
    print("  Expected: 6  (trapped units of water)")

    print(f"longest_valid_parentheses('(()()()')) → {longest_valid_parentheses('(()()())')}")
    print("  Expected: 6  (entire string is valid)")

    print(f"max_rectangle_in_histogram([2,1,5,6,2,3]) → {max_rectangle_in_histogram([2,1,5,6,2,3])}")
    print("  Expected: 10  (height 2, width 5: positions 2-6)")

    print("\n" + "=" * 80)
