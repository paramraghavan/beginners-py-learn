"""Functional Tests for User Management Workflows"""

import pytest
from src.user import UserService, UserAlreadyExistsError, InvalidCredentialsError


@pytest.fixture
def user_service():
    """Fresh user service for each test"""
    return UserService()


class TestUserSignupWorkflow:
    """FUNCTIONAL TEST: Complete user signup workflow"""

    def test_complete_signup_and_login_workflow(self, user_service):
        """
        WORKFLOW:
        1. User signs up with email, name, password
        2. System validates and stores user
        3. User logs in with credentials
        4. System authenticates user
        """
        # Step 1: User signs up
        user = user_service.register(
            email="john@example.com",
            name="John Doe",
            password="SecurePass123"
        )

        # Step 2: Verify user created
        assert user.user_id > 0
        assert user.email == "john@example.com"
        assert user.name == "John Doe"
        assert user.is_active is True

        # Step 3: User logs in
        logged_in_user = user_service.login("john@example.com", "SecurePass123")

        # Step 4: Verify login succeeded
        assert logged_in_user.user_id == user.user_id
        assert logged_in_user.email == "john@example.com"

    def test_signup_with_invalid_email(self, user_service):
        """WORKFLOW: User attempts signup with invalid email"""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.register(
                email="invalid-email",
                name="John Doe",
                password="SecurePass123"
            )

    def test_signup_with_weak_password(self, user_service):
        """WORKFLOW: User attempts signup with weak password"""
        with pytest.raises(ValueError, match="Password must be"):
            user_service.register(
                email="john@example.com",
                name="John Doe",
                password="weak"  # Too short, no uppercase/number
            )

    def test_signup_duplicate_email(self, user_service):
        """WORKFLOW: User attempts to signup with existing email"""
        # First signup succeeds
        user_service.register(
            email="john@example.com",
            name="John Doe",
            password="SecurePass123"
        )

        # Second signup with same email fails
        with pytest.raises(UserAlreadyExistsError):
            user_service.register(
                email="john@example.com",
                name="John Smith",
                password="SecurePass456"
            )


class TestUserLoginWorkflow:
    """FUNCTIONAL TEST: Complete login workflows"""

    @pytest.fixture
    def registered_user(self, user_service):
        """Register a user for login tests"""
        return user_service.register(
            email="alice@example.com",
            name="Alice",
            password="TestPass123"
        )

    def test_successful_login(self, user_service, registered_user):
        """
        WORKFLOW:
        1. User provides email and password
        2. System validates credentials
        3. System returns authenticated user
        """
        user = user_service.login("alice@example.com", "TestPass123")

        assert user.user_id == registered_user.user_id
        assert user.email == "alice@example.com"
        assert user.is_active is True

    def test_login_with_wrong_password(self, user_service, registered_user):
        """WORKFLOW: User attempts login with wrong password"""
        with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
            user_service.login("alice@example.com", "WrongPassword")

    def test_login_with_nonexistent_email(self, user_service):
        """WORKFLOW: User attempts login with unregistered email"""
        with pytest.raises(InvalidCredentialsError):
            user_service.login("nonexistent@example.com", "SomePassword123")

    def test_login_with_deactivated_account(self, user_service, registered_user):
        """
        WORKFLOW:
        1. User account is deactivated
        2. User attempts to login
        3. System denies access
        """
        user_service.deactivate_account(registered_user.user_id)

        with pytest.raises(InvalidCredentialsError, match="User account is inactive"):
            user_service.login("alice@example.com", "TestPass123")


class TestUserProfileWorkflow:
    """FUNCTIONAL TEST: User profile management workflows"""

    @pytest.fixture
    def authenticated_user(self, user_service):
        """Register and return authenticated user"""
        user = user_service.register(
            email="bob@example.com",
            name="Bob Smith",
            password="TestPass123"
        )
        return user_service.login("bob@example.com", "TestPass123")

    def test_update_profile_after_signup(self, user_service, authenticated_user):
        """
        WORKFLOW:
        1. User is authenticated
        2. User updates their profile (name)
        3. System persists the change
        """
        # User updates their name
        updated_user = user_service.update_profile(
            authenticated_user.user_id,
            "Robert Smith"
        )

        # Verify change persisted
        assert updated_user.name == "Robert Smith"
        assert updated_user.user_id == authenticated_user.user_id

        # Verify change is permanent (fetch user again)
        fetched_user = user_service.get_user(authenticated_user.user_id)
        assert fetched_user.name == "Robert Smith"

    def test_account_deactivation_workflow(self, user_service, authenticated_user):
        """
        WORKFLOW:
        1. User is authenticated
        2. User deactivates account
        3. User cannot login anymore
        """
        user_id = authenticated_user.user_id

        # User deactivates account
        user_service.deactivate_account(user_id)

        # Verify account is deactivated
        user = user_service.get_user(user_id)
        assert user.is_active is False

        # User cannot login
        with pytest.raises(InvalidCredentialsError):
            user_service.login("bob@example.com", "TestPass123")


class TestMultipleUserWorkflow:
    """FUNCTIONAL TEST: Multiple users interacting"""

    def test_two_users_can_signup_and_login(self, user_service):
        """
        WORKFLOW:
        1. User A signs up
        2. User B signs up
        3. User A logs in
        4. User B logs in
        5. Both have separate accounts
        """
        # User A signs up
        user_a = user_service.register(
            email="alice@example.com",
            name="Alice",
            password="AlicePass123"
        )

        # User B signs up
        user_b = user_service.register(
            email="bob@example.com",
            name="Bob",
            password="BobPass123"
        )

        # User A logs in
        alice_session = user_service.login("alice@example.com", "AlicePass123")
        assert alice_session.name == "Alice"

        # User B logs in
        bob_session = user_service.login("bob@example.com", "BobPass123")
        assert bob_session.name == "Bob"

        # Verify they are different users
        assert alice_session.user_id != bob_session.user_id
        assert alice_session.email != bob_session.email
