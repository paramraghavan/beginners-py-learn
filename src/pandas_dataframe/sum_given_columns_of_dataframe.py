import pandas as pd
import numpy as np

# 1. Create a dummy CSV file for demonstration since the user hasn't provided one yet
data = {
    'colA': [10, 20, 30, 40],
    'colB': [5, 15, 25, 35],
    'colC': [1, 2, 3, 4],
    'colD': [100, 200, 300, 400],
    'colE': [0.1, 0.2, 0.3, 0.4]
}
df_input = pd.DataFrame(data)
df_input.to_csv('input_data.csv', index=False)

# 2. Read the CSV file
df = pd.read_csv('input_data.csv')

# 3. List of column names to sum
cols_to_sum = ['colA', 'colC', 'colD']

# 4. Calculate sums and create a new DataFrame
# We create a dictionary where keys are 'col_name_sum' and values are the sums
sums_dict = {f"{col}_sum": [df[col].sum()] for col in cols_to_sum}
df_sums = pd.DataFrame(sums_dict)

# 5. Write to CSV
df_sums.to_csv('column_sums.csv', index=False)

# Display results
print("Input DataFrame Head:")
print(df.head())
print("\nColumn Sums DataFrame:")
print(df_sums)
