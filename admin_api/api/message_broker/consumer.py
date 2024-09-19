import os
import pika

from api.messages import messages


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)


def consume_user_messages():
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials("guest", "guest"),
    )

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()
    channel.queue_declare(queue="user_updates")

    channel.basic_consume(
        queue="user_updates",
        on_message_callback=messages.handle_user_creation_message,
        auto_ack=True,
    )
    print("Waiting for user messages. To exit press CTRL+C")
    channel.start_consuming()


def consume_borrow_messages():
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials("guest", "guest"),
    )

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()
    channel.queue_declare(queue="borrow_updates")

    channel.basic_consume(
        queue="borrow_updates",
        on_message_callback=messages.handle_borrow_message,
        auto_ack=True,
    )
    print("Waiting for borrow messages. To exit press CTRL+C")
    channel.start_consuming()
