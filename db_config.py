import pymongo
from config.config import db_config

URI,collection_name=db_config()

def pymongo_db():
    try:
        client=pymongo.MongoClient(URI)
        dblist = client.list_database_names()
        print("\ndblist : ", dblist)
        database = client["khulkeV1"]
        collection = database[collection_name]
        return database, collection

    except Exception as ex:
        print("\nError At pymongo_db : ", str(ex))

