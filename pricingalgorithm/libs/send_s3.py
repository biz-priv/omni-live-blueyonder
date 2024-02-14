import boto3
import json
from datetime import datetime
import pytz
import os
env=os.environ['ENVIRONMENT']
def send_s3(data):
    # S3 bucket and object details
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_bucket_name = "pricing-algorithm"
    s3_object_key = f"blueyonder/{env}/{current_datetime}-data.json"
    # Upload data to S3
    s3 = boto3.client("s3")
    data=str(data)
    data = data.replace("\'", "\"")
    #data = data.replace(" ", "")
    s3.put_object(
        Bucket=s3_bucket_name,
        Key=s3_object_key,
        Body=data.encode('utf-8'),
        ACL='bucket-owner-full-control',
        ContentEncoding='utf8'
    )
    print("file transfered to s3 : pricing-algorithm")

    return {
        "statusCode": 200,
        "body": json.dumps("Data successfully sent to S3 !")
    }
