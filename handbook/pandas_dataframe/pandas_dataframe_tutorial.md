# Pandas DataFrame Tutorial

A practical guide with runnable examples using a chargeback dataset.
All examples use the same DataFrame so you can follow top to bottom.

---

## Setup
```shell
pip install pandas numpy pandasql   
```

```python
import pandas as pd
import numpy as np

```


---

## 1. Creating a DataFrame

### From a dictionary — most common way

```python
df = pd.DataFrame({
    'employee_id': ['C1234', 'F5678', 'C9012', 'F3456', 'C7890'],
    'department':  ['Quant', 'Risk',  'Quant', 'Tech',  'Risk'],
    'month':       ['2025-01', '2025-01', '2025-02', '2025-02', '2025-02'],
    'cost':        [1200.0, 850.0, 2100.0, 450.0, 3200.0],
    'cpu_hours':   [120, 80, 210, 45, 310],
    'gpu_hours':   [10,   0,  30,  5,  50],
})
```

```
  employee_id department    month    cost  cpu_hours  gpu_hours
0       C1234      Quant  2025-01  1200.0        120         10
1       F5678       Risk  2025-01   850.0         80          0
2       C9012      Quant  2025-02  2100.0        210         30
3       F3456       Tech  2025-02   450.0         45          5
4       C7890       Risk  2025-02  3200.0        310         50
```

### From a CSV file

```python
df = pd.read_csv('chargeback.csv')
```

### From a list of dicts

```python
rows = [
    {'employee_id': 'C1234', 'cost': 1200.0},
    {'employee_id': 'F5678', 'cost':  850.0},
]
df = pd.DataFrame(rows)
```

---

## 2. Inspecting a DataFrame

```python
df.shape          # (5, 6)  — rows, columns
df.columns        # Index(['employee_id', 'department', ...])
df.dtypes         # data type of each column
df.head(3)        # first 3 rows
df.tail(3)        # last 3 rows
df.info()         # column types + non-null counts
df.describe()     # statistics for numeric columns
```

**`df.describe()` output:**

```
               cost   cpu_hours  gpu_hours
count     5.000000    5.000000   5.000000
mean   1560.000000  153.000000  19.000000
std    1100.795167  107.214738  20.736441
min     450.000000   45.000000   0.000000
25%     850.000000   80.000000   5.000000
50%    1200.000000  120.000000  10.000000
75%    2100.000000  210.000000  30.000000
max    3200.000000  310.000000  50.000000
```

**Quick value counts:**

```python
df['department'].value_counts()
# Quant    2
# Risk     2
# Tech     1
```

---

## 3. Selecting Data

### Single column → returns a Series

```python
df['cost']
# 0    1200.0
# 1     850.0
# 2    2100.0
# 3     450.0
# 4    3200.0
```

### Multiple columns → returns a DataFrame

```python
df[['employee_id', 'cost']]
```

```
  employee_id    cost
0       C1234  1200.0
1       F5678   850.0
2       C9012  2100.0
3       F3456   450.0
4       C7890  3200.0
```

### By position — `iloc` (integer location)

```python
df.iloc[0]        # first row as Series
df.iloc[0:2]      # rows 0 and 1
df.iloc[0:2, 0:3] # rows 0-1, columns 0-2
df.iloc[-1]       # last row
```

### By label — `loc` (label / condition based)

```python
df.loc[df['department'] == 'Quant']
```

```
  employee_id department    month    cost  cpu_hours  gpu_hours
0       C1234      Quant  2025-01  1200.0        120         10
2       C9012      Quant  2025-02  2100.0        210         30
```

```python
# loc with specific columns
df.loc[df['department'] == 'Quant', ['employee_id', 'cost']]
```

---

## 4. Filtering Rows

### Single condition

```python
df[df['cost'] > 1000]
```

```
  employee_id department    month    cost  cpu_hours  gpu_hours
0       C1234      Quant  2025-01  1200.0        120         10
2       C9012      Quant  2025-02  2100.0        210         30
4       C7890       Risk  2025-02  3200.0        310         50
```

### Multiple conditions

```python
# AND  →  &    (must wrap each condition in parentheses)
df[(df['department'] == 'Quant') & (df['cost'] > 1000)]

# OR   →  |
df[(df['cost'] < 500) | (df['cost'] > 2000)]

# NOT  →  ~
df[~(df['department'] == 'Tech')]
```

### Filter on a list of values

```python
df[df['department'].isin(['Quant', 'Risk'])]
```

### Filter on string pattern

```python
df[df['employee_id'].str.startswith('C')]   # all C employees
df[df['month'].str.contains('2025-02')]     # February rows
```

---

## 5. Adding and Modifying Columns

### Simple arithmetic

