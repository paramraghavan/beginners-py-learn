# read postgres
import psycopg2
import helper
from typing import Dict

database_name:str = 'singlestone'
username:str = 'singlestone'
password:str =  'singlestone'

__debug_on__:bool = True

'''
Reads and returns  one row at a time
'''
def read_row__at_time_postgresql(table_name:str) ->Dict:

    conn_postgresql = None
    try :
        conn_postgresql = psycopg2.connect(database=database_name, user=username, password=password, host="127.0.0.1", port="5432")
        if __debug_on__:
            print("Database opened successfully")

        cur = conn_postgresql.cursor()
        cur.execute("SELECT fname || ' ' || lname as StudentName, cid as ClassId from students")
        rows = cur.fetchall()

        student_teacher = []
        # indicates end rows from database
        item = {}
        item[helper.start_key] = helper.start_key
        for row in rows:
            # print("StudentName =", row[0])
            # print("ClassId =", row[1], "\n")
            # print('teacher =', {dict_of_teachers[row[1]]})
            item['StudentName'] = row[0]
            item['ClassId']     = row[1]
            if __debug_on__:
                print(f'item {item}')
            yield item
            item = {}

        if __debug_on__:
            print("Operation done successfully")
    except Exception:
        helper.printStackTrace('Error with postgres database')
        import sys
        sys.exit(-1)
    finally:
        if conn_postgresql:
            conn_postgresql.close()


if __name__ == "__main__":
    __debug_on__ = False
    for item in read_row__at_time_postgresql('Students'):
        print(f'Student: {item["StudentName"]}, ClassId = {item["ClassId"]}')
