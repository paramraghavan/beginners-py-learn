import requests
import json
import base64
from datetime import datetime
import logging


class GoAnywhereAPI:
    def __init__(self, base_url, username, password, verify_ssl=True):
        """
        Initialize GoAnywhere REST API client

        Args:
            base_url (str): Base URL of GoAnywhere server (e.g., 'https://your-server:8000')
            username (str): Admin username
            password (str): Admin password
            verify_ssl (bool): Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.token = None

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('GoAnywhereAPI')

        # Create session
        self.session = requests.Session()
        self.session.verify = verify_ssl

        # Authenticate immediately
        self.authenticate()

    def authenticate(self):
        """Authenticate and get access token"""
        auth_url = f"{self.base_url}/goanywhere/rest/auth/token"

        # Create basic auth header
        auth_string = f"{self.username}:{self.password}"
        auth_bytes = auth_string.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')

        headers = {
            'Authorization': f'Basic {base64_auth}',
            'Content-Type': 'application/json'
        }

        try:
            response = self.session.post(auth_url, headers=headers)
            response.raise_for_status()
            self.token = response.json().get('token')
            self.session.headers.update({'X-Auth-Token': self.token})
            self.logger.info("Successfully authenticated with GoAnywhere")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            raise

    def _make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to GoAnywhere API"""
        url = f"{self.base_url}/goanywhere/rest/{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params if params else None
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise

    # Workflow management
    def list_workflows(self, page=1, limit=100):
        """List all workflows"""
        return self._make_request('GET', 'workflows', params={'page': page, 'limit': limit})

    def execute_workflow(self, workflow_id, variables=None):
        """Execute a workflow with optional variables"""
        data = {'variables': variables} if variables else {}
        return self._make_request('POST', f'workflows/{workflow_id}/execute', data=data)

    def get_workflow_status(self, workflow_id, instance_id):
        """Get status of a workflow instance"""
        return self._make_request('GET', f'workflows/{workflow_id}/instances/{instance_id}')

    # Job management
    def list_jobs(self, page=1, limit=100):
        """List all jobs"""
        return self._make_request('GET', 'jobs', params={'page': page, 'limit': limit})

    def get_job_details(self, job_id):
        """Get details of a specific job"""
        return self._make_request('GET', f'jobs/{job_id}')

    # Monitor
    def get_active_sessions(self):
        """Get list of active sessions"""
        return self._make_request('GET', 'monitor/sessions')

    def get_system_status(self):
        """Get system status information"""
        return self._make_request('GET', 'monitor/status')

    # File management
    def list_files(self, path, recursive=False):
        """List files in a directory"""
        params = {
            'path': path,
            'recursive': recursive
        }
        return self._make_request('GET', 'files', params=params)

    def upload_file(self, local_path, remote_path):
        """Upload a file"""
        with open(local_path, 'rb') as file:
            files = {'file': file}
            url = f"{self.base_url}/goanywhere/rest/files/upload"
            params = {'path': remote_path}

            response = self.session.post(url, files=files, params=params)
            response.raise_for_status()
            return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize client
    api = GoAnywhereAPI(
        base_url="https://your-goanywhere-server:8000",
        username="admin",
        password="your-password",
        verify_ssl=True  # Set to False if using self-signed certificates
    )

    try:
        # List workflows
        workflows = api.list_workflows()
        print("Available workflows:", workflows)

        # Execute a workflow with variables
        workflow_vars = {
            "sourceFile": "/path/to/source.txt",
            "targetFile": "/path/to/target.txt"
        }
        result = api.execute_workflow("your-workflow-id", workflow_vars)
        print("Workflow execution result:", result)

        # Check system status
        status = api.get_system_status()
        print("System status:", status)

        # List files in a directory
        files = api.list_files("/some/path")
        print("Files:", files)

    except Exception as e:
        print(f"Error: {str(e)}")