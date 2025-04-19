import os

import boto3

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
  table = dynamodb.Table(os.getenv("RESTAURANTS_TABLE"))
  for restaurant in restaurants:
    table.put_item(
        item={
            "name": restaurant["name"],
            "image": restaurant["image"],
            "themes": restaurant["themes"]
                }
        )
  print(f"seeded {len(restaurants)} restaurants to {os.getenv('RESTAURANTS_TABLE')}")
