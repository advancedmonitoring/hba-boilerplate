import inspect
import logging
from typing import Dict, Iterable, Type, Union, Callable, Optional, Tuple

import rest_framework.exceptions
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from drf_rw_serializers.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework import status

from {PROJECT_NAME}.api_v1.serializers import EmptySerializer
from {PROJECT_NAME}.permissions.decorators import PermissionsDenied
from {PROJECT_NAME}.utils.handler import BaseHandler

logger = logging.getLogger(__file__)

class LogicalError(rest_framework.exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("A logic error occurred.")
    default_code = "logic_error"

class File:
    def __init__(self, content: Union[str, bytes], file_name: str, content_type: str):
        self.content = content
        self.file_name = file_name
        self.content_type = content_type


class HandlerView(GenericAPIView):
    """ Основной класс обработки request на основе handler. """

    """ Стандартный текст ошибки, если выполнение handler завершилось с необработанным исключением """
    error_text: str = _("Request error")

    """ Код ответа в случае успешного выполнения """
    response_code: int

    """ Класс handler обработчик запроса """
    handler: Type[BaseHandler]

    """ Сериализатор, используемый для проверки входящих данных """
    write_serializer = None
    serializer_class = EmptySerializer

    """ Сериализатор, используемый подготовки ответа """
    read_serializer_class = None

    def _get_exception_class(self):
        """ Получение ошибки класса обработчика для её перехвата """
        return self.handler.exception

    def get_handler_result(self):
        """
        Метод запуска класса handler.
        :return:

        """

        handler_data = self._get_prepared_data()

        if "user" not in handler_data and "user" in inspect.signature(self.handler).parameters:
            """
            Обычно kwargs - это данные, переданные с запросом. В них не должно быть пользователя, т.к. пользователь
            для запроса - это константа. Добавляет в kwargs объект пользователя, если он нужен классу handler.

            """
            handler_data["user"] = self.request.user

        def run_handler():
            return self.handler(**handler_data).run()  # noqa

        return self.safe_run(method=run_handler, allow_validate_error=True)

    def _get_request_data(self):
        """
        Подготавливает все данные запроса для передачи в сериализатор, т.к. данные могут быть как в строке запроса,
        так и в теле сообщения.

        """
        request_data = self.request.data if self.request.data else self.request.query_params.copy()
        return request_data

    def _get_prepared_data(self):
        write_serializer = self.get_write_serializer(data=self._get_request_data())
        write_serializer.is_valid(raise_exception=True)

        prepared_kwargs = self.safe_run(
            method=self.handler.prepare_data,
            kwargs={
                "user": self.request.user,
                "data": self.kwargs,
            },
            allow_validate_error=False,
        )

        body_data = write_serializer.validated_data

        return self.safe_run(
            method=self.handler.prepare_data,
            kwargs={
                "user": self.request.user,
                "data": {**body_data, **prepared_kwargs},
            },
            allow_validate_error=True,
        )

    def safe_run(self, method: Callable, args: Optional[Tuple] = None, kwargs: Optional[Dict] = None,
                 allow_validate_error: bool = True):

        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        try:
            return method(*args, **kwargs)

        except self._get_exception_class() as exc:
            """
            Если обработчик завершился с типичной для него ошибкой - значит есть нарушение логики, отправляем код
            400 и сообщение, которое вернул обработчик.

            """

            if allow_validate_error:
                errors: Optional[str] = getattr(exc, "errors", None)

                if errors:
                    raise rest_framework.exceptions.ValidationError(errors)

            raise LogicalError(detail=str(exc))

        except PermissionsDenied as exc:
            """ Класс проверки прав отклонил запрос, отправляем код 403 и сообщение """
            raise rest_framework.exceptions.PermissionDenied(detail=str(exc))

        except Exception as exc:
            """ Любая необработанная ошибка - код 500 и стандартный ответ, указанный в классе """
            logger.exception(self.error_text, exc_info=exc)
            raise rest_framework.exceptions.APIException(detail=self.error_text)

    def handle(self):
        handler_result = self.get_handler_result()
        # handler_result is None не вызывает лишнего хинта в БД
        if handler_result is None:
            return Response(status=self.response_code)

        if isinstance(handler_result, File):
            response = HttpResponse(
                content=handler_result.content,
                status=self.response_code,
                content_type=handler_result.content_type,
            )
            response["Content-Disposition"] = f'attachment; filename="{handler_result.file_name}"'
            return response

        many = False

        if isinstance(handler_result, Iterable) and not isinstance(handler_result, Dict):
            many = True

        read_serializer = self.get_read_serializer(handler_result, many=many)
        return Response(read_serializer.data, status=self.response_code)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update(user=self.request.user)
        return ctx
