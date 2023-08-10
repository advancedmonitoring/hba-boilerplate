from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model

from {PROJECT_NAME}.api_v1.accounts.serializers import ReadUserSerializer

User = get_user_model()


def get_data(obj):
    return sync_to_async(lambda: obj.data)()


class UserConnectedHandler:
    def __init__(self, consumer):
        self.consumer = consumer
        self.user = consumer.user

    async def send_data(self):
        await self.send_user_data()
        await self.send_release_version()

        await self.send_loading_end()

    @database_sync_to_async
    def _get_user_data(self):
        self.user.refresh_from_db()
        serializer = ReadUserSerializer(self.user)
        return serializer.data

    async def send_user_data(self):
        data = await self._get_user_data()

        await self.consumer.send_data(
            event="user_data",
            **data,
        )

    async def send_release_version(self):
        release_version: str = "dev"
        if settings.DEBUG is False:
            release_version = settings.RELEASE_VERSION

        await self.consumer.send_data(
            event="release_version",
            release_version=release_version,
        )

    async def _prepare_data(self, handler, serializer):
        result = handler(user=self.user).run()

        serializer = serializer(result, many=True)
        return await get_data(serializer)

    async def send_loading_end(self):
        await self.consumer.send_data(
            event="load_end",
        )
