from rest_framework import generics, permissions

from .serializers import UserSignUpSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]
