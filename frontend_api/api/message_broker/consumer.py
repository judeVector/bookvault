import os
import pika

from api.messages import messages


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")


def consume_messages():
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declare the same queue from the admin api to consume from
    channel.queue_declare(queue="library_books")

    channel.basic_consume(
        queue="library_books",
        on_message_callback=messages.handle_book_creation_message,
        auto_ack=True,
    )

    print("Waiting for book updates. To exit press CTRL+C")
    channel.start_consuming()
