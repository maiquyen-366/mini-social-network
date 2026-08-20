"""Tầng dùng chung: kiểm tra loại và kích thước ảnh upload."""

from pathlib import Path

from rest_framework import serializers


MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def validate_image_file(uploaded_file):
    """Chỉ chấp nhận ảnh đúng MIME, phần mở rộng và tối đa 5 MB."""
    extension = Path(uploaded_file.name).suffix.lower()
    content_type = (getattr(uploaded_file, "content_type", "") or "").lower()
    errors = {}
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        errors["extension"] = "Chỉ chấp nhận JPG, JPEG, PNG, WEBP hoặc GIF."
    if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        errors["content_type"] = "Định dạng MIME của ảnh không được hỗ trợ."
    if uploaded_file.size > MAX_IMAGE_SIZE:
        errors["size"] = "Ảnh không được lớn hơn 5 MB."
    if errors:
        raise serializers.ValidationError(errors)
    return uploaded_file
