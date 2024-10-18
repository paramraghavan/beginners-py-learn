'''
ftp localhost 2121
Username: user
Password: password
ftp> put /path/to/local/file.txt
ftp> quit
pip install pyftpdlib
You'll need to modify the ftpmon.py script to work with FTP instead of SFTP. This mainly
involves changing the paramiko SFTP client to a standard FTP client (you can use Python's built-in ftplib for this).
'''
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    # Create a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions
    authorizer.add_user('user', 'password', '/path/to/ftp/directory', perm='elradfmwMT')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "Welcome to the FTP server."

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 2121)
    server = FTPServer(address, handler)

    # Set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()