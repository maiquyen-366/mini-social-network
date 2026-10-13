"""Tầng Serializer/DTO: validate và format quan hệ bạn bè."""

from rest_framework import serializers

from accounts.models import Friendship
from accounts.serializers.user_serializer import UserSerializer


class FriendRequestCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class FriendshipSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    addressee = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ["id", "requester", "addressee", "status", "created_at", "updated_at"]
        read_only_fields = fields
