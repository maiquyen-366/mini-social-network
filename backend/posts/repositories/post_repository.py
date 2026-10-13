"""Tầng Repository: chỉ truy vấn Post và các annotation thống kê."""

from django.db.models import Count, Exists, OuterRef, Q, Subquery

from accounts.models import Friendship
from core.base_repository import BaseRepository
from posts.models import Like, Post


class PostRepository(BaseRepository):
    model = Post

    def feed_queryset(self, user_id):
        liked = Like.objects.filter(post=OuterRef("pk"), user_id=user_id)
        friendship = Friendship.objects.filter(
            Q(requester_id=user_id, addressee_id=OuterRef("author_id"))
            | Q(requester_id=OuterRef("author_id"), addressee_id=user_id)
        ).order_by("-created_at")
        return self.model.objects.select_related("author").annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
            is_liked=Exists(liked),
            friendship_status=Subquery(friendship.values("status")[:1]),
            friendship_request_id=Subquery(friendship.values("id")[:1]),
            friendship_requester_id=Subquery(friendship.values("requester_id")[:1]),
        ).order_by("-created_at")

    def get_detail(self, post_id, user_id):
        return self.feed_queryset(user_id).filter(pk=post_id).first()

    def delete_with_file(self, post):
        self.delete(post)
