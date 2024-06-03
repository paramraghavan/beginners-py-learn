from datetime import datetime

x = '2024-05-09 10:30:45:123456'


# Current datetime
now = datetime.now()
print(now)

# Creating a specific datetime object
specific_datetime = datetime(2024, 6, 3, 10, 30, 45, 123456)
print(specific_datetime)

# result
# 2024-06-03 11:05:03.058475
# 2024-06-03 10:30:45.123456