```python
df['total_hours']   = df['cpu_hours'] + df['gpu_hours']
df['cost_per_cpu']  = (df['cost'] / df['cpu_hours']).round(2)
```

### Boolean column

```python
df['heavy_user'] = df['cost'] > df['cost'].median()
```

```
  employee_id  total_hours  cost_per_cpu  heavy_user
0       C1234          130         10.00       False
1       F5678           80         10.62       False
2       C9012          240         10.00        True
3       F3456           50         10.00       False
4       C7890          360         10.32        True
```

### Conditional column with `np.where`

```python
# np.where(condition, value_if_true, value_if_false)
df['tier'] = np.where(df['cost'] >= 2000, 'Premium', 'Standard')
```

### Multi-band label with `apply`

```python
def cost_band(cost):
    if cost >= 2000: return 'High'
    if cost >= 1000: return 'Mid'
    return 'Low'

df['cost_band'] = df['cost'].apply(cost_band)

# Or as a lambda:
df['cost_band'] = df['cost'].apply(
    lambda x: 'High' if x >= 2000 else 'Mid' if x >= 1000 else 'Low'
)
```

```
  employee_id    cost cost_band
0       C1234  1200.0       Mid
1       F5678   850.0       Low
2       C9012  2100.0      High
3       F3456   450.0       Low
4       C7890  3200.0      High
```

### Rename columns

```python
df = df.rename(columns={'cost': 'total_cost', 'cpu_hours': 'cpu'})
```

### Drop columns

```python
df = df.drop(columns=['gpu_hours', 'total_hours'])
```

---

## 6. Sorting

```python
# Single column, descending
df.sort_values('cost', ascending=False)

# Multiple columns
df.sort_values(['department', 'cost'], ascending=[True, False])

# Sort by index
df.sort_index()
```

```
  employee_id    cost
4       C7890  3200.0
2       C9012  2100.0
0       C1234  1200.0
1       F5678   850.0
3       F3456   450.0
```

---

## 7. Groupby — Aggregate by Category

### Single aggregation

```python
df.groupby('department')['cost'].sum()
```

```
department
Quant    3300.0
Risk     4050.0
Tech      450.0
```

### Multiple aggregations at once

```python
df.groupby('department').agg(
    total_cost  = ('cost',        'sum'),
    avg_cost    = ('cost',        'mean'),
    max_cost    = ('cost',        'max'),
    num_users   = ('employee_id', 'nunique'),
    total_cpu   = ('cpu_hours',   'sum'),
).round(2)
```

```
            total_cost  avg_cost  max_cost  num_users  total_cpu
department
Quant           3300.0    1650.0    2100.0          2        330
Risk            4050.0    2025.0    3200.0          2        390
Tech             450.0     450.0     450.0          1         45
```

### Groupby multiple columns

```python
df.groupby(['department', 'month'])['cost'].sum().reset_index()
```

### Common aggregation functions

| Function | What it does |
|---|---|
| `sum` | total |
| `mean` | average |
| `median` | middle value |
| `min` / `max` | smallest / largest |
| `count` | number of rows (includes NaN) |
| `nunique` | number of distinct values |
| `std` | standard deviation |
| `first` / `last` | first or last value in group |

---

## 8. Pivot Tables

Pivot tables reshape data: rows become one dimension, columns another.

```python
df.pivot_table(
    index   = 'employee_id',   # rows
    columns = 'month',         # columns
    values  = 'cost',          # values to fill in
    aggfunc = 'sum',           # how to aggregate
    fill_value = 0             # replace NaN with 0
)
```

```
month        2025-01  2025-02
employee_id
C1234         1200.0      0.0
C7890            0.0   3200.0
C9012            0.0   2100.0
F3456            0.0    450.0
F5678          850.0      0.0
```

### Month-over-month change using pivot

```python
pivot = df.pivot_table(
    index='employee_id', columns='month', values='cost',
    aggfunc='sum', fill_value=0
)

months = pivot.columns.tolist()
for i in range(1, len(months)):
    prev, curr = months[i-1], months[i]
    pivot[f'chg_{curr}']  = (pivot[curr] - pivot[prev]).round(2)
    pivot[f'chg%_{curr}'] = (
        (pivot[curr] - pivot[prev]) / pivot[prev].replace(0, pd.NA) * 100
    ).round(1)
```

---

## 9. Merging DataFrames

### Inner join — only rows that match in both

```python
dept_info = pd.DataFrame({
    'department': ['Quant', 'Risk', 'Tech'],
    'vp':         ['Alice', 'Bob',  'Carol'],
    'budget':     [500000, 300000, 200000],
})

merged = df.merge(dept_info, on='department', how='inner')
```

### Left join — keep all rows from left, match where possible

```python
merged = df.merge(dept_info, on='department', how='left')
```

