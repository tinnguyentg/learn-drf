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


class UserPasswordChangeSerializer(serializers.Serializer):
    current = serializers.CharField(max_length=128)
    new = serializers.CharField(max_length=128)

    def validate_current(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Wrong current password")
        return value

    def validate_new(self, value):
        password_validation.validate_password(value)
        return value
