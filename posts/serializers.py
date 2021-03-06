from rest_framework import serializers

from .models import Post, Tag


class TagListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")


class TagListCreateWithNoValidatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")
        extra_kwargs = {"name": {"validators": []}}


class PostSerializer(serializers.ModelSerializer):
    tags = TagListCreateWithNoValidatorSerializer(many=True, required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ["title", "slug", "content", "author", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        tags = []
        post = Post.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)

        post.tags.add(*tags)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        tags = []
        post = super().update(instance, validated_data)
        post.tags.clear()

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)

        post.tags.add(*tags)
        return post


class PostReadSerializer(serializers.ModelSerializer):
    tags = TagListCreateWithNoValidatorSerializer(many=True, read_only=True)
    author = serializers.CharField(source="author.id")

    class Meta:
        model = Post
        fields = ["title", "slug", "content", "author", "tags"]


class TagRetrieveSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ("slug", "name", "posts")
