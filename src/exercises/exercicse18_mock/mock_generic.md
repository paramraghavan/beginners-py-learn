Create a more generic mock connection class that can handle various types of data sources including
databases, AWS services (S3, Lambda), REST APIs, and more. This approach will use a factory pattern to create specific
connection types.

```python
from abc import ABC, abstractmethod
from typing import Dict, Any


class MockConnection(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def execute(self, command: str) -> Any:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class MockDatabaseConnection(MockConnection):
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def connect(self) -> bool:
        print(f"Connecting to database: {self.config['database']}")
        return True

    def execute(self, query: str) -> Any:
        print(f"Executing query: {query}")
        return [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Doe"}]

    def close(self) -> None:
        print("Closing database connection")


class MockS3Connection(MockConnection):
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def connect(self) -> bool:
        print(f"Connecting to S3 bucket: {self.config['bucket']}")
        return True

    def execute(self, command: str) -> Any:
        print(f"Executing S3 command: {command}")
        return {"file1.txt": "content1", "file2.txt": "content2"}

    def close(self) -> None:
        print("Closing S3 connection")


class MockLambdaConnection(MockConnection):
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def connect(self) -> bool:
        print(f"Connecting to Lambda function: {self.config['function_name']}")
        return True

    def execute(self, payload: str) -> Any:
        print(f"Invoking Lambda function with payload: {payload}")
        return {"statusCode": 200, "body": "Function executed successfully"}

    def close(self) -> None:
        print("Closing Lambda connection")


class MockRestApiConnection(MockConnection):
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def connect(self) -> bool:
        print(f"Connecting to REST API: {self.config['base_url']}")
        return True

    def execute(self, endpoint: str) -> Any:
        print(f"Making API request to: {endpoint}")
        return {"data": [{"id": 1, "name": "Product 1"}, {"id": 2, "name": "Product 2"}]}

    def close(self) -> None:
        print("Closing REST API connection")


class MockConnectionFactory:
    @staticmethod
    def create_connection(conn_type: str, config: Dict[str, str]) -> MockConnection:
        if conn_type == "database":
            return MockDatabaseConnection(config)
        elif conn_type == "s3":
            return MockS3Connection(config)
        elif conn_type == "lambda":
            return MockLambdaConnection(config)
        elif conn_type == "rest_api":
            return MockRestApiConnection(config)
        else:
            raise ValueError(f"Unsupported connection type: {conn_type}")


# Example usage
if __name__ == "__main__":
    # Database connection
    db_config = {"database": "test_db", "user": "test_user", "password": "test_pass"}
    db_conn = MockConnectionFactory.create_connection("database", db_config)
    db_conn.connect()
    result = db_conn.execute("SELECT * FROM users")
    print(result)
    db_conn.close()

    # S3 connection
    s3_config = {"bucket": "test-bucket", "region": "us-west-2"}
    s3_conn = MockConnectionFactory.create_connection("s3", s3_config)
    s3_conn.connect()
    files = s3_conn.execute("LIST_FILES")
    print(files)
    s3_conn.close()

    # Lambda connection
    lambda_config = {"function_name": "test-function", "region": "us-east-1"}
    lambda_conn = MockConnectionFactory.create_connection("lambda", lambda_config)
    lambda_conn.connect()
    response = lambda_conn.execute('{"key": "value"}')
    print(response)
    lambda_conn.close()

    # REST API connection
    api_config = {"base_url": "https://api.example.com/v1"}
    api_conn = MockConnectionFactory.create_connection("rest_api", api_config)
    api_conn.connect()
    data = api_conn.execute("/products")
    print(data)
    api_conn.close()

```

This generic mock connection system provides a flexible framework for creating mock connections to various data sources.
Here's a breakdown of the key components:

1. `MockConnection`: An abstract base class that defines the interface for all mock connections.

2. Specific mock connection classes (e.g., `MockDatabaseConnection`, `MockS3Connection`, etc.): These implement the
   `MockConnection` interface for different types of data sources.

3. `MockConnectionFactory`: A factory class that creates the appropriate mock connection based on the connection type.

The system is designed to be easily extensible. To add support for a new type of connection:

1. Create a new class that inherits from `MockConnection`.
2. Implement the `connect()`, `execute()`, and `close()` methods.
3. Add a new condition in the `MockConnectionFactory.create_connection()` method to return an instance of your new
   class.

This mock system allows you to simulate various connection types in your tests or development environment without
actually connecting to real services. You can customize the behavior of each mock connection type to suit your specific
testing needs.

Would you like me to explain any part of this system in more detail or show how to extend it for a specific use case?