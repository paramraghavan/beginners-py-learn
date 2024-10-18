import paramiko
import socket
import threading
import os
import sys

# SFTP Server configuration
HOST = 'localhost'
PORT = 2222
USERNAME = 'user'
PASSWORD = 'password'

# Path for server's files
SERVER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sftp_root')

# Ensure the server directory exists
os.makedirs(SERVER_DIR, exist_ok=True)


class SFTPServer(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        if (username == USERNAME) and (password == PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


def handle_client(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(paramiko.RSAKey.generate(2048))
    server = SFTPServer()

    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        print("*** SSH negotiation failed.")
        return

    channel = transport.accept(20)
    if channel is None:
        print("*** No channel.")
        return

    print("*** Authenticated!")

    try:
        sftp_server = paramiko.SFTPServer(channel, SERVER_DIR)
        sftp_server.serve_forever()
    except Exception as e:
        print(f"*** SFTP server error: {str(e)}")
    finally:
        channel.close()


def start_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
    except Exception as e:
        print(f"*** Bind failed: {str(e)}")
        sys.exit(1)

    print(f"[*] Listening for connection on {HOST}:{PORT}")
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        print(f"[*] Got a connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == "__main__":
    start_server()