"""Tầng Controller: nhận request xác thực, gọi AuthService, trả Response."""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from accounts.serializers.auth_serializer import RefreshTokenSerializer
from accounts.services import AuthService


class RegisterController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = AuthService().register(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            email=serializer.validated_data.get("email", ""),
        )
        return Response({"success": True, "data": self._format(payload, request)}, status=201)

    @staticmethod
    def _format(payload, request):
        return {"access": payload["access"], "refresh": payload["refresh"], "user": UserSerializer(payload["user"], context={"request": request}).data}


class LoginController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = AuthService().login(**serializer.validated_data)
        return Response({"success": True, "data": RegisterController._format(payload, request)})


class RefreshController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = AuthService().refresh_access_token(**serializer.validated_data)
        return Response({"success": True, "data": data})
