from rest_framework import serializers
from .models import User, Book, Borrow


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
    class Meta:
        model = Borrow
        fields = ["user", "return_date"]
