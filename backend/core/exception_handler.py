"""Tầng xử lý lỗi chung: chuyển lỗi Django/DRF/nghiệp vụ thành JSON chuẩn."""

from rest_framework.views import exception_handler

from core.exceptions import AppException


def custom_exception_handler(exc, context):
    if isinstance(exc, AppException):
        from rest_framework.response import Response
        return Response({"success": False, "message": exc.message, "errors": exc.errors}, status=exc.status_code)

    response = exception_handler(exc, context)
    if response is None:
        return None
    detail = response.data
    if isinstance(detail, dict) and "detail" in detail:
        message, errors = str(detail["detail"]), {}
    else:
        message, errors = "Dữ liệu gửi lên không hợp lệ.", detail
    response.data = {"success": False, "message": message, "errors": errors}
    return response
