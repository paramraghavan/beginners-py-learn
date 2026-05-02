#!/usr/bin/env python3
"""
pandas_tutorial.py
==================
Run this file to see every tutorial example execute with real output.
Each section prints a header and its results.
"""

import pandas as pd
import numpy as np

def section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)

def show(label, value):
    print(f"\n--- {label} ---")
    print(value)


# ═══════════════════════════════════════════════════════
# 1. CREATING A DATAFRAME
# ═══════════════════════════════════════════════════════
section("1. Creating a DataFrame")

df = pd.DataFrame({
    'employee_id': ['C1234', 'F5678', 'C9012', 'F3456', 'C7890'],
    'department':  ['Quant', 'Risk',  'Quant', 'Tech',  'Risk'],
    'month':       ['2025-01', '2025-01', '2025-02', '2025-02', '2025-02'],
    'cost':        [1200.0, 850.0, 2100.0, 450.0, 3200.0],
    'cpu_hours':   [120, 80, 210, 45, 310],
    'gpu_hours':   [10,   0,  30,  5,  50],
})
show("Full DataFrame", df)

# ═══════════════════════════════════════════════════════
# 2. INSPECTING
# ═══════════════════════════════════════════════════════
section("2. Inspecting a DataFrame")

show("shape (rows, cols)", df.shape)
show("dtypes", df.dtypes)
show("head(3)", df.head(3))
show("describe()", df.describe().round(2))
show("value_counts department", df['department'].value_counts())


# ═══════════════════════════════════════════════════════
# 3. SELECTING DATA
# ═══════════════════════════════════════════════════════
section("3. Selecting Data")

show("Single column (Series)", df['cost'])
show("Multiple columns", df[['employee_id', 'cost']])
show("iloc [0:2] — first 2 rows by position", df.iloc[0:2])
show("loc — Quant rows only", df.loc[df['department'] == 'Quant'])


# ═══════════════════════════════════════════════════════
# 4. FILTERING
# ═══════════════════════════════════════════════════════
section("4. Filtering Rows")

show("cost > 1000", df[df['cost'] > 1000])
show("Quant AND cost > 1000", df[(df['department'] == 'Quant') & (df['cost'] > 1000)])
show("department in [Quant, Risk]", df[df['department'].isin(['Quant', 'Risk'])])
show("employee_id starts with C", df[df['employee_id'].str.startswith('C')])


# ═══════════════════════════════════════════════════════
# 5. ADDING COLUMNS
# ═══════════════════════════════════════════════════════
section("5. Adding and Modifying Columns")

df['total_hours']  = df['cpu_hours'] + df['gpu_hours']
df['cost_per_cpu'] = (df['cost'] / df['cpu_hours']).round(2)
df['heavy_user']   = df['cost'] > df['cost'].median()

# Conditional with np.where
df['tier'] = np.where(df['cost'] >= 2000, 'Premium', 'Standard')

# Multi-band label with apply
df['cost_band'] = df['cost'].apply(
    lambda x: 'High' if x >= 2000 else 'Mid' if x >= 1000 else 'Low'
)

show("New columns", df[['employee_id','total_hours','cost_per_cpu',
                         'heavy_user','tier','cost_band']])


# ═══════════════════════════════════════════════════════
# 6. SORTING
# ═══════════════════════════════════════════════════════
section("6. Sorting")

show("Sort by cost descending",
     df.sort_values('cost', ascending=False)[['employee_id','cost']])

show("Sort by department asc, cost desc",
     df.sort_values(['department','cost'], ascending=[True, False])
     [['employee_id','department','cost']])


# ═══════════════════════════════════════════════════════
# 7. GROUPBY
# ═══════════════════════════════════════════════════════
section("7. Groupby — Aggregate by Category")

show("Sum cost by department",
     df.groupby('department')['cost'].sum())

show("Multiple aggregations",
     df.groupby('department').agg(
         total_cost  = ('cost',        'sum'),
         avg_cost    = ('cost',        'mean'),
         max_cost    = ('cost',        'max'),
         num_users   = ('employee_id', 'nunique'),
         total_cpu   = ('cpu_hours',   'sum'),
     ).round(2))

show("Groupby department + month",
     df.groupby(['department','month'])['cost'].sum().reset_index())


# ═══════════════════════════════════════════════════════
# 8. PIVOT TABLE
# ═══════════════════════════════════════════════════════
section("8. Pivot Tables")

pivot = df.pivot_table(
    index      = 'employee_id',
    columns    = 'month',
    values     = 'cost',
    aggfunc    = 'sum',
    fill_value = 0,
)
show("Cost by employee × month", pivot)

# Add month-over-month change
months = pivot.columns.tolist()
for i in range(1, len(months)):
    prev, curr = months[i-1], months[i]
    pivot[f'chg_{curr}']  = (pivot[curr] - pivot[prev]).round(2)
    pivot[f'chg%_{curr}'] = (
        (pivot[curr] - pivot[prev]) / pivot[prev].replace(0, float('nan')) * 100
    ).round(1)
show("With month-over-month change", pivot)


