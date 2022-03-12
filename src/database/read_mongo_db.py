import pymongo
if __name__ == "__main__":
    from helper import printStackTrace, start_key
else:
    from .helper import printStackTrace, start_key

from typing import Dict

database_name:str = 'testdb'
username:str = 'testdb'
password:str =  'testdb'

__debug_on__:bool = True

def read_from_mongo_db_collection(name_of_collection:str) -> Dict:
    client = None
    try:
        client = pymongo.MongoClient(f"mongodb://{username}:{password}@localhost:27017/")

        # Database Name
        db = client[database_name]
        # Collection Name
        collection_teachers = db[name_of_collection]

        # keep only the columns you need
        columns = {'fname': 1, 'lname': 1, 'cid':1}
        cursor = collection_teachers.find({},columns).sort("_id", -1).limit(1)
        doc = cursor.next()

        dict_of_teachers = {}

        if doc:
            dict_fname = doc['fname']
            dict_lname = doc['lname']
            dict_cid   = doc['cid']

            loop_count = len(dict_fname)
            for i in range(loop_count):
                dict_of_teachers[dict_cid[str(i)]] = f'{dict_fname[str(i)]} {dict_lname[str(i)]}'
            if __debug_on__:
                print(dict_of_teachers)
        else:
            raise Exception('Error reading from mongodb cursor')
    except Exception:
        printStackTrace(f'Error reading from mongodb. for collection {collection_teachers}')
    finally:
        if client:
            client.close()

    return dict_of_teachers


if __name__ == "__main__":
    __debug_on__ = False
    teachers_map = read_from_mongo_db_collection("teachers")
    print(f'read_from_mondo_db_collection : \n{teachers_map}')