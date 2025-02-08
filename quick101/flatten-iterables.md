# itertools.chain
_This function is great for flattening iterables or combining multiple iterables into a single sequence._

```python
from itertools import chain

# Basic usage - combining lists
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [True, False]

# Chain multiple iterables together
combined = chain(list1, list2, list3)
print(list(combined))  # [1, 2, 3, 'a', 'b', 'c', True, False]

# Practical example - flattening a list of lists
nested_lists = [[1, 2], [3, 4], [5, 6]]
flattened = chain.from_iterable(nested_lists)
print(list(flattened))  # [1, 2, 3, 4, 5, 6]

# Working with different types of iterables
tuple1 = (1, 2)
set1 = {'a', 'b'}
dict1 = {'x': 1, 'y': 2}.keys()

mixed = chain(tuple1, set1, dict1)
print(list(mixed))  # [1, 2, 'a', 'b', 'x', 'y']

# Real-world example - processing multiple files
file_types = [
    ['doc1.txt', 'doc2.txt'],
    ['image1.jpg', 'image2.jpg'],
    ['data1.csv']
]
all_files = chain.from_iterable(file_types) # ['doc1.txt', 'doc2.txt', 'image1.jpg', 'image2.jpg','data1.csv']
for file in all_files:
    print(f"Processing {file}")
```
