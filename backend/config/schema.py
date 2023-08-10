from typing import List, Callable

from channels.routing import URLRouter
from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.utils.module_loading import import_string
from drf_rw_serializers.generics import GenericAPIView as RWGenericAPIView
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.openapi import AutoSchema

from {PROJECT_NAME}.ws_v1.schema.schema import NotReadyError


class CustomAutoSchema(AutoSchema):
    """ Utilize custom drf_rw_serializers methods for directional serializers """

    def get_request_serializer(self):
        if isinstance(self.view, RWGenericAPIView):
            return self.view.get_write_serializer_class()()
        return self._get_serializer()

    def get_response_serializers(self):
        if isinstance(self.view, RWGenericAPIView):
            return self.view.get_read_serializer_class()()
        return self._get_serializer()


class CustomSchemaGenerator(SchemaGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepared = {}

    def parse(self, input_request, public):
        result = super().parse(input_request, public)
        ws_result = self.get_ws_endpoints()
        result.update(ws_result)
        return result

    @staticmethod
    def get_asgi_application():
        return import_string(settings.ASGI_APPLICATION)

    def get_ws_endpoints(self):
        application = self.get_asgi_application()
        socket_routes = application.application_mapping.get("websocket")

        if socket_routes is None:
            return []

        router = socket_routes.inner

        while not isinstance(router, URLRouter):
            router = router.inner

        result = {}

        for route in router.routes:
            consumer = route.callback.consumer_class()
            result.update(self._find_methods(consumer=consumer, path=simplify_regex(str(route.pattern))))

        return result

    def _find_methods(self, consumer, path: str):
        consumer_endpoints = {}

        methods_list = self._get_extended_methods_list(consumer)
        while methods_list:
            method = methods_list.pop(0)
            event: str = getattr(method, "event")
            name: str = "%s::%s" % (path, event)

            action_schema = self.get_action_schema(method=method)
            try:
                consumer_endpoints[name] = {
                    action_schema.method == "receive" and "get" or "post": {
                        "operationId": action_schema.get_operation_id(),
                        "requestBody": action_schema.get_request_body(
                            serializer=action_schema.get_request_serializer(),
                            method=action_schema.method,
                        ),
                        "summary": action_schema.get_description(),
                        "tags": action_schema.get_tags(),
                        "responses": action_schema.get_response_bodies(),
                    }
                }
            except NotReadyError:
                methods_list.append(method)

        return consumer_endpoints

    @staticmethod
    def _get_extended_methods_list(consumer):
        methods_list: List[Callable] = []
        for attr in dir(consumer):
            method = getattr(consumer, attr)
            if callable(method) and hasattr(method, "kwargs"):
                methods_list.append(method)

        return methods_list

    def get_action_schema(self, method: Callable):
        schema_class = getattr(method, "kwargs", {}).get("schema", None)
        schema = schema_class()
        schema.method_name = method.__name__
        schema.method = getattr(method, "type")
        schema.event = getattr(method, "event")
        schema.registry = self.registry
        schema.prepared = self.prepared

        return schema
