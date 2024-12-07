# `@dataclass` decorator 

`@dataclass` is a decorator introduced in Python 3.7 that automatically generates several methods for a class, making it
easier to create classes that are primarily used to store data.

1. Basic Usage:

```python
from dataclasses import dataclass


# Without @dataclass
class FileObjectOld:
    def __init__(self, file_name: str, status: FileStatus):
        self.file_name = file_name
        self.status = status

    def __eq__(self, other):
        if not isinstance(other, FileObjectOld):
            return NotImplemented
        return (self.file_name == other.file_name and
                self.status == other.status)

    def __repr__(self):
        return f"FileObjectOld(file_name={self.file_name!r}, status={self.status!r})"


# With @dataclass - automatically generates __init__, __eq__, __repr__
@dataclass
class FileObject:
    file_name: str
    status: FileStatus = FileStatus.PENDING
```

2. What Methods It Generates:

```python
@dataclass
class FileObject:
    file_name: str
    status: FileStatus = FileStatus.PENDING
    start_time: Optional[datetime] = None

    # Automatically generates:

    # __init__
    # def __init__(self, file_name: str, 
    #              status: FileStatus = FileStatus.PENDING,
    #              start_time: Optional[datetime] = None):
    #     self.file_name = file_name
    #     self.status = status
    #     self.start_time = start_time

    # __repr__
    # def __repr__(self):
    #     return f"FileObject(file_name={self.file_name!r}, status={self.status!r}, start_time={self.start_time!r})"

    # __eq__
    # def __eq__(self, other):
    #     if not isinstance(other, FileObject):
    #         return NotImplemented
    #     return (self.file_name == other.file_name and 
    #             self.status == other.status and 
    #             self.start_time == other.start_time)
```

3. Additional Features and Options:

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)  # Makes instance immutable
class Configuration:
    host: str
    port: int = 8080  # Default value


@dataclass(order=True)  # Adds comparison methods
class Priority:
    priority: int
    name: str = field(compare=False)  # Exclude from comparison


@dataclass
class Stats:
    numbers: List[int] = field(default_factory=list)  # Mutable default
    last_updated: datetime = field(default_factory=datetime.now)  # Dynamic default
```

4. Real-world Example from Our File Monitor:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FileObject:
    # Required field
    file_name: str

    # Optional fields with defaults
    status: FileStatus = FileStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    attempts: int = 0

    # Usage:
    # Simple creation
    file1 = FileObject("data.txt")

    # All fields specified
    file2 = FileObject(
        file_name="report.pdf",
        status=FileStatus.WORKING,
        start_time=datetime.now(),
        attempts=1
    )

    # Automatic string representation
    print(
        file1)  # FileObject(file_name='data.txt', status=FileStatus.PENDING, start_time=None, end_time=None, attempts=0)

    # Automatic equality comparison
    file3 = FileObject("data.txt")
    print(file1 == file3)  # True
```

5. Advanced Features:

```python
from dataclasses import dataclass, field, asdict, astuple


@dataclass
class ProcessingStats:
    file_name: str
    processing_times: List[float] = field(default_factory=list)

    # Custom field with metadata
    retry_count: int = field(
        default=0,
        metadata={'max_retries': 3, 'description': 'Number of retry attempts'}
    )

    # Computed field
    average_time: float = field(init=False)

    def __post_init__(self):
        """Called after __init__"""
        if self.processing_times:
            self.average_time = sum(self.processing_times) / len(self.processing_times)
        else:
            self.average_time = 0.0

    # Convert to dict/tuple
    def to_dict(self):
        return asdict(self)

    def to_tuple(self):
        return astuple(self)
```

6. Benefits of Using @dataclass:

```python
@dataclass
class FileObject:
    file_name: str
    status: FileStatus = FileStatus.PENDING

    # Benefits:

    # 1. Type hints provide better IDE support
    def process(self):
        # IDE knows file_name is str
        return self.file_name.upper()

    # 2. Automatic method generation saves code
    # 3. Immutability option for thread safety
    # 4. Easy conversion to dict/tuple
    # 5. Clear class structure
    # 6. Default value handling
    # 7. Customizable field behavior
```

The `@dataclass` decorator significantly reduces boilerplate code while providing a clear and type-safe way to define
data classes. In our file monitoring system, we use it for `FileObject` because it's primarily a data container that
benefits from automatic method generation and clear attribute definitions.
