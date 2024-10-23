import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import time
from bs4 import BeautifulSoup
import re

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class GoAnywhereCLTLogin:
    def __init__(self):
        self.session = self._create_session()
        self.base_url = 'https://goanywhereclt.bkiconnect.com'
        self.login_url = f"{self.base_url}/webclient/Login.xhtml"
        self.landing_url = f"{self.base_url}/webclient/WebClient.xhtml"
        self.dashboard_url = f"{self.base_url}/webclient/Dashboard.xhtml"

    def _create_session(self):
        session = requests.Session()

        self.timeout = (15, 45)  # (connect, read) in seconds

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=['HEAD', 'GET', 'POST'],
            raise_on_redirect=False
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_maxsize=5,
            pool_block=False
        )

        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # JSF-specific headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Faces-Request': 'partial/ajax',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
        })

        return session

    def _extract_jsf_fields(self, response_text):
        """Extract all JSF-specific fields and form parameters"""
        fields = {}
        soup = BeautifulSoup(response_text, 'html.parser')

        # Extract ViewState (required for JSF)
        viewstate = soup.find('input', {'name': 'javax.faces.ViewState'})
        if viewstate:
            fields['javax.faces.ViewState'] = viewstate.get('value')
            logging.debug(f"Found ViewState: {fields['javax.faces.ViewState'][:20]}...")

        # Find the main form
        form = soup.find('form', id='loginForm')
        if form:
            # Extract form client ID
            fields['form_id'] = form.get('id', 'loginForm')

            # Get all hidden inputs within the form
            for hidden in form.find_all('input', type='hidden'):
                name = hidden.get('name')
                value = hidden.get('value', '')
                if name:
                    fields[name] = value
                    logging.debug(f"Found hidden field {name}: {value[:20] if value else 'empty'}")

        return fields

    def _build_jsf_request(self, form_id, username, password, jsf_fields):
        """Build a proper JSF request payload"""
        data = {
            # JSF form identifiers
            form_id: form_id,
            f'{form_id}:userName': username,
            f'{form_id}:password': password,
            f'{form_id}:loginButton': 'Login',

            # Standard JSF parameters
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': f'{form_id}:loginButton',
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': '@all',

            # Add any ViewState and other JSF fields
            **jsf_fields
        }
        return data

    def _is_logged_in(self, response):
        """Verify if login was successful, accounting for JSF responses"""
        if not response.ok:
            return False

        # Check for JSF XML response
        if 'application/xml' in response.headers.get('Content-Type', ''):
            # Parse XML response for success indicators
            soup = BeautifulSoup(response.text, 'xml')
            redirect = soup.find('redirect')
            if redirect and redirect.get('url'):
                redirect_url = redirect.get('url')
                if any(page in redirect_url for page in ['Dashboard.xhtml', 'Landing.xhtml']):
                    return True
            return False

        # Regular HTML response checks
        soup = BeautifulSoup(response.text, 'html.parser')

        success_indicators = [
            soup.find('div', {'id': 'headerUserName'}),
            soup.find('a', text=re.compile(r'Logout', re.I)),
            soup.find('div', {'class': 'dashboard'}),
            'Dashboard.xhtml' in response.url,
            'Landing.xhtml' in response.url
        ]

        return any(success_indicators)

    def login(self, username, password):
        for attempt in range(3):
            try:
                # Clear session
                self.session.cookies.clear()

                # Initial page load to get JSF state
                logging.info(f"Fetching JSF login page (Attempt {attempt + 1})")
                initial_response = self.session.get(
                    self.login_url,
                    timeout=self.timeout,
                    verify=True,
                    allow_redirects=True
                )
                initial_response.raise_for_status()

                # Extract JSF fields
                jsf_fields = self._extract_jsf_fields(initial_response.text)
                if not jsf_fields.get('javax.faces.ViewState'):
                    logging.error("Could not find ViewState - JSF form may have changed")
                    continue

                # Build JSF request
                login_data = self._build_jsf_request(
                    form_id=jsf_fields.get('form_id', 'loginForm'),
                    username=username,
                    password=password,
                    jsf_fields=jsf_fields
                )

                logging.info("Submitting JSF login request")
                response = self.session.post(
                    self.login_url,
                    data=login_data,
                    timeout=self.timeout,
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': self.base_url,
                        'Referer': self.login_url,
                        'Faces-Request': 'partial/ajax'
                    },
                    allow_redirects=True
                )

                response.raise_for_status()

                # Debug response
                logging.debug(f"Response URL: {response.url}")
                logging.debug(f"Content-Type: {response.headers.get('Content-Type')}")
                logging.debug(f"Response length: {len(response.text)}")

                if self._is_logged_in(response):
                    logging.info("JSF login successful!")

                    # Verify session by accessing dashboard
                    dashboard_response = self.session.get(
                        self.dashboard_url,
                        timeout=self.timeout,
                        allow_redirects=True
                    )

                    if dashboard_response.ok:
                        logging.info("Dashboard access verified")
                        return True
                    else:
                        logging.warning("Dashboard access failed after login")
                        continue

                # Check for JSF error messages
                soup = BeautifulSoup(response.text, 'html.parser')
                error_msgs = soup.find_all(['span', 'div'],
                                           class_=['error', 'errorMessage', 'ui-messages-error'])
                for error in error_msgs:
                    logging.error(f"JSF error message: {error.text.strip()}")

            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {str(e)}")
                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue

        return False


def main():
    try:
        client = GoAnywhereCLTLogin()

        username = 'your_username'
        password = 'your_password'

        if client.login(username, password):
            logging.info("JSF login successful - session established")
            # The session can now be used for subsequent JSF requests

            # Example: Access dashboard
            dashboard = client.session.get(client.dashboard_url)
            logging.info(f"Dashboard access status: {dashboard.status_code}")
        else:
            logging.error("JSF login failed after multiple attempts")

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main()