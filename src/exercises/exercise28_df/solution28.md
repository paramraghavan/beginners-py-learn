import pandas as pd
from datetime import datetime, timedelta
import io

# Sample data

data = """file1.zip,12/5/24 7:15:20 AM, 1.38 MB
file2.zip,12/5/24 7:12:20 AM, 0.21 KB
file3.zip,11/27/24 8:31:00 PM, 22.18 MB
file3.zip,7/2/24 3:31:00 PM, 0.78 KB"""

def convert_size_to_kb(size_str):
# Remove any spaces and split into value and unit
size_str = size_str.strip()
value = float(size_str.split()[0])
unit = size_str.split()[1].upper()

    # Convert to KB based on unit
    if unit == 'KB':
        return value
    elif unit == 'MB':
        return value * 1024
    elif unit == 'GB':
        return value * 1024 * 1024
    elif unit == 'B':
        return value / 1024
    else:
        raise ValueError(f"Unknown unit: {unit}")

# Read the string into a DataFrame

df = pd.read_csv(io.StringIO(data), names=['filename', 'intime', 'filesize'])

# Clean up the data

df['intime'] = pd.to_datetime(df['intime'])
df['filesize'] = df['filesize'].apply(convert_size_to_kb)

# Filter for last 30 minutes (assuming current time as reference)

current_time = datetime.now()
time_threshold = current_time - timedelta(minutes=30)
df_filtered = df[df['intime'] >= time_threshold]

# Sort by intime in ascending order

df_filtered = df_filtered.sort_values('intime')

# Display results

print("Original DataFrame:")
print(df)
print("\nFiltered and sorted DataFrame (last 30 minutes):")
print(df_filtered)