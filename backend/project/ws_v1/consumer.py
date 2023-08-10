import logging
from typing import Any, Dict, Optional

from asgiref.sync import sync_to_async
from channels.consumer import get_handler_name
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from {PROJECT_NAME}.api_v1.serializers import EmptySerializer
from {PROJECT_NAME}.utils.attrdict import AttrDict
from {PROJECT_NAME}.ws_v1.handlers.connected import UserConnectedHandler
from {PROJECT_NAME}.ws_v1.schema.decorators import extend_ws_schema
from {PROJECT_NAME}.ws_v1.serializers.base import NotificationSerializer, UserOnlineStatusChangedSerializer
from {PROJECT_NAME}.ws_v1.utils import (
    get_user_ws_group_name,
    get_global_ws_group_name,
    Connections,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class Consumer(AsyncJsonWebsocketConsumer):
    __user: Optional[User] = None

    async def receive_json(self, content, **kwargs):
        """
        Диспетчер, обрабатывающий входящий json. В нем есть event по которому определяется
        какой метод надо запустить для обработки этого сообщения
        :param content: Словарь { event, data }
        :param kwargs: Остальные параметры
        :return: None

        """
        content = AttrDict(content)

        if not hasattr(self, content.event):
            logger.warning(f"No handler for {content.event} event!")
            return

        await self.process_message(event=content.event, data=content.get("data", {}))

    async def process_message(self, event, data):
        try:
            handler = getattr(self, event)
            res = await handler(**data)

        except Exception as e:
            logger.exception(e)
            await self.send_notify(message=_("Request error"), status="error")

        else:
            if res:
                await self.send_notify(message=res, status="warning")

    async def dispatch(self, message):
        """
        Dispatches incoming messages to type-based handler.
        """

        handler_name: str = get_handler_name(message)
        handler = getattr(self, handler_name, None)

        if handler:
            if handler_name.startswith("websocket"):
                await handler(message)
            else:
                await handler(**message.get("data", {}))
        else:
            raise ValueError("No handler for message type %s" % message["type"])

    @extend_ws_schema(
        type="receive",
        event="notify",
        description="Retrieve notification",
        request=EmptySerializer,
        responses=NotificationSerializer,
    )
    async def send_notify(self, message: str, status: str, title: Optional[str] = None, extra: Optional[Dict] = None):
        if extra is None:
            extra = {}

        await self.send_data(event="notify", message=message, type=status, title=title, extra=extra)

    @property
    def user(self) -> Optional[User]:
        return self.__user

    @user.setter
    def user(self, _) -> None:
        return

    def set_user(self, user: User) -> None:
        self.__user = user

    async def send_data(self, event: str, **kwargs: Any) -> None:
        await self.send_json({
            "event": event,
            "data": kwargs,
        })

    async def add_user_groups(self) -> None:
        if self.__user is not None and not self.__user.is_anonymous:
            await self.__add_group(name=get_user_ws_group_name(user_id=self.__user.id))

        await self.__add_group(name=get_global_ws_group_name())

    async def discard_user_groups(self) -> None:
        if self.__user is not None and not self.__user.is_anonymous:
            await self.__discard_group(name=get_user_ws_group_name(user_id=self.__user.id))

        await self.__discard_group(name=get_global_ws_group_name())

    async def __add_group(self, name: str) -> None:
        await self.channel_layer.group_add(name, self.channel_name)

    async def __discard_group(self, name: str) -> None:
        await self.channel_layer.group_discard(name, self.channel_name)

    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            return self.close()

        self.set_user(user=user)
        await self.add_user_groups()
        await self.accept()

        await sync_to_async(Connections.user_connected)(user=user, channel_name=self.channel_name)
        await UserConnectedHandler(consumer=self).send_data()

    async def disconnect(self, code):
        user = self.scope["user"]
        await sync_to_async(Connections.user_disconnected)(user=user, channel_name=self.channel_name)
        await self.discard_user_groups()

    @extend_ws_schema(
        type="receive",
        event="user_online_status_changed",
        description="Retrieve user online status change",
        request=EmptySerializer,
        responses=UserOnlineStatusChangedSerializer,
    )
    async def user_online_status_changed(self, user_id: int, is_online: bool):
        await self.send_data(
            event="user_online_status_changed",
            user_id=user_id,
            is_online=is_online,
        )
