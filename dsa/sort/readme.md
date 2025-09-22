Here’s a simple Python implementation of **Selection Sort**, **Quick Sort**, and **Merge Sort**, along with explanations of their **Big-O complexities**:

---

## 1. Selection Sort

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Assume the min element is at i
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Example
print(selection_sort([64, 25, 12, 22, 11]))
```

```markdown
Start: [64, 25, 12, 22, 11]

Pass 1: min = 11 → swap with 64
[11, 25, 12, 22, 64]

Pass 2: min = 12 → swap with 25
[11, 12, 25, 22, 64]

Pass 3: min = 22 → swap with 25
[11, 12, 22, 25, 64]

Pass 4: min = 25 → already in place
[11, 12, 22, 25, 64]

Sorted: [11, 12, 22, 25, 64]

```


**Complexity**:

* Best case: **O(n²)**
* Average case: **O(n²)**
* Worst case: **O(n²)**
* Space: **O(1)** (in-place)

👉 Reason: Two nested loops, each up to `n`.

---

## 2. Quick Sort

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]   # choose middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Example
print(quicksort([64, 25, 12, 22, 11]))
```

**Complexity**:

* Best case: **O(n log n)**
* Average case: **O(n log n)**
* Worst case: **O(n²)** (if pivot choice is poor, e.g., always smallest/largest element)
* Space: **O(log n)** for recursion (average)

👉 Reason: Partitioning step is `O(n)`, and depth of recursion is `log n` (on average).

```markdown
Start: [64, 25, 12, 22, 11]
Pivot = 12 (middle element)

Partition:
Left = [11]
Middle = [12]
Right = [64, 25, 22]

Now sort Right [64, 25, 22]:
Pivot = 25
  Left = [22]
  Middle = [25]
  Right = [64]

→ [22, 25, 64]

Combine:
Left + Middle + Right = [11, 12] + [22, 25, 64]

Sorted: [11, 12, 22, 25, 64]

```
---

## 3. Merge Sort

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example
print(merge_sort([64, 25, 12, 22, 11]))
```

**Complexity**:

* Best case: **O(n log n)**
* Average case: **O(n log n)**
* Worst case: **O(n log n)**
* Space: **O(n)** (needs extra arrays for merging)

👉 Reason: The array is divided `log n` times, and each merge step takes `O(n)`.

```markdown
Start: [64, 25, 12, 22, 11]

Split → [64, 25] + [12, 22, 11]

Left half [64, 25]:
Split → [64] + [25]
Merge → [25, 64]

Right half [12, 22, 11]:
Split → [12] + [22, 11]
        [22, 11] → [22] + [11]
                   Merge → [11, 22]
Merge → [12, 11, 22] → [11, 12, 22]

Final merge:
[25, 64] + [11, 12, 22]
→ Compare step by step:
  25 vs 11 → [11]
  25 vs 12 → [11, 12]
  25 vs 22 → [11, 12, 22]
  (Left left: [25, 64]) → add them
  Final → [11, 12, 22, 25, 64]

```
---

✅ **Summary Table**

| Algorithm      | Best       | Average    | Worst      | Space    |
| -------------- | ---------- | ---------- | ---------- | -------- |
| Selection Sort | O(n²)      | O(n²)      | O(n²)      | O(1)     |
| Quick Sort     | O(n log n) | O(n log n) | O(n²)      | O(log n) |
| Merge Sort     | O(n log n) | O(n log n) | O(n log n) | O(n)     |

