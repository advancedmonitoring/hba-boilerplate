from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    message = serializers.CharField()
    type = serializers.CharField()
    title = serializers.CharField()
    extra = serializers.DictField()


class UserOnlineStatusChangedSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    is_online = serializers.BooleanField()
