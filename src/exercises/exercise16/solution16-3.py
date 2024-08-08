def custom_convert_to_string(data):
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            key_str = f'"{key}"'
            value_str = custom_convert_to_string(value)
            items.append(f'{key_str}:{value_str}')
        return "{" + ",".join(items) + "}"
    elif isinstance(data, list):
        items = [custom_convert_to_string(item) for item in data]
        return "[" + ",".join(items) + "]"
    elif isinstance(data, str):
        return f'"{data}"'
    elif isinstance(data, (int, float, bool)):
        return str(data).lower() if isinstance(data, bool) else str(data)
    elif data is None:
        return "null"
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")

# Example usage
data_dict = {
    "name": "John",
    "age": 30,
    "car": None,
    "children": ["Ann", "Billy"],
    "married": True,
    "salary": 5000.50
}

data_list = ["apple", {"color": "red", "size": "large"}, 123]

# Convert the dictionary to a string
dict_str = custom_convert_to_string(data_dict)
list_str = custom_convert_to_string(data_list)

print("Dictionary as string:", dict_str)
print("List as string:", list_str)
