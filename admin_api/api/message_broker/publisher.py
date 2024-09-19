import os
import json
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)


def publish_book_creation_message(event, data):
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials("guest", "guest"),
    )

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    # Declare a queue (if it doesn't exist already)
    channel.queue_declare(queue="library_books")

    # Publish the message
    message = json.dumps({"event": event, "data": data})
    channel.basic_publish(exchange="", routing_key="library_books", body=message)

    connection.close()
