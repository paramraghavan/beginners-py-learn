# 10 Python Features You Should Be Using

Based on the video from ArjanCodes, here are 10 Python features with comprehensive examples and practical use cases.

## 1. Caching with `@cache`

Located in the `functools` module, this decorator automatically stores the results of function calls, perfect for expensive operations.

### Basic Example
```python
from functools import cache

@cache
def total_from_file(filename):
    print("Reading file...")
    with open(filename) as f:
        return sum(int(line) for line in f)

# First call - reads the file
result1 = total_from_file("data.txt")  # Prints: "Reading file..."

# Second call - uses cached result
result2 = total_from_file("data.txt")  # No print - uses cache!
```

### Practical Example: Fibonacci Sequence
```python
from functools import cache
import time

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Without cache: exponential time complexity O(2^n)
# With cache: linear time complexity O(n)

start = time.time()
print(fibonacci(100))  # Returns instantly with cache
print(f"Time: {time.time() - start:.4f}s")
```

### LRU Cache with Size Limit
```python
from functools import lru_cache

@lru_cache(maxsize=128)  # Keep only 128 most recent results
def fetch_user_data(user_id: int):
    # Expensive API call or database query
    return {"id": user_id, "name": f"User{user_id}"}
```

### Use Cases
- File parsing operations
- API calls with same parameters
- Recursive algorithms (Fibonacci, factorial)
- Database queries with repeated parameters

---

## 2. Structural Subtyping with `Protocol`

`Protocol` allows duck typing with type hints - if it walks like a duck and quacks like a duck, it's a duck!

### Basic Example
```python
from typing import Protocol

class RateFetcher(Protocol):
    def get_rate(self, currency: str) -> float:
        ...

def convert_sale(fetcher: RateFetcher, amount: float, currency: str) -> float:
    rate = fetcher.get_rate(currency)
    return amount * rate
```

### Practical Example: Payment Processing
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class PaymentProcessor(Protocol):
    def process_payment(self, amount: float, currency: str) -> bool:
        ...

    def refund(self, transaction_id: str) -> bool:
        ...

# Implementation 1 - doesn't inherit from Protocol
class StripeProcessor:
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Processing ${amount} via Stripe")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding transaction {transaction_id}")
        return True

# Implementation 2
class PayPalProcessor:
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Processing ${amount} via PayPal")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding via PayPal: {transaction_id}")
        return True

def checkout(processor: PaymentProcessor, amount: float):
    if processor.process_payment(amount, "USD"):
        print("Payment successful!")

# Both work without explicit inheritance!
checkout(StripeProcessor(), 99.99)
checkout(PayPalProcessor(), 149.99)
```

### File-like Object Protocol
```python
from typing import Protocol

class FileLike(Protocol):
    def read(self, size: int = -1) -> str:
        ...

    def write(self, data: str) -> int:
        ...

def process_file(file: FileLike):
    content = file.read()
    # Process content
    file.write(content.upper())

# Works with real files, StringIO, custom classes, etc.
from io import StringIO

buffer = StringIO("hello world")
process_file(buffer)  # Type checker happy!
```

---

## 3. Data Class `replace`

Create modified copies of immutable dataclasses without mutation.

### Basic Example
```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Sale:
    amount: float
    currency: str
    converted_value: float = 0.0

original_sale = Sale(100.0, "EUR")
new_sale = replace(original_sale, converted_value=120.0)

print(original_sale)  # Sale(amount=100.0, currency='EUR', converted_value=0.0)
print(new_sale)       # Sale(amount=100.0, currency='EUR', converted_value=120.0)
```

### Practical Example: User Settings
```python
from dataclasses import dataclass, replace
from datetime import datetime

@dataclass(frozen=True)
class UserSettings:
    user_id: int
    theme: str
    notifications: bool
    language: str
    last_updated: datetime

def update_theme(settings: UserSettings, new_theme: str) -> UserSettings:
    return replace(
        settings,
        theme=new_theme,
        last_updated=datetime.now()
    )

def toggle_notifications(settings: UserSettings) -> UserSettings:
    return replace(
        settings,
        notifications=not settings.notifications,
        last_updated=datetime.now()
    )

# Usage
user_settings = UserSettings(
    user_id=123,
    theme="dark",
    notifications=True,
    language="en",
    last_updated=datetime.now()
)

