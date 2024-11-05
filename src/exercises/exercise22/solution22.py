def join_with_escaped_commas(arr):
    """
    Join array elements into a CSV string, properly escaping elements that contain commas
    by wrapping them in quotes.

    Args:
        arr (list): List of strings to join

    Returns:
        str: CSV-formatted string with properly escaped elements
    """
    processed = []
    for item in arr:
        # If item contains a comma, wrap it in quotes
        if ',' in item:
            processed.append(f'"{item}"')
        else:
            processed.append(item)

    return ','.join(processed)


# Example usage
array_str = ['a', 'b', 'c,d,e,ffff']
result = join_with_escaped_commas(array_str)
print(result)  # Output: a,b,"c,d,e,ffff"

# Test with more complex cases
test_cases = [
    ['a', 'b', 'c'],  # Simple case
    ['a,b', 'c', 'd'],  # First element has comma
    ['a', 'b,c', 'd,e'],  # Multiple elements with commas
    ['a', 'b', 'c,d,e,f']  # Last element has multiple commas
]

for test in test_cases:
    print(join_with_escaped_commas(test))