import yaml
import pandas as pd
from sqlalchemy import create_engine

# Load YAML configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setup a database connection (example using SQLite, change as needed)
engine = create_engine('sqlite:///example.db')

# Dictionary to hold data layers
data_layers = {}

# Parse each layer and map it into a matrix
for layer in config['config']['layers']:
    if layer['type'] == 'sql':
        # Execute SQL query and store result in a DataFrame
        df = pd.read_sql_query(layer['query'], engine)
        data_layers[layer['name']] = df
    elif layer['type'] == 'expression':
        # Evaluate expression using the data layers
        df = eval(layer['expression'], {'__builtins__': None}, data_layers)
        data_layers[layer['name']] = df

# Print the resulting matrices (DataFrames)
for name, df in data_layers.items():
    print(f"Layer: {name}")
    print(df)