# Create updated versions
new_settings = update_theme(user_settings, "light")
newer_settings = toggle_notifications(new_settings)
```

### Configuration Management
```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    ssl_enabled: bool = False
    timeout: int = 30

# Base config
dev_config = DatabaseConfig("localhost", 5432, "dev_db", "dev_user")

# Production config - just override what's different
prod_config = replace(
    dev_config,
    host="prod.example.com",
    ssl_enabled=True,
    timeout=60
)
```

---

## 4. `itertools.pairwise`

Iterate over overlapping pairs - perfect for calculating differences or analyzing sequences.

### Basic Example
```python
from itertools import pairwise

numbers = [10, 20, 35, 50]
deltas = [b - a for a, b in pairwise(numbers)]
print(deltas)  # [10, 15, 15]
```

### Practical Example: Time Series Analysis
```python
from itertools import pairwise
from datetime import datetime, timedelta

# Stock prices over time
prices = [
    (datetime(2024, 1, 1), 100.0),
    (datetime(2024, 1, 2), 105.0),
    (datetime(2024, 1, 3), 103.0),
    (datetime(2024, 1, 4), 110.0),
]

# Calculate daily changes
for (date1, price1), (date2, price2) in pairwise(prices):
    change = price2 - price1
    percent = (change / price1) * 100
    print(f"{date2.date()}: ${price2} ({percent:+.2f}%)")

# Output:
# 2024-01-02: $105.0 (+5.00%)
# 2024-01-03: $103.0 (-1.90%)
# 2024-01-04: $110.0 (+6.80%)
```

### Path Smoothness Validation
```python
from itertools import pairwise

def validate_smooth_path(points: list[tuple[float, float]]) -> bool:
    """Check if points form a smooth path (no sharp angles)"""
    max_angle_change = 45  # degrees

    for (x1, y1), (x2, y2) in pairwise(points):
        distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if distance > 100:  # Too far apart
            return False

    return True

path = [(0, 0), (10, 10), (20, 15), (30, 20)]
print(validate_smooth_path(path))
```

### Detecting Duplicates in Sorted Data
```python
from itertools import pairwise

def find_consecutive_duplicates(data: list) -> list:
    """Find items that appear consecutively"""
    return [item for item, next_item in pairwise(data) if item == next_item]

sorted_data = [1, 1, 2, 3, 3, 3, 4, 5, 5]
duplicates = find_consecutive_duplicates(sorted_data)
print(duplicates)  # [1, 3, 3, 5]
```

---

## 5. The Walrus Operator (`:=`)

Assign and use a value in the same expression - cleaner code with fewer repetitions.

### Basic Example
```python
# Without walrus
file = open("data.txt")
line = file.readline()
while line:
    process(line)
    line = file.readline()

# With walrus
file = open("data.txt")
while (line := file.readline()):
    process(line)
```

### Practical Example: Data Validation
```python
def process_user_input(data: dict) -> str:
    # Validate and use in one step
    if (username := data.get("username")) and len(username) > 3:
        return f"Welcome, {username}!"

    if (age := data.get("age")) and age >= 18:
        return "You are an adult"

    return "Invalid data"

print(process_user_input({"username": "john_doe", "age": 25}))
```

### List Comprehension with Expensive Operations
```python
# Without walrus - compute_value called twice!
results = [compute_value(x) for x in data if compute_value(x) > 10]

# With walrus - compute_value called once
results = [value for x in data if (value := compute_value(x)) > 10]
```

### Practical Example: Data Processing Pipeline
```python
import re

