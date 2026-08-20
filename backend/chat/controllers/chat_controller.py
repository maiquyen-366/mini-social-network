"""Tầng Controller: điều phối HTTP API chat qua serializer và ChatService."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.serializers import ConversationCreateSerializer, ConversationSerializer, MessageSerializer
from chat.services import ChatService


class ConversationListCreateController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ConversationSerializer(ChatService().list_conversations(request.user.id), many=True, context={"request": request}).data
        return Response({"success": True, "data": data})

    def post(self, request):
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = ChatService().get_or_create_conversation(request.user.id, serializer.validated_data["username"])
        return Response({"success": True, "data": ConversationSerializer(conversation, context={"request": request}).data}, status=201)


class MessageHistoryController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        messages = ChatService().list_messages(conversation_id, request.user.id)
        return Response({"success": True, "data": MessageSerializer(messages, many=True, context={"request": request}).data})
