from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
import json
from api.message_broker.publisher import publish_book_creation_message


class RabbitMQPublisherTests(APITestCase):

    @patch("api.message_broker.publisher.pika.BlockingConnection")
    def test_publish_book_creation_message(self, mock_blocking_connection):
        # Mock the connection, channel, and queue declaration
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Define the event and data
        event = "book_created"
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "category": "Test Category",
            "created_at": "2024-09-21T03:17:00",
        }

        # Call the function to test
        publish_book_creation_message(event, data)

        # Assert that the queue was declared
        mock_channel.queue_declare.assert_called_once_with(queue="library_books")

        # Assert that a message was published
        expected_message = json.dumps({"event": event, "data": data})
        mock_channel.basic_publish.assert_called_once_with(
            exchange="", routing_key="library_books", body=expected_message
        )

        # Assert the connection was closed
        mock_connection.close.assert_called_once()
