from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import CustomUser


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128)