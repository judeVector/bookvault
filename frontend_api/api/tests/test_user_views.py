from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from api.models import User


class UserCreateViewTest(APITestCase):

    @patch("api.views.publish_user_creation_message")
    def test_create_user(self, mock_publish_message):
        url = reverse("user-create")
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")

        # Check if publish message function was called
        self.assertTrue(mock_publish_message.called)
        self.assertEqual(mock_publish_message.call_args[0][0], "user_created")
