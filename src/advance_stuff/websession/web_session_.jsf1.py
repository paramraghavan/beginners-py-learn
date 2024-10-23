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
        self.landing_url = f"{self.base_url}/webclient/Landing.xhtml"
        self.dashboard_url = f"{self.base_url}/webclient/Dashboard.xhtml"

    def _create_session(self):
        session = requests.Session()

        self.timeout = (15, 45)

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=['HEAD', 'GET', 'POST'],
            raise_on_redirect=False
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        })

        return session

    def _find_viewstate(self, html_content):
        """Extract ViewState from JSF page source"""
        try:
            # First try to find it in the update section of partial response
            match = re.search(r'<update id="javax\.faces\.ViewState"><!\[CDATA\[(.*?)\]\]></update>', html_content)
            if match:
                return match.group(1)

            # Then try to find it in scripts
            match = re.search(r"getElementById\('javax\.faces\.ViewState'\)\.value\s*=\s*'([^']+)'", html_content)
            if match:
                return match.group(1)

            # Look for viewstate in the page source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try finding in update elements
            update_elements = soup.find_all('update', id='javax.faces.ViewState')
            if update_elements:
                return update_elements[0].text.strip()

            # Try finding in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'viewState' in script.string.lower():
                    match = re.search(r"viewState:\s*'([^']+)'", script.string)
                    if match:
                        return match.group(1)

            # Search in tag stack for hidden input
            inputs = soup.find_all('input', {'type': 'hidden', 'name': 'javax.faces.ViewState'})
            if inputs:
                return inputs[0].get('value')

            logging.debug("ViewState not found in common locations, searching entire document...")

            # Last resort: search all text for ViewState pattern
            viewstate_pattern = re.compile(r'(?:javax\.faces\.ViewState|viewState).*?value=["\']([^"\']+)["\']')
            matches = viewstate_pattern.findall(html_content)
            if matches:
                return matches[0]

            logging.warning("Could not find ViewState in page source")
            return None

        except Exception as e:
            logging.error(f"Error extracting ViewState: {str(e)}")
            return None

    def _extract_form_data(self, response_text):
        """Extract all necessary form data including ViewState"""
        form_data = {}

        # Find ViewState
        viewstate = self._find_viewstate(response_text)
        if viewstate:
            form_data['javax.faces.ViewState'] = viewstate
            logging.debug(f"Found ViewState: {viewstate[:30]}...")
        else:
            logging.warning("ViewState not found!")

        # Parse the page
        soup = BeautifulSoup(response_text, 'html.parser')

        # Find the form
        form = soup.find('form', id=lambda x: x and 'loginForm' in x)
        if form:
            form_data['form_id'] = form.get('id', 'loginForm')

            # Get all hidden inputs
            for hidden in form.find_all('input', type='hidden'):
                name = hidden.get('name')
                if name and name != 'javax.faces.ViewState':  # Skip ViewState as we handled it separately
                    form_data[name] = hidden.get('value', '')

        return form_data

    def _prepare_login_data(self, username, password, form_data):
        """Prepare the login request data with all necessary JSF parameters"""
        form_id = form_data.get('form_id', 'loginForm')

        login_data = {
            # Form identification
            'loginForm': form_id,

            # Credentials
            f'{form_id}:userName': username,
            f'{form_id}:password': password,

            # JSF specific fields
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': f'{form_id}:loginButton',
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': '@all',
            f'{form_id}:loginButton': f'{form_id}:loginButton',

            # ViewState
            'javax.faces.ViewState': form_data.get('javax.faces.ViewState', ''),
        }

        # Add any additional hidden fields from the form
        for key, value in form_data.items():
            if key not in ['form_id', 'javax.faces.ViewState'] and key not in login_data:
                login_data[key] = value

        return login_data

    def login(self, username, password):
        for attempt in range(3):
            try:
                self.session.cookies.clear()

                # Get initial page
                logging.info(f"Fetching login page (Attempt {attempt + 1})")
                initial_response = self.session.get(
                    self.login_url,
                    timeout=self.timeout,
                    verify=True
                )
                initial_response.raise_for_status()

                # Extract form data including ViewState
                form_data = self._extract_form_data(initial_response.text)
                if not form_data.get('javax.faces.ViewState'):
                    logging.error("No ViewState found - cannot proceed with login")
                    continue

                # Prepare login data
                login_data = self._prepare_login_data(username, password, form_data)

                # Perform login
                logging.info("Submitting login request")
                response = self.session.post(
                    self.login_url,
                    data=login_data,
                    timeout=self.timeout,
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Faces-Request': 'partial/ajax',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': self.base_url,
                        'Referer': self.login_url
                    }
                )
                response.raise_for_status()

                # Check if login was successful
                if 'Dashboard.xhtml' in response.url or 'Landing.xhtml' in response.url:
                    logging.info("Login successful!")
                    return True

                # Check for error messages
                soup = BeautifulSoup(response.text, 'html.parser')
                error_msgs = soup.find_all(['span', 'div'], class_=['error', 'ui-messages-error'])
                for error in error_msgs:
                    logging.error(f"Login error: {error.text.strip()}")

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
            logging.info("Successfully logged in")
        else:
            logging.error("Failed to log in")

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main()