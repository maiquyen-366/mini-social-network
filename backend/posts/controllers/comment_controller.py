"""Tầng Controller: điều phối API bình luận."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import CommentCreateSerializer, CommentSerializer
from posts.services import CommentService


class CommentListCreateController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        comments = CommentService().list_comments(post_id)
        return Response({"success": True, "data": CommentSerializer(comments, many=True, context={"request": request}).data})

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = CommentService().create_comment(post_id, request.user.id, serializer.validated_data["content"])
        return Response({"success": True, "data": CommentSerializer(comment, context={"request": request}).data}, status=201)
