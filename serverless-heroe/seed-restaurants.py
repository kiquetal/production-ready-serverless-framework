import os
import boto3
import math

def seed_restaurants():

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
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table("development-serverless-heroe-restaurants")
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

if __name__ == "__main__":
    seed_restaurants()
