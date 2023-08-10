from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from {PROJECT_NAME}.api_v1.accounts.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    ReadUserSerializer,
)
from {PROJECT_NAME}.api_v1.serializers import DummyDetailAndStatusSerializer, DummyDetailSerializer, EmptySerializer

User = get_user_model()


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    get=extend_schema(
        summary="Данные о текущем пользователе",
        responses={
            status.HTTP_200_OK: ReadUserSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
)
# endregion
class GetMeView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            status=status.HTTP_200_OK,
            data=ReadUserSerializer(request.user).data,
        )


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Вход в учетную запись",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
        request=LoginSerializer,
    ),
)
# endregion
class LoginView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        login(request, user)
        return JsonResponse({"detail": "Success"})


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Выход из учетной записи",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
)
# endregion
class LogoutView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Смена пароля",
        responses={
            status.HTTP_200_OK: EmptySerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailSerializer,
        },
    ),
)
# endregion
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        """"""
        current_user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not current_user.check_password(serializer.data.get("old_password")):
            return Response(data={"detail": _("Invalid password")}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.data.get("new_password") == serializer.data.get("old_password"):
            return Response(data={"detail": _("The new password cannot be the same as the old password")},
                            status=status.HTTP_400_BAD_REQUEST)

        current_user.set_password(serializer.data.get("new_password"))
        current_user.save()

        return Response(status=status.HTTP_200_OK)
