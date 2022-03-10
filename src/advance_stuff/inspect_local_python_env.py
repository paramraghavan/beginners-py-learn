'''
This is to inspect my local python environment
ref: https://www.geeksforgeeks.org/python-sys-module/
'''

import sys

#dir(sys)
help(sys)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f'Root of your Python installation \n {bcolors.BOLD}{sys.prefix}{bcolors.ENDC}')
print(f'Python executable being used \n {bcolors.BOLD}{sys.executable}{bcolors.ENDC}')
print(f'Returns the list of directories that the interpreter will search for the required module: \n {bcolors.BOLD}{sys.path}{bcolors.ENDC}')
print(f'Returns the name of the Python modules that the current python env/shell has imported \n {bcolors.BOLD}{sys.modules}{bcolors.ENDC}')
# print(f' {bcolors.BOLD}{sys.version}{bcolors.ENDC}')
print(f'Our platform \n {bcolors.BOLD}{sys.platform}{bcolors.ENDC}')
print(f'All the arguments passed to program \n {bcolors.BOLD}{sys.argv}{bcolors.ENDC}')

print('Other interesting ones -->  sys.exit, sys.stdout, sys.stdin and sys.stdin')