from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Book, Borrow, User


class BorrowViewsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="borrower@example.com",
            first_name="Borrower",
            last_name="User",
            created_at=timezone.now(),
        )
        self.book_data = {
            "title": "Unavailable Book",
            "author": "Unavailable Author",
            "publisher": "Unavailable Publisher",
            "category": "Non-fiction",
            "available": False,
        }

    def test_user_borrowed_books_list(self):
        book = Book.objects.create(**self.book_data)
        borrow = Borrow.objects.create(
            user=self.user, book=book, return_date="2024-12-01"
        )

        response = self.client.get(reverse("borrowed_books"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_email"], self.user.email)
        self.assertEqual(response.data[0]["book_title"], book.title)

    def test_unavailable_books_list(self):
        book = Book.objects.create(**self.book_data)
        borrow = Borrow.objects.create(
            user=self.user, book=book, return_date="2024-12-01"
        )
        response = self.client.get(reverse("unavailable_books"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book_title"], book.title)
        self.assertEqual(response.data[0]["return_date"], borrow.return_date)
