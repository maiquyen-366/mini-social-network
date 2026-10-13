"""Tầng Repository: chỉ truy vấn lời mời và quan hệ bạn bè."""

from django.db.models import Q

from accounts.models import Friendship, User
from core.base_repository import BaseRepository


class FriendshipRepository(BaseRepository):
    model = Friendship

    def get_between(self, first_user_id, second_user_id):
        return self.model.objects.select_related("requester", "addressee").filter(
            Q(requester_id=first_user_id, addressee_id=second_user_id)
            | Q(requester_id=second_user_id, addressee_id=first_user_id)
        ).first()

    def create_request(self, requester_id, addressee_id):
        friendship = self.model.objects.create(requester_id=requester_id, addressee_id=addressee_id)
        return self.model.objects.select_related("requester", "addressee").get(pk=friendship.id)

    def get_received_pending(self, request_id, addressee_id):
        return self.model.objects.select_related("requester", "addressee").filter(
            pk=request_id,
            addressee_id=addressee_id,
            status=Friendship.STATUS_PENDING,
        ).first()

    def get_pending_for_user(self, request_id, user_id):
        return self.model.objects.select_related("requester", "addressee").filter(
            Q(requester_id=user_id) | Q(addressee_id=user_id),
            pk=request_id,
            status=Friendship.STATUS_PENDING,
        ).first()

    def accept(self, friendship):
        friendship.status = Friendship.STATUS_ACCEPTED
        friendship.save(update_fields=["status", "updated_at"])
        return friendship

    def are_friends(self, first_user_id, second_user_id):
        return self.model.objects.filter(
            Q(requester_id=first_user_id, addressee_id=second_user_id)
            | Q(requester_id=second_user_id, addressee_id=first_user_id),
            status=Friendship.STATUS_ACCEPTED,
        ).exists()

    def list_friends(self, user_id):
        relationships = self.model.objects.filter(
            Q(requester_id=user_id) | Q(addressee_id=user_id),
            status=Friendship.STATUS_ACCEPTED,
        ).values_list("requester_id", "addressee_id")
        friend_ids = [second_id if first_id == user_id else first_id for first_id, second_id in relationships]
        return User.objects.filter(id__in=friend_ids).order_by("username")

    def get_friend_ids(self, user_id):
        return list(self.list_friends(user_id).values_list("id", flat=True))
