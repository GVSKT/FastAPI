from fastapi import FastAPI, Request
from rt_queries_addition import *
import json
from db_config import pymongo_db
from helper import *
from jencoder import *
import constant_status_codes as error_code

# from bson import json_util
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from response import *

app = FastAPI()


@app.post("/get_user")
async def get_user(request: Request):
    try:
        mydb, mycol = pymongo_db()
        username = await request.json()
        data = mydb.users.find({"username": {"$regex": username['name'], "$options": "i"}},{'_id': 1, 'name': 1, 'username': 1})

        if data:
            response = {'data':  json.loads(JSONEncoder().encode([i for i in data]))
                      , 'message': "Success", 'status': 200}
        else:
            response = {'data': "", 'message': "No data found", 'status': 253}

        return response

        ''' Other Approaches for returning the Response '''

        ''' 
        Approach :-1 
        # json_compatible_item_data = jsonable_encoder(data)
        # return JSONResponse(content=json_compatible_item_data)
        '''

        ''' 
        Approach :-2 
        # json_docs = [json.dumps(doc, default=json_util.default) for doc in data]
        # return json_docs
        '''

    except Exception as ex:
        print("Error At get_user:", str(ex))
        return {"Exception": str(ex)}


@app.post("/get_username")
async def get_username(request: Request):
    try:
        mydb, mycol = pymongo_db()
        username = await request.json()
        data = mydb.users.find({"username": {"$regex": username['name']}}, {'_id': 1, 'name': 1, 'username': 1} )

        if data:
            response = {'data': json.loads(JSONEncoder().encode([i for i in data])),
                        'message': "Success", 'status': 200}
        else:
            response = {'data': "", 'message': "No data found", 'status': 253}

        return response


    except Exception as ex:
        print("Error  At get_username : ", str(ex))
        return {"Exception": str(ex)}


@app.post("/ParticipantListApi")
async def ParticipantListApi(request: Request):
    try:
        helper = GenericHelper()
        rt_id = await request.json()
        roundtable_id = rt_id['roundtable_id']

        userid = "637dc0f80fdaea7fa7cca61d"

        if userid != "" and roundtable_id != "":
            querying = Roundtable_Query()
            data = querying.get_participant_list_rt(roundtable_id)

            if data and len(data) > 0:

                if data:
                    response, status = helper.create_json_response(data=json.loads(JSONEncoder().encode(data)),
                                       message=error_code.SUCCESS_MESSAGE, status=error_code.SUCCESS_CODE)
                else:
                    response, status = helper.create_json_response("", message=error_code.NO_DATA_FOUND,
                                                                   status=error_code.ERROR_INCOMPLETE_DATA)
            else:
                response, status = helper.create_json_response("", message=error_code.NO_DATA_FOUND,
                                                               status=error_code.ERROR_INCOMPLETE_DATA)
        else:
            response, status = helper.create_json_response("", message=error_code.NO_DATA_FOUND,
                                                           status=error_code.ERROR_INCOMPLETE_DATA)

        return response

    except Exception as ex:
        return {"Exception Occurred ": str(ex)}



# @app.post("/PublicRTView")
# async def PublicRTView(request: Request):
#     try:
#         authentication_classes = []
#         helper = GenericHelper()
#         userid='637dc0f80fdaea7fa7cca61d'
#         # if '_id' in request.session:
#         #     userid = request.session['_id']
#
#         limit_data_ = request.data.get("limit")
#         if limit_data_ is None:
#             limit_data_ = 10
#         skip_data_ = request.data.get("skip")
#         if skip_data_ is None:
#             skip_data_ = 0
#
#         userid = request.data.get("user_id")
#         query = Roundtable_Query()
#         paginate = {'limit': int(limit_data_), 'skip': int(skip_data_)}
#         data = query.getPublicRtListV1(userid, paginate)
#
#         if len(data) > 0:
#             response, status = helper.create_json_response(data=json.loads(JSONEncoder().encode(data)),
#                                                            message="Success", status=200)
#         else:
#             response, status = helper.create_json_response(data=[], message="Success", status=200)
#
#         return Response(response, status)
#
#     except Exception as err:
#         print("\nError : ", err)
#         return {"Exception : ": str(ex)}


