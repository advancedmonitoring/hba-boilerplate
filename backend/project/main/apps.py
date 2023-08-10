from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from {PROJECT_NAME}.utils.process_recognizer import ProcessRecognizer


class MainConfig(AppConfig):
    name = "{PROJECT_NAME}.main"
    verbose_name = _("Main app")

    def ready(self):
        ProcessRecognizer.init()
        self.init_connections()

    @staticmethod
    def init_connections():
        from {PROJECT_NAME}.ws_v1.utils import Connections

        Connections.init()
