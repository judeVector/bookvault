from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, serializers
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Book, Borrow
from .serializers import UserSerializer, BookSerializer, BorrowSerializer
from .filters import BookFilter


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class BookDetailView(generics.RetrieveAPIView):
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
