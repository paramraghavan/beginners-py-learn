# read postgres
import psycopg2
if __name__ == "__main__":
    from helper import printStackTrace, start_key
else:
    from .helper import printStackTrace, start_key

from typing import Dict

database_name:str = 'testdb'
username:str = 'testdb'
password:str =  'testdb'

__debug_on__:bool = True
__fetch_size__ = 100

'''
Reads and returns  one row at a time.
We are limiting the fetch size to 100, so that all(fetchall) the records from the table are not read into memory
'''
def read_row__at_time_postgresql(table_name:str) ->Dict:

    conn_postgresql = None
    try :
        conn_postgresql = psycopg2.connect(database=database_name, user=username, password=password, host="127.0.0.1", port="5432")
        if __debug_on__:
            print("Database opened successfully")

        cur = conn_postgresql.cursor()
        # This fetches only 100 records from DB as batches
        # If you don't specify, the default value is 2000
        cur.itersize = __fetch_size__
        cur.execute("SELECT fname || ' ' || lname as StudentName, cid as ClassId from students")

        student_teacher = []
        # indicates end rows from database
        item = {}
        item[start_key] = start_key
        for row in cur:
            item['StudentName'] = row[0]
            item['ClassId']     = row[1]
            if __debug_on__:
                print(f'item {item}')
            yield item
            item = {}

        if __debug_on__:
            print("Operation done successfully")
    except Exception:
        printStackTrace('Error with postgres database')
        import sys
        sys.exit(-1)
    finally:
        if conn_postgresql:
            conn_postgresql.close()


if __name__ == "__main__":
    __debug_on__ = False
    for item in read_row__at_time_postgresql('Students'):
        print(f'Student: {item["StudentName"]}, ClassId = {item["ClassId"]}')

'''

Notes:
https://medium.com/dev-bits/understanding-postgresql-cursors-with-python-ebc3da591fe7
'''