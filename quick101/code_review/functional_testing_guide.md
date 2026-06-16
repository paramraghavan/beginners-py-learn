# Functional Testing Guide

A comprehensive guide to writing and running functional tests in Python.

---

## Table of Contents

1. [What is Functional Testing?](#what-is-functional-testing)
2. [Functional vs Unit vs Integration](#functional-vs-unit-vs-integration)
3. [Why Functional Testing Matters](#why-functional-testing-matters)
4. [Writing Functional Tests](#writing-functional-tests)
5. [Test Organization](#test-organization)
6. [Fixtures and Setup](#fixtures-and-setup)
7. [Real-World Examples](#real-world-examples)
8. [Best Practices](#best-practices)
9. [Common Patterns](#common-patterns)
10. [Troubleshooting](#troubleshooting)

---

## What is Functional Testing?

### Definition
**Functional testing** verifies that **complete features/workflows work as expected** from a user's perspective.

### Characteristics
- Tests **end-to-end workflows**
- Tests **user-facing behavior**
- **Black-box testing** (doesn't care about internal code)
- Tests **integration** between components
- Verifies **business logic** works correctly

### Example Workflow

```
User Story: User can sign up and log in

Workflow:
  1. User provides email, name, password
  2. System validates input
  3. System creates account
  4. User receives confirmation
  5. User logs in with credentials
  6. System authenticates
  7. User sees dashboard

Functional Test: Verify ALL steps work together
```

---

## Functional vs Unit vs Integration

### Comparison

| Aspect | Unit Test | Integration Test | Functional Test |
|--------|-----------|------------------|-----------------|
| **Scope** | Single function | 2-3 components | Complete workflow |
| **Tests** | Code unit | Component interaction | User feature |
| **Speed** | Very fast | Medium | Slower |
| **Failure** | Points to exact function | Points to interaction | Points to workflow |
| **Count** | Many | Some | Few |
| **Example** | `test_add(2, 3)` | `test_user_login()` | `test_complete_signup_and_login()` |

### Pyramid

```
        ▲
        │   Functional (E2E)
        │   Few, slow, complete workflows
        │
       ╱│╲  Integration
       │ │  Some, medium speed
       │
      ╱ │ ╲ Unit
      │ │  Many, fast, isolated
      │
  ────┴─┴──────────────>
```

---

## Why Functional Testing Matters

### Problems Solved
✓ **Catches integration bugs** - Individual functions work, but together they fail
✓ **Tests real scenarios** - Tests what users actually do
✓ **Builds confidence** - Know complete features work before release
✓ **Documents workflows** - Tests show intended user flow
✓ **Prevents regressions** - Catch breaking changes

### Example: Unit vs Functional

**Unit Test Only:**
```python
# ✓ Validates password is strong
def test_validate_password():
    assert validate_password("Pass123") == True

# ✓ Creates user record
def test_create_user():
    user = create_user("john@example.com", "Pass123")
    assert user.id > 0

# ✓ Authenticates user
def test_authenticate():
    user = authenticate("john@example.com", "Pass123")
    assert user.is_authenticated == True
```

**Problem:** Each test passes, but what if together they fail?
- Maybe password validation works, but user creation fails
- Maybe user is created, but authentication is broken
- Maybe email validation is missing

**Functional Test:**
```python
# ✓ Complete workflow
def test_complete_signup_and_login():
    # Step 1: Signup
    user = user_service.register("john@example.com", "Pass123")
    assert user.id > 0

    # Step 2: Login
    authenticated = user_service.login("john@example.com", "Pass123")
    assert authenticated.id == user.id

    # Finds problems unit tests miss!
```

---

## Writing Functional Tests

### Basic Structure

```python
def test_complete_workflow():
    """
    WORKFLOW:
    1. Step 1 description
    2. Step 2 description
    3. Step 3 description
    """
    # Step 1: Setup/Action
    result1 = perform_action_1()

    # Step 2: Verify
    assert result1 is not None

    # Step 3: Continue workflow
    result2 = perform_action_2(result1)

    # Step 4: Final verification
    assert result2.status == "success"
```

### Example: E-Commerce Checkout

```python
def test_complete_checkout_workflow(self, order_service, logged_in_user):
    """
    WORKFLOW:
    1. Customer adds items to cart
    2. Customer proceeds to checkout
    3. Customer enters shipping info
    4. Customer enters payment info
    5. Order is confirmed
    """
    user_id = logged_in_user.user_id

    # Step 1: Add items
    items = [
        Item(1, "Laptop", 999.99),
        Item(2, "Mouse", 29.99)
    ]

    # Step 2: Create order
    order = order_service.create_order(user_id, items)
    assert order.total_amount == 1029.98

    # Step 3: Confirm with details
    confirmed = order_service.confirm_order(
        order.order_id,
        payment_method="credit_card",
        address="123 Main St"
    )

    # Step 4: Verify confirmed
    assert confirmed.status == OrderStatus.CONFIRMED
    assert confirmed.shipping_address == "123 Main St"
```

---

## Test Organization

### By Feature (Recommended)

```
tests/
├── functional/
│   ├── test_user_signup_workflow.py
│   ├── test_user_login_workflow.py
│   ├── test_checkout_workflow.py
│   └── test_payment_workflow.py
├── unit/
│   ├── test_password_validation.py
│   └── test_email_validation.py
└── integration/
    └── test_database_operations.py
```

### By Component

```
tests/
├── user/
│   ├── test_signup.py
│   ├── test_login.py
│   └── test_profile.py
├── order/
│   ├── test_creation.py
│   ├── test_fulfillment.py
│   └── test_cancellation.py
└── payment/
    └── test_processing.py
```

### Class-Based Organization

```python
class TestCheckoutWorkflow:
    """All checkout-related tests"""

    def test_simple_checkout(self):
        """Single item checkout"""
        ...

    def test_multiple_items_checkout(self):
        """Multiple items checkout"""
        ...

    def test_checkout_with_discount(self):
        """Checkout with discount applied"""
        ...

    def test_checkout_fails_without_payment(self):
        """Checkout validation"""
        ...
```

---

## Fixtures and Setup

### Basic Fixture

```python
@pytest.fixture
def user_service():
    """Create fresh service for each test"""
    return UserService()

def test_signup(user_service):
    user = user_service.register(...)
    assert user.id > 0
```

### Fixture with Setup/Teardown

```python
@pytest.fixture
def database_connection():
    # Setup
    db = connect_to_database()
    db.create_tables()

    yield db  # Test runs here

    # Teardown
    db.drop_tables()
    db.close()

def test_something(database_connection):
    # database_connection is available
    ...
```

### Dependent Fixtures

```python
@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def registered_user(user_service):
    """Uses user_service fixture"""
    return user_service.register(
        "john@example.com",
        "Pass123"
    )

@pytest.fixture
def logged_in_user(user_service, registered_user):
    """Uses both fixtures"""
    return user_service.login(
        "john@example.com",
        "Pass123"
    )

def test_something(logged_in_user):
    # logged_in_user is fully set up
    assert logged_in_user.id > 0
```

### Fixture Scope

```python
# Default: function scope (new for each test)
@pytest.fixture
def user_service():
    return UserService()

# Session scope (shared across all tests)
@pytest.fixture(scope="session")
def database():
    db = Database()
    db.initialize()
    yield db
    db.cleanup()

# Module scope (shared within a module)
@pytest.fixture(scope="module")
def large_dataset():
    return load_data()
```

---

## Real-World Examples

### Example 1: User Account Workflow

```python
def test_complete_account_lifecycle(self, user_service):
    """
    WORKFLOW:
    1. User signs up
    2. User logs in
    3. User updates profile
    4. User logs out
    5. User deactivates account
    """
    # Step 1: Sign up
    user = user_service.register(
        "jane@example.com",
        "Jane Doe",
        "SecurePass123"
    )
    assert user.is_active

    # Step 2: Login
    logged_in = user_service.login("jane@example.com", "SecurePass123")
    assert logged_in.id == user.id

    # Step 3: Update profile
    updated = user_service.update_profile(user.id, "Jane Smith")
    assert updated.name == "Jane Smith"

    # Step 4: Deactivate
    user_service.deactivate_account(user.id)
    deactivated_user = user_service.get_user(user.id)
    assert not deactivated_user.is_active

    # Step 5: Cannot login
    with pytest.raises(InvalidCredentialsError):
        user_service.login("jane@example.com", "SecurePass123")
```

### Example 2: Order Lifecycle

```python
def test_order_complete_lifecycle(self, order_service, logged_in_user):
    """
    WORKFLOW:
    1. Create order
    2. Confirm order
    3. Ship order
    4. Deliver order
    """
    # Step 1: Create
    items = [Item(1, "Book", 19.99)]
    order = order_service.create_order(logged_in_user.id, items)
    assert order.status == OrderStatus.PENDING

    # Step 2: Confirm
    order = order_service.confirm_order(
        order.id,
        "credit_card",
        "123 Main St"
    )
    assert order.status == OrderStatus.CONFIRMED

    # Step 3: Ship
    order = order_service.ship_order(order.id)
    assert order.status == OrderStatus.SHIPPED

    # Step 4: Deliver
    order = order_service.deliver_order(order.id)
    assert order.status == OrderStatus.DELIVERED
```

### Example 3: Error Handling Workflow

```python
def test_checkout_validation_workflow(self, order_service, logged_in_user):
    """
    WORKFLOW:
    1. Create order
    2. Try to confirm without payment
    3. System rejects
    4. Add payment
    5. Confirm succeeds
    """
    # Step 1: Create order
    items = [Item(1, "Book", 19.99)]
    order = order_service.create_order(logged_in_user.id, items)

    # Step 2-3: Try without payment
    with pytest.raises(ValueError):
        order_service.confirm_order(
            order.id,
            payment_method="",
            address="123 Main St"
        )

    # Step 4-5: Confirm with payment
    confirmed = order_service.confirm_order(
        order.id,
        payment_method="credit_card",
        address="123 Main St"
    )
    assert confirmed.status == OrderStatus.CONFIRMED
```

---

## Best Practices

### 1. Use Workflow Comments
```python
def test_something(self, service):
    """
    WORKFLOW:
    1. Description of step 1
    2. Description of step 2
    3. Description of step 3
    """
    # Makes it clear what you're testing
```

### 2. Test Both Success and Failure Paths
```python
def test_checkout_success(self, order_service):
    """Happy path"""
    order = order_service.confirm_order(...)
    assert order.status == CONFIRMED

def test_checkout_fails_without_payment(self, order_service):
    """Error path"""
    with pytest.raises(ValueError):
        order_service.confirm_order(payment_method="")
```

### 3. Use Meaningful Names
```python
# Good
def test_complete_checkout_workflow_with_multiple_items()

# Bad
def test_checkout()
def test_order()
```

### 4. One Workflow Per Test
```python
# Good - Tests ONE workflow
def test_signup_and_login():
    user = signup()
    login(user)

# Bad - Tests MULTIPLE workflows
def test_user_management():
    signup()
    login()
    payment()
    shipping()
```

### 5. Setup with Fixtures
```python
# Good
def test_login(self, registered_user):
    logged_in = login(registered_user.email)
    assert logged_in.id == registered_user.id

# Bad
def test_login(self):
    user = register()  # Setup in test
    logged_in = login(user.email)
    assert logged_in.id == user.id
```

### 6. Clear Assertions
```python
# Good
assert order.status == OrderStatus.CONFIRMED
assert order.shipping_address == "123 Main St"

# Bad
assert order is not None
assert order.id > 0
```

---

## Common Patterns

### Pattern 1: Setup → Action → Assert

```python
def test_workflow(self, service):
    # Setup
    item = Item(1, "Product", 99.99)

    # Action
    order = service.create_order(1, [item])

    # Assert
    assert order.total_amount == 99.99
```

### Pattern 2: State Transitions

```python
def test_state_workflow(self, service):
    # State 1
    order = service.create_order(...)
    assert order.status == PENDING

    # State 2
    order = service.confirm_order(...)
    assert order.status == CONFIRMED

    # State 3
    order = service.ship_order(...)
    assert order.status == SHIPPED
```

### Pattern 3: Error Handling

```python
def test_error_workflow(self, service):
    # Valid action
    order = service.create_order(...)

    # Invalid action
    with pytest.raises(ValueError):
        service.confirm_order(order.id, payment="")

    # Order still exists
    assert service.get_order(order.id) is not None
```

### Pattern 4: Multiple Entities

```python
def test_multi_user_workflow(self, service):
    # User 1
    user1 = register("user1@example.com")

    # User 2
    user2 = register("user2@example.com")

    # Verify separate
    assert user1.id != user2.id
    assert user1.email != user2.email
```

---

## Troubleshooting

### Issue: Fixtures Not Applied
```python
# Wrong
def test_something():
    # user_service not available
    user_service.register(...)

# Right
def test_something(user_service):
    # user_service is injected
    user_service.register(...)
```

### Issue: Test Modifying Shared State
```python
# Wrong - service reused, state persists
@pytest.fixture(scope="module")
def user_service():
    return UserService()

# Right - service fresh for each test
@pytest.fixture
def user_service():
    return UserService()
```

### Issue: Hard to Debug Failures
```python
# Wrong - Generic assertion
assert order is not None

# Right - Specific assertion
assert order.status == OrderStatus.CONFIRMED
assert order.user_id == user.id
assert order.total_amount == 99.99
```

### Issue: Test Too Complex
```python
# Wrong - Tests too many things
def test_everything(self, service):
    # ... 50 lines of code

# Right - Split into smaller tests
def test_signup_workflow(self, service):
    ...

def test_login_workflow(self, service):
    ...

def test_checkout_workflow(self, service):
    ...
```

---

## Quick Reference

### Run Tests
```bash
# All tests
pytest tests/

# Specific file
pytest tests/functional/test_user_workflows.py

# Specific class
pytest tests/functional/test_user_workflows.py::TestUserSignupWorkflow

# Specific test
pytest tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_complete_signup_and_login_workflow

# Verbose
pytest -v tests/

# Stop on first failure
pytest -x tests/

# Show print statements
pytest -s tests/
```

### Assertion Patterns
```python
# Equality
assert result == expected

# Existence
assert result is not None

# Contains
assert "text" in result

# Type
assert isinstance(result, User)

# Exceptions
with pytest.raises(ValueError):
    perform_action()

# With message
with pytest.raises(ValueError, match="specific message"):
    perform_action()
```

---

## Summary

**Functional tests:**
- Test complete workflows, not individual functions
- Verify user-facing behavior
- Catch integration bugs
- Document intended workflows
- Are slower but more important

**Best for:**
- Verifying complete features work
- End-to-end testing
- Before release validation
- Real-world scenario testing

**Use with pytest:**
- Easy syntax
- Powerful fixtures
- Great organization
- Clear test discovery

---

## Next Steps

1. **Study the example:** Read `functional_test_example/`
2. **Run tests:** `pytest tests/ -v`
3. **Understand workflows:** Read test comments
4. **Write your own:** Create tests for your application
5. **Run with coverage:** Verify complete workflows

**Happy testing!** 🧪
