import os
import glob
import re


directory = r'/Users/paramraghavan/dev/beginners-py-learn/src/advance_stuff/file_filter'
pattern = '*_processA_ABC-DEF_*_ready.txt'


# Construct the full path pattern
full_pattern = os.path.join(directory, pattern)

# Use glob to find files that match the pattern
matching_files = glob.glob(full_pattern)

# Function to extract the numeric part from the filename
def extract_number(filename):
    match = re.search(r'(\d+)_ready\.txt$', filename)
    return int(match.group(1)) if match else 0

# Sort the files by the numeric part
sorted_files = sorted(matching_files, key=extract_number)

# Count the number of matching files
count = len(sorted_files)
print(f"Number of files matching '{pattern}': {count}")

# Print the sorted files
for file in sorted_files:
    print(file)
