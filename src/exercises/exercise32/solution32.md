I'll help you create a function to search across all columns in a pandas DataFrame and return matching rows. Here are a few different approaches:

1. Basic search using string containment:
```python
def search_dataframe(df, search_string):
    # Convert search string to lowercase for case-insensitive search
    search_string = str(search_string).lower()
    
    # Convert all columns to string and search
    mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search_string, na=False)).any(axis=1)
    
    return df[mask]

# Usage example:
# result_df = search_dataframe(df, "search term")
```

2. More flexible search with error handling and options:
```python
def search_dataframe(df, search_string, case_sensitive=False, partial_match=True):
    """
    Search across all columns in a DataFrame and return matching rows.
    
    Parameters:
    df : pandas DataFrame
        The DataFrame to search in
    search_string : str
        The string to search for
    case_sensitive : bool, default False
        Whether to perform case-sensitive search
    partial_match : bool, default True
        If True, finds partial matches. If False, requires exact matches
    
    Returns:
    pandas DataFrame with matching rows
    """
    try:
        # Convert search string to string type
        search_string = str(search_string)
        
        # Create a mask for matching rows
        mask = pd.Series(False, index=df.index)
        
        # Process each column
        for column in df.columns:
            # Convert column to string type
            col_values = df[column].astype(str)
            
            if not case_sensitive:
                col_values = col_values.str.lower()
                search_term = search_string.lower()
            else:
                search_term = search_string
            
            if partial_match:
                # Add matches to mask using contains
                mask |= col_values.str.contains(search_term, na=False)
            else:
                # Add exact matches to mask
                mask |= col_values == search_term
        
        # Return filtered DataFrame
        return df[mask]
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Usage example:
# result = search_dataframe(df, "search term", case_sensitive=False, partial_match=True)
```

3. Using regex for more advanced search patterns:
```python
def search_dataframe_regex(df, pattern):
    """
    Search DataFrame using regex pattern.
    
    Parameters:
    df : pandas DataFrame
        The DataFrame to search in
    pattern : str
        Regular expression pattern to match
        
    Returns:
    pandas DataFrame with matching rows
    """
    try:
        # Create mask for matching rows using regex
        mask = df.astype(str).apply(lambda x: x.str.contains(pattern, case=False, regex=True, na=False)).any(axis=1)
        return df[mask]
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return pd.DataFrame()

# Usage example:
# result = search_dataframe_regex(df, r"pattern\d+")
```

Example usage with sample data:
```python
import pandas as pd

# Create sample DataFrame
data = {
    'Name': ['John Smith', 'Jane Doe', 'Bob Wilson'],
    'Age': [30, 25, 45],
    'City': ['New York', 'Boston', 'Chicago'],
    'Email': ['john@email.com', 'jane@email.com', 'bob@email.com']
}
df = pd.DataFrame(data)

# Basic search
result1 = search_dataframe(df, "john")
print("\nBasic search for 'john':")
print(result1)

# Case-sensitive exact match
result2 = search_dataframe(df, "John Smith", case_sensitive=True, partial_match=False)
print("\nExact match search:")
print(result2)

# Regex search for email pattern
result3 = search_dataframe_regex(df, r'\w+@email\.com')
print("\nRegex search for email pattern:")
print(result3)
```

Key features of these functions:
- Handle different data types by converting to strings
- Option for case-sensitive/insensitive search
- Option for partial or exact matches
- Error handling for invalid inputs
- Support for regex patterns
- Handle NaN/missing values safely

Choose the version that best fits your needs:
- Use the first version for simple searches
- Use the second version for more control over search behavior
- Use the third version when you need regex pattern matching

The functions will return a DataFrame containing only the rows where the search term appears in any column.