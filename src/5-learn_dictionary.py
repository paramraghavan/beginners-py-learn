'''
Dictionary
Dictionaries consist of key: value pairs.
Variables are stored in a dictionary with their names as keys, so dictionaries behave a lot like variables:
Dictionaries are not ordered.
Setting or getting the value of a key is simple and fast.
Dictionaries can't contain the same key more than once.
'''

# init dictionary
dictionary = {}
# dictionary = dict()
dictionary['mom'] = 'Amma'
dictionary['brother'] = 'Anna'
print(dictionary)

county_capital_dict = {
    "vietnam": "hanoi",
    "thailand": "bankok",
    "bhutan": "thimpu"
}

# add japan to dictionary
county_capital_dict["japan"] = "tokyo"
# print(county_capital_dict)

print(f'capital of bhutan(this is key) : {county_capital_dict["bhutan"]}(this is value)')
