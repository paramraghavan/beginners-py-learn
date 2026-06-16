"""User Management Module"""

import re
from typing import Dict, Optional


class UserAlreadyExistsError(Exception):
    """Raised when user already exists"""
    pass


class InvalidCredentialsError(Exception):
    """Raised when credentials are invalid"""
    pass


class User:
    """User model"""

    def __init__(self, user_id: int, email: str, name: str, password: str):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.is_active = True


class UserService:
    """Service for managing users"""

    def __init__(self):
        self.users: Dict[int, User] = {}
        self.email_index: Dict[str, int] = {}
        self._next_id = 1

    def register(self, email: str, name: str, password: str) -> User:
        """Register a new user

        Args:
            email: User email
            name: User name
            password: User password

        Returns:
            User object

        Raises:
            UserAlreadyExistsError: If email already registered
            ValueError: If email or password invalid
        """
        # Validate email
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        # Validate password
        if not self._is_valid_password(password):
            raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and number")

        # Check if user exists
        if email in self.email_index:
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        # Create user
        user = User(self._next_id, email, name, password)
        self.users[self._next_id] = user
        self.email_index[email] = self._next_id
        self._next_id += 1

        return user

    def login(self, email: str, password: str) -> User:
        """Authenticate user

        Args:
            email: User email
            password: User password

        Returns:
            User object if authentication succeeds

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        if email not in self.email_index:
            raise InvalidCredentialsError("Invalid email or password")

        user_id = self.email_index[email]
        user = self.users[user_id]

        if user.password != password:
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive")

        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID

        Args:
            user_id: User ID

        Returns:
            User object or None if not found
        """
        return self.users.get(user_id)

    def update_profile(self, user_id: int, name: str) -> User:
        """Update user profile

        Args:
            user_id: User ID
            name: New name

        Returns:
            Updated user object

        Raises:
            ValueError: If user not found
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")

        user = self.users[user_id]
        user.name = name
        return user

    def deactivate_account(self, user_id: int) -> None:
        """Deactivate user account

        Args:
            user_id: User ID
        """
        if user_id in self.users:
            self.users[user_id].is_active = False

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def _is_valid_password(password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_lower and has_digit


# Global instance
user_service = UserService()
