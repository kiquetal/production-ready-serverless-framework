import os
import boto3


def handler(event):
    try:
      order = event['detail']
      dynamodb = boto3.resource('dynamodb')
      table_name = os.environ.get('ORDERS_TABLE')
      table = dynamodb.Table(table_name)
      table.put_item(
          Item={
              'order_id': order['order_id'],
              'restaurantName': order['restaurant_name'],

          }
      )
      print(f"Order seeded to DynamoDB table: {table_name}")


    except Exception as e:
      print(f"Error in seed-order: {str(e)}")
      return error_response({"message": "Failed to seed order: " + str(e)}, 500)
