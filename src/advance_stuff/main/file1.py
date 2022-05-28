'''
Run this file as is from cp,,and line as :
python file1.py
'''

print("File1 __name__ = %s" % __name__)
print("Full path/location for File1 __file__ = %s" % __file__)

if __name__ == "__main__":
    print("File1 is being run directly")
else:
    print("File1 is being imported")

# Output:
# File1 __name__ = __main__
# File1 is being run directly
