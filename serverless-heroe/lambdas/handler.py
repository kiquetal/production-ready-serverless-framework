import os

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
    s3_endpoint_url = None
    # Initialize S3 client
    if os.environ.get('IS_LOCAL'):
        s3_endpoint_url = 'http://localhost:4566'
        s3_client = boto3.client(
        's3',
        endpoint_url=s3_endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
    else:
        s3_client = boto3.client('s3')

    print(f"[DEBUG_LOG] Running locally (IS_LOCAL=True), using S3 endpoint: {s3_endpoint_url} with dummy credentials.")

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
