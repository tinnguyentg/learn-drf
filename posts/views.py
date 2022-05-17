from rest_framework import mixins, permissions, viewsets

from .models import Tag
from .serializers import TagListCreateSerializer, TagRetrieveSerializer


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"

    def get_queryset(self):
        return Tag.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return TagRetrieveSerializer
        return TagListCreateSerializer
