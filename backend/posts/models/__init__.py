"""Tầng model posts: export Post, Comment và Like."""

from posts.models.comment import Comment
from posts.models.like import Like
from posts.models.post import Post

__all__ = ["Post", "Comment", "Like"]
