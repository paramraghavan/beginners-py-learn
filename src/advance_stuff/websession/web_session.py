import requests
import pickle
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import logging

logging.basicConfig(level=logging.DEBUG)


class WebSession:
    def __init__(self):
        self.session = self._create_robust_session()
        self.token_file = 'session_token.pkl'
        self.max_retries = 3
        self.retry_delay = 5

    def _create_robust_session(self):
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=frozenset(['GET', 'POST'])
        )

        # Set up adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Connection': 'keep-alive'
        })

        return session

    def make_request(self, method, url, data=None, **kwargs):
        """Make request with retry logic and connection reset handling"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    data=data,
                    timeout=30,
                    **kwargs
                )
                response.raise_for_status()
                return response

            except requests.exceptions.ConnectionError as e:
                logging.error(f"Connection error on attempt {attempt + 1}: {e}")
                if "10054" in str(e):
                    logging.info("Connection reset detected, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise

            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise

        return None

    def login(self, url, username, password):
        try:
            # Get login page and CSRF token
            login_page = self.make_request('GET', url)
            if not login_page:
                return False

            soup = BeautifulSoup(login_page.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})

            login_data = {
                'username': username,
                'password': password
            }

            if csrf_token:
                login_data['csrf_token'] = csrf_token['value']

            # Perform login
            response = self.make_request('POST', url, data=login_data)

            if response and response.ok:
                self.save_session()
                return True
            return False

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def save_session(self):
        """Save session cookies to file"""
        try:
            with open(self.token_file, 'wb') as f:
                pickle.dump(self.session.cookies, f)
        except Exception as e:
            logging.error(f"Failed to save session: {str(e)}")

    def load_session(self):
        """Load session cookies from file"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as f:
                    self.session.cookies.update(pickle.load(f))
                return True
        except Exception as e:
            logging.error(f"Failed to load session: {str(e)}")
        return False

    def navigate(self, url):
        """Navigate to a page with automatic session handling"""
        try:
            response = self.make_request('GET', url)
            if response:
                return response.text
        except Exception as e:
            logging.error(f"Navigation failed: {str(e)}")
        return None

    def check_session_valid(self, url):
        """Check if current session is still valid"""
        try:
            response = self.make_request('GET', url, allow_redirects=False)
            if response:
                # Check if we're still logged in (adjust based on site behavior)
                return 'login' not in response.url.lower()
        except Exception as e:
            logging.error(f"Session check failed: {str(e)}")
        return False


def main():
    # Initialize session
    web = WebSession()

    # Configuration
    login_url = 'https://example.com/login'
    dashboard_url = 'https://example.com/dashboard'

    try:
        # Try to load existing session
        if web.load_session() and web.check_session_valid(dashboard_url):
            logging.info("Using existing session")
        else:
            logging.info("Logging in with new session")
            # Load credentials from environment variables
            username = os.getenv('WEB_USERNAME')
            password = os.getenv('WEB_PASSWORD')

            if not username or not password:
                raise ValueError("Missing credentials in environment variables")

            if not web.login(login_url, username, password):
                raise Exception("Login failed")

        # Navigate the site
        dashboard_content = web.navigate(dashboard_url)
        if dashboard_content:
            soup = BeautifulSoup(dashboard_content, 'html.parser')
            # Process content as needed
            logging.info("Successfully accessed dashboard")

        # Navigate to other pages
        other_page = web.navigate('https://example.com/other-page')
        if other_page:
            # Process other page
            pass

    except Exception as e:
        logging.error(f"Error during execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()