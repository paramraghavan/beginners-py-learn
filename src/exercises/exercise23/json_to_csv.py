# Python script that converts JSON to CSV, handling arrays within the JSON structure.

import json
import csv
import pandas as pd
from typing import List, Dict, Any


# Example 3: Using pandas for more complex transformations
def json_to_csv_pandas(
        json_data: List[Dict],
        output_file: str,
        array_separator: str = '|',
        columns_to_skip: List[str] = []
) -> None:
    df = pd.json_normalize(json_data)

    # Find columns to remove based on exact matches and patterns
    columns_to_remove = []
    for col in df.columns:
        # Check for exact matches
        if col in columns_to_skip:
            columns_to_remove.append(col)
        # Check for pattern matches (e.g., all columns starting with 'contact.')
        elif any(col.startswith(pattern) for pattern in columns_to_skip):
            columns_to_remove.append(col)

    # Remove the identified columns
    if columns_to_remove:
        df.drop(columns=columns_to_remove, inplace=True)
        print(f"Removed columns: {columns_to_remove}")

    # Convert array columns to strings
    for col in df.columns:
        if isinstance(df[col].iloc[0], (list, tuple)):
            df[col] = df[col].apply(lambda x: array_separator.join(map(str, x)))

    df.to_csv(output_file, index=False)


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

    # Using pandas version
    json_to_csv_pandas(sample_data, 'output3.csv', columns_to_skip=['contact'])
