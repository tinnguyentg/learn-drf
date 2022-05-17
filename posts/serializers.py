from rest_framework import serializers

from .models import Post, Tag


class TagListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")
        extra_kwargs = {"slug": {"read_only": True}}


class PostSerializer(serializers.ModelSerializer):
    tags = TagListCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("title", "slug", "content", "author", "tags")
        extra_kwargs = {"content": {"write_only": True}}


class TagRetrieveSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ("slug", "name", "posts")
        extra_kwargs = {"slug": {"read_only": True}}
