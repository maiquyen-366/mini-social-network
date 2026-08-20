"""Tầng exception: các lỗi nghiệp vụ có mã HTTP và thông báo thống nhất."""


class AppException(Exception):
    status_code = 400
    default_message = "Đã xảy ra lỗi."

    def __init__(self, message=None, errors=None):
        self.message = message or self.default_message
        self.errors = errors or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    status_code = 404
    default_message = "Không tìm thấy dữ liệu."


class PermissionError(AppException):
    status_code = 403
    default_message = "Bạn không có quyền thực hiện thao tác này."


class BusinessValidationError(AppException):
    status_code = 400
    default_message = "Dữ liệu nghiệp vụ không hợp lệ."
