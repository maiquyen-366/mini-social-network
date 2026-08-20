"""Tầng route chat HTTP: ánh xạ API conversation và lịch sử."""

from django.urls import path

from chat.controllers import ConversationListCreateController, MessageHistoryController

urlpatterns = [
    path("conversations/", ConversationListCreateController.as_view()),
    path("conversations/<int:conversation_id>/messages/", MessageHistoryController.as_view()),
]
