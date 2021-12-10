# Dictionary of strings and ints
wordsDict = {
    "Hello": 56,
    "at" : 23 ,
    "test" : 43,
    "this" : 43,
    "who" : [56, 34, 44]
    }

import copy

# Let’s create a deep copy of this dictionary,
# Create a deep copy of the dictionary
otherDict = copy.deepcopy(wordsDict)


'''
Modify the contents of list object in deep copied dictionary will 
have no impact on original dictionary because its a deep copy.
'''
otherDict["who"].append(100)

'''
Contents of Deep Copy Dictionary:
Modified Deep copy of Dictionary : 
at  ::  23
this  ::  43
Hello  ::  56
test  ::  43
who  ::  [56, 34, 44, 100]

Contents of Original Dictionary:
Original Dictionary : 
at  ::  23
this  ::  43
Hello  ::  56
test  ::  43
who  ::  [56, 34, 44]

'''

print(f'otherDict(deep copied): {otherDict}')
print(f'wordsDict: {wordsDict}')
