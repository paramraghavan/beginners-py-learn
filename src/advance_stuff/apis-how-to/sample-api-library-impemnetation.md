
# Building a User-Friendly REST API Client Library

A client library for a hypothetical **User Management API** that supports full CRUD operations.

## Sample REST API Endpoints 

```
Base URL: https://api.example.com/v1

GET    /users           - List all users
GET    /users/{id}      - Get user by ID
POST   /users           - Create new user
PUT    /users/{id}      - Update user
DELETE /users/{id}      - Delete user
GET    /users/search    - Search users by criteria
```

***

## Version 1: Without Encapsulation (Raw Implementation)

```python
import requests
import json

# User has to manage all HTTP details directly
base_url = "https://api.example.com/v1"
api_key = "your_api_key_here"

# Get all users - verbose and error-prone
response = requests.get(
    f"{base_url}/users",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
)

if response.status_code == 200:
    users = response.json()
else:
    print(f"Error: {response.status_code}")

# Create a user - must manually format everything
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}

response = requests.post(
    f"{base_url}/users",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    data=json.dumps(user_data)
)

if response.status_code == 201:
    new_user = response.json()
else:
    print(f"Error: {response.status_code}")

# Update user - repetitive code
response = requests.put(
    f"{base_url}/users/123",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    data=json.dumps({"age": 31})
)

# Delete user
response = requests.delete(
    f"{base_url}/users/123",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
)
```

**Problems:**
- User must manually construct URLs
- Headers repeated in every request
- No error handling or retry logic
- Must remember status codes
- No validation or type safety
- Hard to test and maintain

***

## Version 2: With Encapsulation (Production-Ready Client Library)

