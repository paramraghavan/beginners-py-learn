# Get Last date of Month
# Using calendar()
from datetime import datetime
import calendar

'''
get last day of the month from a give date
curr_date = '2019-01-21' #
format_data = '%Y-%m-%d'
'''
def last_day_of_month(curr_date:str, format_data:str) ->str:
    # string parsed to datatime
    run_date = datetime.strptime(curr_date, format_data)
    # calendar applied on the datetime object created above
    res = calendar.monthrange(run_date.year, run_date.month)[1]
    return str(res)

from datetime import datetime
import pytz

def convert_utc_est():
    # UTC time string
    utc_str = "2024-07-11T10:35:50.937931Z"

    # Parse UTC string to datetime object
    utc_time = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_time = pytz.utc.localize(utc_time)

    # Convert to EST
    est_timezone = pytz.timezone('America/New_York')
    est_time = utc_time.astimezone(est_timezone)

    # Format the output
    print(est_time)  # 2024-07-11 06:35:50.937931-04:00

#####################################################
from datetime import datetime
import pytz

"""
Compare b/w given utc time and now
utc_str = "2024-07-11T10:35:50.937931Z"
"""
def is_time_between(check_time):
    # Get current time in EST
    est_timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(est_timezone)

    # Your UTC time string
    utc_str = "2024-07-11T10:35:50.937931Z"
    utc_time = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_time = pytz.utc.localize(utc_time)

    # Convert UTC to EST
    est_time = utc_time.astimezone(est_timezone)

    # Make sure check_time is timezone aware
    if check_time.tzinfo is None:
        check_time = est_timezone.localize(check_time)

    # Check if time falls between current_time and est_time
    if current_time <= check_time <= est_time:
        return True
    return False


# Example usage:
check_datetime = datetime.now()  # time you want to check
result = is_time_between(check_datetime)
print(f"Is time between? {result}")

# To check specific time:
specific_time = datetime.strptime("2024-07-11 08:00:00", "%Y-%m-%d %H:%M:%S")
result = is_time_between(specific_time)
print(f"Is specific time between? {result}")







######################################################

# datetime object containing current date and time
now = datetime.now()
print("now =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)


curr_date = '2019-06-01' #
format_data = '%Y-%m-%d'
run_date = datetime.strptime(curr_date, format_data)
print(run_date)
# get the day for he give run date
day_val = run_date.strftime("%d")