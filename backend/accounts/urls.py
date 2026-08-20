"""Tầng route accounts: ánh xạ URL tới controller."""

from django.urls import path

from accounts.controllers import CurrentUserController, LoginController, LogoutController, RefreshController, RegisterController

urlpatterns = [
    path("register/", RegisterController.as_view()),
    path("login/", LoginController.as_view()),
    path("refresh/", RefreshController.as_view()),
    path("logout/", LogoutController.as_view()),
    path("me/", CurrentUserController.as_view()),
]
