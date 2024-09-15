from rest_framework import serializers
from .models import AdminBook, User


class AdminBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminBook
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "category",
            "available",
            "borrowed_until",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
