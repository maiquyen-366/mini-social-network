"""Tầng Controller: điều phối API toggle like."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.services import LikeService


class LikeToggleController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        result = LikeService().toggle_like(post_id, request.user.id)
        return Response({"success": True, "data": result})
