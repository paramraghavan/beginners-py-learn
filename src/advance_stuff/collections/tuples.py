
github = ('https://github.com/', 2008, True)

print(f'tuple: {github}')
print(f'url: {github[0]}, founding year: {github[1]}, site free to use: {github[2]}')

print('for loop with tuple:')
for thing in github:
    print(thing)

print()

'''
collections.namedtuple
'''

import collections
'''
creating named tuple called Website
'''
Website = collections.namedtuple('Website', 'url founding_year free_to_use')
github = Website('https://github.com/', 2008, True)
print(f'named tuple: {github}')
print(f'url: {github[0]}, founding year: {github[1]}, site free to use: {github[2]}')