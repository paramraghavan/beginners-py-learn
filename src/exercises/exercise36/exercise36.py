from datetime import datetime, date
import calendar
import holidays


def get_us_financial_holidays(year):
    """
    Returns a list of US financial institution holidays for a given year.
    Uses the holidays library for accurate and maintained holiday calculations.
    """
    # Get US federal holidays
    us_holidays = holidays.US(years=year)

    # Convert to list of date objects and filter for financial institution holidays
    financial_holidays = []

    for holiday_date, holiday_name in us_holidays.items():
        # Include all major federal holidays that financial institutions observe
        if any(keyword in holiday_name.lower() for keyword in [
            'new year', 'martin luther king', 'washington', 'presidents',
            'memorial', 'juneteenth', 'independence', 'labor', 'columbus',
            'veterans', 'thanksgiving', 'christmas'
        ]):
            financial_holidays.append(holiday_date)

    return sorted(financial_holidays)


def is_business_day(check_date, holidays_list):
    """
    Check if a date is a business day (Monday-Friday, not a holiday)
    """
    # Check if it's a weekend (Saturday=5, Sunday=6)
    if check_date.weekday() >= 5:
        return False

    # Check if it's a holiday
    if check_date in holidays_list:
        return False

    return True


def get_fifth_business_day(year, month):
    """
    Find the 5th business day of a given month and year
    """
    holidays_list = get_us_financial_holidays(year)
    business_days_count = 0
    day = 1

    while day <= calendar.monthrange(year, month)[1]:
        current_date = date(year, month, day)

        if is_business_day(current_date, holidays_list):
            business_days_count += 1
            if business_days_count == 5:
                return current_date

        day += 1

    return None  # If there's no 5th business day in the month


def check_fifth_business_day():
    """
    Check if today is the 5th business day of the current month
    """
    today = datetime.now().date()
    current_year = today.year
    current_month = today.month

    fifth_business_day = get_fifth_business_day(current_year, current_month)

    print(f"Today's date: {today}")
    print(f"5th business day of {calendar.month_name[current_month]} {current_year}: {fifth_business_day}")

    if fifth_business_day and today == fifth_business_day:
        print("Hello 5th business day!")
    else:
        print("Not the right day")

    # Show holidays for reference
    holidays_list = get_us_financial_holidays(current_year)
    us_holidays = holidays.US(years=current_year)

    print(f"\nUS Financial Institution holidays for {current_year}:")
    for holiday_date in holidays_list:
        holiday_name = us_holidays.get(holiday_date, "Unknown Holiday")
        print(f"  {holiday_date} - {holiday_name}")


def test_given_date(test_date):
    """
    Test if a given date is the 5th business day of its month

    Args:
        test_date: Can be a date object, datetime object, or string in format 'YYYY-MM-DD'

    Returns:
        bool: True if it's the 5th business day, False otherwise
    """
    # Convert string to date if necessary
    if isinstance(test_date, str):
        try:
            test_date = datetime.strptime(test_date, '%Y-%m-%d').date()
        except ValueError:
            print(f"Invalid date format. Please use 'YYYY-MM-DD' format.")
            return False
    elif isinstance(test_date, datetime):
        test_date = test_date.date()

    year = test_date.year
    month = test_date.month

    fifth_business_day = get_fifth_business_day(year, month)

    print(f"Testing date: {test_date}")
    print(f"5th business day of {calendar.month_name[month]} {year}: {fifth_business_day}")

    # Check if the test date is a holiday
    us_holidays = holidays.US(years=year)
    if test_date in us_holidays:
        holiday_name = us_holidays[test_date]
        print(f"Note: {test_date} is {holiday_name}")

    if fifth_business_day and test_date == fifth_business_day:
        print("Hello 5th business day!")
        return True
    else:
        print("Not the right day")
        return False


def show_business_days_for_month(year, month):
    """
    Show all business days for a given month with their sequence number
    """
    holidays_list = get_us_financial_holidays(year)
    us_holidays = holidays.US(years=year)

    print(f"\nBusiness days for {calendar.month_name[month]} {year}:")
    business_day_count = 0

    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        current_date = date(year, month, day)

        if is_business_day(current_date, holidays_list):
            business_day_count += 1
            marker = " *** 5TH BUSINESS DAY ***" if business_day_count == 5 else ""
            print(f"  Business Day #{business_day_count}: {current_date}{marker}")
        else:
            reason = "Weekend"
            if current_date in us_holidays:
                reason = f"Holiday ({us_holidays[current_date]})"
            print(f"  {current_date} - {reason}")


# Run the check
if __name__ == "__main__":
    # Check if holidays library is available
    try:
        import holidays

        print("Using the 'holidays' library for accurate US holiday calculations")
        print("Install with: pip install holidays")
    except ImportError:
        print("ERROR: 'holidays' library not found!")
        print("Please install it with: pip install holidays")
        exit(1)

    print("=== Checking Today's Date ===")
    check_fifth_business_day()

    print("\n" + "=" * 50)

    # Test some specific dates as examples
    print("=== Testing Specific Dates ===")

    # Test current month's 5th business day
    today = datetime.now().date()
    fifth_bd = get_fifth_business_day(today.year, today.month)
    if fifth_bd:
        print(f"\nTesting the actual 5th business day of this month:")
        test_given_date(fifth_bd)

    # Test some other dates
    test_dates = [
        "2025-01-07",  # Example date
        "2025-02-06",  # Example date
        "2025-07-04",  # Independence Day - should not be 5th business day
        "2025-12-25",  # Christmas - should not be 5th business day
    ]

    for test_date in test_dates:
        print(f"\nTesting {test_date}:")
        test_given_date(test_date)

    print("\n" + "=" * 50)
    print("=== Business Days Breakdown for Current Month ===")
    show_business_days_for_month(today.year, today.month)

    print("\n" + "=" * 50)
    print("Usage examples:")
    print("- test_given_date('2025-08-07')")
    print("- test_given_date(date(2025, 8, 7))")
    print("- test_given_date(datetime(2025, 8, 7, 10, 30))")
    print("- show_business_days_for_month(2025, 8)")
# or make an array of 5th business day for next 10 years and use it