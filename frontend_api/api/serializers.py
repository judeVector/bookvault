from rest_framework import serializers
from .models import Book, Borrow


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "publisher", "category", "available"]


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ["id", "user", "book", "borrow_date", "return_date"]
