"""
ASGI config for railway project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from Trainstation import consumers
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway.settings')

application = get_asgi_application()


ws_pattern = [
    path('ws/platform/<id>',consumers.PlatformUpdate.as_asgi()),
    path('ws/arrival/<id>',consumers.ArrivalUpdate.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket":AuthMiddlewareStack(URLRouter(ws_pattern))
})
