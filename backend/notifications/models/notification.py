"""Tầng Model/Entity: thông báo kết bạn, thích và bình luận."""

from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_FRIEND_REQUEST = "friend_request"
    TYPE_FRIEND_ACCEPTED = "friend_accepted"
    TYPE_POST_LIKE = "post_like"
    TYPE_POST_COMMENT = "post_comment"
    TYPE_CHOICES = [
        (TYPE_FRIEND_REQUEST, "Lời mời kết bạn"),
        (TYPE_FRIEND_ACCEPTED, "Chấp nhận kết bạn"),
        (TYPE_POST_LIKE, "Thích bài viết"),
        (TYPE_POST_COMMENT, "Bình luận bài viết"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="triggered_notifications",
    )
    notification_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    friend_request = models.ForeignKey(
        "accounts.Friendship",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read", "-created_at"])]

    def __str__(self):
        return f"{self.notification_type}: {self.actor} -> {self.recipient}"
