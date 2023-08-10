from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    pass


class DummyDetailSerializer(serializers.Serializer):
    """Заглушка для правильного отображения ответов от сервера"""
    detail = serializers.CharField()


class DummyDetailAndStatusSerializer(serializers.Serializer):
    """Заглушка для правильного отображения ответов от сервера"""
    detail = serializers.CharField()
    status = serializers.IntegerField()
