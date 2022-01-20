'''
We can add together strings, lists, tuples and sets
'''


str_add = "hello" + "world"
print(f'string add: {str_add}')

list_add = [1, 2, 3] + [4, 5]
print(f'list add: {list_add}')

l1 = [1, 2, 3]
l2 = [4, 5]
list_add_1 = [*l1, *l2]
print(f'list add 1: {list_add_1}')

tuple_add = (1, 2, 3) + (4, 5)
print(f'tuple add: {tuple_add}')

'''
Note pipe '|'/or used  for adding sets
'''
set_add = {1, 2, 3} | {4, 5}
print(f'set add: {set_add}')

'''
adding dictionary
'''

dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3}
dict1_add_dict2 = {**dict1, **dict2}
print(f'dict1 + dict2: {dict1_add_dict2}')

merged = {}
merged.update(dict1)
merged.update(dict2)
print(f'merge dict1 and dict2: {merged}')

print()
the_dict = {'hi': 'this is working'}
value = the_dict.get('hi', 'lol hi is not there')
print(f'value of hi: {value}')

value = the_dict.get('hello', 'lol hello is not there')
print(f'value of key hello that does not exist in dictionary: {value}')
