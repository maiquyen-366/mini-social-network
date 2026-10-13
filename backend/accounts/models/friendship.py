"""Tầng Model/Entity: lời mời và quan hệ bạn bè giữa hai User."""

from django.conf import settings
from django.db import models


class Friendship(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Đang chờ"),
        (STATUS_ACCEPTED, "Bạn bè"),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
    )
    addressee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["requester", "addressee"], name="unique_directed_friendship"),
            models.CheckConstraint(
                condition=~models.Q(requester=models.F("addressee")),
                name="friendship_users_must_differ",
            ),
        ]
        indexes = [
            models.Index(fields=["requester", "status"]),
            models.Index(fields=["addressee", "status"]),
        ]

    def __str__(self):
        return f"{self.requester} -> {self.addressee} ({self.status})"
