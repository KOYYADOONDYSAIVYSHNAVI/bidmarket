import pika
import json


RABBITMQ_URI = "amqp://guest:guest@localhost:5672"  

def send_notification(event_type, data):
    """
    Sends a notification event to RabbitMQ.
    :param event_type: The type of event (e.g., item_watchlist_match)
    :param data: Dictionary containing event-related data (e.g., user_email, item_name)
    """
    message = {
        "event_type": event_type,
        **data  # Add additional data for the event (e.g., user_email, item_name)
    }

    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue='auction_notifications', durable=True)

    # Publish the message to RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='auction_notifications',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )

    print(f"Sent notification event: {event_type} with data: {data}")
    connection.close()
