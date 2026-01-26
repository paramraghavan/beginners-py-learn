"""
Test file with path manipulation vulnerabilities
"""
import os
import sys
from pathlib import Path

# BAD: Path from command-line argument without validation
def read_user_file_bad1():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        return f.read()

# BAD: Path from environment variable without validation
def read_config_bad():
    config_path = os.getenv('CONFIG_PATH')
    with open(config_path, 'r') as f:
        return f.read()

# BAD: Path constructed with os.path.join from user input
def save_upload_bad(user_filename):
    base_dir = "/uploads"
    filepath = os.path.join(base_dir, user_filename)
    with open(filepath, 'w') as f:
        f.write("data")

# BAD: Path using f-string without validation
def delete_file_bad(filename):
    filepath = f"/data/{filename}"
    os.remove(filepath)

# BAD: Path concatenation
def read_data_bad(subdir):
    path = "/var/data/" + subdir + "/file.txt"
    with open(path, 'r') as f:
        return f.read()

# BAD: Creating Path from variable without validation
def process_file_bad(user_path):
    file_path = Path(user_path)
    with file_path.open('r') as f:
        return f.read()

# BAD: Using getenv in path construction
def load_config_bad():
    config_dir = os.getenv('CONFIG_DIR', '/etc')
    config_file = os.path.join(config_dir, 'app.conf')
    with open(config_file, 'r') as f:
        return f.read()

# BAD: Directory traversal with makedirs
def create_user_dir_bad(username):
    user_dir = os.path.join('/data/users', username)
    os.makedirs(user_dir, exist_ok=True)

# GOOD: Path with validation
def read_user_file_good(user_id):
    # Allowlist of valid user IDs
    ALLOWED_USERS = ['user1', 'user2', 'user3']
    
    if user_id not in ALLOWED_USERS:
        raise ValueError("Invalid user ID")
    
    filename = f"/data/users/{user_id}/data.txt"
    with open(filename, 'r') as f:
        return f.read()

# GOOD: Path with directory validation
def save_upload_good(user_filename):
    base_dir = Path("/uploads")
    
    # Sanitize filename
    safe_filename = os.path.basename(user_filename)
    
    # Prevent directory traversal
    if '..' in safe_filename or safe_filename.startswith('/'):
        raise ValueError("Invalid filename")
    
    filepath = base_dir / safe_filename
    
    # Verify resolved path is within base directory
    if not str(filepath.resolve()).startswith(str(base_dir.resolve())):
        raise ValueError("Path traversal detected")
    
    with filepath.open('w') as f:
        f.write("data")

# GOOD: Using allowlist for environment-based paths
def load_config_good():
    ENV = os.getenv('APP_ENV', 'dev').lower()
    
    ALLOWED_CONFIGS = {
        'dev': '/etc/app/dev.conf',
        'prod': '/etc/app/prod.conf',
        'test': '/etc/app/test.conf'
    }
    
    if ENV not in ALLOWED_CONFIGS:
        raise ValueError(f"Invalid environment: {ENV}")
    
    config_file = ALLOWED_CONFIGS[ENV]
    with open(config_file, 'r') as f:
        return f.read()
