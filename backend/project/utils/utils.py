import logging
from pathlib import Path
from typing import Generic, Iterator, Optional, TypeVar

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def validate_file_extension(*extensions):
    def wrapper(value):
        """
        Checks whether the file extension matches the allowed extensions.
        The validator is used for model fields.
        If the file extension is not correct, it causes raises ValidationError.
        """
        file = Path(value.path)
        file_extension = file.suffix
        if file_extension not in extensions:
            raise ValidationError("File not supported!")

    return wrapper


T = TypeVar("T")


class QueryType(Generic[T], QuerySet):
    def __iter__(self) -> Iterator[T]: ...


def first(ordered_dict):
    """
    Return the first element from an ordered collection
    or an arbitrary element from an unordered collection.
    Raise StopIteration if the collection is empty.
    """
    return next(iter(ordered_dict))


def get_field_label(field_name, serializer):
    fields = serializer().fields
    if field_name in fields:
        return fields[field_name].label


def get_admin_link(obj, model_name: Optional[str] = None):
    app_label = obj._meta.app_label
    model_name_ = model_name or obj._meta.model_name
    view_name = f"admin:{app_label}_{model_name_}_change"
    link_url = reverse(view_name, args=[obj.pk])
    return format_html('<a target="_blank" href="{}">{}</a>', link_url, obj)


def linkify(field_name, model_name: Optional[str] = None, model: Optional = None):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(obj):
        try:
            linked_obj = getattr(obj, field_name)
            if linked_obj is None:
                return "-"

            return get_admin_link(obj=linked_obj, model_name=model_name)
        except Exception as exc:  # noqa BLE001
            return getattr(obj, field_name)

    if model is not None:
        description = model._meta.get_field(field_name).verbose_name
    else:
        description = _(field_name.capitalize())

    _linkify.short_description = description  # Sets column name
    return _linkify
