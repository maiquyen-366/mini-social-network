"""Tầng Repository: chỉ truy vấn và cập nhật Notification."""

from notifications.models import Notification
from core.base_repository import BaseRepository


class NotificationRepository(BaseRepository):
    model = Notification

    def list_for_user(self, user_id, limit=30):
        return self.model.objects.filter(recipient_id=user_id).select_related(
            "actor", "post", "friend_request",
        ).order_by("-created_at")[:limit]

    def count_unread(self, user_id):
        return self.model.objects.filter(recipient_id=user_id, is_read=False).count()

    def get_for_user(self, notification_id, user_id):
        return self.model.objects.filter(pk=notification_id, recipient_id=user_id).first()

    def mark_read(self, notification):
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return notification

    def mark_all_read(self, user_id):
        return self.model.objects.filter(recipient_id=user_id, is_read=False).update(is_read=True)

    def get_like_notification(self, recipient_id, actor_id, post_id):
        return self.model.objects.filter(
            recipient_id=recipient_id,
            actor_id=actor_id,
            post_id=post_id,
            notification_type=Notification.TYPE_POST_LIKE,
        ).first()

    def delete_like_notification(self, recipient_id, actor_id, post_id):
        self.model.objects.filter(
            recipient_id=recipient_id,
            actor_id=actor_id,
            post_id=post_id,
            notification_type=Notification.TYPE_POST_LIKE,
        ).delete()

    def delete_friend_request_notification(self, friend_request_id, recipient_id):
        self.model.objects.filter(
            friend_request_id=friend_request_id,
            recipient_id=recipient_id,
            notification_type=Notification.TYPE_FRIEND_REQUEST,
        ).delete()
