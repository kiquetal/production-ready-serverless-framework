import boto3
import os

from lambdas.restaurants import default_results
from lib.response import success_response, error_response


def search_by_theme(theme,count):

    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb')
    table_name = os.environ.get('RESTAURANTS_TABLE')

    params = {
        'TableName': table_name,
        'Limit': count,
        'FilterExpression': 'contains(#themes, :theme)',
        'ExpressionAttributeNames': {
            '#themes': 'themes'
        },
        'ExpressionAttributeValues': {
            ':theme': theme }
    }

    # Scan the table with the filter expression
    response = dynamodb.scan(**params)
    items = response.get('Items', [])
    return items

def handler(event, context):
    try:
        # read body to get python dict
        req = event['body']
        theme = req['theme']
        default_results = os.getenv("default_results", 8)
        restaurants = search_by_theme(theme,default_results)
        return success_response(restaurants)
    except Exception as e:
        print(f"[ERROR-handler] {str(e)}")

        return error_response("Failed to search ", str(e))
