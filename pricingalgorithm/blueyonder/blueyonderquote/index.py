from pricingalgorithm.blueyonder.blueyonderquote.by_quoting import blue_yonder
import json
import decimal
from boto3.dynamodb.types import TypeDeserializer
from pricingalgorithm.libs.send_s3 import send_s3

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def ddb_deserialize(r, type_deserializer = TypeDeserializer()):
    return type_deserializer.deserialize({"M": r})

def convert_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = convert_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = convert_decimals(v)
        return obj
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj

def lambda_handler(event, context):
    print("event: ",event)
    new_images = [ddb_deserialize(r["dynamodb"]["NewImage"]) for r in event['Records']]
    new_images = [convert_decimals(record) for record in new_images]
    print(new_images)
    responses = [blue_yonder(record) for record in new_images]
    #return responses
    return {
            "statusCode": 200,
            "body": json.dumps(responses)
        }

