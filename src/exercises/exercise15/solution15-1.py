import pandas as pd

try:

    # Read the CSV into a DataFrame
    df = pd.read_csv('sample-1.csv')

    # Strip whitespace characters from 'effective_date' column
    df['effective_date'] = df['effective_date'].str.strip()
    # Remove the timezone offset
    # datetime_str_no_tz = datetime_str[:-3]
    df['effective_date'] = df['effective_date'].str.slice(stop=-3)

    # format_str = '%m/%d/%Y'
    format_str = "%m/%d/%Y %H:%M:%S.%f"

    # Convert 'effective_date' column to datetime format
    df['effective_date'] = pd.to_datetime(df['effective_date'], format=format_str)

    # Filter rows where id = 1 and find the row with the latest effective_date
    filtered_df = df[df['id'] == 1].sort_values(by='effective_date', ascending=False).head(1)

    # Print the result
    print(filtered_df)

except KeyError as e:
    print(f"KeyError: {e}")
except FileNotFoundError:
    print("FileNotFoundError: Ensure the file path is correct and accessible.")
except Exception as e:
    print(f"An error occurred: {e}")


'''
# Convert 'effective_date' column to datetime format
df['effective_date'] = pd.to_datetime(df['effective_date'], format='%m/%d/%Y')

# Filter rows with id = 1
filtered_df = df[df['id'] == 1]

# Find the row with the latest effective_date
latest_row = filtered_df.loc[filtered_df['effective_date'].idxmax()]

# Example datetime string
datetime_str = "06/16/2024 18:18:24.533-04"

# Define the format to parse the datetime string
format_str = "%m/%d/%Y %H:%M:%S.%f%z"

datetime_str = "06/16/2024 18:18:24.533-04"

# Remove the timezone offset
datetime_str_no_tz = datetime_str[:-3]

# Convert datetime string to datetime format using pandas
dt = pd.to_datetime(datetime_str_no_tz, format='%m/%d/%Y %H:%M:%S.%f')

'''