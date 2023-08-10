from django.urls import path

from {PROJECT_NAME}.api_v1.accounts.views import (
    ChangePasswordView,
    GetMeView,
    LoginView,
    LogoutView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", GetMeView.as_view()),
    path("password/change/", ChangePasswordView.as_view()),
]
