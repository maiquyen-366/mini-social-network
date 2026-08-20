"""Tầng Service: nghiệp vụ toggle lượt thích."""

from core.exceptions import NotFoundError
from posts.repositories import LikeRepository, PostRepository


class LikeService:
    def __init__(self, like_repository=None, post_repository=None):
        self.likes = like_repository or LikeRepository()
        self.posts = post_repository or PostRepository()

    def toggle_like(self, post_id, user_id):
        if not self.posts.get_by_id(post_id):
            raise NotFoundError("Không tìm thấy bài đăng.")
        like = self.likes.get_by_post_user(post_id, user_id)
        if like:
            self.likes.delete(like)
            is_liked = False
        else:
            self.likes.create_like(post_id, user_id)
            is_liked = True

        return {
            "is_liked": is_liked,
            "likes_count": self.likes.count_by_post(post_id),
        }
