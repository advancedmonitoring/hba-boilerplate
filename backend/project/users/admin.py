from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from {PROJECT_NAME}.utils.utils import linkify

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("username",)
    list_display = ("id", "username", "first_name", "last_name", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "email")

    fieldsets = (
        (_("Personal info"),
         {"fields": ("username", "first_name", "last_name", "email", "password", "language")}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups"),
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email", "password1", "password2"),
        }),
    )
