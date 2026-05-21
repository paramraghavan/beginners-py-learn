"""
takne is a csv file , taken in colmsn to order by, taken in array of src and target columsn to
compare(it adds all cloums in src and target separately for each row, if they  do no match print n mismatched rows,
if n is 0 , all rows all rows. would like to know whic exact n rows mismatched
"""
import pandas as pd


def compare_row_sums(file_path, order_by, src_cols, target_cols):
    df = pd.read_csv(file_path)

    # Sort data
    df = df.sort_values(by=order_by).reset_index(drop=True)

    # Calculate row-wise sums for the two groups
    src_sum = df[src_cols].sum(axis=1)
    target_sum = df[target_cols].sum(axis=1)

    # Find where the sums differ
    mismatch_mask = src_sum != target_sum
    mismatched_rows = df[mismatch_mask].index.tolist()

    n = len(mismatched_rows)

    if n == 0:
        print("All rows match.")
    else:
        print(f"{n} mismatched rows found based on sums.")
        print(f"Mismatched indices: {mismatched_rows}")

        # Show the calculation for the mismatches
        for idx in mismatched_rows:
            print(f"\nRow index {idx}:")
            print(f"  Source Sum ({src_cols}): {src_sum[idx]}")
            print(f"  Target Sum ({target_cols}): {target_sum[idx]}")

# Example usage:
# compare_row_sums('data.csv', order_by=['id'], src_cols=['q1', 'q2'], target_cols=['total_q'])