from django.contrib.auth import password_validation, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

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
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        token, created = Token.objects.get_or_create(user=user)
        attrs["token"] = token
        return attrs


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
