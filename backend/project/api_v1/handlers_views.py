import inspect
import logging
from typing import Dict, Iterable, Type, Union

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from drf_rw_serializers.generics import GenericAPIView
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.response import Response

from {PROJECT_NAME}.api_v1.serializers import EmptySerializer
from {PROJECT_NAME}.permissions.decorators import PermissionsDenied
from {PROJECT_NAME}.utils.handler import BaseHandler

logger = logging.getLogger(__file__)


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
        :return: Any

        """

        kwargs = self._get_prepared_data()

        if "user" not in kwargs and "user" in inspect.signature(self.handler).parameters:
            """
            Обычно kwargs - это данные, переданные с запросом. В них не должно быть пользователя, т.к. пользователь
            для запроса - это константа. Добавляет в kwargs объект пользователя, если он нужен классу handler.
            
            """
            kwargs["user"] = self.request.user

        try:
            """ Вызов обработчика """
            # noinspection PyArgumentList
            handler_object: BaseHandler = self.handler(**kwargs)
            handler_result: Any = handler_object.run()

        except self._get_exception_class() as exc:
            """
            Если обработчик завершился с типичной для него ошибкой - значит есть нарушение логики, отправляем код 
            400 и сообщение, которое вернул обработчик.
            
            """
            raise ValidationError(detail={"detail": str(exc)})

        except PermissionsDenied as exc:
            """ Класс проверки прав отклонил запрос, отправляем код 403 и сообщение """
            raise PermissionDenied(detail={"detail": str(exc)})

        except Exception as exc:
            """ Любая необработанная ошибка - код 500 и стандартный ответ, указанный в классе """
            logger.exception(self.error_text, exc_info=exc)
            raise APIException(detail={"detail": self.error_text})

        return handler_result

    def _get_request_data(self):
        """
        Подготавливает все данные запроса для передачи в сериализатор, т.к. данные могут быть как в строке запроса,
        так и в теле сообщения.

        """
        request_data = self.request.data if self.request.data else self.request.query_params.copy()
        request_data.update(self.kwargs)

        return request_data

    def _get_prepared_data(self):
        write_serializer = self.get_write_serializer(data=self._get_request_data())
        write_serializer.is_valid(raise_exception=True)

        data = {**write_serializer.validated_data, **self.kwargs}
        try:
            prepared_data = self.handler.prepare_data(user=self.request.user, data=data)

        except self._get_exception_class() as exc:
            """
            Если обработчик завершился с типичной для него ошибкой - значит есть нарушение логики, отправляем код 
            400 и сообщение, которое вернул обработчик.

            """
            raise ValidationError(detail={"detail": str(exc)})

        except Exception as exc:
            """ Любая необработанная ошибка - код 500 и стандартный ответ, указанный в классе """
            logger.exception(self.error_text, exc_info=exc)
            raise APIException(detail={"detail": self.error_text})

        return prepared_data

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

        elif isinstance(handler_result, Iterable) and not isinstance(handler_result, Dict):
            many: bool = True
            handler_result = self.filter_queryset(handler_result)

            page = self.paginate_queryset(handler_result)
            if page is not None:
                read_serializer = self.get_read_serializer(page, many=many)
                return self.get_paginated_response(read_serializer.data)
        else:
            many: bool = False

        read_serializer = self.get_read_serializer(handler_result, many=many)
        return Response(read_serializer.data, status=self.response_code)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update(user=self.request.user)
        return ctx
