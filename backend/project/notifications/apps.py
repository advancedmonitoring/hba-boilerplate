from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "{PROJECT_NAME}.notifications"
    verbose_name = _("Notifications")

    def ready(self):
        try:
            import {PROJECT_NAME}.notifications.signals.handlers
        except ImportError:
            pass
