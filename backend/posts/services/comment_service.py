"""Tầng Service: nghiệp vụ đọc và tạo bình luận."""

from accounts.repositories import UserRepository
from core.exceptions import NotFoundError
from notifications.services import NotificationService
from posts.repositories import CommentRepository, PostRepository


class CommentService:
    def __init__(self, comment_repository=None, post_repository=None, user_repository=None, notification_service=None):
        self.comments = comment_repository or CommentRepository()
        self.posts = post_repository or PostRepository()
        self.users = user_repository or UserRepository()
        self.notifications = notification_service or NotificationService()

    def list_comments(self, post_id):
        post = self.posts.get_by_id(post_id)
        if not post:
            raise NotFoundError("Không tìm thấy bài đăng.")
        return self.comments.list_by_post(post_id)

    def create_comment(self, post_id, user_id, content):
        post = self.posts.get_by_id(post_id)
        if not post:
            raise NotFoundError("Không tìm thấy bài đăng.")
        author = self.users.get_by_id(user_id)
        if not author:
            raise NotFoundError("Không tìm thấy người dùng.")
        comment = self.comments.create(post_id=post_id, author=author, content=content)
        self.notifications.notify_post_commented(post, user_id)
        return comment
