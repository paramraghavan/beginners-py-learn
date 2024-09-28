import sys
import os

# Add the other_directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'other_directory'))

# Now you can import my_module
import my_module

if __name__ == "__main__":
    print(my_module.my_function())