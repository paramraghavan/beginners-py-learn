# Additional Python File Operations

Here are some additional file operations that you can perform with Python:

## 10. Reading and Writing JSON files:

Python's `json` module allows you to work with JSON files, which is a common format for storing structured data.

```python
import json

# Writing JSON data to a file
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Reading JSON data from a file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    print(data)
```

## 11. Working with CSV files:

Python's `csv` module makes it easy to read from and write to CSV files.

```python
import csv

# Writing to a CSV file
with open('data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Name', 'Age', 'City'])
    writer.writerow(['Alice', 28, 'Los Angeles'])
    writer.writerow(['Bob', 34, 'Chicago'])

# Reading from a CSV file
with open('data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        print(row)
```

## 12. Working with ZIP files:

The `zipfile` module allows you to create, read, write, and extract ZIP files.

```python
import zipfile

# Creating a ZIP file
with zipfile.ZipFile('files.zip', 'w') as zip_file:
    zip_file.write('example.txt')
    zip_file.write('data.json')

# Extracting a ZIP file
with zipfile.ZipFile('files.zip', 'r') as zip_file:
    zip_file.extractall('extracted_files')
```

## 13. Reading and Writing XML files:

You can use the `xml.etree.ElementTree` module to work with XML files.

```python
import xml.etree.ElementTree as ET

# Writing XML data to a file
root = ET.Element("root")
child1 = ET.SubElement(root, "child")
child1.text = "This is child 1"
child2 = ET.SubElement(root, "child")
child2.text = "This is child 2"

tree = ET.ElementTree(root)
tree.write("data.xml")

# Reading XML data from a file
tree = ET.parse('data.xml')
root = tree.getroot()

for child in root:
    print(child.tag, child.text)
```

## 14. Working with Excel files:

The `openpyxl` or `pandas` libraries allow you to read from and write to Excel files.

```python
import openpyxl

# Creating a new Excel file
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = 'Name'
sheet['B1'] = 'Age'
sheet['C1'] = 'City'

sheet.append(['Alice', 28, 'Los Angeles'])
sheet.append(['Bob', 34, 'Chicago'])

workbook.save('data.xlsx')

# Reading from an Excel file
workbook = openpyxl.load_workbook('data.xlsx')
sheet = workbook.active

for row in sheet.iter_rows(values_only=True):
    print(row)
```

## 15. Working with PDFs:

The `PyPDF2` library is often used to read and manipulate PDF files.

```python
import PyPDF2

# Reading from a PDF file
with open('sample.pdf', 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    print(f"Number of pages: {number_of_pages}")

    # Extract text from the first page
    page = reader.pages[0]
    text = page.extract_text()
    print(text)

# Merging two PDF files
merger = PyPDF2.PdfMerger()
merger.append('sample.pdf')
merger.append('another_sample.pdf')
merger.write('merged.pdf')
merger.close()
```

## 16. Working with Pickle files:

The `pickle` module allows you to serialize and deserialize Python objects.

```python
import pickle

# Serializing an object to a file
data = {'name': 'John', 'age': 30, 'city': 'New York'}
with open('data.pkl', 'wb') as pkl_file:
    pickle.dump(data, pkl_file)

# Deserializing an object from a file
with open('data.pkl', 'rb') as pkl_file:
    data = pickle.load(pkl_file)
    print(data)
```

## 17. File Input and Output using `with` Statement:

Using the `with` statement for file I/O operations is recommended as it ensures that resources are properly managed.

```python
# Using with statement for file I/O
with open('example.txt', 'w') as file:
    file.write("Using with statement for file operations.\n")

with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
```
