import paramiko
import schedule
import time
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import logging
import os
import threading
import socket

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
SFTP_HOST = 'localhost'
SFTP_PORT = 2222
SFTP_USERNAME = 'user'
SFTP_PASSWORD = 'password'
SFTP_DIRECTORY = '/path/to/sftp/directory'
TEAM_LEAD_EMAILS = ['lead1@example.com', 'lead2@example.com']
BATCH_WINDOW = 5  # minutes
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

# Global variables
parent_job_map = {}
file_status_map = {}
server_ready = threading.Event()

class SimpleServer(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        if (username == SFTP_USERNAME) and (password == SFTP_PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def send_email(subject, body):
    # ... [email sending function remains unchanged]

def check_sftp_connectivity():
    for attempt in range(MAX_RETRIES):
        try:
            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD, timeout=5)
            logging.info("SFTP connection successful")
            return True
        except (paramiko.ssh_exception.SSHException, socket.error) as e:
            logging.warning(f"SFTP connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                error_msg = f"SFTP connection failed after {MAX_RETRIES} attempts: {str(e)}"
                logging.error(error_msg)
                send_email("SFTP Connection Error", error_msg)
    return False

def get_new_files(start_time, end_time):
    new_files = []
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD)
            with ssh.open_sftp() as sftp:
                for filename in sftp.listdir(SFTP_DIRECTORY):
                    filepath = os.path.join(SFTP_DIRECTORY, filename)
                    file_attr = sftp.stat(filepath)
                    file_time = datetime.fromtimestamp(file_attr.st_mtime)
                    if start_time <= file_time < end_time:
                        new_files.append((filename, file_time))
        logging.info(f"Found {len(new_files)} new files")
    except Exception as e:
        error_msg = f"Error getting new files: {str(e)}"
        logging.error(error_msg)
        send_email("Error Getting New Files", error_msg)
    return new_files

def create_parent_job(files):
    # ... [function remains unchanged]

def add_file_to_status_map(filename, status='open'):
    # ... [function remains unchanged]

def update_file_status(filename, status):
    # ... [function remains unchanged]

def get_file_status(filename):
    # ... [function remains unchanged]

def process_new_files():
    if not check_sftp_connectivity():
        return

    now = datetime.now()
    start_time = now - timedelta(minutes=BATCH_WINDOW)
    new_files = get_new_files(start_time, now)

    if new_files:
        job_id = create_parent_job(new_files)
        for filename, file_time in new_files:
            add_file_to_status_map(filename)

def start_sftp_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((SFTP_HOST, SFTP_PORT))
        server_socket.listen(5)

        logging.info(f"SFTP server listening on {SFTP_HOST}:{SFTP_PORT}")
        server_ready.set()  # Signal that the server is ready

        while True:
            client, addr = server_socket.accept()
            logging.info(f"New connection from {addr}")

            transport = paramiko.Transport(client)
            transport.add_server_key(paramiko.RSAKey.generate(2048))
            server = SimpleServer()

            try:
                transport.start_server(server=server)
            except paramiko.SSHException:
                logging.error("SSH negotiation failed.")
                continue

            channel = transport.accept(20)
            if channel is None:
                logging.error("No channel.")
                continue

            logging.info("SFTP session established")
    except Exception as e:
        logging.error(f"Error in SFTP server: {str(e)}")
    finally:
        server_socket.close()

def main():
    # Start the SFTP server in a separate thread
    sftp_thread = threading.Thread(target=start_sftp_server)
    sftp_thread.daemon = True
    sftp_thread.start()

    # Wait for the SFTP server to start
    server_ready.wait()

    # Wait a bit more to ensure the server is fully operational
    time.sleep(2)

    schedule.every(5).minutes.do(process_new_files)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        error_msg = f"ftpmon crashed: {str(e)}"
        logging.error(error_msg)
        send_email("ftpmon Crash", error_msg)

if __name__ == "__main__":
    main()