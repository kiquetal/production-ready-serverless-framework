import argparse
import os
import boto3
import math

def seed_restaurants(table_name=None, endpoint_url=None, profile=None):

  restaurants = [
    {
        "name": "Fangtasia",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/fangtasia.png",
        "themes": ["true blood"]
    },
    {
        "name": "Shoney's",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/shoney's.png",
        "themes": ["cartoon", "rick and morty"]
    },
    {
        "name": "Freddy's BBQ Joint",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/freddy's+bbq+joint.png",
        "themes": ["netflix", "house of cards"]
    },
    {
        "name": "Pizza Planet",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/pizza+planet.png",
        "themes": ["netflix", "toy story"]
    },
    {
        "name": "Leaky Cauldron",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/leaky+cauldron.png",
        "themes": ["movie", "harry potter"]
    },
    {
        "name": "Lil' Bits",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/lil+bits.png",
        "themes": ["cartoon", "rick and morty"]
    },
    {
        "name": "Fancy Eats",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/fancy+eats.png",
        "themes": ["cartoon", "rick and morty"]
    },
    {
        "name": "Don Cuco",
        "image": "https://d2qt42rcwzspd6.cloudfront.net/manning/don%20cuco.png",
        "themes": ["cartoon", "rick and morty"]
    },
    ]
  if not table_name:
      table_name = os.getenv('RESTAURANTS_TABLE', 'development-serverless-heroe-restaurants')

  print(f"Using table: {table_name}")
  print(f"Using endpoint: {endpoint_url or 'AWS default'}")

  # Configure boto3 client to use LocalStack
  session_kwargs = {}
  if profile:
      session_kwargs['profile_name'] = profile

  session = boto3.Session(**session_kwargs)

  # Connect to LocalStack if endpoint provided
  dynamodb_kwargs = {}
  if endpoint_url:
      dynamodb_kwargs['endpoint_url'] = endpoint_url

  dynamodb = session.resource('dynamodb', **dynamodb_kwargs)
  table = dynamodb.Table(table_name)

  # DynamoDB batch_writer automatically handles batches of up to 25 items
  batch_size = 25
  total_batches = math.ceil(len(restaurants) / batch_size)

  print(f"Starting to seed {len(restaurants)} restaurants in {total_batches} batch(es)")

  with table.batch_writer() as batch:
      for i, restaurant in enumerate(restaurants, 1):
          batch.put_item(
              Item={
                  "name": restaurant["name"],
                  "image": restaurant["image"],
                  "themes": restaurant["themes"]
              }
          )
          if i % batch_size == 0:
              print(f"Processed batch {i // batch_size} of {total_batches}")

  print(f"Successfully seeded {len(restaurants)} restaurants to {os.getenv('RESTAURANTS_TABLE')}")

def create_table_locally(table_name=None, endpoint_url=None, profile=None):
    """Create the DynamoDB table locally in LocalStack."""
    if not table_name:
        table_name = os.getenv('RESTAURANTS_TABLE', 'development-serverless-heroe-restaurants')

    print(f"Creating table: {table_name}")
    print(f"Using endpoint: {endpoint_url or 'AWS default'}")

    # Configure boto3 client to use LocalStack
    session_kwargs = {}
    if profile:
        session_kwargs['profile_name'] = profile

    session = boto3.Session(**session_kwargs)

    # Connect to LocalStack if endpoint provided
    dynamodb_kwargs = {}
    if endpoint_url:
        dynamodb_kwargs['endpoint_url'] = endpoint_url

    dynamodb = session.resource('dynamodb', **dynamodb_kwargs)

    # Check if table already exists
    existing_tables = [t.name for t in dynamodb.tables.all()]
    if table_name in existing_tables:
        print(f"Table {table_name} already exists")
        return dynamodb.Table(table_name)

    # Create the table with the schema from serverless.yml
    table = dynamodb.create_table(
        TableName=table_name,
        BillingMode='PAY_PER_REQUEST',
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
        ]
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table {table_name} created successfully")
    return table


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Seed restaurants table with sample data')
    parser.add_argument('--table', help='DynamoDB table name')
    parser.add_argument('--endpoint-url', help='LocalStack endpoint URL (default: http://localhost:4566)')
    parser.add_argument('--profile', help='AWS profile to use')
    parser.add_argument('--create-table', action='store_true', help='Create the table before seeding')
    args = parser.parse_args()

    endpoint_url = args.endpoint_url or 'http://localhost:4566'
    table_name = args.table

    if args.create_table:
        create_table_locally(table_name=table_name, endpoint_url=endpoint_url, profile=args.profile)

    seed_restaurants(
        table_name=table_name,
        endpoint_url=endpoint_url,
        profile=args.profile
    )
