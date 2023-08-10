from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PermissionsConfig(AppConfig):
    name = "{PROJECT_NAME}.permissions"
    verbose_name = _("Permissions")

    def ready(self):
        try:
            import {PROJECT_NAME}.permissions.signals.handlers  # noqa F401
        except ImportError:
            pass
