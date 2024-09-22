from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User


class AdminUserViewsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="user@example.com",
            first_name="New User",
            last_name="User",
            created_at=timezone.now(),
        )

    def test_admin_user_list(self):
        response = self.client.get(reverse("admin_user_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
