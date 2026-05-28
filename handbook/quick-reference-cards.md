# 📋 Quick Reference Cards

> **One-Page Cheatsheets for Python & Development**
>
> Print-friendly. Interview-ready. Designed for quick lookup.

---

## Table of Contents
1. [Python Syntax Essentials](#python-syntax-essentials)
2. [Data Structures Operations](#data-structures-operations)
3. [String Methods](#string-methods)
4. [List & Dict Comprehensions](#list--dict-comprehensions)
5. [File I/O Patterns](#file-io-patterns)
6. [Exception Handling](#exception-handling)
7. [OOP Quick Reference](#oop-quick-reference)
8. [Common Algorithms & Big-O](#common-algorithms--big-o)
9. [SQL Essentials](#sql-essentials)
10. [Git Commands](#git-commands)
11. [Docker Commands](#docker-commands)
12. [AWS CLI Essentials](#aws-cli-essentials)

---

## Python Syntax Essentials

### Variables & Types
```python
# Assignment
x = 5                          # int
y = 3.14                       # float
name = "Alice"                 # str
is_active = True               # bool
nothing = None                 # NoneType

# Multiple assignment
a, b, c = 1, 2, 3
x = y = z = 0

# Type checking
type(x)                        # <class 'int'>
isinstance(x, int)             # True
```

### String Formatting
```python
# f-strings (Python 3.6+)
name = "Bob"
age = 30
f"{name} is {age} years old"

# format()
"Hello, {}".format("World")
"{0} {1}".format("Hello", "World")
"{name} is {age}".format(name="Bob", age=30)

# % formatting (older)
"Hello, %s" % "World"
"Value: %d" % 42
```

### Control Flow
```python
# if/elif/else
if condition:
    pass
elif other_condition:
    pass
else:
    pass

# for loop
for i in range(10):           # 0-9
    pass
for item in iterable:
    pass
for i, item in enumerate(iterable):
    pass

# while loop
while condition:
    pass

# break, continue, pass
for i in range(10):
    if i == 3:
        break              # exit loop
    if i == 1:
        continue           # skip iteration
    pass                   # do nothing
```

### Functions
```python
# Basic function
def greet(name):
    return f"Hello, {name}"

# Default arguments
def add(a, b=0):
    return a + b

# Variable arguments
def sum_all(*args):           # args is tuple
    return sum(args)

def print_dict(**kwargs):      # kwargs is dict
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Lambda (anonymous function)
double = lambda x: x * 2
numbers = [1, 2, 3]
result = map(double, numbers)  # [2, 4, 6]
```

### Operators
```python
# Arithmetic
+, -, *, /, //, %, **         # +, -, ×, ÷, floor div, mod, power

# Comparison
==, !=, <, >, <=, >=

# Logical
and, or, not

# Membership
in, not in

# Identity
is, is not
```

### Unpacking
```python
# Tuple unpacking
a, b = (1, 2)
a, *rest, c = [1, 2, 3, 4, 5]  # a=1, rest=[2,3,4], c=5

# Dictionary unpacking
dict1 = {**dict2, **dict3}
func(**dictionary_args)
```

---

## Data Structures Operations

### Lists
```python
# Create
lst = [1, 2, 3]
lst = list(range(5))           # [0, 1, 2, 3, 4]

# Access
lst[0]                         # first element
lst[-1]                        # last element
lst[1:3]                       # slice: [2] (index 1-2)

# Modify
lst.append(4)                  # add to end
lst.extend([5, 6])             # add multiple
lst.insert(0, 0)               # insert at index
lst[1] = 10                    # replace
lst.remove(10)                 # remove by value
lst.pop()                      # remove & return last
lst.pop(0)                     # remove & return by index

# Info
len(lst)                       # length
lst.count(2)                   # count occurrences
lst.index(2)                   # first index of value

# Ordering
lst.sort()                     # sort in-place
sorted(lst)                    # return sorted copy
lst.reverse()                  # reverse in-place
```

### Tuples (Immutable)
```python
# Create
tup = (1, 2, 3)
tup = tuple([1, 2, 3])

# Access
tup[0]                         # first element
tup[1:3]                       # slice

# Info
len(tup)
tup.count(2)
tup.index(2)

# Note: tuples are immutable, cannot add/remove/modify
```

### Sets (Unordered, Unique)
```python
# Create
s = {1, 2, 3}
s = set([1, 2, 3])
s = set()                      # empty set

# Add/Remove
s.add(4)                       # add single element
s.update({5, 6})               # add multiple
s.remove(1)                    # remove (error if not found)
s.discard(1)                   # remove (no error if not found)
s.pop()                        # remove & return arbitrary

# Operations
s1 | s2                        # union
s1 & s2                        # intersection
s1 - s2                        # difference
s1 ^ s2                        # symmetric difference
s1.issubset(s2)
s1.issuperset(s2)

# Info
len(s)
1 in s
```

### Dictionaries
```python
# Create
d = {'a': 1, 'b': 2}
d = dict(a=1, b=2)
d = {k: v for k, v in pairs}   # dict comprehension

# Access
d['a']                         # get value (error if key not found)
d.get('a')                     # get value (None if not found)
d.get('a', 0)                  # get with default

# Modify
d['c'] = 3                     # add/update
d.pop('a')                     # remove & return
d.popitem()                    # remove & return arbitrary pair
d.update({'d': 4})             # merge/update
d.clear()                      # remove all

# Info
len(d)
'a' in d                       # check key exists
d.keys()                       # all keys
d.values()                     # all values
d.items()                      # all (key, value) pairs

# Iteration
for key in d:
    pass
for key, value in d.items():
    pass
```

---

## String Methods

### Common String Operations
```python
s = "Hello, World!"

# Case
s.upper()                      # "HELLO, WORLD!"
s.lower()                      # "hello, world!"
s.capitalize()                 # "Hello, world!"
s.title()                      # "Hello, World!"
s.swapcase()                   # "hELLO, wORLD!"

# Search & Replace
s.find('o')                    # 4 (first index, -1 if not found)
s.index('o')                   # 4 (error if not found)
s.count('l')                   # 3
s.startswith('Hello')          # True
s.endswith('!')                # True
s.replace('World', 'Python')   # "Hello, Python!"

# Split & Join
s.split(',')                   # ['Hello', ' World!']
s.split()                      # by whitespace
'-'.join(['a', 'b', 'c'])      # 'a-b-c'

# Strip & Pad
s.strip()                      # remove leading/trailing whitespace
s.lstrip()                     # remove leading whitespace
s.rstrip()                     # remove trailing whitespace
s.ljust(20)                    # pad right to 20 chars
s.rjust(20)                    # pad left to 20 chars
s.center(20)                   # pad both sides

# Check
s.isdigit()                    # all characters are digits?
s.isalpha()                    # all characters are letters?
s.isalnum()                    # all alphanumeric?
s.isspace()                    # all whitespace?
s.islower()                    # all lowercase?
s.isupper()                    # all uppercase?

# Other
len(s)                         # length
s.format(name="Bob")           # format string
```

---

## List & Dict Comprehensions

### List Comprehensions
```python
# Basic
[x for x in range(10)]         # [0, 1, 2, ..., 9]
[x*2 for x in range(5)]        # [0, 2, 4, 6, 8]

# With condition
[x for x in range(10) if x % 2 == 0]  # evens
[x for x in range(10) if x % 2]       # odds

# Nested
[x*y for x in range(3) for y in range(3)]  # all combinations
[[x, y] for x in range(3) for y in range(3)]

# Transformation
[int(x) for x in ['1', '2', '3']]
[word.upper() for word in ['a', 'b', 'c']]
```

### Set Comprehensions
```python
{x for x in range(10)}         # {0, 1, 2, ..., 9}
{x for x in [1, 1, 2, 2, 3]}   # {1, 2, 3} (removes duplicates)
{x*2 for x in range(5) if x % 2 == 0}
```

### Dictionary Comprehensions
```python
{x: x*2 for x in range(5)}     # {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}
{k: v for k, v in pairs}
{word: len(word) for word in ['a', 'bb', 'ccc']}
```

### Generator Expressions
```python
# Lazy evaluation - doesn't create list in memory
(x for x in range(1000000))
sum(x for x in range(100))
list(x*2 for x in range(5))
```

---

## File I/O Patterns

### Reading Files
```python
# Read entire file
with open('file.txt', 'r') as f:
    content = f.read()         # entire content as string

# Read line by line
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Read all lines
with open('file.txt', 'r') as f:
    lines = f.readlines()      # list of lines

# Read specific number of characters
with open('file.txt', 'r') as f:
    chunk = f.read(1024)       # read 1KB
```

### Writing Files
```python
# Write (overwrite)
with open('file.txt', 'w') as f:
    f.write("Hello, World!")

# Write multiple lines
with open('file.txt', 'w') as f:
    f.writelines(['line1\n', 'line2\n'])

# Append
with open('file.txt', 'a') as f:
    f.write("New line\n")
```

### JSON
```python
import json

# Read JSON
with open('data.json', 'r') as f:
    data = json.load(f)        # parse file

json.loads('{"key": "value"}') # parse string

# Write JSON
with open('data.json', 'w') as f:
    json.dump(data, f)         # write to file

json.dumps(data)               # convert to string
```

### CSV
```python
import csv

# Read CSV
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Write CSV
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['col1', 'col2'])
    writer.writerows(data)
```

---

## Exception Handling

### Try-Except
```python
# Basic
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# Multiple exceptions
try:
    pass
except ValueError:
    print("Value error")
except (TypeError, KeyError):
    print("Type or key error")
except Exception as e:
    print(f"Unexpected error: {e}")

# Else clause (if no exception)
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print(f"Result: {result}")

# Finally (always runs)
try:
    file = open('file.txt')
except FileNotFoundError:
    print("File not found")
finally:
    print("Cleanup code")
```

### Raising Exceptions
```python
raise ValueError("Invalid value")
raise ValueError("Invalid value") from original_error

# Custom exception
class CustomError(Exception):
    pass

raise CustomError("Something went wrong")
```

### Common Exceptions
```python
ValueError              # invalid value
TypeError              # wrong type
KeyError               # dictionary key not found
IndexError             # list index out of range
AttributeError         # object has no attribute
ZeroDivisionError      # division by zero
FileNotFoundError      # file doesn't exist
ImportError            # cannot import module
RuntimeError           # generic runtime error
```

---

## OOP Quick Reference

### Class Definition
```python
class Animal:
    species = "Unknown"        # class variable

    def __init__(self, name):  # constructor
        self.name = name       # instance variable

    def speak(self):
        return f"{self.name} makes a sound"

    @classmethod
    def from_species(cls, species_name):
        return cls(species_name)

    @staticmethod
    def is_alive(organism):
        return organism is not None

    @property
    def display_name(self):
        return f"Animal: {self.name}"

# Create instance
dog = Animal("Rex")
print(dog.speak())
```

### Inheritance
```python
class Dog(Animal):           # inherit from Animal
    def speak(self):
        return f"{self.name} barks"

# Multiple inheritance
class Mix(Dog, Cat):
    pass
```

### Special Methods (Dunder)
```python
class MyClass:
    def __init__(self):        # constructor
        pass

    def __str__(self):         # string representation
        return "MyClass instance"

    def __repr__(self):        # developer representation
        return "MyClass()"

    def __len__(self):         # len(obj)
        return 10

    def __getitem__(self, key): # obj[key]
        return f"Value for {key}"

    def __setitem__(self, key, value): # obj[key] = value
        pass

    def __eq__(self, other):   # obj == other
        return True

    def __lt__(self, other):   # obj < other
        return False

    def __add__(self, other):  # obj + other
        return "sum"

    def __call__(self):        # obj()
        return "called"
```

### Access Control
```python
class Example:
    def __init__(self):
        self.public = "public"        # accessible everywhere
        self._protected = "protected" # convention: use within class
        self.__private = "private"    # name-mangled, harder to access

# Access private via name mangling
obj._Example__private

# Properties
class Temperature:
    def __init__(self):
        self._celsius = 0

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value
```

---

## Common Algorithms & Big-O

### Big-O Complexity Cheat Sheet

| Operation | Best | Average | Worst | Notes |
|-----------|------|---------|-------|-------|
| **Array Access** | O(1) | O(1) | O(1) | direct index |
| **Array Search** | O(1) | O(n) | O(n) | unsorted |
| **Array Insert** | O(n) | O(n) | O(n) | middle insertion |
| **Array Delete** | O(n) | O(n) | O(n) | middle deletion |
| **Binary Search** | O(1) | O(log n) | O(log n) | sorted array |
| **Sorting** | O(n) | O(n log n) | O(n²) | quicksort avg |
| **Hash Lookup** | O(1) | O(1) | O(n) | collision |
| **Tree Insert** | O(log n) | O(log n) | O(n) | balanced tree |
| **Tree Search** | O(log n) | O(log n) | O(n) | balanced tree |
| **Graph DFS/BFS** | O(V+E) | O(V+E) | O(V+E) | V=vertices, E=edges |

### Space Complexity
- **O(1)** - Constant (no extra space)
- **O(log n)** - Logarithmic (e.g., recursion depth)
- **O(n)** - Linear (e.g., store all items)
- **O(n²)** - Quadratic (e.g., nested loops)
- **O(2ⁿ)** - Exponential (e.g., all subsets)
- **O(n!)** - Factorial (e.g., all permutations)

### Common Pattern Recognition

| Pattern | Likely Algorithm | Big-O |
|---------|-----------------|-------|
| Sorted array, find target | Binary search | O(log n) |
| Find all pairs | Two pointers or hash | O(n) to O(n²) |
| Overlapping subproblems | Dynamic programming | O(n²) typical |
| Tree/graph traversal | DFS or BFS | O(V+E) |
| Need all combinations | Recursion/backtracking | O(2ⁿ) or O(n!) |
| Divide & conquer | Merge sort, binary search | O(n log n) |

---

## SQL Essentials

### DDL (Data Definition Language)

```sql
-- Create table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    age INT CHECK (age >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alter table
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users MODIFY COLUMN age VARCHAR(10);

-- Drop table
DROP TABLE users;

-- Create index
CREATE INDEX idx_email ON users(email);
```

### DML (Data Manipulation Language)

```sql
-- Insert
INSERT INTO users (name, email, age)
VALUES ('Alice', 'alice@example.com', 30);

-- Insert multiple
INSERT INTO users (name, email, age) VALUES
('Bob', 'bob@example.com', 25),
('Charlie', 'charlie@example.com', 35);

-- Update
UPDATE users SET age = 31 WHERE name = 'Alice';

-- Delete
DELETE FROM users WHERE age < 18;
```

### DQL (Data Query Language)

```sql
-- Select all
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- Where clause
SELECT * FROM users WHERE age > 18;
SELECT * FROM users WHERE age > 18 AND name LIKE 'A%';

-- Order
SELECT * FROM users ORDER BY age DESC;
SELECT * FROM users ORDER BY age ASC, name DESC;

-- Limit
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- pagination

-- Distinct
SELECT DISTINCT city FROM users;

-- Count
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT city) FROM users;

-- Group by
SELECT city, COUNT(*) as count FROM users GROUP BY city;
SELECT city, COUNT(*) as count FROM users
GROUP BY city HAVING count > 5;

-- Aggregate functions
SELECT
    COUNT(*) as total,
    AVG(age) as avg_age,
    MIN(age) as min_age,
    MAX(age) as max_age,
    SUM(salary) as total_salary
FROM users;

-- Join
SELECT u.name, o.order_id
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

SELECT u.name, o.order_id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

SELECT u.name, o.order_id
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

SELECT u.name, o.order_id
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;

-- Subquery
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders);

-- Case statement
SELECT name,
    CASE
        WHEN age < 18 THEN 'Minor'
        WHEN age >= 18 AND age < 65 THEN 'Adult'
        ELSE 'Senior'
    END as age_group
FROM users;
```

### Transaction
```sql
BEGIN TRANSACTION;
UPDATE users SET age = age + 1 WHERE id = 1;
COMMIT;

-- Rollback
BEGIN TRANSACTION;
DELETE FROM users;
ROLLBACK;
```

---

## Git Commands

### Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --list                 # view all settings
```

### Initialize & Clone
```bash
git init                          # initialize local repo
git clone <url>                   # clone remote repo
git clone <url> <directory>       # clone to specific directory
```

### Basic Workflow
```bash
git status                        # see what changed
git add <file>                    # stage single file
git add .                         # stage all changes
git add -p                        # stage by chunks (interactive)

git commit -m "message"           # commit staged changes
git commit -am "message"          # stage & commit tracked files
git commit --amend                # modify last commit

git push                          # push to remote
git push origin <branch>          # push specific branch
git push -u origin <branch>       # push & set upstream

git pull                          # fetch & merge
git fetch                         # fetch without merge
```

### Branching
```bash
git branch                        # list local branches
git branch -a                     # list all branches
git branch <branch>               # create branch
git checkout <branch>             # switch branch
git checkout -b <branch>          # create & switch
git branch -d <branch>            # delete branch
git merge <branch>                # merge branch
```

### History
```bash
git log                           # commit history
git log --oneline                 # compact log
git log --graph --all --oneline   # visual tree
git log -p                        # show changes
git log --author="name"           # filter by author
git log --since="2 weeks ago"     # filter by date

git diff                          # changes not staged
git diff --staged                 # staged changes
git diff <branch1> <branch2>      # compare branches
```

### Undo
```bash
git restore <file>                # discard changes
git restore --staged <file>       # unstage file
git reset HEAD~1                  # undo last commit
git revert <commit>               # create inverse commit
git checkout <commit> <file>      # get file from commit
```

### Remote
```bash
git remote                        # list remotes
git remote -v                     # list with URLs
git remote add <name> <url>       # add remote
git remote remove <name>          # remove remote
git push <remote> <branch>        # push to remote
git pull <remote> <branch>        # pull from remote
```

---

## Docker Commands

### Images
```bash
docker images                     # list images
docker build -t myimage:1.0 .    # build from Dockerfile
docker pull ubuntu:22.04         # pull image from registry
docker push myregistry/myimage    # push to registry
docker rmi image_id               # remove image
docker inspect image_id           # view image details
docker history image_id           # view image layers
```

### Containers
```bash
docker run -d -p 8080:80 nginx   # run container detached
docker run -it ubuntu /bin/bash   # run interactive
docker run -v /host:/container myimage  # mount volume
docker run -e VAR=value myimage   # set environment variable

docker ps                         # running containers
docker ps -a                      # all containers
docker stop container_id          # stop container
docker start container_id         # start container
docker restart container_id       # restart
docker rm container_id            # remove container
docker logs container_id          # view logs
docker exec -it container_id bash # run command in container
docker cp file container:/path    # copy to container
```

### Networks
```bash
docker network create mynet       # create network
docker run --network mynet myimage  # run on network
docker network ls                 # list networks
docker network rm mynet           # remove network
```

### Docker Compose
```bash
docker-compose up                 # start services
docker-compose up -d              # start detached
docker-compose down               # stop services
docker-compose logs               # view logs
docker-compose ps                 # list running services
docker-compose build              # build images
```

---

## AWS CLI Essentials

### Configuration
```bash
aws configure                     # set credentials & region
aws configure --profile myprofile # configure profile
aws s3 ls --profile myprofile     # use specific profile
```

### S3 (Simple Storage Service)
```bash
# List buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-bucket

# Upload file
aws s3 cp file.txt s3://my-bucket/
aws s3 cp file.txt s3://my-bucket/path/

# Download file
aws s3 cp s3://my-bucket/file.txt ./

# Sync directory
aws s3 sync ./local s3://my-bucket/remote/
aws s3 sync s3://my-bucket/remote/ ./local

# Remove
aws s3 rm s3://my-bucket/file.txt
aws s3 rb s3://my-bucket --force  # remove bucket

# List contents
aws s3 ls s3://my-bucket/
aws s3 ls s3://my-bucket/ --recursive
```

### EC2 (Elastic Compute Cloud)
```bash
# List instances
aws ec2 describe-instances

# Run instance
aws ec2 run-instances --image-id ami-12345 --instance-type t2.micro

# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### Lambda
```bash
# List functions
aws lambda list-functions

# Invoke function
aws lambda invoke --function-name my-function output.json
aws lambda invoke --function-name my-function --payload '{"key":"value"}' output.json

# Get function
aws lambda get-function --function-name my-function

# Update code
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

### DynamoDB
```bash
# List tables
aws dynamodb list-tables

# Scan table
aws dynamodb scan --table-name my-table

# Query
aws dynamodb query --table-name my-table --key-condition-expression "pk = :pk" --expression-attribute-values '{":pk":{"S":"value"}}'

# Put item
aws dynamodb put-item --table-name my-table --item '{"id":{"S":"123"},"name":{"S":"test"}}'

# Get item
aws dynamodb get-item --table-name my-table --key '{"id":{"S":"123"}}'

# Delete item
aws dynamodb delete-item --table-name my-table --key '{"id":{"S":"123"}}'
```

### General
```bash
# Help
aws help
aws s3 help
aws s3 cp help

# Check credentials
aws sts get-caller-identity

# List all available services
aws help | grep "^       " | head -20
```

---

## Tips & Tricks

### Python
- Use `pdb` for debugging: `import pdb; pdb.set_trace()`
- Use `timeit` for timing: `python -m timeit 'sum(range(100))'`
- Use list comprehensions for readable, fast code
- Use generator expressions for memory efficiency
- Use context managers (`with` statement) for resource cleanup

### Git
- Create meaningful commit messages (present tense, describe what/why)
- Commit often with logical, atomic changes
- Use branches for features, bugs, and experiments
- Keep master/main branch stable
- Use `.gitignore` to exclude files

### Docker
- Keep images small (use alpine Linux)
- Use `.dockerignore` to exclude files
- Multi-stage builds to reduce image size
- Run containers as non-root user for security
- Use health checks to monitor containers

### AWS
- Use IAM roles for EC2 instances instead of credentials
- Enable versioning on S3 buckets for data protection
- Use CloudWatch for monitoring and alerting
- Tag resources for organization and billing tracking
- Use VPCs to isolate resources

---

## Print-Friendly Tips

This document is designed to be printed. For best results:
1. Use landscape orientation for tables
2. Print in color (to see syntax highlighting)
3. Save as PDF for offline access
4. Use 10-12pt font for better readability
5. Print double-sided to save paper

---

**Last Updated:** May 2026 | **Version:** 1.0

For more detailed information, refer to:
- [Python Study Guide](python-study-guide.md)
- [Python Handbook](PYTHON_HANDBOOK.md)
- Official documentation: [Python Docs](https://docs.python.org/), [Git Book](https://git-scm.com/book), [Docker Docs](https://docs.docker.com/)
