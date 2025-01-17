# This script manages Outlook email rules using Exchange Web Services (EWS)
# It allows users to create rules based on email subject filters and move matching emails to specified folders

from exchangelib import Credentials, Account, DELEGATE, Configuration
from exchangelib.folders import Root
import logging
import sys

# Set up logging configuration to track script execution and errors
# Logs will show timestamp, log level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OutlookRulesManager:
    """
    A class to manage Outlook rules using Exchange Web Services.

    This class provides functionality to:
    - Connect to Exchange server
    - Check for existing rules and folders
    - Create new folders
    - Create new rules with subject filters
    """

    def __init__(self, email, username, password, server):
        """
        Initialize the OutlookRulesManager with user credentials.

        Args:
            email (str): User's email address
            username (str): AD username for authentication
            password (str): AD password for authentication
            server (str): Exchange server address (e.g., outlook.office365.com)
        """
        self.email = email
        self.username = username
        self.password = password
        self.server = server
        self.account = None

    def connect(self):
        """
        Establish connection to Exchange server using provided credentials.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create credentials object with AD username and password
            credentials = Credentials(self.username, self.password)

            # Configure connection to Exchange server
            config = Configuration(server=self.server, credentials=credentials)

            # Create account connection with delegate access
            self.account = Account(
                primary_smtp_address=self.email,
                config=config,
                autodiscover=False,  # Don't use autodiscover as we have server address
                access_type=DELEGATE
            )
            logger.info("Successfully connected to Exchange server")
            return True
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    def get_folder(self, folder_name):
        """
        Find a folder by name in the user's mailbox.

        Args:
            folder_name (str): Name of the folder to find

        Returns:
            Folder object if found, None otherwise
        """
        try:
            # Walk through all folders in the mailbox
            for folder in self.account.root.walk():
                # Case-insensitive folder name comparison
                if folder.name.lower() == folder_name.lower():
                    return folder
            return None
        except Exception as e:
            logger.error(f"Error finding folder: {str(e)}")
            return None

    def check_rule_exists(self, rule_name):
        """
        Check if a rule with the given name already exists.

        Args:
            rule_name (str): Name of the rule to check

        Returns:
            bool: True if rule exists, False otherwise
        """
        try:
            # Get all existing inbox rules
            rules = self.account.inbox.inbox_rules.get()

            # Case-insensitive rule name comparison
            for rule in rules:
                if rule.name.lower() == rule_name.lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking rule existence: {str(e)}")
            return False

    def create_folder(self, folder_name):
        """
        Create a new folder in the mailbox if it doesn't exist.

        Args:
            folder_name (str): Name of the folder to create

        Returns:
            Folder object if created or existing, None if creation fails
        """
        try:
            # Check if folder already exists
            existing_folder = self.get_folder(folder_name)
            if existing_folder:
                logger.warning(f"Folder '{folder_name}' already exists")
                return existing_folder

            # Create new folder in root of mailbox
            new_folder = self.account.root.create_folder(folder_name)
            logger.info(f"Created folder: {folder_name}")
            return new_folder
        except Exception as e:
            logger.error(f"Error creating folder: {str(e)}")
            return None

    def create_rule(self, rule_name, folder_name, subject_filter):
        """
        Create a new rule to move emails with matching subject to specified folder.

        Args:
            rule_name (str): Name for the new rule
            folder_name (str): Destination folder for matching emails
            subject_filter (str): Text to match in email subjects

        Returns:
            bool: True if rule created successfully, False otherwise
        """
        try:
            # First check if rule already exists
            if self.check_rule_exists(rule_name):
                logger.warning(f"Rule '{rule_name}' already exists")
                return False

            # Get or create the target folder
            target_folder = self.get_folder(folder_name)
            if not target_folder:
                target_folder = self.create_folder(folder_name)
                if not target_folder:
                    return False

            # Define the rule configuration
            rule = {
                'name': rule_name,
                'conditions': {
                    'subject_contains': [subject_filter]  # List of strings to match in subject
                },
                'actions': {
                    'move_to_folder': target_folder  # Move matching emails to target folder
                },
                'enabled': True  # Rule is active when created
            }

            # Create the rule in the inbox
            self.account.inbox.inbox_rules.create(**rule)
            logger.info(f"Successfully created rule: {rule_name}")
            return True

        except Exception as e:
            logger.error(f"Error creating rule: {str(e)}")
            return False


def main():
    """
    Main function to run the script interactively.
    Prompts user for credentials and rule details, then creates the rule.
    """
    # Collect user credentials and server information
    email = input("Enter your email address: ")
    username = input("Enter your AD username: ")
    password = input("Enter your password: ")
    server = input("Enter your Exchange server (e.g., outlook.office365.com): ")

    # Initialize the rules manager
    manager = OutlookRulesManager(email, username, password, server)

    # Attempt to connect to Exchange server
    if not manager.connect():
        print("Failed to connect to Exchange server. Please check your credentials and server settings.")
        sys.exit(1)

    # Collect rule details from user
    rule_name = input("Enter rule name: ")
    folder_name = input("Enter folder name: ")
    subject_filter = input("Enter subject filter: ")

    # Create the rule and report result
    if manager.create_rule(rule_name, folder_name, subject_filter):
        print("Rule created successfully!")
    else:
        print("Failed to create rule. Check the logs for details.")


# Entry point of the script
if __name__ == "__main__":
    main()
