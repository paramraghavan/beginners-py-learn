# using requests.raise_for_status

The `raise_for_status()` method is a built-in helper in the Python `requests` library that checks if an HTTP request was
successful.

1. HTTP Status Code Categories:
    - 2xx (200-299): Success responses (e.g., 200 OK, 201 Created)
    - 4xx (400-499): Client errors (e.g., 404 Not Found, 401 Unauthorized)
    - 5xx (500-599): Server errors (e.g., 500 Internal Server Error)

2. What `raise_for_status()` does:
   ```python
   import requests

   # Example usage
   response = requests.get('https://api.example.com/data')
   
   try:
       response.raise_for_status()
       # If we get here, status code was 2xx
       data = response.json()
   except requests.exceptions.HTTPError as e:
       # This will catch any 4xx or 5xx status codes
       print(f"Error: {e}")
       # e will contain the status code and response text
   ```

3. Without `raise_for_status()`, you'd have to check manually:
   ```python
   # Manual checking (more verbose)
   response = requests.get('https://api.example.com/data')
   
   if 200 <= response.status_code < 300:
       data = response.json()
   else:
       raise requests.exceptions.HTTPError(f"Request failed with status: {response.status_code}")
   ```

4. Common status codes it checks for:
   ```python
   # Different scenarios where raise_for_status() would raise an exception
   
   # 404 Not Found
   response = requests.get('https://api.example.com/nonexistent')
   response.raise_for_status()  # Raises HTTPError with 404 message
   
   # 401 Unauthorized
   response = requests.get('https://api.example.com/protected')
   response.raise_for_status()  # Raises HTTPError with 401 message
   
   # 500 Server Error
   response = requests.get('https://api.example.com/error')
   response.raise_for_status()  # Raises HTTPError with 500 message
   ```

5. In our retry handler context:
   ```python
   @retry_with_token_refresh(max_retries=3, backoff_seconds=1)
   def call_api(url, headers):
       response = requests.get(url, headers=headers)
       
       # First check specifically for token expiration
       if response.status_code == 401:
           raise TokenExpiredError()
           
       # Then check for any other error status codes
       response.raise_for_status()
       
       return response.json()
   ```