from datetime import datetime

x = '2024-05-09 10:30:45:123456'


# Current datetime
now = datetime.now()
print(now)

# time with 0 minutes and millis
now_with_zero_seconds = now.replace(second=0,microsecond=0)
print(now_with_zero_seconds)

# Creating a specific datetime object
specific_datetime = datetime(2024, 6, 3, 10, 30, 45, 123456)
print(specific_datetime)

# result
# 2024-06-03 11:05:03.058475
# 2024-06-03 10:30:45.123456

"""
Convert that UTC timestamp string, 2024-05-09T10:30:45:340124Z,  to Eastern Time (EST/EDT) using Python:```

A few key points:
1. `%f` in the format string handles microseconds
2. We use 'America/New_York' which automatically handles EST/EDT transitions
3. In May, you'll get EDT (UTC-4) rather than EST (UTC-5)

The output would be: `2024-05-09 06:30:45.340124-04:00`

"""

from datetime import datetime
import pytz

# Parse the string to datetime (UTC)
utc_time = datetime.strptime("2024-05-09T10:30:45:340124Z", "%Y-%m-%dT%H:%M:%S:%fZ")

# Make it timezone aware (UTC)
utc_time = pytz.utc.localize(utc_time)

# Convert to Eastern Time
eastern = pytz.timezone('America/New_York')
eastern_time = utc_time.astimezone(eastern)

print(eastern_time)  # This will be EDT since May is during Daylight Savings