```
  employee_id department     vp    cost
0       C1234      Quant  Alice  1200.0
1       F5678       Risk    Bob   850.0
2       C9012      Quant  Alice  2100.0
3       F3456       Tech  Carol   450.0
4       C7890       Risk    Bob  3200.0
```

### Join types

| `how=` | Keeps |
|---|---|
| `'inner'` | only rows that match in both DataFrames |
| `'left'` | all rows from left, matched rows from right |
| `'right'` | matched from left, all from right |
| `'outer'` | all rows from both, NaN where no match |

### Join on different column names

```python
df.merge(dept_info, left_on='dept_code', right_on='department', how='left')
```

---

## 10. Concatenating DataFrames

```python
jan = pd.DataFrame({'employee_id': ['C1234'], 'cost': [1200.0], 'month': ['2025-01']})
feb = pd.DataFrame({'employee_id': ['C1234'], 'cost': [1450.0], 'month': ['2025-02']})

# Stack rows
combined = pd.concat([jan, feb], ignore_index=True)

# Stack columns side by side
combined = pd.concat([df1, df2], axis=1)
```

---

## 11. Handling Missing Data

```python
# Introduce some NaN values for demo
df.loc[1, 'cost']      = np.nan
df.loc[3, 'gpu_hours'] = np.nan
```

### Detect missing values

```python
df.isnull()               # True where NaN
df.isnull().sum()         # count per column
df.isnull().sum().sum()   # total NaN count
```

```
cost         1
gpu_hours    1
```

### Drop rows with any NaN

```python
df.dropna()                        # drop if any column is NaN
df.dropna(subset=['cost'])         # drop only if 'cost' is NaN
df.dropna(thresh=5)                # drop if fewer than 5 non-NaN values
```

### Fill missing values

```python
# Fill with a fixed value
df['gpu_hours'].fillna(0)

# Fill with column median
df['cost'].fillna(df['cost'].median())

# Fill multiple columns at once
df.fillna({'cost': df['cost'].median(), 'gpu_hours': 0})

# Forward-fill (use previous row's value) — useful for time series
df['cost'].fillna(method='ffill')
```

### Check before and after

```python
df2 = df.fillna({'cost': df['cost'].median(), 'gpu_hours': 0})
print(df2[['employee_id', 'cost', 'gpu_hours']])
```

```
  employee_id    cost  gpu_hours
0       C1234  1200.0       10.0
1       F5678  1650.0        0.0   ← was NaN, filled with median 1650
2       C9012  2100.0       30.0
3       F3456   450.0        0.0   ← was NaN, filled with 0
4       C7890  3200.0       50.0
```

---

## 12. String Operations

All string methods live under `.str`:

```python
df['employee_id'].str.upper()           # 'C1234' → 'C1234' (already upper)
df['employee_id'].str.lower()           # 'C1234' → 'c1234'
df['employee_id'].str.len()             # 5
df['employee_id'].str.strip()           # remove leading/trailing whitespace
df['employee_id'].str.replace('-', '_') # replace characters
df['employee_id'].str.contains('C')     # True/False mask
df['employee_id'].str.startswith('C')   # True/False mask
df['employee_id'].str[0]                # first character
df['employee_id'].str[1:]               # everything after first character
df['month'].str.split('-')              # split on delimiter → list
```

### Practical example — split employee_id into prefix and number

```python
df['prefix'] = df['employee_id'].str[0]     # 'C' or 'F'
df['number'] = df['employee_id'].str[1:]    # '1234', '5678', etc.
```

```
  employee_id prefix number
0       C1234      C   1234
1       F5678      F   5678
2       C9012      C   9012
3       F3456      F   3456
4       C7890      C   7890
```

---

## 13. DateTime Operations

```python
# Parse strings to datetime
df['date'] = pd.to_datetime(df['month'])

# Extract components
df['year']    = df['date'].dt.year
df['month_n'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['weekday'] = df['date'].dt.day_name()

# Date arithmetic
df['days_since_start'] = (df['date'] - df['date'].min()).dt.days

# Filter by date range
start = pd.Timestamp('2025-01-01')
end   = pd.Timestamp('2025-06-30')
df[df['date'].between(start, end)]

# Resample (group by time period)
df.set_index('date').resample('ME')['cost'].sum()  # monthly totals
```

---

## 14. Apply and Map

### `apply` — run a function on each row or column

```python
# On a column (Series) — one value in, one value out
df['cost_rounded'] = df['cost'].apply(lambda x: round(x, -2))  # nearest 100

# On a whole row — use axis=1
def efficiency(row):
    if row['cpu_hours'] == 0:
        return 0
    return round(row['cost'] / row['cpu_hours'], 2)

df['efficiency'] = df.apply(efficiency, axis=1)
```

