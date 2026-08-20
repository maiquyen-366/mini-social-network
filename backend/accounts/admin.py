"""Tầng admin: đăng ký custom User cho Django Admin."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Thông tin hồ sơ", {"fields": ("avatar_url", "avatar_public_id", "bio")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Thông tin hồ sơ", {"fields": ("avatar_url", "avatar_public_id", "bio")}),)
