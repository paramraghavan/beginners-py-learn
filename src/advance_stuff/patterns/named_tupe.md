NamedTuple is a Python type that creates a tuple subclass with named fields. It combines the immutability of tuples with
the readability of having named attributes.

# Simple usage of tuple

```python
from typing import NamedTuple

# Traditional tuple
file_info_tuple = ('data.txt', 1024, '2024-01-01')
# Access by index (less readable)
print(file_info_tuple[0])  # 'data.txt'


# NamedTuple
class FileInfo(NamedTuple):
    name: str
    size: int
    date: str


# Create instance
file_info = FileInfo('data.txt', 1024, '2024-01-01')
# Access by name (more readable)
print(file_info.name)  # 'data.txt'
```

# Compare with Regular Tuple and Dataclass:

```python
from dataclasses import dataclass
from typing import  NamedTuple
# Three ways to represent the same data:

# Regular Tuple (No names)
regular_tuple = ('data.txt', 1024, '2024-01-01')


# NamedTuple (Immutable, named fields)
class FileInfoNamed(NamedTuple):
    name: str
    size: int
    date: str


named_tuple = FileInfoNamed('data.txt', 1024, '2024-01-01')


# Dataclass (Mutable by default, more features)
@dataclass
class FileInfoData:
    name: str
    size: int
    date: str


data_class = FileInfoData('data.txt', 1024, '2024-01-01')

# Differences:
regular_tuple[0] = 'new.txt'  # TypeError: tuples are immutable
named_tuple.name = 'new.txt'  # TypeError: NamedTuple is immutable
data_class.name = 'new.txt'  # Works: dataclass is mutable by default
```