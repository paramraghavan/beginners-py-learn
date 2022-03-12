import src.database.helper as helper
import src.database.read_mongo_db as read_mongo_db
import src.database.read_from_postgresql as read_from_postgresql
import json

__debug_on__ = True
# output file created as a result of completion of this function
student_class_file = 'student_class.json'

def process(name_of_collection:str, table_name:str) -> None:
    out_file = None
    # this map is keyed by 'class id' and value is the name of the teacher.
    try :
        teachers_map = read_mongo_db.read_from_mongo_db_collection(name_of_collection)
        out_file =  open(student_class_file, 'w')
        out_file.write('[')
        for item in read_from_postgresql.read_row__at_time_postgresql(table_name):
            print(f'Student: {item["StudentName"]}, ClassId = {item["ClassId"]}')
            item['Teacher'] = teachers_map[ item['ClassId']]

            if __debug_on__:
                print(f'item: {item}')

            if helper.start_key not in item:
                out_file.write(f',\n{json.dumps(item)}')
            else:
                item.pop(helper.start_key, None)
                out_file.write(f'{json.dumps(item)}')

    except Exception:
        helper.printStackTrace('Error generating json')
    finally:
        if out_file:
            out_file.write(']')
            out_file.close()

if __name__ == "__main__":
    __debug_on__ = False
    process('teachers','Students');