"""Tầng route accounts: ánh xạ URL tới controller."""

from django.urls import path

from accounts.controllers import (
    CurrentUserController,
    FriendListController,
    FriendRequestAcceptController,
    FriendRequestCreateController,
    FriendRequestDeleteController,
    LoginController,
    LogoutController,
    RefreshController,
    RegisterController,
)

urlpatterns = [
    path("register/", RegisterController.as_view()),
    path("login/", LoginController.as_view()),
    path("refresh/", RefreshController.as_view()),
    path("logout/", LogoutController.as_view()),
    path("me/", CurrentUserController.as_view()),
    path("friends/", FriendListController.as_view()),
    path("friend-requests/", FriendRequestCreateController.as_view()),
    path("friend-requests/<int:request_id>/accept/", FriendRequestAcceptController.as_view()),
    path("friend-requests/<int:request_id>/", FriendRequestDeleteController.as_view()),
]
