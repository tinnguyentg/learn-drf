from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from posts.permissions import IsAuthorOrReadOnly

from .models import Post, Tag
from .serializers import (
    PostReadSerializer,
    PostSerializer,
    TagListCreateSerializer,
    TagRetrieveSerializer,
)


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "posts__title"]
    # ordering_fields = ['name']
    filterset_fields = ["name"]

    def get_queryset(self):
        return Tag.objects.filter(~Q(posts=None)).order_by("name")

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return TagRetrieveSerializer
        return TagListCreateSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    lookup_field = "slug"
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return PostReadSerializer
        return super().get_serializer_class()
