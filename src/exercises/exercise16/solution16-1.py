import json
import csv


def convert_to_csv_safe_string(variable):
    # Convert complex types (dict, list) to JSON string
    if isinstance(variable, (dict, list)):
        string_repr = json.dumps(variable)
    else:
        string_repr = str(variable)

    # Remove newlines, tabs, and extra spaces
    string_repr = string_repr.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    string_repr = ' '.join(string_repr.split())  # Remove extra spaces

    return string_repr


if __name__ == "__main__":
    my_dict = {'name': 'Archie', 'age': 30, 'city': 'New Mexico'}
    my_list = ['apple', 'banana', 'cherry']
    my_str = 'Hello,\nWorld!\tThis is an example string.'
    my_str1 = '"T":1 \n' \
               '"Y":1 \n' \
               '"N":0 \n' \
                '"":None '
    print(f'my_str1: {my_str1}')
    my_int = 42
    my_float = 3.14159

    # Convert variables to CSV-safe strings
    dict_str = convert_to_csv_safe_string(my_dict)
    list_str = convert_to_csv_safe_string(my_list)
    str_str = convert_to_csv_safe_string(my_str)
    str_str1 = convert_to_csv_safe_string(my_str1)
    int_str = convert_to_csv_safe_string(my_int)
    float_str = convert_to_csv_safe_string(my_float)

    print(f'dict_str: {dict_str}')
    print(f'list_str: {list_str}')
    print(f'str_str: {str_str}')
    print(f'str_str: {str_str1}')
    print(f'int_str: {int_str}')
    print(f'float_str: {float_str}')
