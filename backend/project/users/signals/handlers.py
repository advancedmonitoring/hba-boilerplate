from django.contrib.auth import get_user_model
from django.dispatch import receiver

from {PROJECT_NAME}.users.signals.custom_signals import user_online_status_changed
from {PROJECT_NAME}.ws_v1.utils import get_global_ws_group_name, send_to_socket_group

User = get_user_model()


@receiver(user_online_status_changed, sender=User)
def share_user_status_changed(sender, user: User, online: bool, **kwargs):
    if user.is_anonymous:
        return

    group_name: str = get_global_ws_group_name()
    send_to_socket_group(
        group_name=group_name,
        event="user_online_status_changed",
        user_id=user.id,
        is_online=online,
    )
