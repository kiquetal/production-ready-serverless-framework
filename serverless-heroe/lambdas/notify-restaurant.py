import json
import os
import boto3
from lib.response import  success_response, error_response
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer,
    idempotent,
)

from aws_lambda_powertools import Logger

logger = Logger(
    service="notify-restaurant"
)

persistence_layer = DynamoDBPersistenceLayer(
    table_name=os.environ.get('IDEMPOTENCY_TABLE')
)
@idempotent(persistence_store=persistence_layer)
def handler(event, context):
  try:
      # Receive event from evenBridge
    order = event['detail']
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.environ.get('SNS_TOPIC_ARN'),
        Message=json.dumps(order),
    )
    logger.debug("Notification sent to ")
    # publish new event to eventBridge
    event_bridge = boto3.client('events')
    event_bridge.put_events(
        Entries=[
            {
                'Source': 'big-mouth',
                'DetailType': 'restaurant_notified',
                'Detail': json.dumps(order),
                'EventBusName': os.environ.get('EVENT_BUS_NAME')
            }]
    )
    print(f"Restaurant notification event sent to EventBridge for order ID: {order['order_id']}")
    return success_response({"body": json.dumps(order)})
  except Exception as e:
    print(f"Error in notify-restaurant: {str(e)}")
    return error_response({"message": "Failed to notify restaurant: " + str(e)}, 500)
