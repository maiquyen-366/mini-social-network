"""Tầng Repository: chỉ truy vấn Post và các annotation thống kê."""

from django.db.models import Count, Exists, OuterRef

from core.base_repository import BaseRepository
from posts.models import Like, Post


class PostRepository(BaseRepository):
    model = Post

    def feed_queryset(self, user_id):
        liked = Like.objects.filter(post=OuterRef("pk"), user_id=user_id)
        return self.model.objects.select_related("author").annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
            is_liked=Exists(liked),
        ).order_by("-created_at")

    def get_detail(self, post_id, user_id):
        return self.feed_queryset(user_id).filter(pk=post_id).first()

    def delete_with_file(self, post):
        self.delete(post)
