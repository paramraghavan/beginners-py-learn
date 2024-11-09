# Python script that converts JSON to CSV, handling arrays within the JSON structure.


```python
import json
import csv
import pandas as pd
from typing import List, Dict, Any


def flatten_json_array(value: Any, separator: str = '|') -> str:
    """
    Converts array values to a string with the specified separator.
    """
    if isinstance(value, (list, tuple)):
        return separator.join(str(v) for v in value)
    return str(value)


def json_to_csv(
        json_data: List[Dict],
        output_file: str,
        array_separator: str = '|',
        array_fields: List[str] = None,
        selected_fields: List[str] = None
) -> None:
    """
    Convert JSON data to CSV format with special handling for array fields.
    
    Parameters:
    -----------
    json_data : List[Dict]
        Input JSON data as a list of dictionaries
    output_file : str
        Path to the output CSV file
    array_separator : str, optional
        Separator to use when joining array values (default: '|')
    array_fields : List[str], optional
        List of field names that contain arrays
    selected_fields : List[str], optional
        List of fields to include in the CSV (if None, includes all fields)
    """
    # If no specific fields are selected, use all fields from the first record
    if not selected_fields and json_data:
        selected_fields = list(json_data[0].keys())

    # If array_fields is not specified, try to automatically detect them
    if array_fields is None:
        array_fields = []
        if json_data:
            for key, value in json_data[0].items():
                if isinstance(value, (list, tuple)):
                    array_fields.append(key)

    # Process the data
    processed_data = []
    for item in json_data:
        processed_row = {}
        for field in selected_fields:
            value = item.get(field, '')
            if field in array_fields:
                processed_row[field] = flatten_json_array(value, array_separator)
            else:
                processed_row[field] = value
        processed_data.append(processed_row)

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=selected_fields)
        writer.writeheader()
        writer.writerows(processed_data)


# Example usage
if __name__ == "__main__":
    # Sample JSON data
    sample_data = [
        {
            "id": 1,
            "name": "John Doe",
            "tags": ["developer", "python", "web"],
            "skills": ["JavaScript", "Python"],
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890"
            }
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "tags": ["designer", "ui/ux"],
            "skills": ["Figma", "Sketch", "CSS"],
            "contact": {
                "email": "jane@example.com",
                "phone": "098-765-4321"
            }
        }
    ]

    # Example 1: Basic conversion with default settings
    json_to_csv(
        sample_data,
        'output1.csv',
        array_fields=['tags', 'skills']
    )

    # Example 2: Custom separator and selected fields
    json_to_csv(
        sample_data,
        'output2.csv',
        array_separator=';',
        array_fields=['tags', 'skills'],
        selected_fields=['id', 'name', 'tags']
    )


    # Example 3: Using pandas for more complex transformations
    def json_to_csv_pandas(
            json_data: List[Dict],
            output_file: str,
            array_separator: str = '|'
    ) -> None:
        df = pd.json_normalize(json_data)

        # Convert array columns to strings
        for col in df.columns:
            if isinstance(df[col].iloc[0], (list, tuple)):
                df[col] = df[col].apply(lambda x: array_separator.join(map(str, x)))

        df.to_csv(output_file, index=False)


    # Using pandas version
    json_to_csv_pandas(sample_data, 'output3.csv')

```

I've created a comprehensive JSON to CSV converter that handles array fields in multiple ways. Here's how to use it:

1. Basic usage:

```python
json_to_csv(json_data, 'output.csv', array_fields=['tags', 'skills'])
```

2. With custom settings:

```python
json_to_csv(
    json_data,
    'output.csv',
    array_separator=';',
    array_fields=['tags', 'skills'],
    selected_fields=['id', 'name', 'tags']
)
```

The script includes:

- Automatic array field detection
- Custom separator for array values
- Field selection
- Proper UTF-8 encoding
- Alternative pandas-based implementation
- Type hints for better code clarity
