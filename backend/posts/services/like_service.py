"""Tầng Service: nghiệp vụ toggle lượt thích."""

from core.exceptions import NotFoundError
from notifications.services import NotificationService
from posts.repositories import LikeRepository, PostRepository


class LikeService:
    def __init__(self, like_repository=None, post_repository=None, notification_service=None):
        self.likes = like_repository or LikeRepository()
        self.posts = post_repository or PostRepository()
        self.notifications = notification_service or NotificationService()

    def toggle_like(self, post_id, user_id):
        post = self.posts.get_by_id(post_id)
        if not post:
            raise NotFoundError("Không tìm thấy bài đăng.")
        like = self.likes.get_by_post_user(post_id, user_id)
        if like:
            self.likes.delete(like)
            is_liked = False
            self.notifications.delete_post_like_notification(post, user_id)
        else:
            self.likes.create_like(post_id, user_id)
            is_liked = True
            self.notifications.notify_post_liked(post, user_id)

        return {
            "is_liked": is_liked,
            "likes_count": self.likes.count_by_post(post_id),
        }
