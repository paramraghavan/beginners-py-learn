import psycopg2

# printStackTrace prints as follows for postgres connection error
# --------------------------------------------------------------------------------
# Error connecting postgres database:
# --------------------------------------------------------------------------------
# Traceback (most recent call last):
#   File "C:/Users/padma/github/beginners-py-learn/src/advance_stuff/exception_handling_logging.py", line 12, in <module>
#     conn_postgresql = psycopg2.connect(database="abc", user="abc", password="abc", host="127.0.0.1", port="5432")
#   File "C:\Users\padma\github\beginners-py-learn\venv\lib\site-packages\psycopg2\__init__.py", line 122, in connect
#     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
# psycopg2.OperationalError: connection to server at "127.0.0.1", port 5432 failed: Connection refused (0x0000274D/10061)
# 	Is the server running on that host and accepting TCP/IP connections?
# --------------------------------------------------------------------------------
#
#   except:
#    print(traceback.print_exc())
#    sys.exit(1)
#
#   import sys
#   # returns a tuple of 3 - Exeption Type, Exception  and traceback object
#   exception_info_object = sys.exc_info()
#   traceback_obj = sys.exc_info()[2]
#   print(traceback+obj.tb_lineno) --> exactly where the error occured
#   print(traceback+obj.tb_frame)
#   print(traceback+obj.tb_next.tb_lineno) <- one level above, closer to where exception occured
#   print(traceback+obj.tb_next.tb_frame)  <- one level above
#
#
#

import traceback

def printStackTrace(message:str) -> None:
    traceback_error_msg = traceback.format_exc()
    print(f'{80*"-"}\n{message}:\n{80*"-"}\n{traceback_error_msg}{80*"-"}')


conn_postgresql = None
try :
    conn_postgresql = psycopg2.connect(database="abc123", user="abc123", password="abc123", host="127.0.0.1", port="5432")
    print("Database opened successfully")

    cur = conn_postgresql.cursor()
    cur.execute("SELECT fname || ' ' || lname as StudentName, cid as ClassId from students")
    rows = cur.fetchall()

    for row in rows:
        print("StudentName =", row[0])
        print("ClassId =", row[1], "\n")

except Exception:
    '''
    Printing stack trace
    '''
    printStackTrace('Error connecting postgres database')
    import sys
    sys.exit(-1)

if conn_postgresql:
    conn_postgresql.close()
