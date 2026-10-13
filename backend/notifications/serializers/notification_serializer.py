"""Tầng Serializer/DTO: format thông báo cho navbar."""

from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    actor_avatar_url = serializers.SerializerMethodField()
    post_id = serializers.IntegerField(read_only=True, allow_null=True)
    friend_request_id = serializers.IntegerField(read_only=True, allow_null=True)
    friend_request_status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id", "notification_type", "actor", "actor_username", "actor_avatar_url",
            "post_id", "friend_request_id", "friend_request_status", "message", "is_read", "created_at",
        ]

    def get_actor_avatar_url(self, obj):
        url = obj.actor.avatar_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request and url.startswith("/") else url

    def get_friend_request_status(self, obj):
        return obj.friend_request.status if obj.friend_request_id else None

    def get_message(self, obj):
        messages = {
            Notification.TYPE_FRIEND_REQUEST: f"{obj.actor.username} đã gửi lời mời kết bạn.",
            Notification.TYPE_FRIEND_ACCEPTED: f"{obj.actor.username} đã chấp nhận lời mời kết bạn.",
            Notification.TYPE_POST_LIKE: f"{obj.actor.username} đã thích bài viết của bạn.",
            Notification.TYPE_POST_COMMENT: f"{obj.actor.username} đã bình luận bài viết của bạn.",
        }
        return messages.get(obj.notification_type, "Bạn có thông báo mới.")
