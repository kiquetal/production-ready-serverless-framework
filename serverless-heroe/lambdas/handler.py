import boto3
from lib.response import success_response, error_response
from art import tprint

def hello(event, context):
    # Get caller identity to print user/client ID
    sts_client = boto3.client('sts')
    caller_identity = sts_client.get_caller_identity()
    print(f"[DEBUG_LOG] AWS Account ID: {caller_identity['Account']}")
    print(f"[DEBUG_LOG] AWS User/Role ARN: {caller_identity['Arn']}")
    print(f"[DEBUG_LOG] AWS User ID: {caller_identity['UserId']}")
    tprint("kiquetal")
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

        return success_response(body)
    except Exception as e:
        return error_response("Error listing S3 buckets", error=str(e))
