# Python File Operations

Python provides several ways to handle file operations. Here's an overview of some common file operations:

## 1. Reading from a file:

To read data from a file, you can use the `open()` function with the appropriate mode.

```python
# Reading a file
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)

# Reading line by line
with open('example.txt', 'r') as file:
    for line in file:
        print(line)
```

## 2. Writing to a file:

You can use the `write()` or `writelines()` method to write data to a file. If the file doesn't exist, it will be
created.

```python
# Writing to a file
with open('example.txt', 'w') as file:
    file.write("Hello, this is a sample text.\n")
    file.write("Adding more content to the file.")

# Writing a list of lines
lines = ["First line\n", "Second line\n", "Third line\n"]
with open('example.txt', 'w') as file:
    file.writelines(lines)
```

## 3. Appending to a file:

If you want to add content to an existing file without overwriting it, use the `'a'` mode.

```python
# Appending to a file
with open('example.txt', 'a') as file:
    file.write("This will be added to the end of the file.\n")
```

## 4. Checking if a file exists:

To check if a file exists, you can use the `os.path.exists()` method or the `pathlib` module.

```python
import os

# Using os module
if os.path.exists('example.txt'):
    print("File exists")
else:
    print("File doesn't exist")

# Using pathlib module
from pathlib import Path

file_path = Path('example.txt')
if file_path.is_file():
    print("File exists")
else:
    print("File doesn't exist")
```

## 5. Deleting a file:

To delete a file, you can use `os.remove()`.

```python
# Deleting a file
import os

if os.path.exists('example.txt'):
    os.remove('example.txt')
    print("File deleted")
else:
    print("The file does not exist")
```

## 6. Renaming or moving a file:

You can rename or move a file using the `os.rename()` method.

```python
# Renaming a file
import os

os.rename('example.txt', 'new_example.txt')

# Moving a file
os.rename('new_example.txt', 'path/to/destination/new_example.txt')
```

## 7. Copying a file:

To copy a file, you can use the `shutil.copy()` method.

```python
import shutil

# Copying a file
shutil.copy('example.txt', 'example_copy.txt')
```

## 8. Getting file details:

You can obtain details like file size, modification time, etc.

```python
import os
import time

file_stats = os.stat('example.txt')

print(f"File Size: {file_stats.st_size} bytes")
print(f"Last Modified: {time.ctime(file_stats.st_mtime)}")
print(f"Last Accessed: {time.ctime(file_stats.st_atime)}")
```

## 9. Working with binary files:

For binary file operations, you need to open the file in binary mode (`'rb'` for reading and `'wb'` for writing).

```python
# Writing to a binary file
with open('binary_file.bin', 'wb') as file:
    file.write(b'This is binary data')

# Reading from a binary file
with open('binary_file.bin', 'rb') as file:
    content = file.read()
    print(content)
```

## 10. Get a list of all files in a given directory:

```python
import os

"""
Print all files as is and with  directory path  which are in current directory
"""
def list_files(path):
  """List all files in the specified directory."""
  for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):  
      print(f'File: {file}, File with path: {os.path.join(path, file)}')

list_files(".")  # List files in the current directory
```