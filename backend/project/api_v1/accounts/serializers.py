from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        if user:
            if not user.is_active:
                raise ValidationError({"detail": _("User account is disabled.")})
        else:
            raise ValidationError({"detail": _("Unable to log in with provided credentials.")})

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get("new_password")
        try:
            validate_password(password)
        except DjangoValidationError as error:
            raise serializers.ValidationError("%s: %s" % (_("Password"), error.messages[0]))
        return attrs


class ReadUserSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField("get_online")

    @extend_schema_field(field=serializers.BooleanField())
    def get_online(self, user):
        return Connections.is_user_connected(user.id)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_online")
