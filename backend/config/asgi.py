"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
Source: https://channels.readthedocs.io/en/latest/deploying.html#run-protocol-servers
"""

import os
import sys

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

# This allows easy placement of apps within the interior
# {PROJECT_NAME} directory.
app_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
sys.path.append(os.path.join(app_path, "{PROJECT_NAME}"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from {PROJECT_NAME}.ws_v1.consumer import Consumer

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/v1/", Consumer.as_asgi()),
        ])
    ),
})
