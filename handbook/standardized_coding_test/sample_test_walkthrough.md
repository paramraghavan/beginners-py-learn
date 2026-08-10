# Sample GCA Test Walkthrough

This document walks through a simulated 70-minute GCA test with 3 problems.

---

## Simulated Test Problems

### Problem 1 (Easy): Two Sum
**Time: 0-20 minutes**

```
Given an array of integers nums and an integer target,
return the indices of the two numbers that add up to target.

You may assume each input has exactly one solution,
and you cannot use the same element twice.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums[0] + nums[1] == 9, so return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
```

#### Walkthrough (5 minutes)

**0:00-0:30 | Read & Understand**
```
✓ Input: array of integers + target
✓ Output: indices of two numbers
✓ Constraints:
  - Exactly one solution
  - Can't reuse same element
  - Up to 10^4 elements (moderate size)
```

**0:30-1:00 | Examples**
```
Example 1: [2,7,11,15], target 9
  → 2 + 7 = 9 → indices [0,1] ✓

Example 2: [3,2,4], target 6
  → 2 + 4 = 6 → indices [1,2] ✓
```

**1:00-2:00 | Algorithm**
```
Approach 1 (Brute Force):
- Nested loops: check every pair O(n²)
- Too slow for 10^4 elements

Approach 2 (Hash Map): ✓ BEST
- Iterate through array
- For each number, check if (target - number) exists
- Store seen numbers in hash map
- Time: O(n), Space: O(n)

Approach 3 (Sort + Two Pointers):
- Sort array O(n log n)
- Two pointers from ends
- Problem: loses original indices (need to track)
```

**2:00-5:00 | Pseudocode**
```
seen_map = {}
for i, num in nums:
    complement = target - num
    if complement in seen_map:
        return [seen_map[complement], i]
    seen_map[num] = i
return []  # Should never reach if problem guaranteed solution
```

**5:00-15:00 | Code**
```python
def twoSum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []
```

**15:00-20:00 | Test & Debug**

```python
# Test Example 1
nums = [2,7,11,15]
target = 9
result = twoSum(nums, target)
print(result)  # Expected: [0,1]
# ✓ CORRECT

# Test Example 2
nums = [3,2,4]
target = 6
result = twoSum(nums, target)
print(result)  # Expected: [1,2]
# ✓ CORRECT

# Edge cases
nums = [3,2,3]
target = 6
result = twoSum(nums, target)
print(result)  # Expected: [0,2]
# ✓ CORRECT (uses same value, not same element)

# Negatives
nums = [-1,0,1,2]
target = 1
result = twoSum(nums, target)
print(result)  # Expected: [0,3] (-1 + 2 = 1)
# ✓ CORRECT
```

**Status: COMPLETE ✓**
- Correctness: Passes all tests
- Efficiency: O(n) time, O(n) space - OPTIMAL
- Code quality: Clear, readable, no syntax errors

---

### Problem 2 (Medium): Merge Intervals
**Time: 20-50 minutes**

```
Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals, and return an array of non-overlapping
intervals that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4
```

#### Walkthrough (30 minutes)

**20:00-20:30 | Read & Understand**
```
✓ Input: array of [start, end] intervals
✓ Output: merged non-overlapping intervals
✓ Key detail: [1,4] and [4,5] overlap (touching counts as overlap)
✓ Constraints: Up to 10^4 intervals
```

**20:30-22:00 | Examples**
```
Example 1: [[1,3],[2,6],[8,10],[15,18]]
  - [1,3] and [2,6] overlap → merge to [1,6]
  - [8,10] and [15,18] don't overlap
  - Result: [[1,6],[8,10],[15,18]] ✓

Example 2: [[1,4],[4,5]]
  - [1,4] and [4,5] touch → merge to [1,5]
  - Result: [[1,5]] ✓

Edge case: [[1,5]]
  - Single interval → return as-is
  - Result: [[1,5]] ✓

Edge case: [[2,3],[1,2],[3,4],[4,5]]
  - All overlapping after sorting
  - Sort: [[1,2],[2,3],[3,4],[4,5]]
  - Merge all → [[1,5]]
```

**22:00-24:00 | Algorithm**

