'''
Variables that are created outside of a function (as in all of the examples above) are known as global variables.
Global variables can be used by everyone, both inside of functions and outside.
'''


import global_var_one


print(f'global_var_one.x: {global_var_one.x}')

'''
update the global variable
'''

global_var_one.x = f'{global_var_one.x}updated'

print(f'global_var_one.x updated: {global_var_one.x}')