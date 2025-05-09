import boto3
import json
import os
from lib.response import success_response, error_response
import uuid
from  aws_lambda_powertools import Logger
# Create the EventBridge client
events_client = boto3.client('events')

logger = Logger(
   service="place-order"
)
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    try:
        # Read from body json then convert to dict
        body = json.loads(event['body'])
        # Extract order details from the request body
        restaurant_name = body.get('restaurant_name')
        order_id = str(uuid.uuid4())
        logger.debug("Place order %s", order_id)
        event_bridge = boto3.client('events')
        # Create the event to be sent to EventBridge
        event_bridge.put_events(
            Entries=[
                {
                    'Source': 'big-mouth',
                    'DetailType': 'order_placed',
                    'Detail': json.dumps({
                        'order_id': order_id,
                        'restaurant_name': restaurant_name,

                    }),
                    'EventBusName': os.environ.get('EVENT_BUS_NAME')
                }]
        )

        logger.debug("Event sent to %s", os.environ.get('EVENT_BUS_NAME'))
        # Return a success response
        return success_response({"order_id": order_id}, 200)

    except Exception as e:
        # Handle any exceptions that occur during order processing
        logger.error("Error in place-order: " + str(e))
        return error_response({"message": "Failed to place order: " + str(e)}, 500)
