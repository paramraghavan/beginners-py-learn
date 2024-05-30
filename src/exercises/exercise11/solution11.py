'''
Removing non-alphanumeric characters and replacing them with spaces.
Splitting the resulting string into a list of words.
Checking if the given word is in the list of words.
'''


def exact_match(word, string):
    # Split the string into words based on whitespace and punctuation
    words = ''.join(char if char.isalnum() else ' ' for char in string).split()
    # Check if the given word is in the list of words
    return word in words

# Examples
print(exact_match('wordworld', 'this (wordworld #is awesome'))  # Should return True
print(exact_match('world', 'this (wordworld #is awesome'))  # Should return False
print(exact_match('word', 'this (wordworld #is awesome'))  # Should return False
