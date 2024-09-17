import pika
import json
from .models import User


def publish_message_to_queue(event, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare a queue (if it doesn't exist already)
    channel.queue_declare(queue="library_books")

    # Publish the message
    message = json.dumps({"event": event, "data": data})
    channel.basic_publish(exchange="", routing_key="library_books", body=message)

    connection.close()


def handle_user_creation_message(ch, method, properties, body):
    message = json.loads(body)
    event = message["event"]
    data = message["data"]

    if event == "user_created":
        User.objects.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            created_at=data["created_at"],
        )


def consume_user_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="user_updates")

    channel.basic_consume(
        queue="user_updates",
        on_message_callback=handle_user_creation_message,
        auto_ack=True,
    )
    print("Waiting for user messages. To exit press CTRL+C")
    channel.start_consuming()
