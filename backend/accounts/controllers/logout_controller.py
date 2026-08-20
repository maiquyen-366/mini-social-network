"""Tầng Controller: endpoint logout stateless cho JWT."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"success": True, "message": "Đã đăng xuất. Hãy xóa token phía client."})
