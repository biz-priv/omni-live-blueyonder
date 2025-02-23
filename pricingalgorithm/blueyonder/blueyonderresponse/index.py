from pricingalgorithm.blueyonder.blueyonderresponse.by_response import blue_yonder_response
import json
import decimal
from boto3.dynamodb.types import TypeDeserializer

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def ddb_deserialize(r, type_deserializer = TypeDeserializer()):
    return type_deserializer.deserialize({"M": r})

def lambda_handler(event, context):
    print(event)
    new_images = [ddb_deserialize(r["dynamodb"]["NewImage"]) for r in event['Records']]
    print(new_images)
    responses = [blue_yonder_response(record) for record in new_images]
    # return responses
    return {
            "statusCode": 200,
            "body": json.dumps(responses)
        }