# ═══════════════════════════════════════════════════════
# 9. MERGING
# ═══════════════════════════════════════════════════════
section("9. Merging DataFrames")

dept_info = pd.DataFrame({
    'department': ['Quant', 'Risk', 'Tech'],
    'vp':         ['Alice', 'Bob',  'Carol'],
    'budget':     [500000,  300000, 200000],
})

merged = df.merge(dept_info, on='department', how='left')
show("Left join — employee + VP info",
     merged[['employee_id','department','vp','cost','budget']])


# ═══════════════════════════════════════════════════════
# 10. CONCATENATING
# ═══════════════════════════════════════════════════════
section("10. Concatenating DataFrames")

jan = df[df['month'] == '2025-01'].copy()
feb = df[df['month'] == '2025-02'].copy()

combined = pd.concat([jan, feb], ignore_index=True)
show("Concat Jan + Feb (same as original)", combined[['employee_id','month','cost']])


# ═══════════════════════════════════════════════════════
# 11. MISSING DATA
# ═══════════════════════════════════════════════════════
section("11. Handling Missing Data")

df2 = df[['employee_id','cost','gpu_hours']].copy()
df2.loc[1, 'cost']      = np.nan
df2.loc[3, 'gpu_hours'] = np.nan

show("Null counts", df2.isnull().sum())

filled = df2.fillna({
    'cost':      df2['cost'].median(),
    'gpu_hours': 0,
})
show("After fillna (cost→median, gpu→0)", filled)

show("dropna — remove any row with NaN", df2.dropna())


# ═══════════════════════════════════════════════════════
# 12. STRING OPERATIONS
# ═══════════════════════════════════════════════════════
section("12. String Operations")

df['prefix'] = df['employee_id'].str[0]     # 'C' or 'F'
df['number'] = df['employee_id'].str[1:]    # '1234', etc.
df['dept_upper'] = df['department'].str.upper()

show("String splits and transforms",
     df[['employee_id','prefix','number','dept_upper']])


# ═══════════════════════════════════════════════════════
# 13. DATETIME OPERATIONS
# ═══════════════════════════════════════════════════════
section("13. DateTime Operations")

df['date']    = pd.to_datetime(df['month'])
df['year']    = df['date'].dt.year
df['month_n'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

show("Datetime components", df[['month','date','year','month_n','quarter']])


# ═══════════════════════════════════════════════════════
# 14. APPLY AND MAP
# ═══════════════════════════════════════════════════════
section("14. Apply and Map")

# Apply a function row-by-row
def efficiency_score(row):
    if row['cpu_hours'] == 0: return 0.0
    return round(row['cost'] / row['cpu_hours'], 2)

df['efficiency'] = df.apply(efficiency_score, axis=1)

# Map values using a dictionary
dept_map = {
    'Quant': 'Quantitative Research',
    'Risk':  'Risk Management',
    'Tech':  'Technology',
}
df['dept_full'] = df['department'].map(dept_map)

show("Apply (efficiency) + Map (dept_full)",
     df[['employee_id','cost','cpu_hours','efficiency','dept_full']])


# ═══════════════════════════════════════════════════════
# 15. RESHAPING — MELT (wide → long)
# ═══════════════════════════════════════════════════════
section("15. Melt — Wide to Long")

wide = df.pivot_table(
    index='employee_id', columns='month', values='cost',
    aggfunc='sum', fill_value=0
).reset_index()
show("Wide format", wide)

long = wide.melt(
    id_vars    = ['employee_id'],
    var_name   = 'month',
    value_name = 'cost',
)
show("Long format (melted)", long.sort_values(['employee_id','month']))


# ═══════════════════════════════════════════════════════
# 16. COMMON PATTERNS
# ═══════════════════════════════════════════════════════
section("16. Common Patterns")

# Percentage of total
df2 = df[['employee_id','cost']].copy()
df2['cost_pct'] = (df2['cost'] / df2['cost'].sum() * 100).round(1)
show("Percentage of total cost", df2)

# Chain operations
result = (
    df
    .query("department in ['Quant', 'Risk']")
    .assign(cost_k=lambda x: (x['cost'] / 1000).round(2))
    .groupby('department')
    .agg(total_cost_k=('cost_k', 'sum'), users=('employee_id', 'nunique'))
    .sort_values('total_cost_k', ascending=False)
    .reset_index()
)
show("Chained operations", result)

# Rank within group
df['rank_in_dept'] = df.groupby('department')['cost'].rank(ascending=False).astype(int)
show("Rank within department",
     df[['employee_id','department','cost','rank_in_dept']]
     .sort_values(['department','rank_in_dept']))


# ═══════════════════════════════════════════════════════
# 17. EXPORT
# ═══════════════════════════════════════════════════════
section("17. Export")

import os
os.makedirs('./output', exist_ok=True)
df[['employee_id','department','month','cost']].to_csv(
    './output/tutorial_export.csv', index=False)
print("  Saved: ./output/tutorial_export.csv")

print("\n" + "="*55)
print("  All examples complete!")
print("="*55)
