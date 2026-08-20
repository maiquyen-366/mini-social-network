"""Tầng Model/Entity: cuộc trò chuyện riêng giữa hai người dùng."""

from django.conf import settings
from django.db import models


class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
