import smtplib
import logging
import socket
import signal
import sys
import time
from email.mime.text import MIMEText
from datetime import datetime
from logging.handlers import RotatingFileHandler


class ServerMonitor:
    def __init__(self, email_config, log_config):
        """
        Initialize the server monitor with email and logging configurations

        Args:
            email_config (dict): Email configuration settings
            log_config (dict): Logging configuration settings
        """
        self.email_config = email_config
        self.setup_logging(log_config)
        self.setup_signal_handlers()

    def setup_logging(self, config):
        """Configure rotating file logger"""
        self.logger = logging.getLogger('ServerMonitor')
        self.logger.setLevel(logging.INFO)

        # Create rotating file handler
        handler = RotatingFileHandler(
            config['log_file'],
            maxBytes=config['max_size'],
            backupCount=config['backup_count']
        )

        # Create formatter and add it to handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)

    def send_email(self, subject, body):
        """
        Send email notification

        Args:
            subject (str): Email subject
            body (str): Email body
        """
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email_config['sender']
            msg['To'] = self.email_config['recipient']

            # Connect to SMTP server
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                if self.email_config['use_tls']:
                    server.starttls()
                server.login(
                    self.email_config['username'],
                    self.email_config['password']
                )
                server.send_message(msg)

            self.logger.info(f"Email notification sent: {subject}")
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")

    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals"""
        shutdown_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hostname = socket.gethostname()

        # Log shutdown event
        self.logger.warning(f"Server shutdown initiated at {shutdown_time}")

        # Prepare and send email notification
        subject = f"Server Shutdown Alert - {hostname}"
        body = f"""
        Server shutdown detected:

        Hostname: {hostname}
        Time: {shutdown_time}
        Signal: {signal.Signals(signum).name}

        This is an automated notification.
        """

        self.send_email(subject, body)

        # Cleanup and exit
        self.logger.info("Shutdown handling complete")
        sys.exit(0)

    def run(self):
        """Main monitoring loop"""
        self.logger.info("Server monitoring started")
        try:
            while True:
                # Keep the script running and monitoring for signals
                time.sleep(1)
        except Exception as e:
            self.logger.error(f"Monitoring error: {str(e)}")


def main():
    # Email configuration
    email_config = {
        'smtp_server': 'smtp.gmail.com',  # Replace with your SMTP server
        'smtp_port': 587,
        'use_tls': True,
        'username': 'your-email@gmail.com',  # Replace with your email
        'password': 'your-app-password',  # Replace with your app password
        'sender': 'your-email@gmail.com',  # Replace with sender email
        'recipient': 'admin@example.com'  # Replace with recipient email
    }

    # Logging configuration
    log_config = {
        'log_file': '/var/log/server_monitor.log',  # Adjust path as needed
        'max_size': 5 * 1024 * 1024,  # 5 MB
        'backup_count': 3
    }

    # Create and run monitor
    monitor = ServerMonitor(email_config, log_config)
    monitor.run()


if __name__ == "__main__":
    main()
