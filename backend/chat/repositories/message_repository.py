"""Tầng Repository: chỉ truy vấn và lưu Message."""

from django.db import transaction
from django.utils import timezone

from chat.models import Message
from core.base_repository import BaseRepository


class MessageRepository(BaseRepository):
    model = Message

    def list_by_conversation(self, conversation_id):
        return self.model.objects.filter(conversation_id=conversation_id).select_related("sender").order_by("created_at")

    def create_message(self, conversation, sender, content):
        return self.model.objects.create(conversation=conversation, sender=sender, content=content)

    def get_unread_message_ids(self, conversation_id, reader_id):
        return list(self.model.objects.filter(
            conversation_id=conversation_id,
            read_at__isnull=True,
        ).exclude(sender_id=reader_id).values_list("id", flat=True))

    def mark_unread_messages_as_read(self, conversation_id, reader_id):
        with transaction.atomic():
            unread_messages = self.model.objects.select_for_update().filter(
                conversation_id=conversation_id,
                read_at__isnull=True,
            ).exclude(sender_id=reader_id)
            message_ids = list(unread_messages.values_list("id", flat=True))
            if not message_ids:
                return [], None

            read_at = timezone.now()
            self.model.objects.filter(id__in=message_ids, read_at__isnull=True).update(read_at=read_at)
            return message_ids, read_at

    def count_unread_for_user(self, conversation_id, user_id):
        return self.model.objects.filter(
            conversation_id=conversation_id,
            read_at__isnull=True,
        ).exclude(sender_id=user_id).count()
