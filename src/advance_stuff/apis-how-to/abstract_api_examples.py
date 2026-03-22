"""
Abstract API Classes - Practical Examples

Demonstrates how to:
1. Define abstract interfaces
2. Create concrete implementations
3. Write user code that doesn't care about implementation details
4. Seamlessly swap implementations
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

print("="*70)
print("ABSTRACT API CLASSES - PRACTICAL EXAMPLES")
print("="*70)

# =============================================================================
# EXAMPLE 1: DATABASE INTERFACE
# =============================================================================
print("\n1. DATABASE INTERFACE")
print("-" * 70)

class Database(ABC):
    """Abstract interface for databases"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql: str) -> list:
        pass

    @abstractmethod
    def execute(self, sql: str, params: dict = None):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLiteDatabase(Database):
    """Concrete SQLite implementation"""

    def __init__(self, db_path):
        self.db_path = db_path
        self.connected = False

    def connect(self):
        print(f"  ✓ SQLite: Connected to {self.db_path}")
        self.connected = True

    def query(self, sql: str) -> list:
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"  → SQLite: Executing query: {sql[:30]}...")
        return [("Alice", 30), ("Bob", 25)]

    def execute(self, sql: str, params: dict = None):
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"  → SQLite: Executing: {sql[:30]}...")

    def close(self):
        print("  ✓ SQLite: Disconnected")
        self.connected = False


class MySQLDatabase(Database):
    """Concrete MySQL implementation"""

    def __init__(self, host, user, password, database):
        self.host = host
        self.connected = False

    def connect(self):
        print(f"  ✓ MySQL: Connected to {self.host}")
        self.connected = True

    def query(self, sql: str) -> list:
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"  → MySQL: Executing query: {sql[:30]}...")
        return [("Alice", 30), ("Bob", 25)]

    def execute(self, sql: str, params: dict = None):
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"  → MySQL: Executing: {sql[:30]}...")

    def close(self):
        print("  ✓ MySQL: Disconnected")
        self.connected = False


# User code - works with ANY database!
def process_users(database: Database):
    """User code doesn't care which database is underneath!"""
    database.connect()
    users = database.query("SELECT name, age FROM users")
    for user in users:
        print(f"    Processing user: {user}")
    database.close()


# ✅ Easy switching!
print("\nUsing SQLite:")
sqlite_db = SQLiteDatabase("app.db")
process_users(sqlite_db)

print("\nUsing MySQL - NO USER CODE CHANGES:")
mysql_db = MySQLDatabase("localhost", "user", "pass", "mydb")
process_users(mysql_db)

# =============================================================================
# EXAMPLE 2: EMAIL SERVICE INTERFACE
# =============================================================================
print("\n\n2. EMAIL SERVICE INTERFACE")
print("-" * 70)

class EmailService(ABC):
    """Abstract interface for email services"""

    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> str:
        """Send email, return message ID"""
        pass

    @abstractmethod
    def send_bulk(self, recipients: List[str], subject: str, body: str):
        """Send email to multiple recipients"""
        pass


class SMTPEmailService(EmailService):
    """Traditional SMTP email"""

    def send(self, to: str, subject: str, body: str) -> str:
        print(f"  📧 SMTP: Sending to {to}")
        return "smtp_msg_123"

    def send_bulk(self, recipients: List[str], subject: str, body: str):
        print(f"  📧 SMTP: Sending to {len(recipients)} recipients")
        for recipient in recipients:
            print(f"    → {recipient}")


class SendGridEmailService(EmailService):
    """SendGrid cloud service"""

    def send(self, to: str, subject: str, body: str) -> str:
        print(f"  📨 SendGrid: Sending to {to}")
        return "sg_msg_456"

    def send_bulk(self, recipients: List[str], subject: str, body: str):
        print(f"  📨 SendGrid: Bulk sending to {len(recipients)} recipients")


class AWSEmailService(EmailService):
    """AWS SES email service"""

    def send(self, to: str, subject: str, body: str) -> str:
        print(f"  📬 AWS SES: Sending to {to}")
        return "aws_msg_789"

    def send_bulk(self, recipients: List[str], subject: str, body: str):
        print(f"  📬 AWS SES: Bulk sending to {len(recipients)} recipients")


# User code - works with ANY email service!
def send_newsletter(email_service: EmailService, subscribers: List[str]):
    """User code doesn't care which email service is underneath!"""
    email_service.send_bulk(
        subscribers,
        subject="Weekly Newsletter",
        body="Check out this week's updates..."
    )
    print("  ✓ Newsletter sent!")


# ✅ Easy switching!
subscribers = ["alice@example.com", "bob@example.com", "charlie@example.com"]

print("\nUsing SMTP:")
smtp = SMTPEmailService()
send_newsletter(smtp, subscribers)

print("\nUsing SendGrid - NO USER CODE CHANGES:")
sendgrid = SendGridEmailService()
send_newsletter(sendgrid, subscribers)

print("\nUsing AWS SES - NO USER CODE CHANGES:")
aws = AWSEmailService()
send_newsletter(aws, subscribers)

# =============================================================================
# EXAMPLE 3: PAYMENT PROCESSOR INTERFACE
# =============================================================================
print("\n\n3. PAYMENT PROCESSOR INTERFACE")
print("-" * 70)

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
    error_message: Optional[str] = None


class PaymentProcessor(ABC):
    """Abstract interface for payment processing"""

    @abstractmethod
    def charge(self, amount: float, customer_id: str) -> Payment:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> Payment:
        pass


class StripePaymentProcessor(PaymentProcessor):
    """Stripe payment processor"""

    def charge(self, amount: float, customer_id: str) -> Payment:
        print(f"  💳 Stripe: Charging ${amount:.2f} to {customer_id}")
        return Payment(
            transaction_id="ch_stripe_123",
            amount=amount,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def refund(self, transaction_id: str) -> Payment:
        print(f"  💳 Stripe: Refunding {transaction_id}")
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )


