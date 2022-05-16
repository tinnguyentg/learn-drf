from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response

from .serializers import UserSignUpSerializer, UserLoginSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if not user:
            raise serializers.ValidationError("Incorrect email/password")
        return Response(UserSignUpSerializer(user).data, status=status.HTTP_200_OK)