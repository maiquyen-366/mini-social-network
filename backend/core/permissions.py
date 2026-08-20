"""Tầng permission dùng chung cho controller."""

from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedUser(IsAuthenticated):
    """Tên rõ nghĩa cho permission xác thực JWT mặc định."""