def extract_and_validate_emails(text: str) -> list[str]:
    """Extract valid emails from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return [
        email.lower()
        for line in text.split('\n')
        if (match := re.search(pattern, line))
        for email in [match.group()]
        if email.endswith(('.com', '.org', '.net'))
    ]

text = """
Contact us at support@example.com
Sales: sales@company.org
Invalid: notanemail@
Admin: admin@test.co.uk
"""

emails = extract_and_validate_emails(text)
print(emails)  # ['support@example.com', 'sales@company.org']
```

### Regex Matching
```python
import re

def parse_log_line(line: str) -> dict | None:
    pattern = r'\[(\d+)\] (\w+): (.+)'

    if (match := re.match(pattern, line)):
        return {
            'id': match.group(1),
            'level': match.group(2),
            'message': match.group(3)
        }
    return None

log = "[123] ERROR: Connection failed"
if parsed := parse_log_line(log):
    print(f"Level: {parsed['level']}, Message: {parsed['message']}")
```

---

## 6. `pathlib` for File Handling

Object-oriented file system paths - cleaner and more intuitive than `os.path`.

### Basic Example
```python
from pathlib import Path

directory = Path("data/")
for path in directory.glob("*.json"):
    data = path.read_text()
    print(f"File: {path.stem}")  # Filename without extension
```

### Practical Example: Project File Management
```python
from pathlib import Path
import json

class ProjectManager:
    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.src = self.root / "src"
        self.tests = self.root / "tests"
        self.config = self.root / "config.json"

    def setup_project(self):
        """Create project structure"""
        self.src.mkdir(parents=True, exist_ok=True)
        self.tests.mkdir(parents=True, exist_ok=True)

        # Create config file
        config_data = {
            "name": self.root.name,
            "version": "1.0.0"
        }
        self.config.write_text(json.dumps(config_data, indent=2))

    def get_python_files(self) -> list[Path]:
        """Find all Python files"""
        return list(self.src.rglob("*.py"))

    def get_file_size_mb(self, filepath: Path) -> float:
        """Get file size in MB"""
        return filepath.stat().st_size / (1024 * 1024)

# Usage
pm = ProjectManager("my_project")
pm.setup_project()

for py_file in pm.get_python_files():
    size = pm.get_file_size_mb(py_file)
    print(f"{py_file.relative_to(pm.root)}: {size:.2f} MB")
```

### Cross-Platform Path Operations
```python
from pathlib import Path

# Works on Windows, Linux, and macOS
project = Path.home() / "projects" / "myapp"
config_file = project / "config" / "settings.json"

# Check if file exists
if config_file.exists():
    print(f"Config found at: {config_file}")

# Get absolute path
print(f"Absolute: {config_file.resolve()}")

# Get parent directory
print(f"Parent: {config_file.parent}")

# Change extension
backup_file = config_file.with_suffix(".bak")
```

### File Operations
```python
from pathlib import Path
import shutil

def backup_files(source_dir: str, backup_dir: str, pattern: str = "*.txt"):
    """Backup files matching pattern"""
    source = Path(source_dir)
    backup = Path(backup_dir)

    backup.mkdir(parents=True, exist_ok=True)

    for file in source.glob(pattern):
        if file.is_file():
            dest = backup / file.name
            shutil.copy2(file, dest)
            print(f"Backed up: {file.name}")

# Usage
backup_files("documents", "backups/2024-03-07", "*.txt")
```

### Reading and Writing Files
```python
from pathlib import Path

# Read entire file
content = Path("data.txt").read_text()

# Read as bytes
binary_data = Path("image.png").read_bytes()

# Write text
Path("output.txt").write_text("Hello, World!")

# Write bytes
Path("output.bin").write_bytes(b'\x00\x01\x02')

# Iterate over lines
for line in Path("data.txt").read_text().splitlines():
    print(line)
```

---

## 7. Exception Suppression with `suppress`

Cleanly ignore specific exceptions - more readable than try-except-pass.

### Basic Example
```python
from contextlib import suppress

# Old way
try:
    Path("temp.txt").unlink()
except FileNotFoundError:
    pass

# New way
with suppress(FileNotFoundError):
    Path("temp.txt").unlink()
```

### Practical Example: Cleanup Operations
```python
from contextlib import suppress
from pathlib import Path

def cleanup_temp_files(temp_dir: Path):
    """Remove temporary files, ignoring missing files"""
    temp_files = [
        "cache.tmp",
        "log.tmp",
        "session.tmp"
    ]

    for filename in temp_files:
        with suppress(FileNotFoundError):
            (temp_dir / filename).unlink()
            print(f"Deleted {filename}")

# Usage
cleanup_temp_files(Path("temp"))
```

### Multiple Exceptions
```python
from contextlib import suppress

def safe_convert(value: str) -> int | None:
    """Try to convert to int, return None if fails"""
    with suppress(ValueError, TypeError):
        return int(value)
    return None

print(safe_convert("123"))     # 123
print(safe_convert("abc"))     # None
print(safe_convert(None))      # None
```

### Dictionary Operations
```python
from contextlib import suppress

def remove_keys(data: dict, keys: list[str]):
    """Remove keys from dict, ignore if missing"""
    for key in keys:
        with suppress(KeyError):
            del data[key]

user_data = {"name": "John", "age": 30, "email": "john@example.com"}
remove_keys(user_data, ["age", "phone", "address"])  # No error for missing keys
print(user_data)  # {"name": "John", "email": "john@example.com"}
```

### Resource Cleanup
```python
from contextlib import suppress
import os

def safe_cleanup(resource_path: str):
    """Cleanup resource, ignoring common errors"""
    with suppress(FileNotFoundError, PermissionError, OSError):
        os.remove(resource_path)
        print(f"Removed {resource_path}")
```

---

## 8. `contextvars` for Async Context

Manage context-local state in async code - like thread-local storage for async tasks.

### Basic Example
```python
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id", default="unknown")

async def handle_request():
    request_id.set("REQ-123")
    await process_user()

async def process_user():
    # Can access request_id without passing it
    print(f"Processing request: {request_id.get()}")
```

> ContextVar is thread-safe and async-safe, and that is exactly why it exists. A regular dict is not a safe replacement for the same purpose.

**ContextVar stores context-local state.**
That means the value is isolated per:
* async task
* thread
* context propagation
So different requests running concurrently do not overwrite each other.

```python
from contextvars import ContextVar
import asyncio

request_id = ContextVar("request_id", default="unknown")

async def worker(name, rid):
    request_id.set(rid)
    await asyncio.sleep(1)
    print(name, request_id.get())

async def main():
    await asyncio.gather(
        worker("task1", "REQ-1"),
        worker("task2", "REQ-2")
    )

asyncio.run(main())

#output
# task1 REQ-1
# task2 REQ-2
```


### Practical Example: Request Tracing
```python
import asyncio
from contextvars import ContextVar
from datetime import datetime
import random

# Context variables
request_id_var: ContextVar[str] = ContextVar("request_id")
user_id_var: ContextVar[int | None] = ContextVar("user_id", default=None)

def log(message: str):
    """Log with context"""
    req_id = request_id_var.get()
    user_id = user_id_var.get()
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{req_id}] [User:{user_id}] {message}")

async def authenticate(user_id: int):
    """Simulate authentication"""
    await asyncio.sleep(0.1)
    user_id_var.set(user_id)
    log(f"User authenticated")

async def fetch_data(data_type: str):
    """Simulate data fetching"""
    await asyncio.sleep(0.2)
    log(f"Fetched {data_type}")
    return f"{data_type}_data"

async def handle_api_request(request_id: str, user_id: int):
    """Handle a single API request"""
    # Set context for this request
    request_id_var.set(request_id)

    log("Request started")

    # Authenticate
    await authenticate(user_id)

    # Fetch data
    profile = await fetch_data("profile")
    settings = await fetch_data("settings")

    log("Request completed")
    return {"profile": profile, "settings": settings}

async def main():
    """Simulate multiple concurrent requests"""
    tasks = [
        handle_api_request(f"REQ-{i}", user_id=100 + i)
        for i in range(3)
    ]

    results = await asyncio.gather(*tasks)
    return results

# Run
asyncio.run(main())
```

### Practical Example: Database Transaction Context
```python
import asyncio
from contextvars import ContextVar
from typing import Optional

# Context for current database transaction
db_transaction: ContextVar[Optional['Transaction']] = ContextVar('db_transaction', default=None)

class Transaction:
    def __init__(self, transaction_id: str):
        self.id = transaction_id
        self.operations = []

    def add_operation(self, operation: str):
        self.operations.append(operation)

    async def commit(self):
        print(f"Committing transaction {self.id}: {self.operations}")
        await asyncio.sleep(0.1)

    async def rollback(self):
        print(f"Rolling back transaction {self.id}")
        await asyncio.sleep(0.1)

async def execute_query(query: str):
    """Execute query within current transaction context"""
    txn = db_transaction.get()
    if txn:
        txn.add_operation(query)
        print(f"[{txn.id}] Executing: {query}")
    else:
        print(f"Executing without transaction: {query}")

async def with_transaction(func):
    """Decorator to run function in a transaction"""
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        txn = Transaction(f"TXN-{random.randint(1000, 9999)}")
        db_transaction.set(txn)

        try:
            result = await func(*args, **kwargs)
            await txn.commit()
            return result
        except Exception as e:
            await txn.rollback()
            raise
        finally:
            db_transaction.set(None)

    return wrapper

@with_transaction
async def create_user(username: str, email: str):
    """Create user with multiple operations"""
    await execute_query(f"INSERT INTO users (username) VALUES ('{username}')")
    await execute_query(f"INSERT INTO emails (email) VALUES ('{email}')")
    await execute_query(f"INSERT INTO audit_log (action) VALUES ('user_created')")
    return {"username": username, "email": email}

async def main():
    # Each call runs in its own transaction context
    user1 = asyncio.create_task(create_user("alice", "alice@example.com"))
    user2 = asyncio.create_task(create_user("bob", "bob@example.com"))

    await asyncio.gather(user1, user2)

asyncio.run(main())
```

---

## 9. Structural Pattern Matching with Guards

Pattern matching with conditions - more declarative than if-elif chains.

### Basic Example
```python
match amount:
    case x if x < 0:
        return "invalid"
    case 0:
        return "zero"
    case x if x > 10000:
        return "large"
    case _:
        return "normal"
```

### Practical Example: HTTP Response Handling
```python
def handle_http_response(status_code: int, body: dict):
    match status_code:
        case 200:
            return {"success": True, "data": body}

        case 201:
            return {"success": True, "created": True, "data": body}

        case code if 400 <= code < 500:
            return {"success": False, "error": "Client error", "code": code}

        case code if 500 <= code < 600:
            return {"success": False, "error": "Server error", "code": code}

        case _:
            return {"success": False, "error": "Unknown status", "code": status_code}

# Usage
print(handle_http_response(200, {"user": "John"}))
print(handle_http_response(404, {"message": "Not found"}))
print(handle_http_response(500, {"message": "Internal error"}))
```

### Parsing Structured Data
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    width: float
    height: float

def calculate_area(shape):
    match shape:
        case Circle(radius=r):
            return 3.14159 * r * r

        case Rectangle(width=w, height=h):
            return w * h

        case Circle(center=Point(x=0, y=0), radius=r) if r > 100:
            return f"Large circle at origin: {3.14159 * r * r}"

        case _:
            return "Unknown shape"

# Usage
circle = Circle(Point(0, 0), 5)
rect = Rectangle(Point(0, 0), 10, 20)

print(calculate_area(circle))  # 78.53975
print(calculate_area(rect))    # 200
```

### Command Processing
```python
def process_command(command: str, args: list):
    match command.split():
        case ["quit"] | ["exit"]:
            return "Goodbye!"

        case ["help", topic] if topic in ["commands", "usage"]:
            return f"Help for: {topic}"

        case ["add", *numbers] if all(n.isdigit() for n in numbers):
            return sum(int(n) for n in numbers)

        case ["echo", *words]:
            return " ".join(words)

        case ["search", query] if len(query) >= 3:
            return f"Searching for: {query}"

        case _:
            return "Unknown command"

# Usage
print(process_command("add 1 2 3 4", []))      # 10
print(process_command("echo hello world", [])) # hello world
print(process_command("search python", []))    # Searching for: python
```

### API Request Validation
```python
def validate_api_request(request: dict) -> dict:
    match request:
        case {"method": "GET", "path": path, "auth": token} if token:
            return {"valid": True, "type": "authenticated_get", "path": path}

        case {"method": "POST", "path": "/api/users", "body": body} if "email" in body:
            return {"valid": True, "type": "user_creation", "email": body["email"]}

        case {"method": method, "path": path} if method in ["GET", "POST", "PUT", "DELETE"]:
            return {"valid": True, "type": "standard_request", "method": method}

        case {"method": method}:
            return {"valid": False, "error": f"Unsupported method: {method}"}

        case _:
            return {"valid": False, "error": "Invalid request format"}

# Usage
request1 = {"method": "GET", "path": "/api/data", "auth": "token123"}
request2 = {"method": "POST", "path": "/api/users", "body": {"email": "user@example.com"}}

print(validate_api_request(request1))
print(validate_api_request(request2))
```

---

## 10. `ExitStack` for Dynamic Context Managers

Manage multiple context managers dynamically - perfect when you don't know how many files you'll need to open.

### Basic Example
```python
from contextlib import ExitStack
from pathlib import Path

with ExitStack() as stack:
    files = [stack.enter_context(open(p)) for p in paths]
    # All files are automatically closed when exiting
    for f in files:
        print(f.read())
```

### Practical Example: Batch File Processing
```python
from contextlib import ExitStack
from pathlib import Path
import json

def merge_json_files(input_dir: Path, output_file: Path):
    """Merge multiple JSON files into one"""
    json_files = list(input_dir.glob("*.json"))

    merged_data = {}

    with ExitStack() as stack:
        # Open all input files
        opened_files = [
            stack.enter_context(open(f, 'r'))
            for f in json_files
        ]

        # Read and merge all data
        for file in opened_files:
            data = json.load(file)
            merged_data.update(data)

        # Open output file and write merged data
        output = stack.enter_context(open(output_file, 'w'))
        json.dump(merged_data, output, indent=2)

    print(f"Merged {len(json_files)} files into {output_file}")

# Usage
merge_json_files(Path("data/configs"), Path("data/merged_config.json"))
```

### Database Connections Pool
```python
from contextlib import ExitStack
from typing import Protocol

class DatabaseConnection(Protocol):
    def execute(self, query: str): ...
    def close(self): ...

class Connection:
    def __init__(self, conn_id: int):
        self.id = conn_id
        print(f"Opening connection {conn_id}")

    def execute(self, query: str):
        print(f"[Conn {self.id}] Executing: {query}")

    def close(self):
        print(f"Closing connection {self.id}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

def batch_execute_queries(queries: list[str], num_connections: int = 3):
    """Execute queries using a pool of connections"""
    with ExitStack() as stack:
        # Create connection pool
        connections = [
            stack.enter_context(Connection(i))
            for i in range(num_connections)
        ]

        # Distribute queries across connections
        for i, query in enumerate(queries):
            conn = connections[i % num_connections]
            conn.execute(query)

# Usage
queries = [
    "SELECT * FROM users",
    "SELECT * FROM orders",
    "SELECT * FROM products",
    "SELECT * FROM reviews",
]

batch_execute_queries(queries, num_connections=2)
```

### Resource Manager with Conditional Cleanup
```python
from contextlib import ExitStack, contextmanager
from pathlib import Path
import tempfile
import shutil

@contextmanager
def temp_directory():
    """Create a temporary directory"""
    temp_dir = tempfile.mkdtemp()
    try:
        yield Path(temp_dir)
    finally:
        shutil.rmtree(temp_dir)
        print(f"Cleaned up {temp_dir}")

def process_with_resources(use_temp: bool = False, num_files: int = 2):
    """Process with conditional resources"""
    with ExitStack() as stack:
        # Conditionally create temp directory
        if use_temp:
            work_dir = stack.enter_context(temp_directory())
        else:
            work_dir = Path(".")

        # Open multiple files
        files = []
        for i in range(num_files):
            file_path = work_dir / f"file_{i}.txt"
            f = stack.enter_context(open(file_path, 'w'))
            files.append(f)
            f.write(f"Content for file {i}")

        print(f"Processed {num_files} files in {work_dir}")

# Usage
process_with_resources(use_temp=True, num_files=3)
```

### Nested Transaction Management
```python
from contextlib import ExitStack

class Transaction:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f"BEGIN {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"ROLLBACK {self.name}")
        else:
            print(f"COMMIT {self.name}")
        return False

def nested_transaction_example():
    """Example with multiple nested transactions"""
    transaction_names = ["outer", "middle", "inner"]

    with ExitStack() as stack:
        transactions = [
            stack.enter_context(Transaction(name))
            for name in transaction_names
        ]

        print("Doing work in nested transactions...")
        # All transactions will be properly committed/rolled back

nested_transaction_example()
```

---

## Summary

These 10 features can significantly improve your Python code:

1. **`@cache`** - Eliminate redundant computation
2. **`Protocol`** - Type-safe duck typing
3. **`replace`** - Immutable dataclass updates
4. **`pairwise`** - Elegant sequence pair iteration
5. **`:=` (walrus)** - Cleaner assignment expressions
6. **`pathlib`** - Modern file path handling
7. **`suppress`** - Clean exception ignoring
8. **`contextvars`** - Async-safe context state
9. **Pattern matching** - Declarative conditional logic
10. **`ExitStack`** - Dynamic resource management

**Original Video:** [10 Python Features You're Not Using (But Really Should)](http://www.youtube.com/watch?v=cXl-AUXHHZY)
