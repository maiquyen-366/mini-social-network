"""Tầng Service: tạo, đọc và phát tín hiệu thay đổi thông báo."""

from core.exceptions import NotFoundError
from notifications.realtime import publish_notifications_changed
from notifications.repositories import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository=None):
        self.notifications = notification_repository or NotificationRepository()

    def list_notifications(self, user_id):
        return self.notifications.list_for_user(user_id)

    def count_unread(self, user_id):
        return self.notifications.count_unread(user_id)

    def mark_read(self, notification_id, user_id):
        notification = self.notifications.get_for_user(notification_id, user_id)
        if not notification:
            raise NotFoundError("Không tìm thấy thông báo.")
        notification = self.notifications.mark_read(notification)
        self._publish(user_id)
        return notification

    def mark_all_read(self, user_id):
        self.notifications.mark_all_read(user_id)
        self._publish(user_id)

    def notify_friend_request(self, friendship):
        notification = self.notifications.create(
            recipient_id=friendship.addressee_id,
            actor_id=friendship.requester_id,
            notification_type="friend_request",
            friend_request_id=friendship.id,
        )
        self._publish(friendship.addressee_id)
        return notification

    def notify_friend_accepted(self, friendship):
        notification = self.notifications.create(
            recipient_id=friendship.requester_id,
            actor_id=friendship.addressee_id,
            notification_type="friend_accepted",
            friend_request_id=friendship.id,
        )
        self._publish(friendship.requester_id)
        self._publish(friendship.addressee_id)
        return notification

    def notify_post_liked(self, post, actor_id):
        if post.author_id == actor_id:
            return None
        existing = self.notifications.get_like_notification(post.author_id, actor_id, post.id)
        if existing:
            return existing
        notification = self.notifications.create(
            recipient_id=post.author_id,
            actor_id=actor_id,
            notification_type="post_like",
            post_id=post.id,
        )
        self._publish(post.author_id)
        return notification

    def delete_post_like_notification(self, post, actor_id):
        if post.author_id == actor_id:
            return
        self.notifications.delete_like_notification(post.author_id, actor_id, post.id)
        self._publish(post.author_id)

    def notify_post_commented(self, post, actor_id):
        if post.author_id == actor_id:
            return None
        notification = self.notifications.create(
            recipient_id=post.author_id,
            actor_id=actor_id,
            notification_type="post_comment",
            post_id=post.id,
        )
        self._publish(post.author_id)
        return notification

    def delete_friend_request_notification(self, friend_request_id, recipient_id):
        self.notifications.delete_friend_request_notification(friend_request_id, recipient_id)
        self._publish(recipient_id)

    @staticmethod
    def _publish(user_id):
        publish_notifications_changed(user_id)
