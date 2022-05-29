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