```
Key Insight:
- [a,b] and [c,d] overlap if: c <= b
- After sorting by start, we only compare with last merged interval

Algorithm:
1. Sort intervals by start time
2. Iterate through sorted intervals
3. If current overlaps with last in result:
   - Extend last interval's end = max(last_end, current_end)
4. If no overlap:
   - Add current interval to result

Why it works:
- Sorting ensures we process overlapping groups in order
- Once we've merged all overlapping intervals in a group,
  we won't see them again
- Time: O(n log n) for sorting + O(n) for merging = O(n log n)
- Space: O(n) for result
```

**24:00-25:30 | Pseudocode**
```
sort intervals by start time

result = [intervals[0]]

for current in intervals[1:]:
    last = result[-1]

    if current.start <= last.end:
        # Overlapping: merge
        last.end = max(last.end, current.end)
    else:
        # No overlap: add new
        result.append(current)

return result
```

**25:30-40:00 | Code**
```python
def merge(intervals):
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    # Result starts with first interval
    result = [intervals[0]]

    # Merge overlapping intervals
    for current_start, current_end in intervals[1:]:
        last_start, last_end = result[-1]

        # Check if overlapping
        if current_start <= last_end:
            # Merge: extend the end
            result[-1] = [last_start, max(last_end, current_end)]
        else:
            # No overlap: add new interval
            result.append([current_start, current_end])

    return result
```

**40:00-45:00 | Test & Debug**

```python
# Test Example 1
intervals = [[1,3],[2,6],[8,10],[15,18]]
result = merge(intervals)
print(result)  # Expected: [[1,6],[8,10],[15,18]]
# ✓ CORRECT

# Test Example 2
intervals = [[1,4],[4,5]]
result = merge(intervals)
print(result)  # Expected: [[1,5]]
# ✓ CORRECT

# Edge case: single
intervals = [[1,5]]
result = merge(intervals)
print(result)  # Expected: [[1,5]]
# ✓ CORRECT

# Edge case: all separate
intervals = [[1,2],[3,4],[5,6]]
result = merge(intervals)
print(result)  # Expected: [[1,2],[3,4],[5,6]]
# ✓ CORRECT

# Edge case: completely overlapping
intervals = [[1,5],[2,3]]
result = merge(intervals)
print(result)  # Expected: [[1,5]]
# ✓ CORRECT

# Edge case: unsorted input
intervals = [[15,18],[1,3],[2,6],[8,10]]
result = merge(intervals)
print(result)  # Expected: [[1,6],[8,10],[15,18]]
# ✓ CORRECT
```

**Status: COMPLETE ✓**
- Correctness: Passes all test cases
- Efficiency: O(n log n) time, O(n) space - OPTIMAL for this problem
- Code quality: Clear algorithm, readable, handles edge cases

---

### Problem 3 (Hard): Trapping Rain Water
**Time: 50-70 minutes**

```
Given n non-negative integers representing an elevation map
where the width of each bar is 1, compute how much water
it can trap after raining.

Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: 6 units of rain water (in blue) are trapped.
     |
  |  | |
 _|  |_|_
|_|_|_|_|

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5
```

#### Walkthrough (20 minutes)

**50:00-50:30 | Read & Understand**
```
✓ Input: array of bar heights
✓ Output: units of water trapped
✓ Key insight: water trapped at position i depends on:
  - Maximum height to the left
  - Maximum height to the right
  - Current height
```

**50:30-52:00 | Examples**
```
Example 1: [0,1,0,2,1,0,1,3,2,1,2,1]
Index:      0 1 2 3 4 5 6 7 8 9 10 11

At index 2:
- Height: 0
- Max left: 1
- Max right: 3
- Water: min(1,3) - 0 = 1

At index 4:
- Height: 1
- Max left: 2
- Max right: 3
- Water: min(2,3) - 1 = 1

Total: Calculate for each position
Result: 6 units ✓
```

**52:00-54:00 | Algorithm**

```
Approach 1 (Brute Force):
- For each bar, find max left and max right
- Time: O(n²) - TOO SLOW

Approach 2 (Precompute):
- Build left_max array: max height from left to i
- Build right_max array: max height from right to i
- Time: O(n), Space: O(n)

Approach 3 (Two Pointers): ✓ BEST FOR INTERVIEW
- Use left and right pointers
- Track left_max and right_max
- Move pointer with smaller max
- Time: O(n), Space: O(1)
- WHY: Water level at position = min(left_max, right_max)
  If left_max < right_max, we know right_max is at least left_max
  So water at left = left_max - height[left]
  No need to know actual right_max!
```

