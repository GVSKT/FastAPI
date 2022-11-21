from fastapi import FastAPI, Request
from db_config import pymongo_db
from bson import json_util
import json

app = FastAPI()

@app.post("/get_user")
async def get_user(request:Request):
    try:
        mydb = pymongo_db()
        username = await request.json()
        data = mydb.find({"username": {"$regex":username['name'], "$options":"i"}})
        json_docs = [json.dumps(doc, default=json_util.default) for doc in data]
        print("\ndata : ", json_docs)
        return json_docs
    except Exception as ex:
        print("Error At get_user:", str(ex))
        return {"Exception": str(ex)}

@app.post("/get_username")
async def get_username(request:Request):
    try:
        mydb = pymongo_db()
        username = await request.json()
        data = mydb.find({"username": {"$regex": username['name']}})
        json_docs = [json.dumps(doc, default=json_util.default) for doc in data]
        print("\ndata : ", json_docs)
        return json_docs
    except Exception as ex:
        print("Error  At get_username : ", str(ex))
        return {"Exception": str(ex)}