### `map` — replace values using a dictionary

```python
dept_map = {'Quant': 'Quantitative Research',
            'Risk':  'Risk Management',
            'Tech':  'Technology'}

df['dept_full'] = df['department'].map(dept_map)
```

### `applymap` / `map` on whole DataFrame

```python
# Round every numeric cell to 1 decimal place
df[['cost', 'cpu_hours']].map(lambda x: round(x, 1))
```

---

## 15. Reshaping — `melt` (wide → long)

```python
# Start with a wide pivot table
wide = df.pivot_table(index='employee_id', columns='month',
                      values='cost', aggfunc='sum', fill_value=0).reset_index()

# wide:
#   employee_id  2025-01  2025-02
#         C1234   1200.0      0.0
#         C7890      0.0   3200.0

# Melt back to long format
long = wide.melt(
    id_vars    = ['employee_id'],   # columns to keep as-is
    var_name   = 'month',           # new column for old column headers
    value_name = 'cost',            # new column for the values
)

# long:
#   employee_id    month    cost
#         C1234  2025-01  1200.0
#         C1234  2025-02     0.0
#         C7890  2025-01     0.0
#         C7890  2025-02  3200.0
```

---

## 16. Export / Save

```python
# CSV
df.to_csv('output.csv', index=False)      # index=False → don't write row numbers

# Excel
df.to_excel('output.xlsx', index=False, sheet_name='Chargeback')

# Multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='Data',    index=False)
    summary.to_excel(writer, sheet_name='Summary', index=False)

# JSON
df.to_json('output.json', orient='records', indent=2)

# Parquet (fast binary format, good for large files)
df.to_parquet('output.parquet', index=False)
```

---

## 17. Reading Files

```python
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', usecols=['employee_id', 'cost'])  # only some columns
df = pd.read_csv('data.csv', dtype={'employee_id': str})       # force type
df = pd.read_csv('data.csv', parse_dates=['date_column'])      # auto-parse dates
df = pd.read_csv('data.csv', nrows=1000)                       # first 1000 rows only

df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df = pd.read_json('data.json')
df = pd.read_parquet('data.parquet')
```

---

## 18. Common Patterns

### Check for duplicates

```python
df.duplicated()                          # True where duplicate row
df.duplicated(subset=['employee_id'])    # duplicate employee_id only
df.drop_duplicates()                     # remove duplicate rows
df.drop_duplicates(subset=['employee_id'], keep='last')  # keep last occurrence
```

### Reset index after filtering

```python
filtered = df[df['cost'] > 1000].reset_index(drop=True)
```

### Chain operations

```python
result = (
    df
    .query("department in ['Quant', 'Risk']")
    .assign(cost_k = lambda x: x['cost'] / 1000)
    .groupby('department')
    .agg(total_cost_k=('cost_k', 'sum'))
    .sort_values('total_cost_k', ascending=False)
    .reset_index()
)
```

### Percentage of total

```python
df['cost_pct'] = (df['cost'] / df['cost'].sum() * 100).round(1)
```

### Rank within group

```python
df['rank_in_dept'] = df.groupby('department')['cost'].rank(ascending=False)
```

### Rolling average (time series)

```python
df = df.sort_values('month')
df['cost_3mo_avg'] = df.groupby('employee_id')['cost'].transform(
    lambda x: x.rolling(3, min_periods=1).mean()
)
```

---

## Quick Reference

```python
# CREATE
pd.DataFrame({'col': [1,2,3]})          # from dict
pd.read_csv('file.csv')                  # from file

# INSPECT
df.shape | df.dtypes | df.head()
df.describe() | df.info()
df['col'].value_counts()

# SELECT
df['col']                                # single column → Series
df[['a','b']]                            # multiple columns → DataFrame
df.iloc[0:3]                             # by position
df.loc[df['col'] > 5]                    # by condition

# FILTER
df[df['x'] > 5]
df[(df['x'] > 5) & (df['y'] == 'A')]
df[df['x'].isin([1,2,3])]
df.query("x > 5 and y == 'A'")          # SQL-like string

# TRANSFORM
df['new'] = df['a'] + df['b']           # arithmetic
df['new'] = df['col'].apply(fn)          # function per value
df['new'] = np.where(condition, a, b)   # conditional

# AGGREGATE
df.groupby('col').agg(n=('x','sum'))
df.pivot_table(index, columns, values, aggfunc)

# MERGE
df.merge(other, on='key', how='left')
pd.concat([df1, df2], ignore_index=True)

# MISSING
df.isnull().sum()
df.fillna(0)
df.dropna(subset=['col'])

# EXPORT
df.to_csv('out.csv', index=False)
df.to_excel('out.xlsx', index=False)
```
