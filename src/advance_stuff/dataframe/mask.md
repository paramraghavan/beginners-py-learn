# mask 
Use to check if the row exists using the unique key and update the row

- Example row is unique by filename

```python
import pandas as pd
import datetime as datetime

df = pd.DataFrame(columns=['file_name', 'file_size', 'in_time'])

# Create a new row of data
row = {
    'file_name': 'example.txt',
    'file_size': 1024,
    'in_time': datetime.now()
}

# Create mask (boolean series matching file_name)
# row is unique by file_name
mask = df['file_name'] == 'example.txt'

# Example of what mask looks like:
# 0    False
# 1    True    <- matches 'example.txt'
# 2    False
# Name: file_name, dtype: bool

if mask.any():  # If file exists (any True in mask)
    # Update existing row
    df.loc[mask] = pd.Series(row)
else:
    # Append new row
    df.loc[len(df)] = row

```

- Example, row uses composite key of file_name + file_size for uniqueness.
```python

import pandas as pd
import datetime as datetime

df = pd.DataFrame(columns=['file_name', 'file_size', 'in_time'])

# Create a new row of data
row = {
    'file_name': 'example.txt',
    'file_size': 1024,
    'in_time': datetime.now()
}
# Create composite mask using both file_name and file_size
mask = (df['file_name'] == 'example.txt') & \
       (df['file_size'] == '1024')

if mask.any():
    df.loc[mask] = pd.Series(row)
else:
    df.loc[len(df)] = row

```