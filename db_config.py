import pymongo
from config.config import db_config
URI,collection=db_config()

def pymongo_db():
    try:
        client=pymongo.MongoClient(URI)
        dblist = client.list_database_names()
        print("\ndblist : ", dblist)
        mydb = client["khulkeV1"][collection]
        return mydb

    except Exception as ex:
        print("\nError At pymongo_db : ", str(ex))



