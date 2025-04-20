import boto3
import os

from lib.response import success_response, error_response


def search_by_theme(theme,count):

    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb')
    table_name = os.environ.get('RESTAURANTS_TABLE')

    params = {
        'TableName': table_name,
        'Limit': 10,
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
        restaurants = search_by_theme(theme,10)
        return success_response(restaurants)
    except Exception as e:
        print(f"[ERROR] {e}")
        return error_response(str(e))
