import json
import logging


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

    return {"statusCode": 200, "body": json.dumps(result)}
