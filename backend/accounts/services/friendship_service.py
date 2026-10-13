"""Tầng Service: nghiệp vụ gửi, nhận lời mời và lấy danh sách bạn bè."""

from accounts.repositories import FriendshipRepository, UserRepository
from core.exceptions import BusinessValidationError, NotFoundError, PermissionError
from notifications.services import NotificationService


class FriendshipService:
    def __init__(self, friendship_repository=None, user_repository=None, notification_service=None):
        self.friendships = friendship_repository or FriendshipRepository()
        self.users = user_repository or UserRepository()
        self.notifications = notification_service or NotificationService()

    def send_request(self, requester_id, addressee_id):
        if requester_id == addressee_id:
            raise BusinessValidationError("Không thể kết bạn với chính mình.")
        if not self.users.get_by_id(addressee_id):
            raise NotFoundError("Không tìm thấy người dùng.")

        existing = self.friendships.get_between(requester_id, addressee_id)
        if existing:
            if existing.status == "accepted":
                raise BusinessValidationError("Hai người đã là bạn bè.")
            if existing.requester_id == addressee_id:
                return self.accept_request(existing.id, requester_id)
            raise BusinessValidationError("Lời mời kết bạn đã được gửi.")

        friendship = self.friendships.create_request(requester_id, addressee_id)
        self.notifications.notify_friend_request(friendship)
        return friendship

    def accept_request(self, request_id, user_id):
        friendship = self.friendships.get_received_pending(request_id, user_id)
        if not friendship:
            raise PermissionError("Bạn không thể chấp nhận lời mời này.")
        friendship = self.friendships.accept(friendship)
        self.notifications.notify_friend_accepted(friendship)
        return friendship

    def reject_or_cancel_request(self, request_id, user_id):
        friendship = self.friendships.get_pending_for_user(request_id, user_id)
        if not friendship:
            raise NotFoundError("Không tìm thấy lời mời kết bạn.")
        recipient_id = friendship.addressee_id
        self.notifications.delete_friend_request_notification(friendship.id, recipient_id)
        self.friendships.delete(friendship)

    def list_friends(self, user_id):
        return self.friendships.list_friends(user_id)
