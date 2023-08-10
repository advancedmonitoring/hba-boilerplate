import enum
from functools import wraps

from django.contrib.auth import get_user_model

from {PROJECT_NAME}.permissions.permissions import EventPermissions

User = get_user_model()


class Events(enum.Enum):
    ...


class PermissionsDenied(Exception):
    pass


def check_permissions(event_code: Events):
    def wrapper(func):

        @wraps(func)
        def check_permission(handler, *args, **kwargs):
            if args:
                raise ValueError("Pass only keyword args for permissions check")

            user = kwargs.get("user")

            if user is None:
                raise ValueError("Pass user to check permissions")

            func(handler, **kwargs)
            checker = EventPermissions(user, event_code, kwargs)
            granted: bool = checker()

            if granted is False:
                raise PermissionsDenied(checker.get_denied_message())

        return check_permission

    return wrapper
