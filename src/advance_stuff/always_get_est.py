"""
To get the date in EST (Eastern Standard Time) in your Python code regardless of the server's timezone, you can use the
pytz library along with the standard datetime module. This approach allows you to specify the timezone explicitly,
ensuring consistency across different environments.
"""

import datetime
import pytz


def get_est_time():
    """
    The benefit of this approach is that it works regardless of what timezone your server is in,
    because it first creates a UTC time and then explicitly converts it to Eastern time.
    """
    # Get the current UTC time
    utc_now = datetime.datetime.now(pytz.UTC)

    # Convert to Eastern Time (US & Canada)
    eastern = pytz.timezone('US/Eastern')
    est_now = utc_now.astimezone(eastern)

    return est_now


# Example usage
est_time = get_est_time()
print(f"Current EST time: {est_time}")
print(f"Formatted date: {est_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")