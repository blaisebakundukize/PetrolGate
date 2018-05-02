import json


class ExtractData(object):

    def __init__(self, json_file):
        self.json_file = json_file

    @staticmethod
    def load_json(file_name):
        data = json.loads(file_name)
        return data

    @staticmethod
    def response(success):
        response_obj = {
            "success": success,
            "errorMessage": "Process failed! Check your internet connection, and Try again"
        }
        if success:
            response_obj["errorMessage"] = "Process Done Successfully!!!!"
        return response_obj

    @staticmethod
    def login_response(success, name="empty"):
        response_obj = {
            "success": success,
            "errorMessage":"Username or password is not valid",
            "responseDate": {
                "name": "fail",
                "photo": "fail"
            }
        }
        if success:
            response_obj['responseDate'] = {
                "name": name,
                "photo": "should be there!!!"
            }
            response_obj['errorMessage'] = "logged in"

        return response_obj




