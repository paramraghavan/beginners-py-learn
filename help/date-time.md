```
import datetime as d

x = d.datetime.now()
x.year

We can use a method strftime() to format the date outputs.
print(x.strftime("%A")) #Weekday Full Version

List Of All Format Codes:
%a	Weekday, short version	(Wed)	
%A	Weekday, full version	(Wednesday)	
%w	Weekday as a number 0-6, 0 is Sunday	(3)	
%d	Day of month 01-31	(31)	
%b	Month name, short version	(Dec)	
%B	Month name, full version	(December)	
%m	Month as a number 01-12	(12)	
%y	Year, short version, without century	(18)
%Y	Year, full version	(2018)	
%H	Hour 00-23	(17)	
%I	Hour 00-12	(05)	
%p	AM/PM	(PM)	
%M	Minute 00-59	(41)	
%S	Second 00-59	(08)	
%f	Microsecond 000000-999999	(548513)	
%z	UTC offset	(+0100)	
%Z	Timezone	(CST)	
%j	Day number of year 001-366	(365)	
%U	Week number of year, Sunday as the first day of week, 00-53	(52)	
%W	Week number of year, Monday as the first day of week, 00-53	(52)	
%c	Local version of date and time	Mon Dec 31 17:41:00 2018	
%C	Century	(20)	
%x	Local version of date	(12/31/18)	
%X	Local version of time	(17:41:00)	
%%	A % character	(%)	
%G	ISO 8601 year	(2018)	
%u	ISO 8601 weekday (1-7)	(1)	

### Creating Date Objects
Use datetime() class which takes three compulsory parameters - year, month and day. 
It also takes hour, minute, second, microsecond and zone but they are optional.
x = datetime.datetime(2020, 5, 17)

### Time Module
time is one more popular modules in python.
import time

# The function time.time() returns the current system time in ticks since 00:00:00 hrs January 1, 1970(epoch)
ticks = time.time()

# Get Current Time
localtime = time.localtime(time.time())

# Get the Formatted Timelocaltime = time.asctime( time.localtime(time.time())
#Sleep
time.sleep(5)

```
