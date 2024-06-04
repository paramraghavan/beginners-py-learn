def search_dict_ignore_case(dictionary, search_key):
    # Convert the search key to lower case
    search_key_lower = search_key.lower()

    # Iterate through the dictionary keys, converting them to lower case for comparison
    for key in dictionary.keys():
        if key.lower() == search_key_lower:
            return dictionary[key]

    return None  # Return None if the key is not found


# Example usage
my_dict = {'Name': 'Alice', 'Age': 25, 'City': 'Wonderland'}
key_to_search = 'city'
result = search_dict_ignore_case(my_dict, key_to_search)

print(result)  # Output: 'Wonderland'


# another save all keys in upper case and when you match then make the search key to upper case and search for keys as usual