"""Tầng Controller: API lời mời và danh sách bạn bè."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import FriendRequestCreateSerializer, FriendshipSerializer, UserSerializer
from accounts.services import FriendshipService


class FriendListController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = FriendshipService().list_friends(request.user.id)
        data = UserSerializer(friends, many=True, context={"request": request}).data
        return Response({"success": True, "data": data})


class FriendRequestCreateController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        friendship = FriendshipService().send_request(
            request.user.id,
            serializer.validated_data["user_id"],
        )
        data = FriendshipSerializer(friendship, context={"request": request}).data
        return Response({"success": True, "data": data}, status=201)


class FriendRequestAcceptController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        friendship = FriendshipService().accept_request(request_id, request.user.id)
        data = FriendshipSerializer(friendship, context={"request": request}).data
        return Response({"success": True, "data": data})


class FriendRequestDeleteController(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, request_id):
        FriendshipService().reject_or_cancel_request(request_id, request.user.id)
        return Response({"success": True, "message": "Đã xóa lời mời kết bạn."})
