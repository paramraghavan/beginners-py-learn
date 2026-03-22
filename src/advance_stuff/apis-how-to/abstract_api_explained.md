# Abstract API Classes - Complete Guide

Learn how to create interfaces that users interact with while keeping implementation hidden and changeable.

---

## The Problem We're Solving

Imagine you're building a data processing system. Different users want to:
- Store data in PostgreSQL, MySQL, or SQLite
- Send emails via SMTP, SendGrid, or AWS SES
- Process payments with Stripe, PayPal, or Square

**The Challenge:**
```python
# ❌ BAD - Users hardcode specific implementations
if database_type == "postgresql":
    db = PostgreSQLDatabase()
elif database_type == "mysql":
    db = MySQLDatabase()
elif database_type == "sqlite":
    db = SQLiteDatabase()

# If you want to add a new database, you must modify ALL user code!
```

**The Solution:**
```python
# ✅ GOOD - Users interact with abstract interface
db = DatabaseFactory.create(database_type)  # Returns some Database implementation
db.connect()
db.query("SELECT * FROM users")

# Users don't care WHICH database is underneath!
# You can swap implementations seamlessly!
```

---

## Core Concept: Abstract Base Classes (ABC)

### What is an Abstract Base Class?

An ABC is a **contract** that says:
- "These methods MUST exist"
- "Here's how to use them"
- "You can't instantiate me directly - create a concrete subclass"

Think of it like:
- **Pizza recipe (Abstract)** → Defines steps: dough, sauce, cheese, bake
- **Concrete pizzas** → Pepperoni pizza, Vegetarian pizza, Hawaiian pizza

All follow the recipe but have different ingredients and implementation.

---

## Example 1: Simple Database Interface

### Step 1: Define the Abstract Interface

```python
from abc import ABC, abstractmethod

class Database(ABC):
    """
    Abstract interface for all databases.
    Users interact with this - they don't care about the concrete implementation!
    """

    @abstractmethod
    def connect(self):
        """Connect to the database"""
        pass

    @abstractmethod
    def query(self, sql: str):
        """Execute a SELECT query"""
        pass

    @abstractmethod
    def execute(self, sql: str, params: dict = None):
        """Execute INSERT/UPDATE/DELETE"""
        pass

    @abstractmethod
    def close(self):
        """Close the connection"""
        pass
```

**Key Points:**
- Use `@abstractmethod` decorator
- Inherit from `ABC`
- Define methods but DON'T implement them
- Docstrings explain WHAT to do, not HOW

### Step 2: Create Concrete Implementations

```python
import sqlite3
import mysql.connector

class SQLiteDatabase(Database):
    """Concrete implementation using SQLite"""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """SQLite-specific connection logic"""
        self.conn = sqlite3.connect(self.db_path)
        print(f"✓ Connected to SQLite: {self.db_path}")

    def query(self, sql: str):
        """SQLite-specific query execution"""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def execute(self, sql: str, params: dict = None):
        """SQLite-specific execute logic"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        """SQLite-specific cleanup"""
        if self.conn:
            self.conn.close()
        print("✓ SQLite connection closed")


class MySQLDatabase(Database):
    """Concrete implementation using MySQL"""

    def __init__(self, host, user, password, database):
        self.config = {"host": host, "user": user, "password": password, "database": database}
        self.conn = None

    def connect(self):
        """MySQL-specific connection logic"""
        self.conn = mysql.connector.connect(**self.config)
        print(f"✓ Connected to MySQL: {self.config['host']}")

    def query(self, sql: str):
        """MySQL-specific query execution"""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def execute(self, sql: str, params: dict = None):
        """MySQL-specific execute logic"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        """MySQL-specific cleanup"""
        if self.conn:
            self.conn.close()
        print("✓ MySQL connection closed")
```

### Step 3: User Code (Simple & Flexible!)

```python
# User code - DOESN'T CARE about the implementation!
def process_users(database: Database):
    """
    Works with ANY database implementation!
    SQLite, MySQL, PostgreSQL, doesn't matter.
    """
    database.connect()

    # Query users
    users = database.query("SELECT * FROM users")
    for user in users:
        print(f"User: {user}")

    # Add new user
    database.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        {"name": "Alice", "email": "alice@example.com"}
    )

    database.close()


# ✅ Easy switching - no user code changes!
if config.database == "sqlite":
    db = SQLiteDatabase("app.db")
elif config.database == "mysql":
    db = MySQLDatabase("localhost", "user", "pass", "mydb")

# Same user code works!
process_users(db)
```

---

## Example 2: Email Service Interface

Real-world example showing how changing implementation is seamless.

### Abstract Interface

