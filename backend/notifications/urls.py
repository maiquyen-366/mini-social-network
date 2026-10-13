"""Tầng route notifications: ánh xạ URL tới controller."""

from django.urls import path

from notifications.controllers import (
    NotificationListController,
    NotificationMarkAllReadController,
    NotificationMarkReadController,
)

urlpatterns = [
    path("", NotificationListController.as_view()),
    path("read-all/", NotificationMarkAllReadController.as_view()),
    path("<int:notification_id>/read/", NotificationMarkReadController.as_view()),
]
