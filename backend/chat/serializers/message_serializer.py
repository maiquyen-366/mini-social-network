"""Tầng Serializer/DTO: validate và format tin nhắn."""

from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.IntegerField(source="conversation_id", read_only=True)
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    sender_avatar_url = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id", "conversation", "sender", "sender_username", "sender_avatar_url",
            "content", "created_at", "read_at", "is_read",
        ]
        read_only_fields = ["id", "conversation", "sender", "created_at", "read_at", "is_read"]

    def get_sender_avatar_url(self, obj):
        url = obj.sender.avatar_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request and url.startswith("/") else url

    def get_is_read(self, obj):
        return obj.read_at is not None


class MessageCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2000, allow_blank=False)


class MessageReadReceiptSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()
    reader_id = serializers.IntegerField()
    message_ids = serializers.ListField(child=serializers.IntegerField())
    read_at = serializers.DateTimeField(allow_null=True)
