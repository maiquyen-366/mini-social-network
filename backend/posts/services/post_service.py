"""Tầng Service: nghiệp vụ tạo, đọc và xóa bài của chính chủ."""

from accounts.repositories import UserRepository
from core.exceptions import NotFoundError, PermissionError
from core.storage import CloudinaryStorage
from posts.repositories import PostRepository


class PostService:
    def __init__(self, post_repository=None, user_repository=None, storage=None):
        self.posts = post_repository or PostRepository()
        self.users = user_repository or UserRepository()
        self.storage = storage or CloudinaryStorage()

    def list_feed(self, user_id):
        return self.posts.feed_queryset(user_id)

    def get_post(self, post_id, user_id):
        post = self.posts.get_detail(post_id, user_id)
        if not post:
            raise NotFoundError("Không tìm thấy bài đăng.")
        return post

    def create_post(self, user_id, data):
        author = self.users.get_by_id(user_id)
        if not author:
            raise NotFoundError("Không tìm thấy người dùng.")
        create_data = dict(data)
        image_file = create_data.pop("image_file", None)
        uploaded = None
        if image_file:
            uploaded = self.storage.upload(image_file, "mini_social/posts")
            create_data["image_url"] = uploaded["secure_url"]
            create_data["image_public_id"] = uploaded["public_id"]
        try:
            return self.posts.create(author=author, **create_data)
        except Exception:
            if uploaded:
                self._try_delete(uploaded["public_id"])
            raise

    def delete_post(self, post_id, user_id):
        post = self.get_post(post_id, user_id)
        if post.author_id != user_id:
            raise PermissionError("Bạn chỉ được xóa bài của mình.")
        public_id = post.image_public_id
        self.posts.delete_with_file(post)
        if public_id:
            self._try_delete(public_id)

    def _try_delete(self, public_id):
        try:
            self.storage.delete(public_id)
        except Exception:
            pass
