from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "{PROJECT_NAME}.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import {PROJECT_NAME}.users.signals.handlers  # noqa F401
        except ImportError:
            pass
