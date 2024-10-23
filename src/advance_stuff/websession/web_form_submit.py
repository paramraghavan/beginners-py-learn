import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import time
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


class WebFormSession:
    def __init__(self):
        self.session = self._create_session()
        self.base_url = 'https://goanywhereclt.bkiconnect.com'

    def _create_session(self):
        session = requests.Session()

        # Extended timeouts for form submission
        self.timeout = (30, 90)  # (connect, read) timeouts in seconds

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })

        return session

    def submit_form(self, username, password):
        try:
            # First get the login page to capture any tokens
            login_url = f"{self.base_url}/login"  # adjust if different

            logging.info("Fetching login page...")
            response = self.session.get(
                login_url,
                timeout=self.timeout
            )
            response.raise_for_status()

            # Parse the page for form details
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')

            # Get all hidden fields
            form_data = {}
            if form:
                for hidden in form.find_all('input', type='hidden'):
                    form_data[hidden.get('name')] = hidden.get('value')

            # Add login credentials
            form_data.update({
                'username': username,
                'password': password,
                # Add other required form fields
                # 'submit': 'Login'  # if needed
            })

            logging.info("Submitting form...")

            # Submit the form
            response = self.session.post(
                login_url,
                data=form_data,
                timeout=self.timeout,
                allow_redirects=True,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': self.base_url,
                    'Referer': login_url
                }
            )

            response.raise_for_status()

            # Check if login successful (adjust based on site behavior)
            if "login" not in response.url.lower():
                logging.info("Login successful")
                return True
            else:
                logging.error("Login failed - redirected back to login page")
                return False

        except requests.exceptions.ReadTimeout:
            logging.error("Form submission timed out")
            return False
        except requests.exceptions.RequestException as e:
            logging.error(f"Form submission error: {str(e)}")
            return False


def main():
    form = WebFormSession()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            logging.info(f"Attempt {attempt + 1} of {max_retries}")

            success = form.submit_form(
                username='your_username',
                password='your_password'
            )

            if success:
                logging.info("Form submitted successfully")
                # Continue with other operations
                break
            else:
                logging.error(f"Form submission failed on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(5 * (attempt + 1))  # Increasing delay between retries
                    continue

        except Exception as e:
            logging.error(f"Error during form submission: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise


if __name__ == "__main__":
    main()