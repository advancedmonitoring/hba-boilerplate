from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from {PROJECT_NAME}.ws_v1.utils import Connections

User = get_user_model()


class LoginSerializer(DefaultLoginSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    email = None

    def validate(self, attrs):
        username: str = attrs.get("username")
        password: str = attrs.get("password")
        user = self._validate_username(username, password)
        if not user or not user.is_active:
            raise AuthenticationFailed()

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value: str):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(detail=_("Invalid password"))

        return value

    def validate_new_password(self, value: str):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs.get("new_password") == attrs.get("old_password"):
            raise serializers.ValidationError(
                {"new_password": _("The new password cannot be the same as the old password")},
            )

        return attrs


class ReadUserSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField("get_online")

    @extend_schema_field(field=serializers.BooleanField())
    def get_online(self, user):
        return Connections.is_user_connected(user.id)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_online")
