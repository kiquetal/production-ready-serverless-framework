
import json
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer
from jinja2 import FileSystemLoader, Environment

from lib.response import success_response, error_response, html_response
import datetime
# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

default_results = int(os.environ.get('default_results'))
table_name = os.environ.get('RESTAURANTS_TABLE')

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
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


def return_page():
    try:
        template_dir = os.path.join(os.path.dirname(__file__), '..','static')
        env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
        template = env.get_template('index.html')
        return template
    except Exception as e:
        print("Error loading template: ", str(e))
        return error_response("Failed to return template", str(e))

def load_restaurants(event, context):
    try:
        template = return_page()
        restaurants = get_restaurants(default_results)
        print("Weekday is", datetime.datetime.now().weekday())
        dayOfWeek = days[datetime.datetime.now().weekday()]
        rendered_page = template.render(dayOfWeek=dayOfWeek, restaurants=restaurants)
        return html_response(rendered_page)
    except Exception as e:
        return error_response("Failed to load restaurants", str(e))
