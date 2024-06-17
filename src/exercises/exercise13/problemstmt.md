Python code to search a folder and subfolder with csv and non csv text files, 
perform an exact match and return the matching line


Solution
---------
* **Directory Traversal**: The script uses os.walk to traverse the given directory and its subdirectories.
* **File Identification**: It identifies both CSV and text files.
* **CSV File Handling**: If a file is a CSV, it reads it into a pandas DataFrame and performs an exact match search.
* **Text File Handling**: If a file is not a CSV, it reads it line by line and checks if the search value is present.
* **Store Matches**: Matches are stored in a list. For CSV files, the matches include the file path and the matching DataFrame. For text files, the matches include the file path, line number, and the matching line.
* **Results Display**: It prints the file paths, line numbers (for text files), and the matching lines or DataFrames.