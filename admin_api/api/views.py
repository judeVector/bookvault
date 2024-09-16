from rest_framework import generics
import requests

from .models import AdminBook, User, Book
from .serializers import AdminBookSerializer, UserSerializer, BookSerializer


class CreateUserFromFrontendAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminBookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        book = serializer.save()

        # This Notifies the Frontend API about the new book
        frontend_api_url = "http://localhost:8000/api/books/create/"
        headers = {"Content-Type": "application/json"}

        # Data to send to the Frontend API
        data = {
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "category": book.category,
            "created_at": book.created_at.isoformat(),
        }

        response = requests.post(frontend_api_url, json=data, headers=headers)

        if response.status_code != 201:
            raise Exception(f"Error creating book in Frontend API: {response.text}")


class AdminBookDeleteView(generics.DestroyAPIView):
    queryset = AdminBook.objects.all()
    serializer_class = AdminBookSerializer


class AdminBorrowedBooksView(generics.ListAPIView):
    queryset = AdminBook.objects.filter(available=False)
    serializer_class = AdminBookSerializer
