"""Tầng Serializer/DTO: format danh sách conversation và validate username đối thoại."""

from rest_framework import serializers

from chat.models import Conversation
from accounts.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    last_message_content = serializers.CharField(read_only=True, allow_null=True)
    last_message_at = serializers.DateTimeField(read_only=True, allow_null=True)
    last_message_sender_id = serializers.IntegerField(read_only=True, allow_null=True)
    last_message_read_at = serializers.DateTimeField(read_only=True, allow_null=True)
    unread_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Conversation
        fields = [
            "id", "participants", "last_message_content", "last_message_at",
            "last_message_sender_id", "last_message_read_at", "unread_count", "updated_at",
        ]

    def get_participants(self, obj):
        return UserSerializer(obj.participants.all(), many=True, context=self.context).data


class ConversationCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
