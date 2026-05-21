"""
compare_csv.py
==============
Exhaustive side-by-side comparison of two CSV files using pandas.
Easy to read, tweak, and extend.

HOW TO USE
----------
1. Set FILE_A and FILE_B to your actual CSV paths.
2. Set KEY_COLS to the column(s) that uniquely identify each row (like a primary key).
   Set to None if you just want positional row comparison.
3. Run:  python compare_csv.py
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
#  CONFIGURATION  ← edit these
# ─────────────────────────────────────────────
FILE_A   = "file_a.csv"          # path to first  CSV
FILE_B   = "file_b.csv"          # path to second CSV
KEY_COLS = ["id"]                # column(s) that act as a unique key; None = row-by-row
ROUND_TO = 2                     # decimal places when comparing floats (None = exact)
# ─────────────────────────────────────────────


# ── helpers ───────────────────────────────────
SEP = "─" * 60

def section(title):
    print(f"\n{SEP}\n  {title}\n{SEP}")

def load(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()        # remove accidental whitespace
    return df

def normalise(df):
    """Sort columns alphabetically so column order doesn't matter."""
    return df.reindex(sorted(df.columns), axis=1)


# ── 1. load ───────────────────────────────────
df_a = load(FILE_A)
df_b = load(FILE_B)

print(f"\nLoaded  A: {FILE_A}  →  {df_a.shape[0]} rows × {df_a.shape[1]} cols")
print(f"Loaded  B: {FILE_B}  →  {df_b.shape[0]} rows × {df_b.shape[1]} cols")


# ── 2. shape ──────────────────────────────────
section("2. SHAPE")
if df_a.shape == df_b.shape:
    print("✅ Same shape:", df_a.shape)
else:
    print(f"❌ Different shapes  A={df_a.shape}  B={df_b.shape}")


# ── 3. columns ────────────────────────────────
section("3. COLUMNS")
cols_a = set(df_a.columns)
cols_b = set(df_b.columns)

only_in_a = cols_a - cols_b
only_in_b = cols_b - cols_a
common    = cols_a & cols_b

print(f"Columns only in A : {sorted(only_in_a) or 'none'}")
print(f"Columns only in B : {sorted(only_in_b) or 'none'}")
print(f"Common columns    : {len(common)}")

# Work only on common columns from here on
df_a = df_a[sorted(common)]
df_b = df_b[sorted(common)]


# ── 4. dtypes ─────────────────────────────────
section("4. DATA TYPES")
dtype_df = pd.DataFrame({"A": df_a.dtypes, "B": df_b.dtypes})
dtype_df["match"] = dtype_df["A"] == dtype_df["B"]
mismatches = dtype_df[~dtype_df["match"]]
if mismatches.empty:
    print("✅ All dtypes match")
else:
    print("❌ dtype mismatches:")
    print(mismatches.to_string())


# ── 5. duplicates ─────────────────────────────
section("5. DUPLICATE ROWS")
dup_a = df_a.duplicated().sum()
dup_b = df_b.duplicated().sum()
print(f"Duplicate rows in A: {dup_a}")
print(f"Duplicate rows in B: {dup_b}")


# ── 6. missing values ─────────────────────────
section("6. MISSING VALUES (NaN counts per column)")
na = pd.DataFrame({"A_nulls": df_a.isna().sum(), "B_nulls": df_b.isna().sum()})
na["diff"] = na["A_nulls"] - na["B_nulls"]
print(na.to_string())


# ── 7. key-based or positional alignment ──────
section("7. ROW ALIGNMENT")