```python
class EmailService(ABC):
    """Abstract interface for sending emails"""

    @abstractmethod
    def send(self, to: str, subject: str, body: str):
        """Send an email"""
        pass

    @abstractmethod
    def send_bulk(self, recipients: list, subject: str, body: str):
        """Send email to multiple recipients"""
        pass

    @abstractmethod
    def get_status(self, message_id: str):
        """Get delivery status"""
        pass
```

### Concrete Implementations

```python
class SMTPEmailService(EmailService):
    """Traditional SMTP (like Gmail)"""

    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send(self, to: str, subject: str, body: str):
        # SMTP-specific implementation
        print(f"📧 SMTP: Sending to {to}")
        return "message_id_123"

    def send_bulk(self, recipients: list, subject: str, body: str):
        # SMTP-specific bulk implementation
        for recipient in recipients:
            self.send(recipient, subject, body)

    def get_status(self, message_id: str):
        return "sent"


class SendGridEmailService(EmailService):
    """SendGrid cloud service (completely different implementation)"""

    def __init__(self, api_key):
        self.api_key = api_key

    def send(self, to: str, subject: str, body: str):
        # SendGrid API call
        print(f"📨 SendGrid: Sending to {to}")
        return "sg_message_12345"

    def send_bulk(self, recipients: list, subject: str, body: str):
        # SendGrid bulk endpoint
        print(f"📨 SendGrid: Bulk sending to {len(recipients)} recipients")
        return "bulk_job_id"

    def get_status(self, message_id: str):
        # SendGrid API status check
        return "delivered"


class AWSEmailService(EmailService):
    """AWS SES (Simple Email Service)"""

    def __init__(self, aws_region):
        self.aws_region = aws_region

    def send(self, to: str, subject: str, body: str):
        # AWS SES implementation
        print(f"📬 AWS SES: Sending to {to}")
        return "aws_message_456"

    def send_bulk(self, recipients: list, subject: str, body: str):
        # AWS SES bulk implementation
        print(f"📬 AWS SES: Bulk sending to {len(recipients)} recipients")
        return "aws_bulk_job"

    def get_status(self, message_id: str):
        return "delivered"
```

### User Code (Works with ALL implementations!)

```python
def send_newsletter(email_service: EmailService, subscribers: list):
    """
    Send newsletter to all subscribers.
    Works with SMTP, SendGrid, AWS SES - doesn't care!
    """
    email_service.send_bulk(
        subscribers,
        subject="Weekly Newsletter",
        body="Check out this week's updates..."
    )
    print("✓ Newsletter sent!")


def send_notification(email_service: EmailService, user_email: str):
    """
    Send notification to user.
    Works with any email service!
    """
    email_service.send(
        to=user_email,
        subject="Your notification",
        body="Important update..."
    )


# ✅ Switch implementations without changing user code!

# Use SMTP
smtp_service = SMTPEmailService("smtp.gmail.com", 587, "user@gmail.com", "password")
send_newsletter(smtp_service, ["alice@example.com", "bob@example.com"])

# Switch to SendGrid - no user code changes!
sendgrid_service = SendGridEmailService("sg_api_key_12345")
send_newsletter(sendgrid_service, ["alice@example.com", "bob@example.com"])

# Switch to AWS - still no user code changes!
aws_service = AWSEmailService("us-east-1")
send_newsletter(aws_service, ["alice@example.com", "bob@example.com"])
```

---

## Example 3: Payment Processor Interface

### Define Abstract Interface

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class Payment:
    transaction_id: str
    amount: float
    status: PaymentStatus
    timestamp: datetime
    error_message: str = None

class PaymentProcessor(ABC):
    """Abstract interface for processing payments"""

    @abstractmethod
    def charge(self, amount: float, customer_id: str, metadata: dict = None) -> Payment:
        """Charge a customer"""
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> Payment:
        """Refund a previous charge"""
        pass

    @abstractmethod
    def get_transaction(self, transaction_id: str) -> Payment:
        """Get transaction details"""
        pass

    @abstractmethod
    def validate_payment_method(self, payment_method: dict) -> bool:
        """Validate if payment method is valid"""
        pass
```

### Concrete Implementations

```python
class StripePaymentProcessor(PaymentProcessor):
    """Process payments using Stripe API"""

    def __init__(self, api_key):
        self.api_key = api_key

    def charge(self, amount: float, customer_id: str, metadata: dict = None) -> Payment:
        # Stripe-specific API call
        print(f"💳 Stripe: Charging ${amount} to {customer_id}")
        return Payment(
            transaction_id="ch_stripe_123",
            amount=amount,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def refund(self, transaction_id: str) -> Payment:
        print(f"💳 Stripe: Refunding {transaction_id}")
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )

    def get_transaction(self, transaction_id: str) -> Payment:
        # Query Stripe API
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def validate_payment_method(self, payment_method: dict) -> bool:
        # Stripe-specific validation
        return "stripe_token" in payment_method


