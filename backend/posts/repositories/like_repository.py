"""Tầng Repository: chỉ truy vấn Like."""

from core.base_repository import BaseRepository
from posts.models import Like


class LikeRepository(BaseRepository):
    model = Like

    def get_by_post_user(self, post_id, user_id):
        return self.model.objects.filter(post_id=post_id, user_id=user_id).first()

    def create_like(self, post_id, user_id):
        return self.model.objects.create(post_id=post_id, user_id=user_id)

    def count_by_post(self, post_id):
        return self.model.objects.filter(post_id=post_id).count()
