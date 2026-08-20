"""Tầng Repository: chỉ truy vấn Conversation, participant và summary."""

from django.db.models import Count, OuterRef, Q, Subquery
from django.utils import timezone

from chat.models import Conversation, Message
from core.base_repository import BaseRepository


class ConversationRepository(BaseRepository):
    model = Conversation

    def _with_summary(self, queryset, user_id):
        last_message = Message.objects.filter(conversation=OuterRef("pk")).order_by("-created_at")
        return queryset.prefetch_related("participants").annotate(
            last_message_content=Subquery(last_message.values("content")[:1]),
            last_message_at=Subquery(last_message.values("created_at")[:1]),
            last_message_sender_id=Subquery(last_message.values("sender_id")[:1]),
            last_message_read_at=Subquery(last_message.values("read_at")[:1]),
            unread_count=Count(
                "messages",
                filter=Q(messages__read_at__isnull=True) & ~Q(messages__sender_id=user_id),
                distinct=True,
            ),
        )

    def list_for_user(self, user_id):
        queryset = self.model.objects.filter(participants=user_id)
        return self._with_summary(queryset, user_id).order_by("-updated_at")

    def get_private_between(self, first_user_id, second_user_id):
        return self.model.objects.filter(participants=first_user_id).filter(participants=second_user_id).annotate(
            participant_count=Count("participants", distinct=True)
        ).filter(participant_count=2).first()

    def create_private(self, first_user, second_user):
        conversation = self.model.objects.create()
        conversation.participants.add(first_user, second_user)
        return conversation

    def get_for_response(self, conversation_id):
        return self.model.objects.prefetch_related("participants").filter(pk=conversation_id).first()

    def get_summary_for_user(self, conversation_id, user_id):
        queryset = self.model.objects.filter(pk=conversation_id, participants=user_id)
        return self._with_summary(queryset, user_id).first()

    def get_participant_ids(self, conversation_id):
        return list(self.model.objects.filter(pk=conversation_id).values_list("participants__id", flat=True))

    def is_participant(self, conversation_id, user_id):
        return self.model.objects.filter(pk=conversation_id, participants=user_id).exists()

    def touch(self, conversation_id):
        self.model.objects.filter(pk=conversation_id).update(updated_at=timezone.now())
