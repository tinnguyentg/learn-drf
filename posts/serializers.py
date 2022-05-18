from rest_framework import serializers

from .models import Post, Tag


class TagListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")
        extra_kwargs = {"slug": {"read_only": True}}


class PostSerializer(serializers.ModelSerializer):
    tags = TagListCreateSerializer(many=True, required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ["title", "slug", "content", "author", "tags"]
        extra_kwargs = {"content": {"write_only": True}, "slug": {"read_only": True}}

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        tags = []
        post = Post.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)

        post.tags.add(*tags)
        return post


class TagRetrieveSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ("slug", "name", "posts")
        extra_kwargs = {"slug": {"read_only": True}}
