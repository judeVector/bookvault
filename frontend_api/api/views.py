from rest_framework import generics, serializers

from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowBookView(generics.CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.available:
            book.available = False
            book.save()
            serializer.save()
        else:
            raise serializers.ValidationError("Book is not available.")
