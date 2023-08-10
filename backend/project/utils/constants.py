from django.contrib.auth import get_user_model

User = get_user_model()


def floor_round(number, n=1):
    """
    floor_round(1127, 1) -> 1120
    floor_round(1127, 2) -> 1100
    floor_round (1127, 3) -> 1000
    """
    if number:
        number -= number % 10 ** n
    return number


def get_max_length(model, field_name):
    return model._meta.get_field(field_name).max_length
