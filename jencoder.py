from bson.objectid import ObjectId
import json
import datetime



class JSONEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, (datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        return json.JSONEncoder.default(self, obj)