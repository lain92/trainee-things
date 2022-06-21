import json
import logging
import os
import time
import uuid
from decimal import Decimal

import boto3

dynamodb = boto3.resource('dynamodb')


def calculate_response(event, context):
    body = json.loads(event['body'])

    number1 = body['number1']
    number2 = body['number2']

    if number2 == 0:
        logging.error("division by 0 not possible")
        body['errorMessage'] = "division by 0 not possible"
        return {"statusCode": 400, "body": json.dumps(body)}

    result = {
        'sum': number1 + number2,
        'diff': number1 - number2,
        'product': number1 + number2,
        'quotient': number1 / number2
    }
    save_calculation(result, body)
    return {"statusCode": 200, "body": json.dumps(result, cls=DecimalEncoder)}


def save_calculation(result, body):
    table = dynamodb.Table(os.environ['DYNAMO_DB_CALC_RESULTS'])
    db_item = {
        'primary_key': str(uuid.uuid1()),
        'created_on': str(time.time()),
        'requestBody': body,
        'result': result
    }
    parsed_db_item = json.loads(json.dumps(db_item), parse_float=Decimal)
    table.put_item(Item=parsed_db_item)


def get_latest_dynamo_entry(event, context):
    table = dynamodb.Table(os.environ['DYNAMO_DB_CALC_RESULTS'])
    scan_result = table.scan()
    items = scan_result['Items']
    sorted_items = sorted(items, key=lambda item: item['created_on'], reverse=True)
    return {"statusCode": 200, "body": json.dumps(sorted_items[0], cls=DecimalEncoder)}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
