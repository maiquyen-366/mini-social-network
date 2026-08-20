"""Tầng WebSocket Controller: điều phối room/sidebar realtime qua ChatService."""

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.serializers import (
    ConversationSerializer,
    MessageCreateSerializer,
    MessageReadReceiptSerializer,
    MessageSerializer,
)
from chat.services import ChatService
from core.exceptions import AppException


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.conversation_id = int(self.scope["url_route"]["kwargs"]["conversation_id"])
        self.group_name = f"chat_{self.conversation_id}"
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.user_id = user.id
        try:
            await self._ensure_participant()
        except AppException:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        receipt = await self._mark_messages_as_read()
        if receipt:
            await self._broadcast_read_receipt(receipt)
            await self._notify_sidebar_users()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        serializer = MessageCreateSerializer(data=content)
        if not serializer.is_valid():
            await self.send_json({"type": "error", "errors": serializer.errors})
            return

        try:
            message = await self._save_message(serializer.validated_data["content"])
        except AppException as exc:
            await self.send_json({"type": "error", "message": exc.message, "errors": exc.errors})
            return

        await self.channel_layer.group_send(self.group_name, {
            "type": "chat.message_created",
            "data": message,
            "sender_id": self.user_id,
        })
        await self._notify_sidebar_users()

    async def chat_message_created(self, event):
        await self.send_json({"type": "message.created", "data": event["data"]})
        if event["sender_id"] == self.user_id:
            return

        receipt = await self._mark_messages_as_read()
        if receipt:
            await self._broadcast_read_receipt(receipt)
            await self._notify_sidebar_users()

    async def chat_messages_read(self, event):
        await self.send_json({"type": "messages.read", "data": event["data"]})

    async def _broadcast_read_receipt(self, receipt):
        await self.channel_layer.group_send(self.group_name, {
            "type": "chat.messages_read",
            "data": receipt,
        })

    async def _notify_sidebar_users(self):
        updates = await self._get_sidebar_updates()
        for update in updates:
            await self.channel_layer.group_send(f"chat_user_{update['user_id']}", {
                "type": "sidebar.conversation_updated",
                "data": update["data"],
            })

    @database_sync_to_async
    def _ensure_participant(self):
        return ChatService().ensure_participant(self.conversation_id, self.user_id)

    @database_sync_to_async
    def _save_message(self, content):
        message = ChatService().save_message(self.conversation_id, self.user_id, content)
        return dict(MessageSerializer(message).data)

    @database_sync_to_async
    def _mark_messages_as_read(self):
        receipt = ChatService().mark_messages_as_read(self.conversation_id, self.user_id)
        if not receipt["message_ids"]:
            return None
        return dict(MessageReadReceiptSerializer(receipt).data)

    @database_sync_to_async
    def _get_sidebar_updates(self):
        service = ChatService()
        updates = []
        for participant_id in service.get_participant_ids(self.conversation_id):
            summary = service.get_conversation_summary(self.conversation_id, participant_id)
            updates.append({
                "user_id": participant_id,
                "data": dict(ConversationSerializer(summary).data),
            })
        return updates


class ChatNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.user_group_name = f"chat_user_{user.id}"
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def sidebar_conversation_updated(self, event):
        await self.send_json({"type": "conversation.updated", "data": event["data"]})
