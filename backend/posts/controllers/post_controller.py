"""Tầng Controller: điều phối API bài đăng, không chứa ORM/nghiệp vụ."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import SimplePagePagination
from posts.serializers import PostCreateSerializer, PostSerializer
from posts.services import PostService


class PostListCreateController(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        queryset = PostService().list_feed(request.user.id)
        paginator = SimplePagePagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        return paginator.get_paginated_response(PostSerializer(page, many=True, context={"request": request}).data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PostService()
        post = service.create_post(request.user.id, serializer.validated_data)
        post = service.get_post(post.id, request.user.id)
        return Response({"success": True, "data": PostSerializer(post, context={"request": request}).data}, status=201)


class PostDetailController(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, post_id):
        post = PostService().get_post(post_id, request.user.id)
        return Response({"success": True, "data": PostSerializer(post, context={"request": request}).data})

    def delete(self, request, post_id):
        PostService().delete_post(post_id, request.user.id)
        return Response({"success": True, "message": "Đã xóa bài đăng."})
