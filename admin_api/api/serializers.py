from rest_framework import serializers
from .models import Borrow, User, Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "created_at"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "category",
            "available",
            "created_at",
        ]


class BorrowSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrow
        fields = ["user_email", "book_title", "borrow_date", "return_date"]


class UnavailableBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrow
        fields = ["book_title", "return_date"]
