import logging
import re
from abc import ABCMeta
from collections import defaultdict
from itertools import chain
from typing import Any, Callable, DefaultDict, Dict, Set, Type, Optional, List

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from {PROJECT_NAME}.main.models import Note, Todo

User = get_user_model()

logger = logging.getLogger(__name__)

GROUP_NAME: str = "name"
SINGLE_OBJECT_REGEX: str = rf"^(?P<{GROUP_NAME}>[a-zA-Z_]+)_id$"
MANY_OBJECTS_REGEX: str = rf"^(?P<{GROUP_NAME}>[a-zA-Z_]+)_ids$"


class NotReady(Exception):
    """ Значение атрибута ещё не вычислено """
    pass


class DependencyCannotBeResolved(Exception):
    """ Значение атрибута не может быть вычислено для текущего контекста """
    pass


class BaseDataHandler:
    """
    Класс подготовки (например получение из БД):
    {
        entity_id: 213,
        comment_id: 12,
        user_ids: [1, 2, 3],
    } -> {
        entity: <Entity: 213>,
        comment: <Comment: 12>,
        users: <QuerySet [<User: 1>, <User: 2>, <User: 3>]>
    }
    Ищет метод с названием "_prepare_{dict_key}", если такой метод есть - он должен вернуть подготовленное для работы
    значение. Название поля в итоговом словаре должно быть указано в `field_names`. По умолчанию переводит названия типа
    `[some_element]_id` в `some_element` и `[some_object]_ids` в `some_objects`.

    """
    field_names: Dict[str, str] = {
        # частный случай, пользователь уже есть у каждого запроса, название такого аргумента нельзя
        # обрабатывать по общим правилам
        "user_id": "user_id",
    }

    def __init__(self, handler: Type["BaseHandler"], user: User, data: Dict[str, Any]):
        """
        :param user: Объект пользователя. Может быть необходим для получения значения.
        :param data: Данные для преобразования.

        """
        # Класс обработчик
        self.handler: Type[BaseHandler] = handler

        # Данные, которые необходимо подготовить
        self.data: Dict[str, Any] = data
        self.data.update(user=user)

        # Подготовленные данные
        self.prepared_data: Dict[str, Any] = {}
        # Названия объектов в словаре подготовленных данных
        self._prepared_names: Dict[str, str] = self._get_prepared_names()
        # Множество, содержит только названия. Необходимо для проверки, что требуемый атрибут может быть вычислен.
        self._allowed_names: Set[str] = set(chain.from_iterable(self._prepared_names.items()))

        # Словарь, содержащий зависимости одних атрибутов от других
        self._attr_dependencies: DefaultDict[str, List[str]] = defaultdict(list)
        # Текущий обрабатываемый атрибут
        self._cur_attr: Optional[str] = None

    def __getattr__(self, item: str) -> Any:
        """
        Метод, благодаря которому внутри методов подготовки можно обращаться к полям (переданным или вычисленным) как к
        атрибутам.

        Проводит проверку, что запрашиваемое поле может быть вычислено на основе переданных данных.

        :raise DependencyCannotBeResolved: Значение атрибута не может быть вычислено для текущего контекста.
        :raise NotReady: Значение атрибута ещё не вычислено.

        """
        if item.startswith("_prepare"):
            return None

        if item not in self._allowed_names:
            """ Если атрибут не может быть вычислен """
            raise DependencyCannotBeResolved(item)

        if item in self.prepared_data:
            """ Если уже подготовлен """
            return self.prepared_data[item]

        if item in self.data:
            """ Иначе берём из исходных данных """
            return self.data[item]

        """ Проверка циклических зависимостей """
        self._check_circular(item)

        """ Иначе - атрибут ещё не готов """
        raise NotReady(item)

    def _check_circular(self, item: str):
        """
        Метод ищет циклические зависимости вычисления атрибутов. Если такие есть - выдает ошибку.

        Такие зависимости возникают при использовании атрибута внутри его же метода подготовки:

        def _prepare_entity_id(self):
            return Entity.objects.get(pk=self.entity)

        Здесь методу подготовки entity нужен сам объект entity, что не есть правильно.

        Другой пример:

        def _prepare_author_id(self):
            return Author.objects.get(books=self.book)

        def _prepare_book_id(self):
            return Book.objects.get(author=self.author)

        Здесь методу подготовки автора нужна книга, а методу подготовки книги нужен автор. Без проверки циклических
        зависимостей такое вычисление уйдет в ∞ рекурсию.

        """
        if self._cur_attr is not None:
            self._attr_dependencies[self._cur_attr].append(item)

            if self._cur_attr in self._attr_dependencies[item]:
                raise DependencyCannotBeResolved("Circular dependency found: %s, %s" % (self._cur_attr, item))

        self._cur_attr = item

    def prepare(self) -> Dict[str, Any]:
        """
        Основной рабочий метод. Перебирает все поля переданного словаря, ищет методы подготовки, складывает в словарь
        подготовленных данных.
        :return:
        """
        data_keys: List[str] = list(self.data.keys())
        while data_keys:
            """ Пока есть неготовые атрибуты """
            name: str = data_keys.pop(0)
            prepare_method: Callable = getattr(self, "_prepare_%s" % name, None)

            if prepare_method:
                try:
                    value: Any = prepare_method()
                except NotReady:
                    """ Если на данной итерации необходимые значения не готовы - ставим в конец списка """
                    data_keys.append(name)
                    continue

            else:
                value: Any = self.data[name]

            self.prepared_data.update({self._prepared_names[name]: value})

        return self.prepared_data

    def _get_prepared_names(self) -> Dict[str, str]:
        """ Метод получения словаря исходных названий к итоговым названиям """

        result: Dict[str, str] = {}
        for name in self.data:
            prepared_name: str = self._get_prepared_name(name=name)
            result.update({name: prepared_name})

        logger.debug("%s prepared names: %s" % (
            self.handler,
            result,
        ))

        return result

    def _get_prepared_name(self, name: str) -> str:
        """ Метод получения итогового названия поля """

        if name in self.field_names:
            """ Если итоговое название указано в словаре """
            return self.field_names[name]

        single_object_result = re.search(pattern=SINGLE_OBJECT_REGEX, string=name)
        if single_object_result:
            """ Если название атрибута подходит под регулярку идентификатора одиночного объекта """
            return single_object_result.group(GROUP_NAME)

        many_objects_result = re.search(pattern=MANY_OBJECTS_REGEX, string=name)
        if many_objects_result:
            """ Если название атрибута подходит под регулярку идентификаторов объектов """
            return "%ss" % many_objects_result.group(GROUP_NAME)

        """ Если название не найдено - оставляем начальное """
        return name


class HandlerException(Exception):
    pass


class BaseHandler(metaclass=ABCMeta):
    """ Базовый класс обработки запроса. Отвечает за проверку бизнес-логики и её реализацию. """
    data_handler = BaseDataHandler
    exception = HandlerException

    def run(self) -> Any:
        """
        Основной метод любого класса обработчика.
        :return: Any
        """
        raise NotImplementedError()

    @classmethod
    def prepare_data(cls, user, data):
        """ Метод подготовки данных для класса """
        return cls.data_handler(handler=cls, user=user, data=data).prepare()

    @staticmethod
    def _clean_length(value: str, max_length: int):
        if value:
            return value[:max_length]

        return value
