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

# Path for server's files and host key
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(SCRIPT_DIR, 'sftp_root')
HOST_KEY_FILE = os.path.join(SCRIPT_DIR, 'sftp_host_key')

# Ensure the server directory exists
os.makedirs(SERVER_DIR, exist_ok=True)


def generate_host_key():
    if not os.path.exists(HOST_KEY_FILE):
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(HOST_KEY_FILE)
    else:
        key = paramiko.RSAKey(filename=HOST_KEY_FILE)
    return key


class SFTPHandler(paramiko.SFTPServerInterface):
    def __init__(self, server, *largs, **kwargs):
        super().__init__(server, *largs, **kwargs)

    def list_folder(self, path):
        try:
            return super().list_folder(path)
        except IOError:
            return []


class SFTPServer(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        if (username == USERNAME) and (password == PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


def handle_client(client_socket, host_key):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)
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
        sftp_handler = SFTPHandler(server)
        sftp_server = paramiko.SFTPServer(channel, SERVER_DIR, sftp_si=sftp_handler)
        sftp_server.serve_forever()
    except Exception as e:
        print(f"*** SFTP server error: {str(e)}")
    finally:
        channel.close()


def start_server():
    host_key = generate_host_key()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
    except Exception as e:
        print(f"*** Bind failed: {str(e)}")
        sys.exit(1)

    print(f"[*] Listening for connection on {HOST}:{PORT}")
    print(f"[*] Host key fingerprint is: {host_key.get_fingerprint().hex()}")
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        print(f"[*] Got a connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client, host_key))
        client_handler.start()


if __name__ == "__main__":
    start_server()