"""Tầng Model/Entity: custom User kế thừa AbstractUser."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar_url = models.URLField(blank=True)
    avatar_public_id = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