class PayPalPaymentProcessor(PaymentProcessor):
    """PayPal payment processor"""

    def charge(self, amount: float, customer_id: str) -> Payment:
        print(f"  🅿️ PayPal: Charging ${amount:.2f} to {customer_id}")
        return Payment(
            transaction_id="pp_paypal_456",
            amount=amount,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def refund(self, transaction_id: str) -> Payment:
        print(f"  🅿️ PayPal: Refunding {transaction_id}")
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )


class SquarePaymentProcessor(PaymentProcessor):
    """Square payment processor"""

    def charge(self, amount: float, customer_id: str) -> Payment:
        print(f"  ⬛ Square: Charging ${amount:.2f} to {customer_id}")
        return Payment(
            transaction_id="sq_square_789",
            amount=amount,
            status=PaymentStatus.COMPLETED,
            timestamp=datetime.now()
        )

    def refund(self, transaction_id: str) -> Payment:
        print(f"  ⬛ Square: Refunding {transaction_id}")
        return Payment(
            transaction_id=transaction_id,
            amount=100.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )


# User code - works with ANY payment processor!
class CheckoutService:
    """User code that doesn't care about payment processor details!"""

    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def process_order(self, order_total: float, customer_id: str) -> bool:
        """Process order payment"""
        payment = self.processor.charge(order_total, customer_id)

        if payment.status == PaymentStatus.COMPLETED:
            print(f"  ✓ Payment successful!")
            return True
        else:
            print(f"  ✗ Payment failed!")
            return False


# ✅ Easy switching!
print("\nUsing Stripe:")
stripe = StripePaymentProcessor()
checkout1 = CheckoutService(stripe)
checkout1.process_order(99.99, "customer_1")

print("\nUsing PayPal - NO USER CODE CHANGES:")
paypal = PayPalPaymentProcessor()
checkout2 = CheckoutService(paypal)
checkout2.process_order(49.99, "customer_2")

print("\nUsing Square - NO USER CODE CHANGES:")
square = SquarePaymentProcessor()
checkout3 = CheckoutService(square)
checkout3.process_order(29.99, "customer_3")

# =============================================================================
# EXAMPLE 4: TESTING WITH ABSTRACT INTERFACES
# =============================================================================
print("\n\n4. TESTING WITH ABSTRACT INTERFACES")
print("-" * 70)

class MockPaymentProcessor(PaymentProcessor):
    """Mock processor for testing - NO EXTERNAL CALLS!"""

    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.charges = []

    def charge(self, amount: float, customer_id: str) -> Payment:
        self.charges.append({"amount": amount, "customer_id": customer_id})

        if self.should_fail:
            return Payment(
                transaction_id="mock_failed",
                amount=amount,
                status=PaymentStatus.FAILED,
                timestamp=datetime.now(),
                error_message="Insufficient funds"
            )
        else:
            return Payment(
                transaction_id="mock_success",
                amount=amount,
                status=PaymentStatus.COMPLETED,
                timestamp=datetime.now()
            )

    def refund(self, transaction_id: str) -> Payment:
        return Payment(
            transaction_id=transaction_id,
            amount=0.0,
            status=PaymentStatus.REFUNDED,
            timestamp=datetime.now()
        )


# Test with mock - no real payments!
print("\nTesting with Mock Processor:")

print("  Test 1: Successful payment")
mock_processor = MockPaymentProcessor(should_fail=False)
checkout = CheckoutService(mock_processor)
success = checkout.process_order(50.0, "test_customer")
print(f"  Result: {'PASS ✓' if success else 'FAIL ✗'}")

print("\n  Test 2: Failed payment")
mock_processor = MockPaymentProcessor(should_fail=True)
checkout = CheckoutService(mock_processor)
success = checkout.process_order(50.0, "test_customer")
print(f"  Result: {'PASS ✓' if not success else 'FAIL ✗'}")

# =============================================================================
# WHY THIS MATTERS
# =============================================================================
print("\n\n5. WHY THIS MATTERS")
print("-" * 70)

print("\n❌ WITHOUT Abstract Classes (Hard to change):")
print("""
  def process_order(amount, customer):
      if config.payment_processor == "stripe":
          stripe_charge(amount)
      elif config.payment_processor == "paypal":
          paypal_charge(amount)
      elif config.payment_processor == "square":
          square_charge(amount)
      # To add a new processor, change THIS code!
      # To switch processors, change THIS code!
""")

print("\n✅ WITH Abstract Classes (Easy to change):")
print("""
  def process_order(processor: PaymentProcessor, amount, customer):
      processor.charge(amount, customer)
      # To add a new processor, just create a new class!
      # To switch processors, inject a different class!
      # This code NEVER changes!
""")

# =============================================================================
# KEY BENEFITS
# =============================================================================
print("\n\n6. KEY BENEFITS SUMMARY")
print("-" * 70)

benefits = {
    "✅ For Users (Application Code)": [
        "- Simple to use: just call abstract methods",
        "- Implementation-agnostic: don't care about details",
        "- Easy to test: use mock implementations",
        "- No code changes: swap implementations seamlessly"
    ],
    "✅ For Implementors": [
        "- Freedom to change: rewrite without breaking user code",
        "- Clear contract: know exactly what to implement",
        "- Easy to extend: add new implementations easily",
        "- Maintainability: all implementations follow same pattern"
    ]
}

for category, points in benefits.items():
    print(f"\n{category}")
    for point in points:
        print(f"  {point}")

print("\n" + "="*70)
print("✅ Done! You now understand Abstract API Classes!")
print("="*70)
