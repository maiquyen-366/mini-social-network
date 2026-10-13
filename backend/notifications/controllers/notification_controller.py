"""Tầng Controller: API danh sách và đánh dấu thông báo đã đọc."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.serializers import NotificationSerializer
from notifications.services import NotificationService


class NotificationListController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = NotificationService()
        items = service.list_notifications(request.user.id)
        data = NotificationSerializer(items, many=True, context={"request": request}).data
        return Response({
            "success": True,
            "data": {"items": data, "unread_count": service.count_unread(request.user.id)},
        })


class NotificationMarkReadController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = NotificationService().mark_read(notification_id, request.user.id)
        data = NotificationSerializer(notification, context={"request": request}).data
        return Response({"success": True, "data": data})


class NotificationMarkAllReadController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        NotificationService().mark_all_read(request.user.id)
        return Response({"success": True, "message": "Đã đọc tất cả thông báo."})
