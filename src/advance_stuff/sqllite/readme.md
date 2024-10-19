# Using Sqllite to store state
Shared memory,[sharedmemory](../sharedmemory), usage did not work when  tracking state in dictionary. We tried to 
share this dictionary shared across scripts that run as separate python scripts. Using SQLLite as alternative approach. 


* We have 2 scripts
* One to add  new file name with state and another to view state by given filename
* Creating and initializing an SQLite database.
* Adding and updating records in the database.
* Retrieving specific records and all records from the database.
* Using timestamps to track when statuses were last updated.

## persis_file_state.py:
* Use add <filename> <status> to add or update a file's status.
* Use get <filename> to check a specific file's status.
* Use list to see all file statuses.
* Use quit to exit the program.


# view_file_state.py:
* Choose option 1 to view all file statuses.
* Choose option 2 to check a specific file's status.
* Choose option 3 to quit.