import pandas as pd
from datetime import datetime, timedelta
import io


def convert_size_to_kb(size_str):
    """Convert file size string to KB"""
    size = float(size_str.split()[0])
    unit = size_str.split()[1].upper()

    conversion = {
        'KB': 1,
        'MB': 1024,
        'GB': 1024 * 1024,
        'B': 1 / 1024
    }

    return size * conversion.get(unit, 0)


def process_file_data(data_string, minutes_limit=30):
    """Process file data with early filtering"""
    # Current time for comparison
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(minutes=minutes_limit)

    # Convert string to buffer for reading
    buffer = io.StringIO(data_string)

    # Process lines individually to apply early filtering
    filtered_lines = []

    for line in buffer:
        if line.strip():  # Skip empty lines
            filename, intime_str, size_str = [x.strip() for x in line.split(',')]

            # Convert intime string to datetime
            intime = datetime.strptime(intime_str, '%m/%d/%y %I:%M:%S %p')

            # Early filtering: only keep recent records
            if intime >= cutoff_time:
                # Convert size to KB
                size_kb = convert_size_to_kb(size_str)

                filtered_lines.append({
                    'filename': filename,
                    'intime': intime,
                    'size_kb': size_kb
                })

    # Create DataFrame from filtered data
    df = pd.DataFrame(filtered_lines)

    if not df.empty:
        # Sort by intime in ascending order
        df = df.sort_values('intime', ascending=True)

    return df


# Example usage
data = """file1.zip,12/5/24 7:15:20 AM, 1.38 MB
file2.zip,12/5/24 7:12:20 AM, 0.21 KB
file3.zip,11/27/24 8:31:00 PM, 22.18 MB
file3.zip,7/2/24 3:31:00 PM, 0.78 KB"""

# Process the data
df = process_file_data(data, minutes_limit=30)
print("\nFiltered and sorted DataFrame:")
print(df)

# Display memory usage
print("\nMemory usage per column:")
print(df.memory_usage(deep=True))
