from typing import Optional, Dict

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_media_type_object, force_instance, is_serializer, is_list_serializer
from inflection import camelize
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from {PROJECT_NAME}.api_v1.serializers import EmptySerializer


class NotReadyError(Exception):
    pass


class EventHandler:
    request = None
    kwargs = {}
    versioning_class = None

    def __init__(self, name):
        self.name = name

    def get_parsers(self):
        """ Сокет использует только json сериализацию """
        return [JSONParser, ]

    def get_renderers(self):
        """ Сокет использует только json сериализацию """
        return [JSONRenderer, ]

    def determine_version(self, *args, **kwargs):
        """ Версионирование на уровне документации пока не поддерживается """
        return None, None


class ConsumerAutoSchema(AutoSchema):
    """
    Класс схема для документирования методов сокета.
    """

    def __init__(self):
        super().__init__()
        self.method_name: Optional[str] = None
        self.event: Optional[str] = None
        self.prepared = {}

    @property
    def view(self):
        return EventHandler(name=self.event)

    def get_operation_id(self):
        return "%s_%s" % (self.method, self.method_name)

    def get_request_body(self, serializer, method):
        _, serializer = self._force_ws_serializer(serializer=serializer).popitem()

        schema, request_body_required = self._get_request_for_media_type(serializer, method)
        if schema is None:
            return None

        content = [
            (media_type, schema, self._get_examples(serializer, "request", media_type))
            for media_type in self.map_parsers()
        ]

        request_body = {
            "content": {
                media_type: build_media_type_object(schema, examples)
                for media_type, schema, examples in content
            }
        }
        return request_body

    def _get_request_for_media_type(self, serializer, method):  # noqa
        component = self.resolve_serializer(serializer, method)

        if not component:
            # serializer is empty so skip content enumeration
            return None, False

        schema = component.ref
        return schema, True

    def get_response_bodies(self):
        response_serializers = self.get_response_serializers()

        if response_serializers:
            serializers_ = self._force_ws_serializer(serializer=response_serializers, direction="receive")

            return {
                event: self._get_response_for_code(serializer, status.HTTP_200_OK)
                for event, serializer in serializers_.items()
            }

    def _get_serializer_name(self, serializer, direction: str, bypass_extensions: bool = False):
        return serializer.__class__.__name__

    def get_tags(self):
        return ["Web Socket"]

    def get_description(self):
        return ""

    def _force_ws_serializer(self, serializer, direction: Optional[str] = None) -> Dict[str, serializers.Serializer]:
        serializer = force_instance(serializer)

        if isinstance(serializer, EmptySerializer):
            return {self.event: serializer}

        if direction is None:
            direction = self.method

        if isinstance(serializer, list):
            return self._force_serializers_list(events=serializer)

        if self.event in self.prepared:
            return {self.event: self.prepared[self.event]}

        if is_list_serializer(serializer):
            serializer_name = serializer.child.__class__.__name__
        elif is_serializer(serializer):
            serializer_name = serializer.__class__.__name__
        else:
            raise AssertionError("Invalid type of serializer")

        name: str = self._get_forced_serializer_name(direction=direction, serializer_name=serializer_name)

        if is_list_serializer(serializer):
            inner_name: str = "Ws%sDataSerializer" % self.event.capitalize()
            inner_serializer = type(inner_name, (serializers.Serializer,), {self.event: serializer})()
            attrs = {
                "event": serializers.CharField(default=self.event),
                "data": inner_serializer,
            }
        else:
            attrs = {
                "event": serializers.CharField(default=self.event),
                "data": serializer,
            }

        prepared = type(name, (serializers.Serializer,), attrs)()
        self.prepared[self.event] = prepared
        return {self.event: prepared}

    def _force_serializers_list(self, events) -> Dict[str, serializers.Serializer]:
        result: Dict[str, serializers.Serializer] = {}

        for index, event in enumerate(events):
            forced = self.prepared.get(event)
            if forced is None:
                raise NotReadyError()
            result[event] = forced

        return result

    def _get_forced_serializer_name(self, direction: str, serializer_name: str) -> str:
        name: str = "Ws%s" % direction.capitalize()
        event: str = camelize(self.event)
        if serializer_name.startswith(event):
            return "%s%s" % (name, serializer_name)

        return "%s%s%s" % (name, event, serializer_name)
