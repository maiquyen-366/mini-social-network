"""Tầng Repository: chỉ truy vấn Comment."""

from core.base_repository import BaseRepository
from posts.models import Comment


class CommentRepository(BaseRepository):
    model = Comment

    def list_by_post(self, post_id):
        return self.model.objects.filter(post_id=post_id).select_related("author").order_by("created_at")

