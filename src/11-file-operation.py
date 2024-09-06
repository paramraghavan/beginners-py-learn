import os

"""
List all files in current directory
"""
def list_files(path):
  """List all files in the specified directory."""
  for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
      print(f'File: {file}, File with path: {os.path.join(path, file)}')

list_files("/Users/paramraghavan/dev/beginners-py-learn/src")  # List files in the current directory