class PayPalPaymentProcessor(PaymentProcessor):
    """Process payments using PayPal API"""

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def charge(self, amount: float, customer_id: str, metadata: dict = None) -> Payment:
        # PayPal-specific API call
        print(f"🅿️ PayPal: Charging ${amount} to {customer_id}")
        return Payment(
            transaction_id="pp_paypal_456",
            amount=amount,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def refund(self, transaction_id: str) -> Payment:
        print(f"🅿️ PayPal: Refunding {transaction_id}")
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )

    def get_transaction(self, transaction_id: str) -> Payment:
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def validate_payment_method(self, payment_method: dict) -> bool:
        return "paypal_email" in payment_method


class SquarePaymentProcessor(PaymentProcessor):
    """Process payments using Square API"""

    def __init__(self, api_key):
        self.api_key = api_key

    def charge(self, amount: float, customer_id: str, metadata: dict = None) -> Payment:
        # Square-specific API call
        print(f"⬛ Square: Charging ${amount} to {customer_id}")
        return Payment(
            transaction_id="sq_square_789",
            amount=amount,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def refund(self, transaction_id: str) -> Payment:
        print(f"⬛ Square: Refunding {transaction_id}")
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )

    def get_transaction(self, transaction_id: str) -> Payment:
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def validate_payment_method(self, payment_method: dict) -> bool:
        return "square_nonce" in payment_method
```

### User Code (Works with ALL processors!)

```python
class CheckoutService:
    """User code - doesn't care about payment processor details!"""

    def __init__(self, payment_processor: PaymentProcessor):
        self.processor = payment_processor

    def process_order(self, order: dict, customer_id: str):
        """Process order payment"""
        amount = order["total"]

        # Same code works with Stripe, PayPal, Square!
        payment = self.processor.charge(amount, customer_id, metadata={"order_id": order["id"]})

        if payment.status == PaymentStatus.COMPLETED:
            print(f"✓ Payment successful! Transaction: {payment.transaction_id}")
            return True
        else:
            print(f"✗ Payment failed: {payment.error_message}")
            return False

    def refund_order(self, order_id: str):
        """Refund an order"""
        # Same code works with any processor!
        refund = self.processor.refund(order_id)
        print(f"✓ Refund processed: {refund.transaction_id}")


# ✅ Seamless switching!

# Start with Stripe
stripe = StripePaymentProcessor("sk_live_123")
checkout1 = CheckoutService(stripe)
checkout1.process_order({"id": "order_1", "total": 99.99}, "customer_1")

# Switch to PayPal - no code changes!
paypal = PayPalPaymentProcessor("client_id", "client_secret")
checkout2 = CheckoutService(paypal)
checkout2.process_order({"id": "order_2", "total": 49.99}, "customer_2")

# Switch to Square - still no code changes!
square = SquarePaymentProcessor("api_key_123")
checkout3 = CheckoutService(square)
checkout3.process_order({"id": "order_3", "total": 29.99}, "customer_3")
```

---

## Benefits Summary

### For Users (Application Code):
✅ **Simple to use** - Just call methods from the abstract interface
✅ **Implementation-agnostic** - Don't need to know WHICH database/service
✅ **Easy to test** - Can pass mock implementations for testing
✅ **No code changes** - Swap implementations without touching user code

### For Implementors:
✅ **Freedom to change** - Rewrite implementation without breaking user code
✅ **Clear contract** - Abstract class shows exactly what must be implemented
✅ **Extensibility** - Easy to add new implementations
✅ **Maintainability** - All implementations follow same pattern

### Example: Why This Matters

```python
# Before Abstract Classes (Hard to change):
# Application code tightly coupled to PostgreSQL
if query_type == "SELECT":
    result = postgres_client.query(sql)
elif query_type == "INSERT":
    postgres_client.execute(sql)
# If you want to support MySQL, you need to change ALL this code!

# After Abstract Classes (Easy to change):
# Application code uses abstract interface
result = database.query(sql)
# To support MySQL? Just create MySQLDatabase and inject it!
# User code doesn't change at all!
```

---

## Key Takeaways

1. **Define Abstract Interface** - Use `ABC` and `@abstractmethod`
2. **Create Concrete Implementations** - Implement the abstract methods
3. **Write User Code Against Interface** - Not concrete classes
4. **Inject Implementations** - Pass concrete implementations at runtime
5. **Change Seamlessly** - Swap implementations without changing user code

This pattern is used everywhere:
- ✅ Database ORMs (SQLAlchemy)
- ✅ Cloud providers (AWS, GCP, Azure)
- ✅ Web frameworks (Flask, Django)
- ✅ Payment processors (Stripe, PayPal)
- ✅ Testing (Mocks and stubs)

Master this pattern and your code becomes flexible, testable, and maintainable! 🎯
