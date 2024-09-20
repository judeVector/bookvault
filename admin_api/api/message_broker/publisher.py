import os
import json
import pika

# Fetch environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")


def publish_book_creation_message(event, data):

    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue="library_books")

    message = json.dumps({"event": event, "data": data})
    channel.basic_publish(exchange="", routing_key="library_books", body=message)

    connection.close()
