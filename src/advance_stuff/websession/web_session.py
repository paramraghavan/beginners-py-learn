import requests
import pickle
import os
from bs4 import BeautifulSoup


class WebSession:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.token_file = 'session_token.pkl'

    def login(self, url, username, password):
        try:
            # First get the login page to capture any CSRF token if needed
            login_page = self.session.get(url)
            soup = BeautifulSoup(login_page.text, 'html.parser')

            # Some sites have CSRF token in form
            csrf_token = soup.find('input', {'name': 'csrf_token'})

            login_data = {
                'username': username,
                'password': password
            }

            # Add CSRF token if found
            if csrf_token:
                login_data['csrf_token'] = csrf_token['value']

            # Perform login
            response = self.session.post(url, data=login_data)

            if response.ok:
                # Save session cookies
                self.save_session()
                return True
            return False

        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def save_session(self):
        """Save session cookies to file"""
        with open(self.token_file, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def load_session(self):
        """Load session cookies from file"""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            return True
        return False

    def navigate(self, url):
        """Navigate to a page using existing session"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Navigation failed: {str(e)}")
            return None

    def check_session_valid(self, url):
        """Check if current session is still valid"""
        try:
            response = self.session.get(url)
            # Adjust this based on how your site indicates logged-in state
            return 'login' not in response.url.lower()
        except:
            return False


# Usage example
def main():
    # Initialize session
    web = WebSession()

    login_url = 'https://example.com/login'
    dashboard_url = 'https://example.com/dashboard'

    # Try to load existing session
    if web.load_session() and web.check_session_valid(dashboard_url):
        print("Using existing session")
    else:
        print("Logging in with new session")
        # Load credentials from environment variables
        username = os.getenv('WEB_USERNAME')
        password = os.getenv('WEB_PASSWORD')

        if not web.login(login_url, username, password):
            print("Login failed")
            return

    # Navigate the site
    try:
        # Get dashboard content
        dashboard_content = web.navigate(dashboard_url)
        if dashboard_content:
            # Process the content
            soup = BeautifulSoup(dashboard_content, 'html.parser')
            # Extract what you need
            print("Successfully accessed dashboard")

        # Navigate to other pages
        other_page = web.navigate('https://example.com/other-page')
        if other_page:
            # Process other page
            pass

    except Exception as e:
        print(f"Error during navigation: {str(e)}")


if __name__ == "__main__":
    main()