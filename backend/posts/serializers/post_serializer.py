"""Tầng Serializer/DTO: validate input và format bài đăng."""

from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_avatar_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "author_username", "author_avatar_url", "content", "image_url", "likes_count", "comments_count", "is_liked", "created_at"]
        read_only_fields = ["id", "author", "created_at"]

    def get_author_avatar_url(self, obj):
        url = obj.author.avatar_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request and url.startswith("/") else url

    def get_image_url(self, obj):
        url = obj.image_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request and url.startswith("/") else url


class PostCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=5000)
    image_file = serializers.FileField(required=False, allow_null=True, write_only=True)

    def validate_image_file(self, value):
        from core.file_validation import validate_image_file

        return validate_image_file(value)
