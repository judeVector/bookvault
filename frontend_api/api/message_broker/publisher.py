import os
import json
import pika


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")


def publish_user_creation_message(event, data):

    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue="user_updates")

    message = json.dumps({"event": event, "data": data})
    channel.basic_publish(exchange="", routing_key="user_updates", body=message)

    connection.close()


def publish_book_borrowing_message(event, data):
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue="borrow_updates")

    message = json.dumps({"event": event, "data": data})

    channel.basic_publish(exchange="", routing_key="borrow_updates", body=message)
    connection.close()
