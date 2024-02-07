from pricingalgorithm.blueyonder.blueyonderrequest.by_request import blue_yonder_request
import json
def lambda_handler(event, context):
    print("event",event)
    event=json.loads(event['body'])
    print("event:",event)
    response= blue_yonder_request(event)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }