import types
from abc import ABC

from django.db import transaction


class SignalMixin(ABC):
    """ Примесь, добавляющая возможность отправки сигнала. Отравляет сигнал после завершения транзакции. """

    _signal_prevented: bool = False
    signal = None
    signal_sender = None

    def prevent_signal_send(self):
        """
        Метод предотвращения отправки сигнала. Удобно, когда один обработчик вызывается внутри другого, и есть
        необходимость не отправлять сигнал

        """
        self._signal_prevented = True

    def _send_signal(self, **kwargs):
        """ Основной метод отправки сигнала. """
        if self._signal_prevented:
            return

        self._inner_send_signal(**kwargs)

    @classmethod
    def _inner_send_signal(cls, **kwargs):
        signal_kwargs = cls._get_signal_kwargs(**kwargs)

        if isinstance(signal_kwargs, types.GeneratorType):
            """ 
            Метод подготовки данных для сигнала вернул генератор - бежим по генератору и отправляем много сигналов
            с параметрами, которые возвращает генератор.

            """
            for kwargs in signal_kwargs:
                cls.send_signal(**kwargs)

        else:
            cls.send_signal(**signal_kwargs)

    @staticmethod
    def _get_signal_kwargs(**kwargs):
        """ Метод подготовки параметров для сигнала. Иногда удобно """
        return kwargs

    @classmethod
    def send_signal(cls, **kwargs):
        """ Отправка сигнала. Устанавливает задачу как callback применения транзакции """

        def send():
            cls.signal.send(sender=cls.signal_sender, **kwargs)

        transaction.on_commit(send)
