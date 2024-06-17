import pandas as pd

# Define the path to your CSV file
csv_file_path = 'sample.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Display the DataFrame (optional)
print("DataFrame:")
print(df)

# Define the column and value you want to query
column_name = 'age'
value_to_query = 25

# Query the DataFrame
result = df[df[column_name] >= value_to_query]





# Display the result
print(f"\nRows where {column_name} is {value_to_query}:")
print(result)

# Query the DataFrame
result = df[df[column_name] == value_to_query]

# Display the result
print(f"\nRows where {column_name} is {value_to_query}:")
print(result)

# Parse the result by columns
parsed_result = {}
for col in result.columns:
    parsed_result[col] = result[col].tolist()

# Display the parsed result
print("\nParsed result by columns:")
for key, value in parsed_result.items():
    print(f"{key}: {value}")