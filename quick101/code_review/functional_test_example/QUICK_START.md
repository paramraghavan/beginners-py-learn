# Functional Testing - Quick Start Example

Complete working example of functional tests for an e-commerce application.

---

## 📁 Project Structure

```
functional_test_example/
├── src/
│   ├── __init__.py
│   ├── user.py              # User management module
│   └── order.py             # Order management module
├── tests/
│   ├── functional/
│   │   ├── test_user_workflows.py      # User workflows
│   │   └── test_order_workflows.py     # Order workflows
│   └── unit/                (Not implemented yet)
├── pytest.ini               # Pytest config
├── requirements.txt         # Dependencies
└── QUICK_START.md           # This file
```

---

## 🎯 What is This?

This is a **functional test example** for an e-commerce system:
- Users can sign up and log in
- Users can create orders
- Orders go through a lifecycle (pending → confirmed → shipped → delivered)

**Functional tests verify COMPLETE WORKFLOWS**, not individual functions.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Navigate to Example
```bash
cd quick101/code_review/functional_test_example
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
# Or: pip install pytest pytest-cov
```

### Step 3: Run All Tests
```bash
pytest tests/
```

### Step 4: Run Only Functional Tests
```bash
pytest tests/functional/
```

### Step 5: Run with Verbose Output
```bash
pytest -v tests/
```

### Step 6: Run Specific Test
```bash
pytest -v tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_complete_signup_and_login_workflow
```

---

## 📊 Expected Output

```
tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_complete_signup_and_login_workflow PASSED
tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_signup_with_invalid_email PASSED
tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_signup_with_weak_password PASSED
...

====== 27 passed in 0.45s ======
```

---

## 📖 Understanding the Tests

### What is a Functional Test?

**Functional Test** = Tests a complete workflow/feature from start to finish

Example from `test_user_workflows.py`:
```python
def test_complete_signup_and_login_workflow(self, user_service):
    """
    WORKFLOW:
    1. User signs up with email, name, password
    2. System validates and stores user
    3. User logs in with credentials
    4. System authenticates user
    """
    # Step 1: User signs up
    user = user_service.register(...)

    # Step 2: Verify user created
    assert user.user_id > 0

    # Step 3: User logs in
    logged_in_user = user_service.login(...)

    # Step 4: Verify login succeeded
    assert logged_in_user.user_id == user.user_id
```

**What it tests:** Complete workflow (not individual functions)

### vs Unit Test

**Unit Test** = Tests single function in isolation

```python
def test_validate_email():
    assert UserService._is_valid_email("john@example.com") == True
    assert UserService._is_valid_email("invalid") == False
```

**What it tests:** Just the validation function

---

## 🧪 Test Categories

### User Workflows
Located in: `tests/functional/test_user_workflows.py`

**Tests:**
1. **TestUserSignupWorkflow** - User signup process
   - Complete signup and login
   - Invalid email validation
   - Weak password validation
   - Duplicate email prevention

2. **TestUserLoginWorkflow** - User authentication
   - Successful login
   - Wrong password
   - Nonexistent user
   - Deactivated account

3. **TestUserProfileWorkflow** - Profile management
   - Update profile
   - Account deactivation

4. **TestMultipleUserWorkflow** - Multiple users
   - Two users signup and login separately

### Order Workflows
Located in: `tests/functional/test_order_workflows.py`

**Tests:**
1. **TestSimpleCheckoutWorkflow** - Basic checkout
   - Create order with items
   - Confirm with payment details
   - Missing payment validation
   - Missing address validation

2. **TestOrderFulfillmentWorkflow** - Complete order lifecycle
   - Pending → Confirmed → Shipped → Delivered
   - Cannot ship unconfirmed
   - Cannot deliver unshipped

3. **TestOrderCancellationWorkflow** - Order cancellation
   - Cancel pending order
   - Cancel confirmed order
   - Cannot cancel shipped
   - Cannot cancel delivered

4. **TestMultipleOrdersWorkflow** - Multiple orders
   - Customer places multiple orders
   - Multiple customers with orders

---

## 🎓 Learning Path

### Level 1: Beginner
1. ✅ Run all tests: `pytest tests/`
2. ✅ Read test names and understand workflows
3. ✅ Run tests with verbose: `pytest -v tests/`

### Level 2: Intermediate
1. ✅ Read `test_user_workflows.py`
2. ✅ Understand each test's workflow comments
3. ✅ Run specific test: `pytest -v tests/functional/test_user_workflows.py`
4. ✅ Run specific class: `pytest -v tests/functional/test_user_workflows.py::TestUserSignupWorkflow`

### Level 3: Advanced
1. ✅ Read `test_order_workflows.py`
2. ✅ Understand fixtures and how they work
3. ✅ Modify a test and run it
4. ✅ Add a new test for a workflow

---

## ✨ Key Concepts Demonstrated

### 1. Fixtures (Setup/Teardown)
```python
@pytest.fixture
def user_service():
    """Fresh user service for each test"""
    return UserService()

def test_something(user_service):  # Injected automatically
    user_service.register(...)
```

