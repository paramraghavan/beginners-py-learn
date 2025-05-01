I'd be happy to provide examples of common Unix commands for file manipulation. Here's a guide to these essential commands:

# File Manipulation Commands in Unix

## grep - Search for patterns in files

```bash
# Search for the word "error" in a log file
grep "error" logfile.txt

# Case-insensitive search
grep -i "warning" logfile.txt

# Show line numbers
grep -n "TODO" *.java

# Recursively search in directories
grep -r "function main" /path/to/project

# Show only filenames that contain matches
grep -l "deprecated" *.py

# Invert match (show lines that don't match)
grep -v "success" logfile.txt

# Match whole words only
grep -w "log" script.sh
```

## find - Search for files in a directory hierarchy

```bash
# Find all .txt files in current directory and subdirectories
find . -name "*.txt"

# Find files modified in the last 24 hours
find /home/user -mtime -1

# Find empty files
find . -type f -empty

# Find files with specific permissions
find . -type f -perm 644

# Find and delete files older than 7 days
find /tmp -type f -mtime +7 -exec rm {} \;

# Find and execute a command on each file
find . -name "*.log" -exec wc -l {} \;

# Find files by size (larger than 10MB)
find . -size +10M
```
### find and delete
```shell

# This will list all the files that match the pattern. Once you're confident the 
# results are correct, you can append -delete to perform the removal:
find . -name '._*' -type f


# To recursively remove all files starting with `._`  you can use the following command:

```bash
find . -name '._*' -type f -delete
```

### Explanation:
- `find .` — starts searching in the current directory.
- `-name '._*'` — looks for files that start with `._`.
- `-type f` — ensures only files are targeted (not directories).
- `-delete` — deletes the matching files.

⚠️ **Note**: This command **cannot be undone**, so double-check your path and intention before running it.

```


## sort - Sort lines in text files

```bash
# Simple sort
sort data.txt

# Sort numerically
sort -n numbers.txt

# Sort in reverse order
sort -r data.txt

# Sort by specific field (column 3)
sort -k3 data.txt

# Sort by multiple fields (first by col 2, then by col 1)
sort -k2,2 -k1,1 data.txt

# Remove duplicates while sorting
sort -u data.txt

# Case-insensitive sort
sort -f names.txt
```

## cut - Remove sections from each line of files

```bash
# Extract the 1st field using tab as delimiter
cut -f1 data.tsv

# Extract the 2nd and 4th fields using comma as delimiter
cut -d',' -f2,4 data.csv

# Extract characters 1-10 from each line
cut -c1-10 file.txt

# Extract from 5th character to the end of line
cut -c5- file.txt

# Extract multiple character ranges
cut -c1-5,10-15 file.txt

# Use with other commands via pipe
grep "ERROR" logfile.txt | cut -d':' -f2
```

## xargs - Build and execute command lines from standard input

```bash
# Find all .txt files and count lines in each
find . -name "*.txt" | xargs wc -l

# Find all .jpg files and create a backup with .bak extension
find . -name "*.jpg" | xargs -I{} cp {} {}.bak

# Delete all files listed in files.txt
cat files.txt | xargs rm

# Run multiple commands with xargs
find . -name "*.log" | xargs -I{} sh -c 'echo "Processing {}"; gzip {}'

# Limit number of arguments per command execution
find . -name "*.jpg" | xargs -n 10 tar -cvzf pics.tar.gz

# Prompt before execution
find . -name "*.tmp" | xargs -p rm
```

## sed - Stream editor for filtering and transforming text

```bash
# Replace first occurrence of 'old' with 'new' in each line
sed 's/old/new/' file.txt

# Replace all occurrences of 'old' with 'new' in each line
sed 's/old/new/g' file.txt

# Delete lines containing pattern
sed '/pattern/d' file.txt

# Insert text at beginning of each line
sed 's/^/PREFIX /' file.txt

# Append text at end of each line
sed 's/$/ SUFFIX/' file.txt

# Edit files in-place (change the original file)
sed -i 's/error/warning/g' logfile.txt

# Apply multiple sed commands
sed -e 's/old/new/g' -e 's/bad/good/g' file.txt
```

## awk - Pattern scanning and processing language

```bash
# Print specific columns (fields)
awk '{print $1, $3}' file.txt

# Use different field separator
awk -F, '{print $1, $3}' data.csv

# Sum numbers in a column
awk '{sum += $3} END {print sum}' data.txt

# Filter rows based on a condition
awk '$3 > 100 {print $0}' data.txt

# Count lines satisfying a condition
awk '$3 == "ERROR" {count++} END {print count}' logfile.txt

# Calculate average of values in column 3
awk '{sum += $3; count++} END {print sum/count}' data.txt

# Print lines between patterns
awk '/START/,/END/' file.txt
```

## Other Useful Commands

```bash
# Count lines, words, and characters
wc file.txt

# Compare two files
diff file1.txt file2.txt

# Join lines from two files based on a common field
join file1.txt file2.txt

# Translate or delete characters
tr 'a-z' 'A-Z' < lowercase.txt > uppercase.txt

# Remove leading and trailing whitespace
cat file.txt | tr -s '[:blank:]' | sed 's/^[ \t]*//;s/[ \t]*$//'

# Split a file into pieces
split -b 10M largefile.bin part_

# Remove duplicate lines (must be sorted first)
sort file.txt | uniq
```

These commands can be combined using pipes (|) to create powerful data processing pipelines. For example:

```bash
# Find all Python files containing "TODO", extract the line numbers and sort them
grep -n "TODO" $(find . -name "*.py") | cut -d':' -f1,2 | sort -t':' -k1,1 -k2n,2

# Count occurrences of each error type in log files
grep "ERROR" *.log | cut -d':' -f3 | sort | uniq -c | sort -nr
```

