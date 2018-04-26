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
            "success": False
        }
        if success:
            response_obj["success"] = success
        return response_obj



