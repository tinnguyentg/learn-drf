from rest_framework import generics, permissions, authentication

from .serializers import UserSerializer
from .models import CustomUser


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def get_queryset(self):
        return CustomUser.objects.all().order_by("email")
