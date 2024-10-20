import ftplib
import schedule
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import uuid
import logging
import os
from shared_file_state import update_file_status, add_file_status, get_file_status

# Configure logging
logging.basicConfig(filename='ftpmon.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
FTP_HOST = 'ftp.example.com'  # Replace with your FTP host
FTP_PORT = 21
FTP_USERNAME = ''
FTP_PASSWORD = ''
REMOTE_PATH = f'/Users/{FTP_USERNAME}/ftp_test'
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
    # Email sending code remains the same


def test_ftp_connectivity():
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
        logging.info("FTP connection test successful")
        return True
    except Exception as e:
        error_msg = f"FTP connection test failed: {str(e)}"
        logging.error(error_msg)
        send_email("FTP Connectivity Error", error_msg)
        return False


def get_ftp_file_list(time_window_minutes=5):
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
            ftp.cwd(REMOTE_PATH)

            now = datetime.now()
            time_threshold = now - timedelta(minutes=time_window_minutes)

            filtered_files = []

            def process_file(line):
                parts = line.split()
                filename = parts[-1]
                date_str = ' '.join(parts[5:8])

                # Parse the date. Adjust the format string if needed.
                file_mtime = datetime.strptime(date_str, "%b %d %Y")

                if file_mtime > time_threshold:
                    filtered_files.append((filename, file_mtime))

            ftp.retrlines('LIST', process_file)

            return sorted(filtered_files, key=lambda x: x[1])
    except Exception as e:
        logging.error(f"Failed to get FTP file list: {str(e)}")
        return []


def process_files(files):


# This function remains the same as it doesn't directly interact with FTP

def create_random_file(filename, size=1024):


# This function remains the same as it's for local file creation

def simulate_file_transfer():
    if not test_ftp_connectivity():
        logging.error("FTP connection failed. Can't simulate file transfer.")
        return

    num_files = random.randint(1, 2)
    transferred_files = []

    try:
        with ftplib.FTP() as ftp:
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
            ftp.cwd(REMOTE_PATH)

            for i in range(num_files):
                filename = f"file_{uuid.uuid4()}.txt"
                local_path = os.path.join(LOCAL_TEMP_DIR, filename)

                # Create a random file
                create_random_file(filename)

                # Transfer the file
                with open(local_path, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)

                # Update file status
                update_file_status(filename, 'open')

                transferred_files.append(filename)
                logging.info(f"Transferred file: {filename}")

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


def monitor_ftp():
    if not test_ftp_connectivity():
        return

    files = get_ftp_file_list(time_window_minutes=TIME_INTERVAL)
    process_files(files)
    # cleanup parent_job_map, remove all the parent jobs that have all child jobs that are not in open state
    cleanup()


def main():
    schedule.every(TIME_INTERVAL).minutes.do(monitor_ftp)
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
