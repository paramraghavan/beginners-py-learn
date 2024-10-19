import paramiko
import schedule
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import uuid
import logging
import os
from shared_file_state import  update_file_status, add_file_status, get_file_status

# Configure logging
logging.basicConfig(filename='ftpmon.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
SFTP_HOST = 'sftp.blacknight.com'
SFTP_PORT = 22
SFTP_USERNAME = ''
SFTP_PASSWORD = ''
REMOTE_PATH = f'/Users/{SFTP_USERNAME}/sftp_test'
BATCH_WINDOW = timedelta(minutes=7)
TIME_INTERVAL = 5
TEAM_LEADS_EMAILS = ['lead1@example.com', 'lead2@example.com']
LOCAL_TEMP_DIR = 'temp_files'
os.makedirs(LOCAL_TEMP_DIR, exist_ok=True)



# Global variables
parent_job_map = {}
current_batch_start_time = None
current_parent_job_id = None

def send_email(subject, body):
    print(rf'Subject: {subject}, Body: {body}')
    return
    # sender = 'your_email@example.com'
    # recipients = TEAM_LEADS_EMAILS
    # msg = MIMEText(body)
    # msg['Subject'] = subject
    # msg['From'] = sender
    # msg['To'] = ', '.join(recipients)
    #
    # try:
    #     with smtplib.SMTP('your_smtp_server', 587) as server:
    #         server.starttls()
    #         server.login('your_email@example.com', 'your_password')
    #         server.sendmail(sender, recipients, msg.as_string())
    #     logging.info("Email sent successfully")
    # except Exception as e:
    #     logging.error(f"Failed to send email: {str(e)}")

def test_sftp_connectivity():
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD)
        logging.info("SFTP connection test successful")
        return True
    except Exception as e:
        error_msg = f"SFTP connection test failed: {str(e)}"
        logging.error(error_msg)
        send_email("SFTP Connectivity Error", error_msg)
        return False

'''
Paramiko's SFTP client doesn't provide a direct way to filter files by modification time on the server side.
We'll need to retrieve all files and filter them on the client side.
'''
def get_sftp_file_list(time_window_minutes=5):
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD)
            sftp = ssh.open_sftp()

            now = datetime.now()
            time_threshold = now - timedelta(minutes=time_window_minutes)

            filtered_files = []
            for file_attr in sftp.listdir_attr(REMOTE_PATH):
                file_mtime = datetime.fromtimestamp(file_attr.st_mtime)
                if file_mtime > time_threshold:
                    filtered_files.append((file_attr.filename, file_mtime))

            return sorted(filtered_files, key=lambda x: x[1])
    except Exception as e:
        logging.error(f"Failed to get SFTP file list: {str(e)}")
        return []




'''
When we get a list to files at the 5 min interval run, then we create parent job id and add  the files  to list to  the
parent_job_map add parent job_id as key and list files as values.
We have a concept of batch window  if the batch window is five min.s, then all the files within that time windows get 
assigned to the same parent job id.
For example:
- From 10.55 to 11.00 we have 2 files, one file at 10.57  and another one at 10.58, so the batch windows starts at 10.57 am
- From 11.00 - 11.05 wre have 2 files , one file at 11.01 and another one at 11.03
- The files at time 10.57, 10.58 and 11.01 all get assigned the same parent job id
- But file at 11.03 gets assigned a new parent job id
# TODO, check
- If the same file arrives at 10.57 thru 11.04 , we pickup the latest file. Hopefully file names are unique
'''
def process_files(files):
    global current_batch_start_time, current_parent_job_id

    if not files:
        return

    now = datetime.now()
    for filename, file_time in files:
        if current_batch_start_time is None or (file_time - current_batch_start_time) > BATCH_WINDOW:
            current_batch_start_time = file_time
            current_parent_job_id = '-'.join([str(uuid.uuid4()), str(current_batch_start_time)])

            if current_parent_job_id not in parent_job_map:
                parent_job_map[current_parent_job_id] = []
            parent_job_map[current_parent_job_id].append(filename)
            update_file_status(filename, 'open')

        logging.info(f"Processed file: {filename}, Time: {file_time}, Parent Job ID: {current_parent_job_id}")


import random, string
def create_random_file(filename, size=1024):
    """Create a file with filename as its content."""
    with open(os.path.join(LOCAL_TEMP_DIR, filename), 'w') as f:
        f.write(filename)
        #f.write(''.join(random.choices(string.ascii_letters + string.digits, k=size)))

def simulate_file_transfer():
    if not test_sftp_connectivity():
        logging.error("SFTP connection failed. Can't simulate file transfer.")
        return

    num_files = random.randint(1, 2)
    transferred_files = []

    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD)
            sftp = ssh.open_sftp()

            for i in range(num_files):
                filename = f"file_{uuid.uuid4()}.txt"
                local_path = os.path.join(LOCAL_TEMP_DIR, filename)
                remote_path = os.path.join(REMOTE_PATH, filename)

                # Create a random file
                create_random_file(filename)

                # Transfer the file
                sftp.put(local_path, remote_path)

                # Update file status
                update_file_status(filename, 'open')

                transferred_files.append(filename)
                logging.info(f"Transferred file: {filename}")

            sftp.close()

    except Exception as e:
        logging.error(f"Error in simulating file transfer: {str(e)}")
        for filename in transferred_files:
            update_file_status(filename, 'error')
    else:
        for filename in transferred_files:
            update_file_status(filename, 'complete')

    finally:
        # Clean up local temporary files
        for filename in transferred_files:
            try:
                os.remove(os.path.join(LOCAL_TEMP_DIR, filename))
            except OSError as e:
                logging.warning(f"Error removing temporary file {filename}: {str(e)}")

def monitor_sftp():
    if not test_sftp_connectivity():
        return

    files = get_sftp_file_list(time_window_minutes=TIME_INTERVAL)
    process_files(files)
    #cleeanup parent_job_map, remove all the parent jobs that have all child jobs that are no tin open state
    cleanup()

def main():
    schedule.every(TIME_INTERVAL).minutes.do(monitor_sftp)
    # schedule.every(TIME_INTERVAL).minutes.do(simulate_file_transfer)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            error_msg = f"ftpmon crashed: {str(e)}"
            logging.error(error_msg)
            send_email("ftpmon Crash Alert", error_msg)
            break

if __name__ == "__main__":
    main()