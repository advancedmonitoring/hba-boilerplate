from abc import ABC
from typing import Any, Dict, Optional


class ValidationMixin(ABC):
    """ Примесь, добавляющая возможность валидации данных. """

    validated_data: Optional[Dict[str, Any]] = None

    def validate(self, **kwargs):
        self.validated_data = {}

        for attr, value in kwargs.items():
            if value is None:
                continue

            clean_method = getattr(self, f"_clean_{attr}", None)
            if clean_method:
                value = clean_method(value)

            self.validated_data[attr] = value
