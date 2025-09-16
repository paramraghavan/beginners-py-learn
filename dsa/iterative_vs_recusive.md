Here's when to choose iterative vs recursive binary search:

## Choose Iterative When:

**Performance is critical**

- Iterative is generally faster due to no function call overhead
- Uses O(1) constant space vs O(log n) for recursive
- No risk of stack overflow, even with very large arrays

**Memory is constrained**

- Each recursive call uses stack space
- For arrays with millions of elements, recursive calls can add up

**Production code**

- More predictable performance characteristics
- Easier to debug and profile
- Industry standard for performance-critical applications

```python
# Iterative - preferred for production
def binary_search_iterative(arr, target):
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
```

## Choose Recursive When:

**Learning/teaching algorithms**

- More intuitive and matches the mathematical definition
- Easier to understand the divide-and-conquer concept
- Cleaner, more readable code

**Problem naturally recursive**

- When binary search is part of a larger recursive algorithm
- Tree traversals that incorporate binary search
- Divide-and-conquer problems

**Code clarity over performance**

- Prototyping or non-performance-critical code
- When the elegance of the solution matters more

```python
# Recursive - cleaner but less efficient
def binary_search_recursive(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1

    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

## Summary:

- **Default choice: Iterative** - better performance, no stack overflow risk
- **Use recursive when**: teaching, prototyping, or when code readability is more important than performance
- **Never use recursive for**: very large datasets or performance-critical systems
