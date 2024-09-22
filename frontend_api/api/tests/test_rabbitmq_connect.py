from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
import json
from api.message_broker.publisher import (
    publish_user_creation_message,
    publish_book_borrowing_message,
)


class RabbitMQPublisherTests(APITestCase):

    @patch("api.message_broker.publisher.pika.BlockingConnection")
    def test_publish_user_creation_message(self, mock_blocking_connection):
        # Mock the connection, channel, and queue declaration
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Define the event and data
        event = "user_created"
        data = {"id": 1, "email": "test@example.com"}

        # Call the function to test
        publish_user_creation_message(event, data)

        # Assert that the queue was declared
        mock_channel.queue_declare.assert_called_once_with(queue="user_updates")

        # Assert that a message was published
        expected_message = json.dumps({"event": event, "data": data})
        mock_channel.basic_publish.assert_called_once_with(
            exchange="", routing_key="user_updates", body=expected_message
        )

        # Assert the connection was closed
        mock_connection.close.assert_called_once()

    @patch("api.message_broker.publisher.pika.BlockingConnection")
    def test_publish_book_borrowing_message(self, mock_blocking_connection):
        # Mock the connection, channel, and queue declaration
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Define the event and data
        event = "book_borrowed"
        data = {"book_id": 1, "user_id": 1, "borrow_date": "2024-09-20"}

        # Call the function to test
        publish_book_borrowing_message(event, data)

        # Assert that the queue was declared
        mock_channel.queue_declare.assert_called_once_with(queue="borrow_updates")

        # Assert that a message was published
        expected_message = json.dumps({"event": event, "data": data})
        mock_channel.basic_publish.assert_called_once_with(
            exchange="", routing_key="borrow_updates", body=expected_message
        )

        # Assert the connection was closed
        mock_connection.close.assert_called_once()
