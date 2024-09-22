from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from django.utils import timezone

from api.models import Book, User, Borrow


class BorrowBookViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", first_name="John", last_name="Doe"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            category="Test Category",
            available=True,
            created_at=timezone.now(),
        )

    @patch("api.views.publish_book_borrowing_message")
    def test_borrow_book(self, mock_publish_message):
        url = reverse("book-borrow", kwargs={"book_id": self.book.id})
        data = {
            "user": self.user.id,
            "return_date": "2024-10-01",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)
        self.assertEqual(Borrow.objects.count(), 1)

        # Check if publish message function was called
        self.assertTrue(mock_publish_message.called)
        self.assertEqual(mock_publish_message.call_args[0][0], "book_borrowed")
