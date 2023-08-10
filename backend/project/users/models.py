from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Language(TextChoices):
    RUSSIAN = "ru", _("Russian")
    ENGLISH = "en", _("English")


class User(AbstractUser):
    language = models.CharField(
        verbose_name=_("User language"),
        choices=Language.choices,
        default=Language.RUSSIAN,
        max_length=3,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = _("Users")
        verbose_name = _("User")
