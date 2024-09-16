from django.db import transaction
from django.shortcuts import get_object_or_404
import requests

from rest_framework import generics, serializers
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Book, Borrow
from .serializers import UserSerializer, BookSerializer, BorrowSerializer
from .filters import BookFilter


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # This Notifies the Admin API about the new user
        admin_api_url = "http://localhost:7000/api/users/create/"
        headers = {"Content-Type": "application/json"}

        # Data to send to the Admin API
        data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
        }

        response = requests.post(admin_api_url, json=data, headers=headers)

        if response.status_code != 201:
            raise Exception(f"Error creating user in Admin API: {response.text}")


class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CreateBookView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowBookView(generics.CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, pk=book_id)

        if book.available:
            book.available = False
            book.save()
            serializer.save(book=book)
        else:
            raise serializers.ValidationError({"book": "Book is not available."})
