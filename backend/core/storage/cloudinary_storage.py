"""Tầng storage: chỉ cấu hình và gọi Cloudinary upload/delete, không truy vấn ORM."""

import cloudinary
from cloudinary import uploader
from django.conf import settings

from core.exceptions import AppException


class StorageError(AppException):
    status_code = 503
    default_message = "Storage ảnh hiện không khả dụng."


class CloudinaryStorage:
    def _configure(self):
        values = {
            "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "api_key": settings.CLOUDINARY_API_KEY,
            "api_secret": settings.CLOUDINARY_API_SECRET,
        }
        missing = [key for key, value in values.items() if not value]
        if missing:
            raise StorageError("Chưa cấu hình Cloudinary trong backend/.env.", {"missing": missing})
        cloudinary.config(**values, secure=True)

    def upload(self, uploaded_file, folder):
        self._configure()
        try:
            result = uploader.upload(
                uploaded_file,
                folder=folder,
                resource_type="image",
                use_filename=False,
                unique_filename=True,
                overwrite=False,
            )
            return {"secure_url": result["secure_url"], "public_id": result["public_id"]}
        except Exception as exc:
            raise StorageError("Không thể upload ảnh lên Cloudinary.") from exc

    def delete(self, public_id):
        if not public_id:
            return
        self._configure()
        try:
            uploader.destroy(public_id, resource_type="image", invalidate=True)
        except Exception as exc:
            raise StorageError("Không thể xóa ảnh cũ trên Cloudinary.") from exc
