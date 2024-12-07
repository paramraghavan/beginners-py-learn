# Enum

Enum is a class in Python that creates a set of named constants, where each constant is unique and immutable

The benefits of using Enum are:

1. Type safety - can't use invalid status values
2. Self-documenting code - clear what states are possible
3. IDE support - autocomplete shows valid options
4. Immutable - status values can't be changed accidentally
5. Easy comparison and matching
6. Clear intent in code


1. Basic Enum Usage:

```python
from enum import Enum


class FileStatus(Enum):
    PENDING = "PENDING"
    WORKING = "WORKING"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"


# Usage
status = FileStatus.PENDING
print(status)  # FileStatus.PENDING
print(status.value)  # "PENDING"
print(status.name)  # "PENDING"
```

2. Why Use Enum Instead of Constants:

```python
# Bad: Using plain strings
status = "PENDING"  # Could accidentally use "pending" or "Pending"
status = "TYPO_IN_STATUS"  # No error catching


# Bad: Using class constants
class FileStatus:
    PENDING = "PENDING"
    WORKING = "WORKING"
    # Can be modified: FileStatus.PENDING = "Something else"


# Good: Using Enum
class FileStatus(Enum):
    PENDING = "PENDING"
    WORKING = "WORKING"

    # Cannot be modified
    # FileStatus.PENDING = "Something else"  # This raises an error
    # Only valid values can be used
```

3. Common Use Cases for Enums:

```python
# 1. Status/State Management
class OrderStatus(Enum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


# 2. Configuration Options
class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


# 3. Command Types
class CommandType(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


# 4. Days of Week
class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    # etc...
```

4. Using Enums in Functions:

```python
def process_file(file_name: str) -> FileStatus:
    try:
        # Process the file
        return FileStatus.COMPLETE
    except Exception:
        return FileStatus.FAIL


def handle_status(status: FileStatus):
    match status:
        case FileStatus.COMPLETE:
            print("File processed successfully")
        case FileStatus.FAIL:
            print("File processing failed")
        case FileStatus.PENDING:
            print("File is waiting to be processed")
```

5. Advanced Enum Features:

```python
from enum import Enum, auto


# Auto-numbering
class Priority(Enum):
    LOW = auto()  # 1
    MEDIUM = auto()  # 2
    HIGH = auto()  # 3


# Enum with methods
class FileStatus(Enum):
    PENDING = "PENDING"
    WORKING = "WORKING"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"

    def is_terminal_state(self) -> bool:
        return self in (FileStatus.COMPLETE, FileStatus.FAIL)

    def can_retry(self) -> bool:
        return self == FileStatus.FAIL
```

6. When to Use Enums:

```python
# 1. When you need a fixed set of constants:
class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    # etc...


# 2. When you want to prevent invalid values:
def set_status(status: FileStatus):
    # Can only use valid FileStatus values
    pass


# 3. When you need to group related constants:
class HttpStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    SERVER_ERROR = 500


# 4. When you need to compare states:
if file.status == FileStatus.COMPLETE:
    process_complete_file(file)
```

7. Real-world Example from Our File Monitor[file_monitor.py](../../exercises/exercise29/file_monitor.py):

```python
class FileStatus(Enum):
    PENDING = "PENDING"
    WORKING = "WORKING"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"


class FileObject:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.status = FileStatus.PENDING  # Initial state

    def update_status(self, new_status: FileStatus):
        self.status = new_status

        if self.status == FileStatus.FAIL:
            # Handle failure
            alert_admin()
        elif self.status == FileStatus.COMPLETE:
            # Handle completion
            cleanup_resources()
```

