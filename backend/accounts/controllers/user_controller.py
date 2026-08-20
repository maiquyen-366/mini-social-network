"""Tầng Controller: API hồ sơ hiện tại, chỉ điều phối serializer và UserService."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import ProfileUpdateSerializer, UserSerializer
from accounts.services import UserService


class CurrentUserController(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        user = UserService().get_profile(request.user.id)
        return Response({"success": True, "data": UserSerializer(user, context={"request": request}).data})

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = UserService().update_profile(request.user.id, serializer.validated_data)
        return Response({"success": True, "data": UserSerializer(user, context={"request": request}).data})

    def post(self, request):
        return self.patch(request)
