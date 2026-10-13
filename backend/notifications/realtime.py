"""Hạ tầng realtime: báo cho client tải lại danh sách thông báo."""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def publish_notifications_changed(user_id):
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user_id}",
            {"type": "notifications.changed"},
        )
