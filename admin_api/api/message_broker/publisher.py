import os
import json
import pika

# Fetch environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")


def publish_book_creation_message(event, data):
    try:
        connection_params = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=int(RABBITMQ_PORT),
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
        )

        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        # Declare a durable queue
        channel.queue_declare(queue="library_books", durable=True)

        # Prepare the message
        message = json.dumps({"event": event, "data": data})

        # Publish the message with persistence
        channel.basic_publish(
            exchange="",
            routing_key="library_books",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ),
        )

        # Close connection
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
