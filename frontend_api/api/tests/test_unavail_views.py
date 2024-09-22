from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone

from api.models import Book, User


class BorrowBookViewUnavailableTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", first_name="John", last_name="Doe"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            category="Test Category",
            available=False,
            created_at=timezone.now(),
        )

    def test_borrow_unavailable_book(self):
        url = reverse("book-borrow", kwargs={"book_id": self.book.id})
        data = {
            "user": self.user.id,
            "return_date": "2024-10-01",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"book": "Book is not available."})