**54:00-56:00 | Pseudocode**
```
left = 0, right = n-1
left_max = 0, right_max = 0
water = 0

while left <= right:
    if height[left] < height[right]:
        if height[left] >= left_max:
            left_max = height[left]
        else:
            water += left_max - height[left]
        left += 1
    else:
        if height[right] >= right_max:
            right_max = height[right]
        else:
            water += right_max - height[right]
        right -= 1

return water
```

**56:00-65:00 | Code**
```python
def trap(height):
    if not height or len(height) < 3:
        return 0

    left = 0
    right = len(height) - 1
    left_max = 0
    right_max = 0
    water = 0

    while left <= right:
        if height[left] < height[right]:
            # Process from left side
            if height[left] >= left_max:
                left_max = height[left]
            else:
                # Water trapped
                water += left_max - height[left]
            left += 1
        else:
            # Process from right side
            if height[right] >= right_max:
                right_max = height[right]
            else:
                # Water trapped
                water += right_max - height[right]
            right -= 1

    return water
```

**65:00-68:00 | Test & Debug**

```python
# Test Example 1
height = [0,1,0,2,1,0,1,3,2,1,2,1]
result = trap(height)
print(result)  # Expected: 6
# Manual trace:
# left=0: height=0, left_max=0, water+=0
# left=1: height=1, left_max=1, water+=0
# left=2: height=0, left_max=1, water+=1 (total: 1)
# left=3: height=2, left_max=2, water+=0
# left=4: height=1, left_max=2, water+=1 (total: 2)
# left=5: height=0, left_max=2, water+=2 (total: 4)
# left=6: height=1, left_max=2, water+=1 (total: 5)
# ... continue ...
# ✓ CORRECT

# Test Example 2
height = [4,2,0,3,2,5]
result = trap(height)
print(result)  # Expected: 9
# ✓ CORRECT

# Edge case: no water
height = [3,0,2,0,4]
result = trap(height)
print(result)  # Expected: 7
# ✓ CORRECT
```

**68:00-70:00 | Review & Submit**

```
Checklist:
[✓] Problem understood
[✓] Algorithm chosen (two pointers - optimal)
[✓] Code written and tested
[✓] Edge cases handled
[✓] Efficiency good (O(n) time, O(1) space)
[✓] Code readable

SUBMIT!
```

---

## Test Summary

| Problem | Difficulty | Time | Status | Points |
|---------|-----------|------|--------|--------|
| Two Sum | Easy | 20 min | Complete | ~30% |
| Merge Intervals | Medium | 30 min | Complete | ~45% |
| Trap Rain Water | Hard | 20 min | Complete | ~25% |
| **Total** | - | **70 min** | **All Complete** | **~100%** |

---

## Key Takeaways from This Test

### Time Management
- ✓ Started with easiest (built confidence)
- ✓ Allocated appropriate time per difficulty
- ✓ Completed all 3 problems
- ✓ Had time for testing and review

### Problem Solving
- ✓ Read carefully before coding
- ✓ Worked through examples
- ✓ Used pseudocode to plan
- ✓ Chose optimal algorithms
- ✓ Tested edge cases
- ✓ Verified correctness

### What Made It Work
1. **Reading problems first** - Understood all tasks before starting
2. **Algorithm selection** - Chose efficient approaches (not brute force)
3. **Pseudocode** - Planned before coding
4. **Testing** - Verified with examples and edge cases
5. **Time discipline** - Moved on when appropriate
6. **Code quality** - Readable, not clever

### Common Patterns Seen
1. **Two Pointers** - Used in problem 1 & 3
2. **Sorting + Iteration** - Used in problem 2
3. **State Tracking** - Used in all problems
4. **Optimization** - All O(n) or O(n log n) time

---

## Practice Tips

1. **Practice under time pressure**
   - Set 70-minute timer
   - Simulate real test conditions

2. **Always work through examples first**
   - Before coding, trace through examples
   - Understand the pattern

3. **Use pseudocode**
   - Saves debugging time later
   - Clarifies thinking

4. **Test edge cases**
   - Empty input
   - Single element
   - All same elements
   - Negative numbers

5. **Move on when stuck**
   - Max 10-15 minutes on one problem
   - Partial credit is better than zero

---

## Good Luck!

This walkthrough shows a successful 70-minute test. Your test will have different problems, but the approach remains the same:

1. **Read carefully** (5 min total)
2. **Plan algorithm** (pseudocode)
3. **Code implementation**
4. **Test thoroughly**
5. **Move on and repeat**
