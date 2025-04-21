Given a date time return True if the date and time fall within 8 am and 10 pm and it's a working day(meaning it is not saturday or
sunday or federal holiday or the days when stock market is closed)


* Checks if the date is a weekend (Saturday or Sunday)
* Checks if the date is a US federal holiday
* Checks for additional stock market closure days (like Good Friday)
* Verifies if the time is within the specified working hours

You'll need to install the holidays and python-dateutil packages:
```shell
pip install holidays python-dateutil
```
