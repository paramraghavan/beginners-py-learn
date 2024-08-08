import json
import csv

def convert_to_string(variable):
    """
    This function handles various data types including dictionaries, lists, and other common types. It
    will ensure that the data is appropriately formatted and escaped for CSV use.
    """
    if isinstance(variable, (dict, list)):
        return json.dumps(variable)
    elif isinstance(variable, str):
        return variable
    else:
        return str(variable)


if __name__ == "__main__":

    # Example variables
    my_dict = {'name': 'Archie', 'age': 30, 'city': 'New Mexico'}
    my_list = ['apple', 'banana', 'cherry']
    my_str = 'Hello, World!'
    my_int = 42
    my_float = 3.14159
    my_bool = True
    my_none = None

    # Convert variables to strings
    variables = [my_dict, my_list, my_str, my_int, my_float, my_bool, my_none]
    converted_variables = [convert_to_string(var) for var in variables]

    # Define the CSV file name
    csv_file = 'output.csv'

    # Writing converted strings to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['data'])  # header
        for var in converted_variables:
            writer.writerow([var])

    print(f"Converted data has been written to {csv_file}")
