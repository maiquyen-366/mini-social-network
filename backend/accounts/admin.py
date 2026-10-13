"""Tầng admin: đăng ký User và Friendship cho Django Admin."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Friendship, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Thông tin hồ sơ", {"fields": ("avatar_url", "avatar_public_id", "bio")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Thông tin hồ sơ", {"fields": ("avatar_url", "avatar_public_id", "bio")}),)


admin.site.register(Friendship)
