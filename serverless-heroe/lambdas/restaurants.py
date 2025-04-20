
import json
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

from lib.response import success_response, error_response

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

default_results = int(os.environ.get('default_results'))
table_name = os.environ.get('RESTAURANTS_TABLE')

def deserialize(item):
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in item.items()}

def get_restaurants(count):
    print(f"fetching {count} restaurants from {table_name}...")

    response = dynamodb.scan(
        TableName=table_name,
        Limit=count
    )

    # Convert DynamoDB items to regular Python dicts
    items = [deserialize(item) for item in response.get('Items', [])]
    print(f"found {len(items)} restaurants")
    return items

def handler(event, context):
    try:
        restaurants = get_restaurants(default_results)
        return success_response(restaurants)
    except Exception as e:
        return error_response("Failed to fetch restaurants", str(e))


