from abc import ABC
from collections import defaultdict
from typing import Optional, List, DefaultDict, Any

from {PROJECT_NAME}.utils.attrdict import AttrDict


class ValidationMixin(ABC):
    """ Примесь, добавляющая возможность валидации данных. """

    validated_data: Optional[AttrDict[str, Any]] = None
    exception: Exception

    def validate(self, **kwargs):
        self.validated_data = AttrDict()
        errors: DefaultDict[str, List[str]] = defaultdict(list)

        for attr, value in kwargs.items():
            if value is None:
                continue

            clean_method = getattr(self, f"_clean_{attr}", None)
            if clean_method:
                value = clean_method(value)
                try:
                    value = clean_method(value)
                except self.exception as exc:
                    if exc.errors:
                        errors.update(exc.errors)
                    else:
                        errors[exc.field or attr].append(str(exc))

                    continue

            self.validated_data[attr] = value

        if errors:
            raise self.exception("Some errors", errors=errors)
