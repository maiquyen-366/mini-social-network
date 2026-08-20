"""Tầng Repository: chỉ thực hiện truy vấn ORM liên quan User."""

from accounts.models import User
from core.base_repository import BaseRepository
from django.contrib.auth import authenticate


class UserRepository(BaseRepository):
    model = User

    def get_by_username(self, username):
        return self.model.objects.filter(username=username).first()

    def get_by_email(self, email):
        return self.model.objects.filter(email=email).first()

    def create_user(self, username, password, email=""):
        user = self.model(username=username, email=email or "")
        user.set_password(password)
        user.save()
        return user

    def authenticate_user(self, username, password):
        return authenticate(username=username, password=password)

    def update_profile(self, user, data):
        update_data = dict(data)
        update_data.pop("avatar_file", None)
        remove_avatar = update_data.pop("remove_avatar", False)
        update_fields = list(update_data.keys())
        for field, value in update_data.items():
            setattr(user, field, value)
        if remove_avatar:
            user.avatar_url = ""
            user.avatar_public_id = ""
            update_fields.extend(["avatar_url", "avatar_public_id"])
        if update_fields:
            user.save(update_fields=list(dict.fromkeys(update_fields)))
        return user
