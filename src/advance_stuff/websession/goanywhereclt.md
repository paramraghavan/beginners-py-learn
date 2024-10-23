I'll help you create a Python script to interact with GoAnywhere CLI. Here's how you can do it:

```python
import subprocess
import os
import logging


class GoAnywhereCLI:
    def __init__(self, cli_path, host, username, password=None, key_file=None):
        """
        Initialize GoAnywhere CLI wrapper
        
        Args:
            cli_path (str): Path to goanywherecli executable
            host (str): Target host address
            username (str): Username for authentication
            password (str, optional): Password for authentication
            key_file (str, optional): Path to private key file
        """
        self.cli_path = cli_path
        self.host = host
        self.username = username
        self.password = password
        self.key_file = key_file

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('GoAnywhere')

    def execute_command(self, command, args=None):
        """Execute a GoAnywhere CLI command"""
        base_cmd = [
            self.cli_path,
            '-server', self.host,
            '-user', self.username
        ]

        # Add authentication
        if self.password:
            base_cmd.extend(['-password', self.password])
        if self.key_file:
            base_cmd.extend(['-keyfile', self.key_file])

        # Add command and arguments
        base_cmd.append(command)
        if args:
            base_cmd.extend(args)

        try:
            result = subprocess.run(
                base_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            self.logger.info(f"Command executed successfully: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e.stderr}")
            raise

    def upload_file(self, local_path, remote_path):
        """Upload a file to the server"""
        return self.execute_command('-put', [local_path, remote_path])

    def download_file(self, remote_path, local_path):
        """Download a file from the server"""
        return self.execute_command('-get', [remote_path, local_path])

    def list_directory(self, remote_path='.'):
        """List contents of a directory"""
        return self.execute_command('-ls', [remote_path])

    def make_directory(self, remote_path):
        """Create a new directory"""
        return self.execute_command('-mkdir', [remote_path])

    def remove_file(self, remote_path):
        """Remove a file"""
        return self.execute_command('-rm', [remote_path])


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = GoAnywhereCLI(
        cli_path="C:/Program Files/GoAnywhere CLI/goanywherecli.exe",  # Adjust path as needed
        host="sftp.example.com",
        username="your_username",
        password="your_password"  # Or use key_file for key-based auth
    )

    try:
        # List directory contents
        print("Listing directory contents:")
        print(client.list_directory())

        # Upload a file
        print("Uploading file:")
        client.upload_file("local_file.txt", "/remote/path/file.txt")

        # Download a file
        print("Downloading file:")
        client.download_file("/remote/path/file.txt", "downloaded_file.txt")

    except Exception as e:
        print(f"Error: {str(e)}")

```

Here's how to use this code:

1. First, ensure you have GoAnywhere CLI installed on your system and note its installation path.

2. Adjust the paths and credentials in the example to match your setup:
    - Update the `cli_path` to point to your GoAnywhere CLI executable
    - Set the correct `host`, `username`, and authentication method (password or key file)

3. Basic operations you can perform:

```python
# Initialize the client
client = GoAnywhereCLI(
    cli_path="/path/to/goanywherecli",
    host="your.server.com",
    username="your_username",
    password="your_password"
)

# List files
client.list_directory()

# Upload a file
client.upload_file("local.txt", "/remote/path/file.txt")

# Download a file
client.download_file("/remote/file.txt", "local_copy.txt")
```