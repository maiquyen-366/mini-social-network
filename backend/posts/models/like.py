"""Tầng Model/Entity: model lượt thích, mỗi User chỉ thích một lần."""

from django.conf import settings
from django.db import models


class Like(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post", "user"], name="unique_post_like")]
