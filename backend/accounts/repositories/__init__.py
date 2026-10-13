"""Tầng repository accounts: export repository User và Friendship."""

from accounts.repositories.friendship_repository import FriendshipRepository
from accounts.repositories.user_repository import UserRepository

__all__ = ["UserRepository", "FriendshipRepository"]
