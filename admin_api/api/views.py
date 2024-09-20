from rest_framework import generics

from .models import Borrow, User, Book
from .serializers import (
    BorrowSerializer,
    UserSerializer,
    BookSerializer,
    UnavailableBookSerializer,
)
from .message_broker.publisher import publish_book_creation_message


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminBookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        book = serializer.save()

        # Send a message to RabbitMQ
        data = {
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "category": book.category,
            "created_at": book.created_at.isoformat(),
        }
        publish_book_creation_message("book_created", data)


class AdminBookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_destroy(self, instance):
        data = {"id": instance.id}
        publish_book_creation_message("book_deleted", data)

        super().perform_destroy(instance)


class UserBorrowedBooksListView(generics.ListAPIView):
    queryset = Borrow.objects.select_related("user", "book")
    serializer_class = BorrowSerializer


class UnavailableBooksListView(generics.ListAPIView):
    queryset = Borrow.objects.filter(book__available=False).select_related("book")
    serializer_class = UnavailableBookSerializer
