from copy import copy
from functools import wraps

from django.db import transaction
from expression import Ok as OOk, Error as OError
from raven import breadcrumbs

from {PROJECT_NAME}.utils.attrdict import AttrDict
from {PROJECT_NAME}.utils.logger import LoggerMixin


class Ok(OOk):
    def __or__(self, other):
        return self.bind(other)


class Error(OError):
    def __or__(self, other):
        return Error(self._error)


class ServiceObject(LoggerMixin):
    _context = AttrDict()

    def success(self, **kwargs):
        self._update_context(**kwargs)

        return Ok(copy(self._context))

    def fail(self, fail_obj):
        if isinstance(fail_obj, str):
            message = fail_obj
        elif isinstance(fail_obj, Exception):
            message = str(fail_obj.args)
        else:
            message = fail_obj

        self.logger.error(f"Failed with message: \'{message}\' and context {self._context}")

        return Error(message)

    @staticmethod
    def fail_with(exception):
        return Error(exception)

    def _reset_context(self):
        self._context = AttrDict()

    def _update_context(self, **kwargs):
        self._context = AttrDict(self._context, **kwargs)

    def __call__(self, **kwargs):
        raise NotImplementedError


def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with transaction.atomic():
            result = func(self, *args, **kwargs)

            if result.is_error():
                transaction.set_rollback(True)
                self.logger.info("Transaction rollback")

            return result

    return wrapper


def service_call(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        service_name = self.__class__.__name__

        breadcrumbs.record(message="Call args",
                           category=service_name, level="info",
                           data={"args": args, **kwargs})

        try:
            self._reset_context()

            return func(self, *args, **kwargs)
        except Exception as e:
            self.logger.error(f"Service {service_name} thrown exception, context: {self._context}",
                              exc_info=e)

            raise

    return wrapper
