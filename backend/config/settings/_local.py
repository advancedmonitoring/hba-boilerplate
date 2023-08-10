from .base import *  # noqa

ALLOWED_HOSTS = ["*"]

DEBUG = True

SECRET_KEY = "{PROJECT_NAME}_secret_key"  # Only for local use

# https://docs.djangoproject.com/en/4.2/topics/email/#console-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions", ]  # noqa F405

# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"]["persistAuthorization"] = True  # noqa F405