```python
"""
User Management API Client Library
===================================
A user-friendly wrapper for the User Management REST API.

Example Usage:
    from user_api import UserAPIClient
    
    client = UserAPIClient(api_key="your_key")
    
    # Simple, clean operations
    users = client.users.list()
    user = client.users.get(123)
    new_user = client.users.create(name="John", email="john@example.com")
"""

import requests
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import time
import logging


# ============================================================================
# DATA MODELS - Clean Python objects for API data
# ============================================================================

@dataclass
class User:
    """
    Represents a User resource.
    Users don't see raw JSON - they work with Python objects.
    """
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    age: Optional[int] = None
    status: str = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            k: v for k, v in self.__dict__.items() 
            if v is not None and k not in ['id', 'created_at', 'updated_at']
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User from API response."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


class HTTPMethod(Enum):
    """Supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


# ============================================================================
# CUSTOM EXCEPTIONS - Clear error handling
# ============================================================================

class APIError(Exception):
    """Base exception for all API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response: Optional[requests.Response] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Raised when authentication fails (401)."""
    pass


class NotFoundError(APIError):
    """Raised when resource not found (404)."""
    pass


class ValidationError(APIError):
    """Raised when request validation fails (400)."""
    pass


class RateLimitError(APIError):
    """Raised when rate limit exceeded (429)."""
    pass


# ============================================================================
# BASE CLIENT - Handles all HTTP communication
# ============================================================================

class BaseClient:
    """
    Low-level HTTP client.
    Private class - users never interact with this directly.
    """
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self._base_url = base_url.rstrip('/')  # Private - implementation detail
        self._api_key = api_key                # Private
        self._timeout = timeout                # Private
        self._session = requests.Session()    # Private - connection pooling
        self._logger = logging.getLogger(__name__)
        
        # Set default headers once
        self._session.headers.update({
            'Authorization': f'Bearer {self._api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'UserAPI-Python-Client/1.0'
        })
    
    def _build_url(self, endpoint: str) -> str:
        """Private helper - construct full URL."""
        return f"{self._base_url}/{endpoint.lstrip('/')}"
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        Private helper - handle HTTP response and errors.
        Converts HTTP status codes into meaningful exceptions.
        """
        # Success responses
        if 200 <= response.status_code < 300:
            if response.status_code == 204:  # No content
                return None
            try:
                return response.json()
            except ValueError:
                return response.text
        
        # Error responses - convert to specific exceptions
        try:
            error_data = response.json()
            error_message = error_data.get('message', response.text)
        except ValueError:
            error_message = response.text
        
        if response.status_code == 400:
            raise ValidationError(error_message, response.status_code, response)
        elif response.status_code == 401:
            raise AuthenticationError(error_message, response.status_code, response)
        elif response.status_code == 404:
            raise NotFoundError(error_message, response.status_code, response)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response.status_code, response)
        else:
            raise APIError(error_message, response.status_code, response)
    
    def _request(self, method: HTTPMethod, endpoint: str, 
                 data: Optional[Dict] = None, 
                 params: Optional[Dict] = None,
                 retry: int = 3) -> Any:
        """
        Private method - make HTTP request with retry logic.
        
        This encapsulates:
        - URL construction
        - Request execution
        - Error handling
        - Retry logic for transient failures
        """
        url = self._build_url(endpoint)
        
        for attempt in range(retry):
            try:
                self._logger.debug(f"{method.value} {url}")
                
                response = self._session.request(
                    method=method.value,
                    url=url,
                    json=data,
                    params=params,
                    timeout=self._timeout
                )
                
                return self._handle_response(response)
                
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt == retry - 1:  # Last attempt
                    raise APIError(f"Connection failed after {retry} attempts: {str(e)}")
                
                # Exponential backoff
                wait_time = 2 ** attempt
                self._logger.warning(f"Request failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            
            except RateLimitError as e:
                if attempt == retry - 1:
                    raise
                
                # Respect rate limits
                wait_time = 60
                self._logger.warning(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
    
    def close(self):
        """Close the HTTP session."""
        self._session.close()


# ============================================================================
# RESOURCE CLASSES - High-level API for specific resources
# ============================================================================

class UserResource:
    """
    User resource manager - provides clean CRUD operations.
    This is what users interact with - simple, intuitive methods.
    """
    
    def __init__(self, client: BaseClient):
        self._client = client  # Private - holds reference to base client
    
    def list(self, page: int = 1, per_page: int = 20) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
        
        Returns:
            List of User objects
        
        Example:
            users = client.users.list()
            for user in users:
                print(user.name)
        """
        params = {'page': page, 'per_page': per_page}
        response = self._client._request(HTTPMethod.GET, '/users', params=params)
        
        # Convert raw JSON to User objects
        return [User.from_dict(user_data) for user_data in response.get('data', [])]
    
    def get(self, user_id: int) -> User:
        """
        Get a specific user by ID.
        
        Args:
            user_id: The user's ID
        
        Returns:
            User object
        
        Raises:
            NotFoundError: If user doesn't exist
        
        Example:
            user = client.users.get(123)
            print(f"Name: {user.name}, Email: {user.email}")
        """
        response = self._client._request(HTTPMethod.GET, f'/users/{user_id}')
        return User.from_dict(response)
    
    def create(self, name: str, email: str, age: Optional[int] = None, 
               status: str = 'active') -> User:
        """
        Create a new user.
        
        Args:
            name: User's full name
            email: User's email address
            age: User's age (optional)
            status: User status (default: 'active')
        
        Returns:
            Created User object with ID populated
        
        Raises:
            ValidationError: If input validation fails
        
        Example:
            new_user = client.users.create(
                name="Jane Doe",
                email="jane@example.com",
                age=28
            )
            print(f"Created user with ID: {new_user.id}")
        """
        # Client-side validation
        if not email or '@' not in email:
            raise ValidationError("Invalid email address")
        
        user = User(name=name, email=email, age=age, status=status)
        response = self._client._request(HTTPMethod.POST, '/users', data=user.to_dict())
        return User.from_dict(response)
    
    def update(self, user_id: int, **kwargs) -> User:
        """
        Update an existing user.
        
        Args:
            user_id: The user's ID
            **kwargs: Fields to update (name, email, age, status)
        
        Returns:
            Updated User object
        
        Example:
            updated = client.users.update(123, age=31, status='inactive')
        """
        response = self._client._request(HTTPMethod.PUT, f'/users/{user_id}', data=kwargs)
        return User.from_dict(response)
    
    def delete(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: The user's ID
        
        Returns:
            True if successful
        
        Example:
            if client.users.delete(123):
                print("User deleted successfully")
        """
        self._client._request(HTTPMethod.DELETE, f'/users/{user_id}')
        return True
    
    def search(self, query: str, status: Optional[str] = None) -> List[User]:
        """
        Search users by name or email.
        
        Args:
            query: Search term
            status: Filter by status (optional)
        
        Returns:
            List of matching User objects
        
        Example:
            results = client.users.search("john", status="active")
        """
        params = {'q': query}
        if status:
            params['status'] = status
        
        response = self._client._request(HTTPMethod.GET, '/users/search', params=params)
        return [User.from_dict(user_data) for user_data in response.get('data', [])]


# ============================================================================
# MAIN API CLIENT - This is what users import and use
# ============================================================================

class UserAPIClient:
    """
    Main entry point for the User Management API.
    
    This class provides a simple, clean interface to all API operations.
    All complexity is hidden - users just work with Python objects.
    
    Example:
        # Initialize once
        client = UserAPIClient(api_key="your_api_key")
        
        # All operations are simple and intuitive
        users = client.users.list()
        user = client.users.get(123)
        new_user = client.users.create(name="John", email="john@example.com")
        client.users.update(123, age=31)
        client.users.delete(123)
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.example.com/v1",
                 timeout: int = 30):
        """
        Initialize the API client.
        
        Args:
            api_key: Your API authentication key
            base_url: API base URL (default: production URL)
            timeout: Request timeout in seconds (default: 30)
        """
        if not api_key:
            raise ValueError("API key is required")
        
        # Private base client handles all HTTP
        self._base_client = BaseClient(base_url, api_key, timeout)
        
        # Public resource managers - users interact with these
        self.users = UserResource(self._base_client)
        
        # Can easily add more resources:
        # self.orders = OrderResource(self._base_client)
        # self.products = ProductResource(self._base_client)
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources."""
        self.close()
    
    def close(self):
        """Close the client and clean up connections."""
        self._base_client.close()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Setup logging to see what's happening
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("USER API CLIENT - USAGE EXAMPLES")
    print("=" * 70)
    
    # Initialize client - simple one-liner
    client = UserAPIClient(api_key="demo_api_key_12345")
    
    print("\n1️⃣  LIST ALL USERS")
    print("-" * 70)
    try:
        users = client.users.list(page=1, per_page=10)
        print(f"✓ Retrieved {len(users)} users")
        for user in users[:3]:  # Show first 3
            print(f"  - {user.name} ({user.email})")
    except APIError as e:
        print(f"✗ Error: {e.message}")
    
    print("\n2️⃣  GET SPECIFIC USER")
    print("-" * 70)
    try:
        user = client.users.get(123)
        print(f"✓ Found user: {user.name}")
        print(f"  Email: {user.email}")
        print(f"  Age: {user.age}")
        print(f"  Status: {user.status}")
    except NotFoundError:
        print("✗ User not found")
    except APIError as e:
        print(f"✗ Error: {e.message}")
    
    print("\n3️⃣  CREATE NEW USER")
    print("-" * 70)
    try:
        new_user = client.users.create(
            name="Alice Johnson",
            email="alice@example.com",
            age=27
        )
        print(f"✓ Created user with ID: {new_user.id}")
        print(f"  Name: {new_user.name}")
        print(f"  Email: {new_user.email}")
    except ValidationError as e:
        print(f"✗ Validation error: {e.message}")
    except APIError as e:
        print(f"✗ Error: {e.message}")
    
    print("\n4️⃣  UPDATE USER")
    print("-" * 70)
    try:
        updated = client.users.update(123, age=31, status="premium")
        print(f"✓ Updated user {updated.id}")
        print(f"  New age: {updated.age}")
        print(f"  New status: {updated.status}")
    except APIError as e:
        print(f"✗ Error: {e.message}")
    
    print("\n5️⃣  SEARCH USERS")
    print("-" * 70)
    try:
        results = client.users.search("john", status="active")
        print(f"✓ Found {len(results)} matching users")
        for user in results:
            print(f"  - {user.name} ({user.email})")
    except APIError as e:
        print(f"✗ Error: {e.message}")
    
    print("\n6️⃣  DELETE USER")
    print("-" * 70)
    try:
        success = client.users.delete(123)
        if success:
            print("✓ User deleted successfully")
    except NotFoundError:
        print("✗ User not found")
    except APIError as e:
        print(f"✗ Error: {e.message}")
    
    print("\n7️⃣  CONTEXT MANAGER USAGE")
    print("-" * 70)
    with UserAPIClient(api_key="demo_key") as client:
        users = client.users.list()
        print(f"✓ Retrieved {len(users)} users")
    print("✓ Client automatically closed")
    
    print("\n8️⃣  ERROR HANDLING")
    print("-" * 70)
    try:
        # Invalid email triggers validation
        client.users.create(name="Bad User", email="not-an-email")
    except ValidationError as e:
        print(f"✓ Caught validation error: {e.message}")
    
    # Clean up
    client.close()
    print("\n" + "=" * 70)
    print("✓ All examples completed!")
    print("=" * 70)
```

