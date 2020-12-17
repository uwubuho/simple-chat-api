"""
Websocket Routes for chat app
"""

from django.urls import re_path
from apps.chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/echo/$', consumers.EchoConsumer.as_asgi()),
]
