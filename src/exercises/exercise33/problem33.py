import datetime
import holidays
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


def is_working_time(datetime_str, start_time="08:00", end_time="22:00"):
    """
    Check if a datetime falls within working hours on a working day.

    Args:
        datetime_str (str): Datetime string in format "YYYY-MM-DD HH:MM:SS"
        start_time (str, optional): Start of working hours in format "HH:MM". Defaults to "08:00".
        end_time (str, optional): End of working hours in format "HH:MM". Defaults to "22:00".

    Returns:
        bool: True if datetime is within working hours on a working day, False otherwise
    """
    # Parse the input datetime
    try:
        current_dt = dt.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid datetime format. Use 'YYYY-MM-DD HH:MM:SS'")

    # Parse start and end times
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))

    # Check if it's a weekend
    if current_dt.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        return False

    # Get US holidays for the next 10 years
    ten_years_later = current_dt.date() + relativedelta(years=10)
    us_holidays = holidays.US(years=range(current_dt.year, ten_years_later.year + 1))

    # Check if it's a US federal holiday
    if current_dt.date() in us_holidays:
        return False

    # Hardcoded stock market closures (NYSE and NASDAQ) - not included in US holidays
    stock_market_closures = [
        # Good Friday closures (2025-2035)
        datetime.date(2025, 4, 18),
        datetime.date(2026, 4, 3),
        datetime.date(2027, 3, 26),
        datetime.date(2028, 4, 14),
        datetime.date(2029, 3, 30),
        datetime.date(2030, 4, 19),
        datetime.date(2031, 4, 11),
        datetime.date(2032, 3, 26),
        datetime.date(2033, 4, 15),
        datetime.date(2034, 4, 7),
        datetime.date(2035, 3, 23),

        # Add any other non-federal holidays specific to stock markets
        # Note: The regular holidays (New Year's, MLK Day, Presidents' Day, Memorial Day,
        # Juneteenth, Independence Day, Labor Day, Thanksgiving, Christmas)
        # are already handled by the holidays.US library + plus Good Friday, which we have hardcoded
        # for each year from 2025-2035
    ]

    # Check if it's a stock market closure day
    if current_dt.date() in stock_market_closures:
        return False

    # Check if time is within working hours
    current_time = current_dt.time()
    start_work_time = datetime.time(start_hour, start_minute)
    end_work_time = datetime.time(end_hour, end_minute)

    return start_work_time <= current_time <= end_work_time


# Example usage
if __name__ == "__main__":
    test_times = [
        "2025-04-21 09:30:00",  # Monday, during working hours
        "2025-04-20 14:00:00",  # Sunday, working hours but weekend
        "2025-12-25 13:00:00",  # Christmas, during working hours but holiday
        "2025-04-18 07:00:00",  # Good Friday (market closed)
        "2025-04-21 06:00:00",  # Monday, but before working hours
        "2025-04-21 23:00:00",  # Monday, but after working hours
        "2030-04-19 12:00:00",  # Good Friday 2030
        "2035-03-23 09:00:00",  # Good Friday 2035
    ]

    for test_time in test_times:
        print(f"{test_time}: {is_working_time(test_time)}")