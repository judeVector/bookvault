from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, serializers
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Book, Borrow
from .serializers import UserSerializer, BookSerializer, BorrowSerializer
from .filters import BookFilter
from .utils.publisher import publish_message_to_queue, publish_book_borrowing_message


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
        }

        publish_message_to_queue("user_created", data)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class BorrowBookView(generics.CreateAPIView):
#     queryset = Borrow.objects.all()
#     serializer_class = BorrowSerializer

#     @transaction.atomic
#     def perform_create(self, serializer):
#         book_id = self.kwargs.get("book_id")
#         book = get_object_or_404(Book, pk=book_id)

#         if book.available:
#             book.available = False
#             book.save()
#             serializer.save(book=book, user=self.request.user)
#         else:
#             raise serializers.ValidationError({"book": "Book is not available."})


# class BorrowBookView(generics.CreateAPIView):
#     queryset = Borrow.objects.all()
#     serializer_class = BorrowSerializer

#     @transaction.atomic
#     def perform_create(self, serializer):
#         book_id = self.kwargs.get("book_id")
#         book = get_object_or_404(Book, pk=book_id)

#         if book.available:
#             book.available = False
#             book.save()
#             # When Authentication is enabled
#             # borrow = serializer.save(book=book, user=self.request.user)
#             borrow = serializer.save(book=book)

#             data = {
#                 "user": borrow.user.email,
#                 "book": borrow.book.title,
#                 "borrow_date": borrow.borrow_date.isoformat(),
#                 "return_date": borrow.return_date.isoformat(),
#             }

#             publish_book_borrowing_message("book_borrowed", data)
#         else:
#             raise serializers.ValidationError({"book": "Book is not available."})


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

            borrow = serializer.save(book=book)

            data = {
                "book_id": borrow.book.id,
                "user": borrow.user.email,
                "book": borrow.book.title,
                "borrow_date": borrow.borrow_date.isoformat(),
                "return_date": borrow.return_date.isoformat(),
            }

            publish_book_borrowing_message("book_borrowed", data)
        else:
            raise serializers.ValidationError({"book": "Book is not available."})


# Only meant for Admin interface only
class CreateBookView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class DeleteBookView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
