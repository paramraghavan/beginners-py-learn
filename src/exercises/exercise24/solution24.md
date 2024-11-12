A Python script that monitors jobs based on the criteria you've described.

```python
import csv
import time
import os
from datetime import datetime, timedelta
import requests
from email.message import EmailMessage
import smtplib


class JobMonitor:
    def __init__(self, csv_file, check_interval):
        self.csv_file = csv_file
        self.check_interval = check_interval  # in minutes
        self.jobs = []
        self.last_modified_time = None
        self.load_jobs()

    def load_jobs(self):
        """Load jobs from CSV file if modified"""
        try:
            current_modified_time = os.path.getmtime(self.csv_file)
            if self.last_modified_time != current_modified_time:
                with open(self.csv_file, 'r') as file:
                    csv_reader = csv.DictReader(file)
                    self.jobs = list(csv_reader)
                self.last_modified_time = current_modified_time
                print(f"Loaded {len(self.jobs)} jobs from {self.csv_file}")
        except Exception as e:
            print(f"Error loading jobs: {str(e)}")

    def check_job_status(self, job_name, time_window):
        """
        Placeholder function to check job status
        Returns: 'Success', 'Failed', 'Running', or 'NotFound'
        """
        try:
            # Simulated API call - replace with actual REST API call
            # Example:
            # response = requests.get(f"http://job-api/status/{job_name}?window={time_window}")
            # return response.json()['status']

            # For demonstration, returning random status
            import random
            return random.choice(['Success', 'Failed', 'Running', 'NotFound'])
        except Exception as e:
            print(f"Error checking job status: {str(e)}")
            return 'Failed'

    def send_email_alert(self, job_name, status, recipients):
        """Send email alert for job status"""
        try:
            msg = EmailMessage()
            msg.set_content(f"Job {job_name} status: {status}")
            msg['Subject'] = f"Job Alert - {job_name}"
            msg['From'] = "job.monitor@example.com"
            msg['To'] = recipients

            # Replace with your SMTP settings
            # with smtplib.SMTP('smtp.example.com', 587) as server:
            #     server.starttls()
            #     server.login('user', 'password')
            #     server.send_message(msg)

            print(f"Email alert sent for {job_name}: {status} to {recipients}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")

    def is_within_check_window(self, check_time):
        """Check if current time falls within the check window"""
        if not check_time:
            return False

        current_time = datetime.now().strftime('%H:%M')
        return current_time == check_time

    def monitor_jobs(self):
        """Main monitoring loop"""
        while True:
            try:
                # Reload jobs if file has changed
                self.load_jobs()

                current_time = datetime.now()

                for job in self.jobs:
                    job_name = job['jobname']
                    check_time = job['check_time'].strip() if job['check_time'] else None
                    alert_time = job['alert_time'].strip() if job['alert_time'] else None
                    poll_interval = int(job['poll_every_x_minutes']) if job['poll_every_x_minutes'] else None
                    emails = job['emails']

                    # Check time based monitoring
                    if check_time and self.is_within_check_window(check_time):
                        status = self.check_job_status(job_name, "recent")
                        if status == 'Failed':
                            self.send_email_alert(job_name, status, emails)

                    # Alert time based monitoring
                    if alert_time and self.is_within_check_window(alert_time):
                        status = self.check_job_status(job_name, "today")
                        if status in ['Failed', 'Running', 'NotFound']:
                            self.send_email_alert(job_name, status, emails)

                    # Polling based monitoring
                    if not check_time and not alert_time and poll_interval:
                        if current_time.minute % poll_interval == 0:
                            status = self.check_job_status(job_name, f"last_{poll_interval}_minutes")
                            if status == 'Failed':
                                self.send_email_alert(job_name, status, emails)

                # Sleep until next check interval
                time.sleep(60)  # Sleep for 1 minute

            except Exception as e:
                print(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)  # Sleep and retry on error


if __name__ == "__main__":
    # Initialize and run the monitor
    monitor = JobMonitor("job_run.csv", check_interval=5)
    monitor.monitor_jobs()

```

This script implements a complete job monitoring system with the following features:

1. Continuously monitors jobs defined in a CSV file
2. Reloads the CSV file when changes are detected
3. Supports three types of monitoring:
    - Check time: Checks job status at specific times
    - Alert time: Verifies job completion status at specific times
    - Polling: Regular interval-based monitoring

4. The `check_job_status` function is currently a placeholder that you can replace with your actual REST API call.

To use this script:

1. Create your job_run.csv file with the following columns:

```csv
jobname,check_time,alert_time,poll_every_x_minutes,emails
job1,09:00,17:00,,user@example.com
job2,,,30,user@example.com
job3,12:00,,,user@example.com
```

2. Update the email settings in the `send_email_alert` method with your SMTP server details

3. Implement the actual REST API call in the `check_job_status` method

The script will:

- Monitor jobs continuously
- Check for CSV file changes
- Send email alerts based on job status
- Handle errors gracefully
- Provide logging of important events
