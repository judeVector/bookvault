import pika
import json
from .models import Book


def callback(ch, method, properties, body):
    message = json.loads(body)
    event = message["event"]
    data = message["data"]

    if event == "book_created":
        # Add book to frontend database
        Book.objects.create(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            publisher=data["publisher"],
            category=data["category"],
            available=True,  # A new book is available by default
        )
    elif event == "book_deleted":
        # Delete book from frontend database
        try:
            book = Book.objects.get(id=data["id"])
            book.delete()
        except Book.DoesNotExist:
            print(f"Book with ID {data['id']} does not exist")


def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the same queue to consume from
    channel.queue_declare(queue="library_books")

    # Set up subscription on the queue
    channel.basic_consume(
        queue="library_books", on_message_callback=callback, auto_ack=True
    )

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def publish_user_creation_message(user):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="user_updates")

    data = {
        "event": "user_created",
        "data": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
        },
    }
    channel.basic_publish(
        exchange="", routing_key="user_updates", body=json.dumps(data)
    )
    connection.close()
