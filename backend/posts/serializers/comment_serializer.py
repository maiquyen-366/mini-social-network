"""Tầng Serializer/DTO: validate và format bình luận."""

from rest_framework import serializers

from posts.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField(source="post_id", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "author_avatar_url", "content", "created_at"]
        read_only_fields = ["id", "post", "author", "created_at"]

    def get_author_avatar_url(self, obj):
        url = obj.author.avatar_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request and url.startswith("/") else url


class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)
