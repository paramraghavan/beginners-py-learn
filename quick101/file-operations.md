```python
### open():
f = open("demo.txt","rt") #r for read and t for text are default values

### read():
f.read()
f.read(5)  # Read first 5 characters
f.read(10)  # Next 10 characters
 
str = f.read(10)
print(str)

# Check current position
position = f.tell()
print("Current Position is : " + position)

# Reposition pointer at the beginning once again
position = f.seek(0)
str = f.read(10)
print("Again read String is : ", str)

f.close()
 
### readline():
# Read one line of the file.
f = open(r"./quick101/lambda-functions.md","rt")
f.readline() # first line read
 
### Loop through the file line by line, 2nd line onwards:
for x in f:
  print(x)
  
### Close the file
f.close()

### write()
# "w" - Will overwrite any existing content
# "a" - Append to end of file
 
f = open("demo.txt","a")
f.write("Hello")

f = open("demo.txt","r")
f.read()

### Create a new file
# "x" - Create - will create a file, returns an error if the file exist
# "a" - Append - will create a file if the specified file does not exist
# "w" - Write - will create a file if the specified file does not exist

f = open("myfile.txt", "x") #  new empty file is created!
f = open("myfile.txt", "w")

### Rename a File
import os
os.rename('myfile.txt', 'newMyfile.txt')

### Delete a File 
import os
os.remove("myfile.txt")


### Check if File Exist
import os
if os.path.exists("myfile.txt"):
  os.remove("myfile.txt")
else:
  print("The file does not exist")
  
### Delete Folder
import os
os.rmdir("myfolder")

### Create Folder
import os
os.mkdir("newDir")
```
