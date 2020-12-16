"""
ASGI config for chat project.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application =  ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(apps.chat.routing.websocket_urlpatterns)
    ),
})
