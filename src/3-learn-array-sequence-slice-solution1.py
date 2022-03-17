'''
Exercise1:
Exercise check if a string is a palindrome  using slice.
A string is a palindrome if the reverse of the string is identical
to the original string. For example, ‘civic’ is a palindrome, but
‘radio’ is not, since the reverse of ‘radio’ is ‘oidar’, but
the reverse of ‘civic’ is ‘civic’.

'''

# Solution

def palindrome_check(word:str) ->bool:
    word =  word.lower()
    return word == word[::-1]


if __name__ == '__main__':
    my_word = 'malayalam'
    print(f'Is this word {my_word} a plaindrome ? {palindrome_check(my_word)}')
    my_word = 'radio'
    print(f'Is this word {my_word} a plaindrome ? {palindrome_check(my_word)}')


