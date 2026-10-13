"""Kiểm thử tích hợp nhỏ: kết bạn, quyền chat và thông báo tương tác bài viết."""

from django.test import TestCase

from accounts.models import User
from accounts.services import FriendshipService
from chat.services import ChatService
from core.exceptions import PermissionError
from notifications.models import Notification
from posts.models import Post
from posts.services import CommentService, LikeService


class FriendshipNotificationFlowTests(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user(username="first", password="TestPass123!")
        self.second_user = User.objects.create_user(username="second", password="TestPass123!")

    def test_only_friends_can_chat(self):
        with self.assertRaises(PermissionError):
            ChatService().get_or_create_conversation(self.first_user.id, self.second_user.username)

        friendship = FriendshipService().send_request(self.first_user.id, self.second_user.id)
        self.assertEqual(friendship.status, "pending")
        self.assertTrue(Notification.objects.filter(
            recipient=self.second_user,
            notification_type="friend_request",
        ).exists())

        FriendshipService().accept_request(friendship.id, self.second_user.id)
        conversation = ChatService().get_or_create_conversation(
            self.first_user.id,
            self.second_user.username,
        )
        self.assertEqual(conversation.participants.count(), 2)

    def test_like_and_comment_create_notifications(self):
        post = Post.objects.create(author=self.first_user, content="Bài viết kiểm thử")

        LikeService().toggle_like(post.id, self.second_user.id)
        CommentService().create_comment(post.id, self.second_user.id, "Bình luận kiểm thử")

        notification_types = set(Notification.objects.filter(
            recipient=self.first_user,
            actor=self.second_user,
        ).values_list("notification_type", flat=True))
        self.assertEqual(notification_types, {"post_like", "post_comment"})

        LikeService().toggle_like(post.id, self.second_user.id)
        self.assertFalse(Notification.objects.filter(
            recipient=self.first_user,
            actor=self.second_user,
            notification_type="post_like",
        ).exists())
