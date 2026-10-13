"""Tầng admin: đăng ký Notification để hỗ trợ kiểm tra dữ liệu."""

from django.contrib import admin

from notifications.models import Notification

admin.site.register(Notification)
