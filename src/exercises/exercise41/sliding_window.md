```python
from collections import deque


def sliding_window(iterable, n):
    if n < 1:
        raise ValueError("Window size must be at least 1")

    window = deque(maxlen=n)

    for item in iterable:
        window.append(item)
        if len(window) == n:
            yield tuple(window)


numbers = [1, 2, 3, 4, 5]

print(list(sliding_window(numbers, 2)))
# [(1, 2), (2, 3), (3, 4), (4, 5)]

print(list(sliding_window(numbers, 3)))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

print(list(sliding_window(numbers, 4)))
# [(1, 2, 3, 4), (2, 3, 4, 5)]
```

```python
def sliding_window(iterable, n):
    if n < 1:
        raise ValueError("Window size must be at least 1")
    window = []
    
    count =1
    for item in range(0,len(iterable),n):
        print(iterable[item:n])
        
        
            

```



For [1, 2, 3, 4, 5], this happens:

```markdown
| Incoming item | Window after `append()` | What gets yielded |
| --- | --- | --- |
| `1` | `[1]` | Nothing—too short |
| `2` | `[1, 2]` | Nothing—too short |
| `3` | `[1, 2, 3]` | `(1, 2, 3)` |
| `4` | `[2, 3, 4]`—drops `1` | `(2, 3, 4)` |
| `5` | `[3, 4, 5]`—drops `2` | `(3, 4, 5)` |
```