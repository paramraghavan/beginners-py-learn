import paramiko
import schedule
import time
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import logging
import os
import threading
from paramiko import SFTPServer, ServerInterface, AUTH_SUCCESSFUL, OPEN_SUCCEEDED

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

# Global variables
parent_job_map = {}
file_status_map = {}

class SimpleServer(ServerInterface):
    def check_auth_password(self, username, password):
        if (username == SFTP_USERNAME) and (password == SFTP_PASSWORD):
            return AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'ftpmon@example.com'
    msg['To'] = ', '.join(TEAM_LEAD_EMAILS)

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('ftpmon@example.com', 'email_password')
            server.send_message(msg)
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

def check_sftp_connectivity():
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD)
        logging.info("SFTP connection successful")
        return True
    except Exception as e:
        error_msg = f"SFTP connection failed: {str(e)}"
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
    job_id = f"job_{int(time.time())}"
    parent_job_map[job_id] = files
    logging.info(f"Created parent job {job_id} with {len(files)} files")
    return job_id

def add_file_to_status_map(filename, status='open'):
    file_status_map[filename] = {'filename': filename, 'status': status}
    logging.info(f"Added file {filename} to status map with status {status}")

def update_file_status(filename, status):
    if filename in file_status_map:
        file_status_map[filename]['status'] = status
        logging.info(f"Updated status of file {filename} to {status}")
    else:
        logging.warning(f"File {filename} not found in status map")

def get_file_status(filename):
    return file_status_map.get(filename, {}).get('status', 'unknown')

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
    server_socket = paramiko.Transport(('localhost', SFTP_PORT))
    server_socket.add_server_key(paramiko.RSAKey.generate(2048))
    server = SimpleServer()
    try:
        server_socket.start_server(server=server)
    except Exception as e:
        logging.error(f'*** SSH negotiation failed: {str(e)}')

    while True:
        chan = server_socket.accept(20)
        if chan is None:
            continue
        server_socket.close()

def main():
    # Start the SFTP server in a separate thread
    sftp_thread = threading.Thread(target=start_sftp_server)
    sftp_thread.daemon = True
    sftp_thread.start()

    # Wait for the SFTP server to start
    time.sleep(1)

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