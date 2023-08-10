import django.dispatch

__all__ = (
    "user_online_status_changed",
)

# providing_args=["user"]
user_online_status_changed = django.dispatch.Signal()
