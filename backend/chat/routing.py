"""Tầng route WebSocket: ánh xạ room chat và sidebar notification."""

from django.urls import re_path

from chat.consumers import ChatConsumer, ChatNotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/sidebar/$", ChatNotificationConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<conversation_id>\d+)/$", ChatConsumer.as_asgi()),
]
