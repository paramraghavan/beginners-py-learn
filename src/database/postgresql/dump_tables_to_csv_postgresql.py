"""
dump table to csv
lsit all the tables ib database
pip install pandas sqlalchemy psycopg2

"""

import pandas as pd
from sqlalchemy import create_engine

# Define your database connection details
db_config = {
    'dbname': 'your_dbname',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# Create the connection string
connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Function to export a table to CSV
def export_table_to_csv(table_name, output_path):
    # Read the table into a DataFrame
    df = pd.read_sql_table(table_name, engine)
    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False)
    print(f"Table {table_name} exported to {output_path}")


# Function to get the list of all tables in the database
def get_table_names():
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    """
    with engine.connect() as connection:
        result = connection.execute(query)
        table_names = [row[0] for row in result]
    return table_names

if __name__ == '__main__':
    # Example usage dump table to csv file
    tables_to_export = ['table1', 'table2', 'table3']  # List your table names here
    for table in tables_to_export:
        output_file_path = f"{table}.csv"  # Define your output file path
        export_table_to_csv(table, output_file_path)

    # Example usage, print all the tables in postgres db
    tables = get_table_names()
    for table in tables:
        print(table)