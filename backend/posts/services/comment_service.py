"""Tầng Service: nghiệp vụ đọc và tạo bình luận."""

from accounts.repositories import UserRepository
from core.exceptions import NotFoundError
from posts.repositories import CommentRepository, PostRepository


class CommentService:
    def __init__(self, comment_repository=None, post_repository=None, user_repository=None):
        self.comments = comment_repository or CommentRepository()
        self.posts = post_repository or PostRepository()
        self.users = user_repository or UserRepository()

    def list_comments(self, post_id):
        if not self.posts.get_by_id(post_id):
            raise NotFoundError("Không tìm thấy bài đăng.")
        return self.comments.list_by_post(post_id)

    def create_comment(self, post_id, user_id, content):
        if not self.posts.get_by_id(post_id):
            raise NotFoundError("Không tìm thấy bài đăng.")
        author = self.users.get_by_id(user_id)
        if not author:
            raise NotFoundError("Không tìm thấy người dùng.")
        return self.comments.create(post_id=post_id, author=author, content=content)
