import os
import pandas as pd


def search_files(directory, search_value):
    matches = []

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith('.csv'):
                    # Read the CSV file into a DataFrame
                    df = pd.read_csv(file_path)
                    # Perform an exact match search
                    match = df[df.apply(lambda row: row.astype(str).str.contains(f'^{search_value}$').any(), axis=1)]
                    if not match.empty:
                        matches.append((file_path, match))
                else:
                    # Read the file as a text file
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if search_value in line:
                                matches.append((file_path, i + 1, line.strip()))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return matches


# Usage
directory = r'/Users/paramraghavan/dev/beginners-py-learn/src/advance_stuff'
search_value = 'superclass'
matching_lines = search_files(directory, search_value)

# Print the results
for match in matching_lines:
    if isinstance(match[1], pd.DataFrame):
        print(f"File: {match[0]}")
        print(match[1])
    else:
        print(f"File: {match[0]}, Line: {match[1]}")
        print(match[2])
    print()
