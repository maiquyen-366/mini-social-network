"""Tầng repository posts: export các repository ORM."""

from posts.repositories.comment_repository import CommentRepository
from posts.repositories.like_repository import LikeRepository
from posts.repositories.post_repository import PostRepository

__all__ = ["PostRepository", "CommentRepository", "LikeRepository"]
