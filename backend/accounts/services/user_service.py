"""Tầng Service: nghiệp vụ xem và cập nhật hồ sơ người dùng."""

from accounts.repositories import UserRepository
from core.exceptions import BusinessValidationError, NotFoundError
from core.storage import CloudinaryStorage


class UserService:
    def __init__(self, user_repository=None, storage=None):
        self.users = user_repository or UserRepository()
        self.storage = storage or CloudinaryStorage()

    def get_profile(self, user_id):
        user = self.users.get_by_id(user_id)
        if not user:
            raise NotFoundError("Không tìm thấy người dùng.")
        return user

    def update_profile(self, user_id, data):
        user = self.get_profile(user_id)
        update_data = dict(data)
        avatar_file = update_data.pop("avatar_file", None)
        remove_avatar = update_data.get("remove_avatar", False)
        if avatar_file and remove_avatar:
            raise BusinessValidationError("Chỉ chọn đổi ảnh hoặc xóa ảnh tại một thời điểm.")

        old_public_id = user.avatar_public_id
        uploaded = None
        if avatar_file:
            uploaded = self.storage.upload(avatar_file, "mini_social/avatars")
            update_data["avatar_url"] = uploaded["secure_url"]
            update_data["avatar_public_id"] = uploaded["public_id"]

        try:
            updated_user = self.users.update_profile(user, update_data)
        except Exception:
            if uploaded:
                self._try_delete(uploaded["public_id"])
            raise

        new_public_id = updated_user.avatar_public_id
        if (avatar_file or remove_avatar) and old_public_id and old_public_id != new_public_id:
            self._try_delete(old_public_id)
        return updated_user

    def _try_delete(self, public_id):
        try:
            self.storage.delete(public_id)
        except Exception:
            pass
