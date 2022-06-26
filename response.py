import json


class Response:

    def __init__(self, status_code, content, error_message):
        self.body = {}
        self.statusCode = status_code
        self.body['content'] = content
        self.body['errorMessage'] = error_message

    def return_as_json(self, encoder: None):
        return {"statusCode": self.statusCode, "body": json.dumps(self.body, cls=encoder)}
