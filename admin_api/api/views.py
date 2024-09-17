from rest_framework.exceptions import ValidationError

from rest_framework import generics
import requests

from .models import AdminBook, User, Book
from .serializers import AdminBookSerializer, UserSerializer, BookSerializer
from api.helpers import publish_message_to_queue


# # Only meant for Frontend interface only
class CreateUserFromFrontendAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class AdminBookCreateView(generics.CreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def perform_create(self, serializer):
#         book = serializer.save()
#         frontend_api_url = "http://localhost:8000/api/books/create/"
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "title": book.title,
#             "author": book.author,
#             "publisher": book.publisher,
#             "category": book.category,
#             "created_at": book.created_at.isoformat(),
#         }

#         try:
#             response = requests.post(frontend_api_url, json=data, headers=headers)
#             response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             # Log the error for future investigation
#             print(f"Error creating book in Frontend API: {e}")
#             raise ValidationError("Failed to notify the Frontend API.")


class AdminBookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        book = serializer.save()

        # Send a message to RabbitMQ
        data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "category": book.category,
            "created_at": book.created_at.isoformat(),
        }
        publish_message_to_queue("book_created", data)


# class AdminBookDeleteView(generics.DestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def perform_destroy(self, instance):
#         book_id = instance.id
#         frontend_api_url = f"http://localhost:8000/api/books/{book_id}/delete/"
#         headers = {"Content-Type": "application/json"}

#         try:
#             response = requests.delete(frontend_api_url, headers=headers)
#             response.raise_for_status()
#             instance.delete()
#         except requests.exceptions.RequestException as e:
#             print(f"Error deleting book in Frontend API: {e}")
#             raise ValidationError("Failed to delete the book in the Frontend API.")


class AdminBookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_destroy(self, instance):
        data = {"id": instance.id}
        publish_message_to_queue("book_deleted", data)

        super().perform_destroy(instance)


class AdminBorrowedBooksView(generics.ListAPIView):
    queryset = AdminBook.objects.filter(available=False)
    serializer_class = AdminBookSerializer