***

## Key Implementation Techniques

### 1. **Private Methods and Attributes**

```python
class BaseClient:
    def __init__(self, api_key):
        self._api_key = api_key         # _prefix = internal use only
        self._session = requests.Session()
    
    def _request(self, method, url):    # Private helper method
        # Implementation details hidden
        pass
```

**Note:** Single underscore (`_`) is Python's convention for "internal use" - signals to developers not to access directly.

### 2. **Layered Architecture**

```
User's Code
    ↓
UserAPIClient (Public API - simple interface)
    ↓
UserResource (Business logic - CRUD operations)
    ↓
BaseClient (HTTP details - requests, errors, retries)
    ↓
REST API
```

Each layer encapsulates complexity from the layer above.

### 3. **Data Transfer Objects (DTOs)**

```python
@dataclass
class User:
    """Clean Python object - users never see raw JSON"""
    name: str
    email: str
    
    @classmethod
    def from_dict(cls, data):
        """Private conversion from API response"""
        return cls(**data)
```

### 4. **Custom Exceptions**

```python
class NotFoundError(APIError):
    """Specific error types make handling easier"""
    pass

# User can catch specific errors
try:
    user = client.users.get(999)
except NotFoundError:
    print("User doesn't exist")
```

### 5. **Context Manager Support**

