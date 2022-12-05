

class GenericHelper():

    def create_json_response(self, data, message, status):
        response = {}
        if type(data) == list:
            response['data'] = data
        else:
            if data == '':
                response['data'] = []
            else:
                response['data'] = [data]
        response['message'] = message
        response['status'] = status
        status_code = status
        return response, status_code

    def create_api_data(self, route, method, data):
        user_details = {}
        user_details["route"] = route
        if method is not None or method != '':
            user_details["method"] = method.upper()
        user_details["data"] = data

        return user_details