if KEY_COLS and all(k in common for k in KEY_COLS):
    keys_a = set(map(tuple, df_a[KEY_COLS].values.tolist()))
    keys_b = set(map(tuple, df_b[KEY_COLS].values.tolist()))

    only_a = keys_a - keys_b
    only_b = keys_b - keys_a
    shared  = keys_a & keys_b

    print(f"Rows only in A (by key) : {len(only_a)}")
    print(f"Rows only in B (by key) : {len(only_b)}")
    print(f"Rows in both            : {len(shared)}")

    if only_a:
        print("\nSample keys only in A:", list(only_a)[:5])
    if only_b:
        print("\nSample keys only in B:", list(only_b)[:5])

    # align on shared keys
    # For a single key column pandas uses scalar index values, not tuples
    shared_lookup = [k[0] if len(KEY_COLS) == 1 else k for k in shared]
    df_a = df_a.set_index(KEY_COLS).loc[shared_lookup].sort_index()
    df_b = df_b.set_index(KEY_COLS).loc[shared_lookup].sort_index()
    value_cols = [c for c in df_a.columns if c not in KEY_COLS]

else:
    print("No KEY_COLS set → comparing row by row (positional)")
    min_rows = min(len(df_a), len(df_b))
    df_a = df_a.iloc[:min_rows].reset_index(drop=True)
    df_b = df_b.iloc[:min_rows].reset_index(drop=True)
    value_cols = list(df_a.columns)


# ── 8. cell-level diff ────────────────────────
section("8. CELL-LEVEL DIFFERENCES")

# optional float rounding before compare
if ROUND_TO is not None:
    num_cols = df_a[value_cols].select_dtypes(include="number").columns
    df_a[num_cols] = df_a[num_cols].round(ROUND_TO)
    df_b[num_cols] = df_b[num_cols].round(ROUND_TO)

# boolean mask: True = values differ
diff_mask = df_a[value_cols].ne(df_b[value_cols])

total_cells   = diff_mask.size
changed_cells = diff_mask.values.sum()
print(f"Total cells compared : {total_cells}")
print(f"Cells that differ    : {changed_cells}  ({changed_cells/total_cells*100:.2f}%)")

# per-column breakdown
col_diff = diff_mask.sum().rename("n_diffs")
col_diff = col_diff[col_diff > 0].sort_values(ascending=False)
if col_diff.empty:
    print("\n✅ No cell differences found!")
else:
    print("\nColumns with differences (sorted by count):")
    print(col_diff.to_string())


# ── 9. sample diffs (first 10 changed rows) ───
section("9. SAMPLE ROWS WITH DIFFERENCES (up to 10)")

changed_rows = diff_mask.any(axis=1)
n_changed    = changed_rows.sum()
print(f"Rows with at least one difference: {n_changed}")

if n_changed > 0:
    sample_idx = diff_mask[changed_rows].head(10).index
    for idx in sample_idx:
        changed_cols = diff_mask.loc[idx][diff_mask.loc[idx]].index.tolist()
        print(f"\n  Row [{idx}]  —  differs in: {changed_cols}")
        for col in changed_cols:
            print(f"    {col:20s}  A={df_a.at[idx, col]!r:20}  B={df_b.at[idx, col]!r}")


# ── 10. numeric column stats ──────────────────
section("10. NUMERIC COLUMN SUMMARY STATS (A vs B)")

num_cols = df_a[value_cols].select_dtypes(include="number").columns.tolist()
if num_cols:
    stats_a = df_a[num_cols].describe().T.add_prefix("A_")
    stats_b = df_b[num_cols].describe().T.add_prefix("B_")
    stats   = pd.concat([stats_a, stats_b], axis=1).sort_index(axis=1)
    print(stats.round(4).to_string())
else:
    print("No numeric columns in common set.")


# ── 11. full diff export ──────────────────────
section("11. EXPORT")

if n_changed > 0:
    out = "differences.csv"
    # build a side-by-side diff frame
    rows = []
    for idx in diff_mask[changed_rows].index:
        for col in diff_mask.columns:
            if diff_mask.at[idx, col]:
                rows.append({"row": idx, "column": col,
                              "value_A": df_a.at[idx, col],
                              "value_B": df_b.at[idx, col]})
    diff_export = pd.DataFrame(rows)
    diff_export.to_csv(out, index=False)
    print(f"Differences saved to: {out}  ({len(diff_export)} changed cells)")
else:
    print("No differences to export. ✅")

print(f"\n{SEP}\n  COMPARISON COMPLETE\n{SEP}\n")
