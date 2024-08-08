**Gracefully convert all Python data types to a string suitable for use in a CSV file**

- You can create a function that handles various data types including dictionaries, lists, and other common types. This
function will ensure that the data is appropriately formatted and escaped for CSV use.

- Next step remove new lines, tabs and extra spaces so each string fits in single excel cell
- To convert a Python dictionary or list to a string recursively without using json.dumps, you can write a custom 
function that traverses the structure and builds the string representation.