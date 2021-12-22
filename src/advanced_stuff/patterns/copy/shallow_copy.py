# Dictionary of strings and ints
wordsDict = {
    "Hello": 56,
    "at" : 23 ,
    "test" : 43,
    "this" : 43,
    "who" : [56, 34, 44]
    }

# create a Shallow copy  the original dictionary
newDict = wordsDict.copy()

# Modify the value of key in new dictionary
newDict["at"] = 200

'''
Now Contents of new Dictionary is,
Modified New Dictionary :
test  ::  43
who  ::  [56, 34, 44]
at  ::  200
Hello  ::  56
this  ::  43

Now check the contents of original dictionary i.e.
Original Dictionary : 
test  ::  43
who  ::  [56, 34, 44]
at  ::  23
Hello  ::  56
this  ::  43
'''

print(newDict)
print(wordsDict)

'''
Observe:
Value of key ‘at’ is different 200 and 23 in both. So, modifying the new 
dictionary didn’t changed the original dictionary contents. Then how it is shallow ?
'''

'''
The word Shallow copy comes in picture when there is some object in dictionary like list 
or user define objects instead of primitive datatypes - string, int, float, the usual suspects.

Now let’s modify the value of key that contains list as value i.e.
'''

newDict["who"].append(222)

'''
Now Contents of new Dictionary is,
Modified New dictionary : 
at  ::  200
this  ::  43
Hello  ::  56
test  ::  43
who  ::  [56, 34, 44, 222]

Now check the contents of original dictionary i.e.
Original Dictionary : 
at  ::  23
this  ::  43
Hello  ::  56
test  ::  43
who  ::  [56, 34, 44, 222]
'''

'''
Observe that the list object in dictionary has been modified in both original,wordsDict, and 
the shallow copy of it, newDict
'''
print(newDict)
print(wordsDict)
