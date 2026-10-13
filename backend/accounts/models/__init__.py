"""Tầng model accounts: export User và Friendship để import gọn."""

from accounts.models.friendship import Friendship
from accounts.models.user import User

__all__ = ["User", "Friendship"]
