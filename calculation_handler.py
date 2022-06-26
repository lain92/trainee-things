import datetime
import json
import os
import time
from decimal import Decimal
from json import JSONDecodeError

import boto3
from boto3.dynamodb.conditions import Key

from calculation import Calculation, CalculationResult
from response import Response

dynamodb = boto3.resource('dynamodb')


def calculate_response(event, context):
    try:
        body = json.loads(event['body'])
    except JSONDecodeError:
        return Response(400, "", "invalid body as input").return_as_json(encoder=DecimalEncoder)

    if not body or 'number1' not in body or 'number2' not in body:
        return Response(400, "", "invalid body as input").return_as_json(encoder=DecimalEncoder)

    calculation_result = Calculation(body['number1'], body['number2']).calculate()

    if not isinstance(calculation_result, CalculationResult):
        return Response(400, "", calculation_result).return_as_json(encoder=DecimalEncoder)

    save_calculation(calculation_result, body)
    return Response(200, calculation_result.return_as_json(), "").return_as_json(encoder=DecimalEncoder)


def save_calculation(calculation_result, body):
    table = dynamodb.Table(os.environ['DYNAMO_DB_CALC_RESULTS'])
    db_item = {
        'creation_date': str(datetime.date.today()),
        'creation_time': str(time.time()),
        'requestBody': body,
        'result': calculation_result.return_as_json()
    }
    parsed_db_item = json.loads(json.dumps(db_item), parse_float=Decimal)
    table.put_item(Item=parsed_db_item)


def get_latest_dynamo_entry(event, context):
    if "queryStringParameters" not in event and "date" not in event["queryStringParameters"]:
        return Response(400, "", "missing date as queryParameter").return_as_json()

    date = event["queryStringParameters"]["date"]
    try:
        validate_date(date)
    except ValueError:
        return Response(400, "", "Incorrect data format, should be YYYY-MM-DD").return_as_json()

    table = dynamodb.Table(os.environ['DYNAMO_DB_CALC_RESULTS'])
    query_result = table.query(KeyConditionExpression=Key('creation_date').eq(date), Limit=1, ScanIndexForward=False)
    items = query_result['Items']
    return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}


def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
