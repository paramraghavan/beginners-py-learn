"""
create a simple python script to compare 2 csv file which have identitical schema
takens in a array of colums to order by , taken in an arary of column s to compare if no columns are metnioned then all columns.
 If rows do no match print n mismatched rows, if n is 0 , all rows. would like to know which exact n rows mismatched in src and target
"""

import pandas as pd

def compare_csv_files(file_src, file_target, order_by, compare_cols=None):
    # Load data
    df_src = pd.read_csv(file_src)
    df_target = pd.read_csv(file_target)

    # Sort to ensure rows align
    df_src = df_src.sort_values(by=order_by).reset_index(drop=True)
    df_target = df_target.sort_values(by=order_by).reset_index(drop=True)

    # If no columns mentioned, compare all
    if not compare_cols:
        compare_cols = df_src.columns.tolist()

    # Create a mask for rows that do not match in the specified columns
    mismatch_mask = (df_src[compare_cols] != df_target[compare_cols]).any(axis=1)
    mismatched_rows = df_src[mismatch_mask].index.tolist()

    n = len(mismatched_rows)

    if n == 0:
        print("All rows match.")
    else:
        print(f"{n} mismatched rows found.")
        print(f"Mismatched indices: {mismatched_rows}")

        # Display the specific differences
        for idx in mismatched_rows:
            print(f"\nRow index {idx}:")
            print(f"  Source: {df_src.loc[idx, compare_cols].to_dict()}")
            print(f"  Target: {df_target.loc[idx, compare_cols].to_dict()}")

# Example usage:
# compare_csv_files('src.csv', 'target.csv', order_by=['id'], compare_cols=['name', 'price'])
# compare_csv_files('src.csv', 'target.csv', order_by=['id'], compare_cols=['name', 'price'])