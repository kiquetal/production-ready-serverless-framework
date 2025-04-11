import json
import boto3


def hello(event, context):
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # List all S3 buckets
    try:
        response_s3 = s3_client.list_buckets()

        # Extract bucket names
        bucket_names = [bucket['Name'] for bucket in response_s3['Buckets']]

        body = {
            "message": "Go Serverless v4.0! Your function executed successfully!",
            "buckets": bucket_names
        }

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        body = {
            "message": "Error listing S3 buckets",
            "error": str(e)
        }
        response = {"statusCode": 500, "body": json.dumps(body)}

    return response