### 2. Workflow Comments
```python
def test_complete_checkout_workflow(self, order_service, logged_in_user):
    """
    WORKFLOW:
    1. User adds items to order
    2. User creates order
    3. User confirms order
    4. Order is confirmed
    """
```

### 3. Testing Exceptions
```python
def test_login_with_wrong_password(self, user_service, registered_user):
    with pytest.raises(InvalidCredentialsError, match="Invalid"):
        user_service.login("email", "wrong_password")
```

### 4. State Transitions
```python
def test_order_lifecycle(self, order_service, logged_in_user):
    order = order_service.create_order(...)        # PENDING
    order = order_service.confirm_order(...)       # CONFIRMED
    order = order_service.ship_order(...)          # SHIPPED
    order = order_service.deliver_order(...)       # DELIVERED
```

---

## 🔍 Analyzing Test Results

### Running Tests with Different Options

**Basic:**
```bash
pytest tests/
```

**Verbose (see all test names):**
```bash
pytest -v tests/
```

**Very Verbose (see assert details):**
```bash
pytest -vv tests/
```

**Show Summary:**
```bash
pytest --tb=short tests/
```

**Stop on First Failure:**
```bash
pytest -x tests/
```

**Run Specific Class:**
```bash
pytest tests/functional/test_user_workflows.py::TestUserSignupWorkflow -v
```

**Run Specific Test:**
```bash
pytest tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_complete_signup_and_login_workflow -v
```

---

## 📝 Understanding Test Structure

### Class-Based Tests
```python
class TestUserSignupWorkflow:
    """Organizes related tests together"""

    def test_complete_signup_and_login_workflow(self, user_service):
        """Each method is a test"""
        ...
```

### Fixtures
```python
@pytest.fixture
def user_service():
    """Setup code - runs before each test"""
    return UserService()

@pytest.fixture
def registered_user(user_service):
    """Can depend on other fixtures"""
    return user_service.register(...)

# Used in tests:
def test_something(self, registered_user):
    # registered_user is automatically created
    ...
```

---

## 🎯 Exercises

### Exercise 1: Run All Tests
```bash
pytest tests/ -v
# Should show 27 passed tests
```

### Exercise 2: Run Specific Workflow
```bash
pytest tests/functional/test_user_workflows.py::TestUserSignupWorkflow -v
# Should show 3 tests in signup workflow
```

### Exercise 3: Add a New Test
Edit `tests/functional/test_user_workflows.py` and add:

```python
def test_signup_with_long_name(self, user_service):
    """WORKFLOW: User signs up with very long name"""
    user = user_service.register(
        email="john@example.com",
        name="A" * 100,  # Very long name
        password="SecurePass123"
    )
    assert len(user.name) == 100
```

Run it:
```bash
pytest tests/functional/test_user_workflows.py::TestUserSignupWorkflow::test_signup_with_long_name -v
```

### Exercise 4: Modify a Test
Edit `tests/functional/test_order_workflows.py`:

Change the laptop price and rerun:
```python
Item(item_id=1, name="Laptop", price=1299.99, quantity=1),  # Changed from 999.99
```

Run test:
```bash
pytest tests/functional/test_order_workflows.py::TestSimpleCheckoutWorkflow::test_complete_checkout_workflow -v
```

### Exercise 5: Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=term-missing
# Should show near 100% coverage since functional tests exercise complete workflows
```

---

## 🐛 Troubleshooting

### Error: "No module named src"
```bash
# Make sure you're in the project root
pwd
# Should show: .../functional_test_example

# Then run
pytest tests/
```

### Error: "ImportError"
```bash
# Make sure __init__.py exists
ls src/__init__.py
ls tests/__init__.py

# If missing, create them:
touch src/__init__.py
touch tests/__init__.py
```

### Error: "ModuleNotFoundError"
```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Then run
pytest tests/
```

---

## 🎓 Key Takeaways

### Functional Tests
✓ Test complete workflows (not individual functions)
✓ Test from user perspective
✓ Test integration between components
✓ Verify business logic works end-to-end

### This Example
✓ Shows real workflows (signup, login, checkout)
✓ Demonstrates test organization (classes, fixtures)
✓ Shows exception testing
✓ Demonstrates state transitions

### Best Practices
✓ Use fixtures for setup/teardown
✓ Write workflow comments
✓ Test both success and failure paths
✓ Test edge cases and validations

---

## 📚 Test Count

- **User Workflows:** 10 tests
- **Order Workflows:** 17 tests
- **Total:** 27 functional tests

All tests together exercise complete user and order workflows!

---

## 🚀 Next Steps

1. **Run tests:** `pytest tests/ -v`
2. **Read tests:** Open `tests/functional/test_user_workflows.py`
3. **Understand workflows:** Read the WORKFLOW comments
4. **Add tests:** Create your own test workflows
5. **Run with coverage:** `pytest tests/ --cov=src --cov-report=html`

---

## 🎉 You're Ready!

You now understand:
- What functional tests are
- How to write them with pytest
- How to organize tests with fixtures
- How to test workflows end-to-end

**Start with:** `pytest tests/ -v`

Happy testing! 🧪
