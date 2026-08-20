"""Tầng Service: nghiệp vụ tạo phòng, kiểm tra quyền và lưu/lấy tin nhắn."""

from accounts.repositories import UserRepository
from chat.repositories import ConversationRepository, MessageRepository
from core.exceptions import BusinessValidationError, NotFoundError, PermissionError


class ChatService:
    def __init__(self, conversation_repository=None, message_repository=None, user_repository=None):
        self.conversations = conversation_repository or ConversationRepository()
        self.messages = message_repository or MessageRepository()
        self.users = user_repository or UserRepository()

    def list_conversations(self, user_id):
        return self.conversations.list_for_user(user_id)

    def get_or_create_conversation(self, user_id, other_username):
        other_user = self.users.get_by_username(other_username)
        if not other_user:
            raise NotFoundError("Không tìm thấy người dùng muốn chat.")
        if other_user.id == user_id:
            raise BusinessValidationError("Không thể tạo cuộc trò chuyện với chính mình.")
        conversation = self.conversations.get_private_between(user_id, other_user.id)
        if conversation:
            return self.get_conversation_summary(conversation.id, user_id)
        current_user = self.users.get_by_id(user_id)
        conversation = self.conversations.create_private(current_user, other_user)
        return self.get_conversation_summary(conversation.id, user_id)

    def ensure_participant(self, conversation_id, user_id):
        conversation = self.conversations.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Không tìm thấy cuộc trò chuyện.")
        if not self.conversations.is_participant(conversation_id, user_id):
            raise PermissionError("Bạn không thuộc cuộc trò chuyện này.")
        return conversation

    def list_messages(self, conversation_id, user_id):
        self.ensure_participant(conversation_id, user_id)
        return self.messages.list_by_conversation(conversation_id)

    def save_message(self, conversation_id, user_id, content):
        conversation = self.ensure_participant(conversation_id, user_id)
        sender = self.users.get_by_id(user_id)
        message = self.messages.create_message(conversation, sender, content)
        self.conversations.touch(conversation_id)
        return message

    def mark_messages_as_read(self, conversation_id, reader_id):
        self.ensure_participant(conversation_id, reader_id)
        message_ids, read_at = self.messages.mark_unread_messages_as_read(conversation_id, reader_id)
        return {
            "conversation_id": conversation_id,
            "reader_id": reader_id,
            "message_ids": message_ids,
            "read_at": read_at,
        }

    def get_conversation_summary(self, conversation_id, user_id):
        self.ensure_participant(conversation_id, user_id)
        conversation = self.conversations.get_summary_for_user(conversation_id, user_id)
        if not conversation:
            raise NotFoundError("Không tìm thấy cuộc trò chuyện.")
        return conversation

    def get_participant_ids(self, conversation_id):
        conversation = self.conversations.get_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Không tìm thấy cuộc trò chuyện.")
        return self.conversations.get_participant_ids(conversation_id)
