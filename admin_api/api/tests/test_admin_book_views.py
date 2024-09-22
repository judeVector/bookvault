from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from api.models import Book


class AdminBookViewsTest(APITestCase):

    def setUp(self):
        self.book_data = {
            "title": "New Book",
            "author": "Author Test",
            "publisher": "Publisher Test",
            "category": "Fiction",
        }

    @patch("api.views.publish_book_creation_message")
    def test_admin_book_create(self, mock_publish):
        response = self.client.post(reverse("admin_book_create"), self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(title="New Book")
        self.assertIsNotNone(book)

        # Assert that the publish function was called once
        mock_publish.assert_called_once_with(
            "book_created",
            {
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "category": book.category,
                "created_at": book.created_at.isoformat(),
            },
        )

    @patch("api.views.publish_book_creation_message")
    def test_admin_book_delete(self, mock_publish):

        book = Book.objects.create(**self.book_data)

        response = self.client.delete(reverse("admin_book_delete", args=[book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

        mock_publish.assert_called_once_with("book_deleted", {"id": book.id})
