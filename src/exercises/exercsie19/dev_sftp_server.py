import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import SFTPHandler
from pyftpdlib.servers import FTPServer
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# SFTP Server Configuration
SFTP_HOST = "127.0.0.1"
SFTP_PORT = 2222
SFTP_USERNAME = "user"
SFTP_PASSWORD = "password"
SFTP_DIRECTORY = os.path.expanduser("~/sftp_root")  # Use a directory in the user's home


def main():
    # Ensure the SFTP directory exists
    os.makedirs(SFTP_DIRECTORY, exist_ok=True)

    # Create a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions
    authorizer.add_user(SFTP_USERNAME, SFTP_PASSWORD, SFTP_DIRECTORY, perm='elradfmwM')

    # Instantiate a SFTPHandler with RSA host key
    handler = SFTPHandler
    handler.authorizer = authorizer

    # Define RSA host key path
    keyfile_path = os.path.expanduser('~/sftp_server_rsa.key')

    # Generate RSA key if it doesn't exist
    if not os.path.exists(keyfile_path):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(keyfile_path, 'wb') as keyfile:
            keyfile.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        logging.info(f"Generated RSA key: {keyfile_path}")

    handler.host_key = keyfile_path

    # Instantiate FTP server class and listen to 127.0.0.1:2222
    server = FTPServer((SFTP_HOST, SFTP_PORT), handler)

    # Start ftp server
    logging.info(f"SFTP Server is starting on {SFTP_HOST}:{SFTP_PORT}")
    logging.info(f"SFTP root directory: {SFTP_DIRECTORY}")
    logging.info(f"Username: {SFTP_USERNAME}, Password: {SFTP_PASSWORD}")
    server.serve_forever()


if __name__ == "__main__":
    main()