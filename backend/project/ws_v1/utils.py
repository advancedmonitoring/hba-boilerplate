import logging
from typing import Optional

import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import get_user_model

from {PROJECT_NAME}.users.signals.custom_signals import user_online_status_changed
from {PROJECT_NAME}.utils.process_recognizer import ProcessRecognizer

logger = logging.getLogger(__name__)

USER_GROUP_MASK = "user_%s"
GLOBAL_GROUP_MASK = "all"

CHANNEL_LAYER = get_channel_layer()

User = get_user_model()


def get_user_ws_group_name(user_id: int) -> str:
    return USER_GROUP_MASK % user_id


def get_global_ws_group_name() -> str:
    return GLOBAL_GROUP_MASK


def send_to_socket_group(group_name: str, event: str, **data) -> None:
    async_to_sync(CHANNEL_LAYER.group_send)(
        group_name,
        {
            "type": event,
            "data": data,
        },
    )


class Connections:
    __connections: Optional[redis.Redis] = None
    __initialized: bool = False

    @classmethod
    def init(cls):
        redis_url: Optional[str] = getattr(settings, "REDIS_URL", None)
        if redis_url is None:
            return

        cls.__connections = redis.from_url(settings.REDIS_URL)
        cls.__initialized = True

        if ProcessRecognizer.is_server():
            for old_connection in cls.__connections.scan_iter("ws_conn:*"):
                cls.__connections.delete(old_connection)

    @classmethod
    def user_connected(cls, user: User, channel_name: str):
        if not cls.__initialized:
            return

        user_come_online = not cls.is_user_connected(user.id)
        cls.__connections.sadd(f"ws_conn:{user.id}", channel_name)

        if user_come_online:
            cls.send_status_changed(user=user, online=True)

    @classmethod
    def user_disconnected(cls, user: User, channel_name):
        if not cls.__initialized:
            return

        cls.__connections.srem(f"ws_conn:{user.id}", channel_name)

        if not cls.is_user_connected(user.id):
            cls.send_status_changed(user=user, online=False)

    @classmethod
    def get_user_connections(cls, user_id) -> set:
        if not cls.__initialized:
            return set()

        user_connections = cls.__connections.smembers(f"ws_conn:{user_id}")
        return user_connections

    @classmethod
    def is_user_connected(cls, user_id) -> bool:
        if not cls.__initialized:
            return False

        return bool(cls.__connections.scard(f"ws_conn:{user_id}"))

    @classmethod
    def send_status_changed(cls, user: User, online: bool):
        user_online_status_changed.send(sender=User, user=user, online=online)
