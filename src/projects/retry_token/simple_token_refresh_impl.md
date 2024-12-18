# RetryHandler  functionality

```python
import time
import requests
from functools import wraps

"""
Exception simulated. 
The function invoking the api throws this exception if the actual api 
does not raise this exception type
"""
class TokenExpiredError(Exception):
    pass


def retry_with_token_refresh(max_retries=3, backoff_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)

                except TokenExpiredError:
                    # Get new token
                    new_token = get_new_token()

                    # Update Authorization header
                    if 'headers' in kwargs:
                        kwargs['headers']['Authorization'] = f'Bearer {new_token}'

                    # Wait before retry
                    time.sleep(backoff_seconds * (retries + 1))
                    retries += 1

                except requests.RequestException:
                    # Wait before retry
                    time.sleep(backoff_seconds * (retries + 1))
                    retries += 1

            # If we get here, we've exhausted our retries
            raise Exception(f"Failed after {max_retries} retries")

        return wrapper

    return decorator


def get_new_token():
    """Replace this with your token refresh logic"""
    response = requests.post('https://api.example.com/refresh-token')
    return response.json()['access_token']


# Example usage
@retry_with_token_refresh(max_retries=3, backoff_seconds=1)
def call_api(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        raise TokenExpiredError()

    response.raise_for_status()
    return response.json()


# How to use it
if __name__ == "__main__":
    headers = {
        'Authorization': 'Bearer old_token',
        'Content-Type': 'application/json'
    }

    try:
        result = call_api('https://api.example.com/data', headers=headers)
        print(result)
    except Exception as e:
        print(f"Error: {e}")

```

