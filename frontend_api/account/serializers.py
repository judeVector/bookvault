from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(maxlength=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used.")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise AuthenticationFailed("Account is disabled.")

            else:
                raise AuthenticationFailed("Invalid email or password.")
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        return attrs
