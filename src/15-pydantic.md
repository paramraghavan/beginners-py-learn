# Pydantic: Data Validation and Settings Management

Pydantic is a Python library for data validation and settings management using Python type annotations. It enforces type hints at runtime and provides user-friendly error messages.

## Table of Contents
1. [Installation](#installation)
2. [Basic Models](#basic-models)
3. [Field Validation](#field-validation)
4. [Custom Validators](#custom-validators)
5. [Advanced Features](#advanced-features)
6. [Real-World Examples](#real-world-examples)

---

## Installation

```bash
pip install pydantic
```

**Versions:**
- **Pydantic v1:** `pip install "pydantic<2"`
- **Pydantic v2:** `pip install pydantic>=2.0` (latest with major improvements)

---

## Basic Models

### Simple Model Definition

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True

# Creating a valid instance
user = User(id=1, name="John Doe", email="john@example.com", age=30)
print(user)
# Output: id=1 name='John Doe' email='john@example.com' age=30 is_active=True

# Accessing fields
print(user.id)           # 1
print(user.name)         # John Doe
print(user.dict())       # {'id': 1, 'name': 'John Doe', ...}
print(user.model_dump()) # Pydantic v2 method
```

### Type Enforcement

```python
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float
    quantity: int

# Valid
product = Product(name="Laptop", price=999.99, quantity=5)

# Invalid - ValidationError raised
try:
    product = Product(name="Laptop", price="invalid", quantity=5)
except ValidationError as e:
    print(e)
    # Shows which field failed and why
```

---

## Field Validation

### Basic Field Constraints

```python
from pydantic import BaseModel, Field, field_validator

class Article(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    tags: list[str] = Field(default=[], max_items=5)
    views: int = Field(default=0, ge=0)  # ge = greater than or equal

article = Article(title="Python Tips", content="Here are useful tips")
print(article)

# Invalid
try:
    bad = Article(title="Bad", content="short")
except ValidationError as e:
    print(e.errors())
```

### Common Field Constraints

| Constraint | Use Case | Example |
|-----------|----------|---------|
| `min_length` | Minimum string/list length | `Field(..., min_length=1)` |
| `max_length` | Maximum string/list length | `Field(..., max_length=100)` |
| `pattern` | Regex validation | `Field(..., pattern=r"^\d{3}-\d{3}-\d{4}$")` |
| `ge`, `le` | Greater/less than or equal | `Field(..., ge=0, le=100)` |
| `gt`, `lt` | Greater/less than | `Field(..., gt=0)` |
| `multiple_of` | Must be multiple of value | `Field(..., multiple_of=5)` |
| `max_items` | Maximum items in list | `Field(..., max_items=10)` |
| `min_items` | Minimum items in list | `Field(..., min_items=1)` |

---

## Custom Validators

### Field-Level Validators

```python
from pydantic import BaseModel, field_validator, ValidationInfo

class User(BaseModel):
    username: str
    email: str
    age: int

    @field_validator('username')
    @classmethod
    def username_lowercase(cls, v):
        """Convert username to lowercase"""
        return v.lower()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        """Age must be between 0 and 150"""
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

# Valid
user = User(username="JohnDoe", email="john@example.com", age=30)
print(user.username)  # johndoe (converted to lowercase)

# Invalid
try:
    user = User(username="Test", email="invalid-email", age=200)
except ValidationError as e:
    print(e.errors())
```

### Model-Level Validators

```python
from pydantic import BaseModel, model_validator

class Account(BaseModel):
    username: str
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def validate_passwords_match(self):
        """Validate at model level after all fields are parsed"""
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self

# Valid
account = Account(
    username="john",
    password="SecurePass123",
    password_confirm="SecurePass123"
)

# Invalid
try:
    account = Account(
        username="john",
        password="SecurePass123",
        password_confirm="DifferentPass123"
    )
except ValidationError as e:
    print(e.errors())
```

### Validator with Multiple Fields

```python
from pydantic import BaseModel, field_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, v, info: ValidationInfo):
        """Validate that end_date is after start_date"""
        if 'start_date' in info.data:
            if v <= info.data['start_date']:
                raise ValueError('end_date must be after start_date')
        return v

# Valid
dr = DateRange(start_date="2024-01-01", end_date="2024-12-31")

# Invalid
try:
    dr = DateRange(start_date="2024-12-31", end_date="2024-01-01")
except ValidationError as e:
    print(e.errors())
```

---

## Advanced Features

### Nested Models

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class Contact(BaseModel):
    name: str
    email: str
    phone: str

class Person(BaseModel):
    name: str
    address: Address
    contacts: List[Contact]

# Creating with nested data
person = Person(
    name="John Doe",
    address={
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "zip_code": "10001"
    },
    contacts=[
        {"name": "Mom", "email": "mom@example.com", "phone": "555-1234"},
        {"name": "Work", "email": "work@example.com", "phone": "555-5678"}
    ]
)

print(person.address.city)  # New York
print(person.contacts[0].name)  # Mom
print(person.model_dump())  # Full nested dictionary
```

### Computed Fields (Pydantic v2)

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        """Calculate area on the fly"""
        return self.width * self.height

    @computed_field
    @property
    def perimeter(self) -> float:
        """Calculate perimeter on the fly"""
        return 2 * (self.width + self.height)

rect = Rectangle(width=5, height=10)
print(rect.area)        # 50
print(rect.perimeter)   # 30
print(rect.model_dump())  # Includes computed fields
```

### Config and Settings

```python
from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,    # Validate when assigning to fields
        use_enum_values=True,        # Use enum values, not names
        populate_by_name=True,       # Accept both field name and alias
    )

    name: str
    price: float
    quantity: int = 0

# Whitespace automatically stripped
product = Product(name="  Laptop  ", price=999.99)
print(product.name)  # "Laptop" (stripped)

# Validation on assignment
product.quantity = "10"  # Automatically converted to int
print(product.quantity)  # 10
```

### Aliases

```python
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    user_id: int = Field(..., alias='userId')
    first_name: str = Field(..., alias='firstName')
    last_name: str = Field(..., alias='lastName')

# Accept data with aliases (from API)
data = {
    'userId': 123,
    'firstName': 'John',
    'lastName': 'Doe'
}
response = APIResponse(**data)
print(response.user_id)  # 123

# Can access with field name or alias
print(response.model_dump())  # Uses field names
print(response.model_dump(by_alias=True))  # Uses aliases
```

### Type Coercion

```python
from pydantic import BaseModel

class Data(BaseModel):
    count: int
    price: float
    active: bool
    items: list[str]

# Pydantic automatically coerces types
data = Data(
    count="42",           # String → int
    price="19.99",        # String → float
    active="yes",         # String → bool (non-empty is True)
    items=("apple", "banana")  # Tuple → list
)

print(data.count)     # 42 (int)
print(data.price)     # 19.99 (float)
print(data.active)    # True (bool)
print(data.items)     # ['apple', 'banana'] (list)
```

---

## Real-World Examples

### API Request Validation

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: EmailStr  # Requires pip install pydantic[email]
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    age: int = Field(..., ge=18, le=120)
    bio: Optional[str] = Field(default=None, max_length=500)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username must be alphanumeric'
        return v

# FastAPI/Flask integration
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = CreateUserRequest(**request.json)
        # Process valid user data
        return jsonify({'status': 'success', 'user_id': 123}), 201
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
```

### Database Models

```python
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class BlogPost(BaseModel):
    id: int
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=50)
    author: str
    tags: list[str] = Field(default=[], max_items=5)
    published: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    view_count: int = Field(default=0, ge=0)

    @field_validator('tags')
    @classmethod
    def tags_lowercase(cls, v):
        return [tag.lower() for tag in v]

    @field_validator('content')
    @classmethod
    def no_spam_keywords(cls, v):
        spam_words = ['viagra', 'casino', 'lottery']
        if any(word in v.lower() for word in spam_words):
            raise ValueError('Content contains spam keywords')
        return v

# Create and validate
post = BlogPost(
    id=1,
    title="Getting Started with Pydantic",
    content="Pydantic is a powerful validation library...",
    author="John Doe",
    tags=["Python", "validation"],
    created_at=datetime.now()
)
```

### Configuration Management

```python
from pydantic import BaseModel, Field
from typing import Optional

class DatabaseConfig(BaseModel):
    host: str = Field(default='localhost')
    port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str
    database: str
    pool_size: int = Field(default=10, ge=1, le=100)
    timeout: int = Field(default=30, ge=1)
    ssl_enabled: bool = False

class AppConfig(BaseModel):
    debug: bool = False
    log_level: str = Field(default='INFO')
    database: DatabaseConfig
    api_key: Optional[str] = None
    max_workers: int = Field(default=4, ge=1)

# Load from environment or config file
config = AppConfig(
    debug=True,
    database={
        'host': 'db.example.com',
        'port': 5432,
        'username': 'user',
        'password': 'secret',
        'database': 'myapp'
    },
    api_key='secret-key-123'
)

print(config.database.host)  # db.example.com
print(config.model_dump())   # Full config as dict
```

### Data Transformation Pipeline

```python
from pydantic import BaseModel, field_validator
from datetime import datetime

class RawData(BaseModel):
    timestamp: str  # "2024-01-15 10:30:00"
    amount: str     # "1,234.56"
    status: str     # "ACTIVE"

    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

    @field_validator('amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        return float(v.replace(',', ''))

    @field_validator('status', mode='before')
    @classmethod
    def normalize_status(cls, v):
        return v.lower()

class ProcessedData(BaseModel):
    timestamp: datetime
    amount: float
    status: str

# Transform
raw = RawData(
    timestamp="2024-01-15 10:30:00",
    amount="1,234.56",
    status="ACTIVE"
)

processed = ProcessedData(**raw.model_dump())
print(processed.timestamp)  # datetime object
print(processed.amount)     # 1234.56 (float)
print(processed.status)     # "active"
```

---

## Common Patterns

### Optional vs Required

```python
from pydantic import BaseModel, Field
from typing import Optional

class Profile(BaseModel):
    # Required
    name: str
    email: str

    # Optional with default None
    phone: Optional[str] = None

    # Optional with specific default
    language: str = "en"

    # Required but with Field options
    age: int = Field(..., ge=0)

    # Optional with Field options
    bio: Optional[str] = Field(default=None, max_length=500)

# Valid with only required fields
p1 = Profile(name="John", email="john@example.com")

# Valid with optional fields
p2 = Profile(
    name="Jane",
    email="jane@example.com",
    phone="+1-555-0100",
    language="es",
    bio="Software engineer"
)
```

### Handling JSON Serialization

```python
from pydantic import BaseModel
from datetime import datetime
import json

class Event(BaseModel):
    name: str
    timestamp: datetime
    data: dict

event = Event(
    name="login",
    timestamp=datetime.now(),
    data={"user_id": 123, "ip": "192.168.1.1"}
)

# To JSON
json_str = event.model_dump_json()
print(json_str)

# From JSON
json_data = '{"name":"logout","timestamp":"2024-01-15T10:30:00","data":{}}'
event2 = Event.model_validate_json(json_data)
```

---

## Quick Reference

| Task | Code |
|------|------|
| Create model | `class User(BaseModel): id: int` |
| Create instance | `user = User(id=1)` |
| Validate | Auto when creating instance |
| To dict | `user.model_dump()` |
| To JSON | `user.model_dump_json()` |
| From dict | `User.model_validate(data)` |
| From JSON | `User.model_validate_json(json_str)` |
| Field validation | `field: int = Field(..., ge=0)` |
| Custom validator | `@field_validator('field')` |
| Model validator | `@model_validator(mode='after')` |

---

## Best Practices

1. **Use Field for constraints:** Always use `Field()` for validation rules
2. **Type hints matter:** Pydantic relies on Python type hints
3. **Compose models:** Use nested models for complex structures
4. **Validate early:** Validate at the boundary (API endpoints)
5. **Custom validators sparingly:** Use Field constraints first
6. **Document models:** Add docstrings and Field descriptions
7. **Version your models:** Track changes to API schemas
8. **Use computed_field:** For derived data, not stored data

---

## Links and Resources

- [Pydantic Official Docs](https://docs.pydantic.dev/)
- [Pydantic GitHub](https://github.com/pydantic/pydantic)
- [Pydantic v1 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [FastAPI with Pydantic](https://fastapi.tiangolo.com/)

