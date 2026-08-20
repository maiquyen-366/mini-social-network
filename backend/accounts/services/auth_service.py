"""Tầng Service: nghiệp vụ đăng ký, đăng nhập, refresh và logout."""

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.repositories import UserRepository
from core.exceptions import BusinessValidationError


class AuthService:
    def __init__(self, user_repository=None):
        self.users = user_repository or UserRepository()

    def register(self, username, password, email=""):
        if self.users.get_by_username(username):
            raise BusinessValidationError("Username đã tồn tại.", {"username": "Đã được sử dụng."})
        user = self.users.create_user(username=username, password=password, email=email)
        return self._token_payload(user)

    def login(self, username, password):
        user = self.users.authenticate_user(username, password)
        if not user:
            raise BusinessValidationError("Username hoặc mật khẩu không đúng.")
        return self._token_payload(user)

    def refresh_access_token(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            return {"access": str(token.access_token)}
        except Exception as exc:
            raise BusinessValidationError("Refresh token không hợp lệ.") from exc

    def _token_payload(self, user):
        refresh = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh), "user": user}
