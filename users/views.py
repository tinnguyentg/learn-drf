from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import (
    UserSignUpSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer,
)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeView(generics.CreateAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new"])
        user.save()
        return Response({"msg": "Successfully"}, status=status.HTTP_200_OK)