```python
def __enter__(self):
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    self.close()

# Clean resource management
with UserAPIClient(api_key="key") as client:
    users = client.users.list()
# Automatically closes
```

***

## Comparison: Before vs After

| Aspect | Without Encapsulation | With Encapsulation |
|--------|----------------------|-------------------|
| **Creating a user** | 15 lines, manual JSON | 1 line: `client.users.create(...)` |
| **Error handling** | Check status codes manually | Automatic exceptions with clear types |
| **Authentication** | Repeated in every call | Configured once at init |
| **Retry logic** | Must implement yourself | Built-in, transparent |
| **Type safety** | Raw dictionaries | Typed User objects |
| **Testability** | Hard to mock HTTP calls | Easy to mock resource classes |
| **Documentation** | Must refer to API docs | Self-documenting with docstrings |

***

## Benefits for Other Teams

1. **Simple to use**: `client.users.create(name="John", email="john@example.com")`
2. **No HTTP knowledge needed**: Teams don't think about URLs, headers, or status codes
3. **Type safety**: Work with `User` objects, not raw JSON
4. **Clear errors**: Specific exceptions like `NotFoundError`, not generic HTTP errors
5. **Built-in features**: Retry logic, connection pooling, rate limiting—all transparent
6. **Easy to test**: Mock `UserResource`, not HTTP calls
7. **Self-documenting**: Docstrings and type hints explain everything

This is **encapsulation at its best**—hiding all REST API complexity behind a clean, Pythonic interface! 🎯

[1](https://www.reddit.com/r/Python/comments/vty3sx/any_design_patterns_and_tips_on_writing_an_api/)
[2](https://benhoyt.com/writings/python-api-design/)
[3](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
[4](https://vineeth.io/posts/sdk-development)
[5](http://bhomnick.net/design-pattern-python-api-client/)
[6](https://realpython.com/primer-on-python-decorators/)
[7](https://realpython.com/api-integration-in-python/)
[8](https://stackoverflow.com/questions/64859702/wrapper-for-an-encapsulated-function)
[9](https://stackoverflow.com/questions/58140435/how-to-organize-python-api-module-to-make-it-neat)
[10](https://www.reddit.com/r/Python/comments/u7vquv/how_to_write_a_python3_wrapper_librarymodule_for/)
[11](https://blog.wahab2.com/api-architecture-best-practices-for-designing-rest-apis-bf907025f5f)
[12](https://refactoring.guru/design-patterns/python)
[13](https://betterprogramming.pub/design-pattern-gateways-in-python-for-nice-services-and-not-nice-services-95e6c867cc1b)
[14](https://www.youtube.com/watch?v=l_7ZpHE4EEY)
[15](https://github.com/ardydedase/apiwrapper)