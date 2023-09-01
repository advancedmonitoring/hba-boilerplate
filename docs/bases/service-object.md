`backend.project.utils.service_object.ServiceObject`

Базовый класс для создания сервиса. Сервис реализует выполнение логики, не проверяя бизнес-логику или проверку прав ролевой системы.

Основная суть класса, унаследованного от `ServiceObject` - выполнение логики по шагам, т.е. каждый метод сервиса - это маленький шаг, содержащий одну операцию. Все такие методы вызываются в порядке, указанном в методе `__call__`, передавая друг другу контекст выполнения.

### Атрибуты:
* `_context` - контекст выполнения сервиса - словарь, который передается от метода к методу в процессе работы сервиса.
* `logger` - атрибут примеси. Используется для легирования внутри сервиса.

### Методы:
* `success` - метод, вызов которого возвращает каждый этап (метод) в процессе работы сервиса, если метод отработал 
ожидаемо (без ошибок). Внутрь метода `success` можно передавать неограниченное количество именованных аргументов, 
  которые будут доступны в следующем по порядку выполнения методе.
* `fail` - метод, вызов которого возвращает каждый этап (метод) в процессе работы сервиса, если дальнейшая работа 
  сервиса невозможна. На вход принимает ошибку, либо текст ошибки. Логирует текст ошибки и текущий контекст выполнения.
* `fail_with` - метод, вызов которого возвращает каждый этап (метод) в процессе работы сервиса, если дальнейшая 
  работа сервиса невозможна. На вход принимает ошибку, либо текст ошибки. Не производит легирование ошибки и контекста.
* `__call__` - метод вызова экземпляра сервиса. Основной метод, внутри которого происходит пошаговое выполнение 
  логики сервиса.

### Пример сервиса:

```python
class UpdateBooksService(ServiceObject):
    """
    Сервис получения и сохранения книг автора.
    """

    def prepare_sdk_init_kwargs(self, context):
        """
         Метод подготовки данных для инициализации класса подключения к сервису "книги".

        :param context: Контекст выполнения сервиса.
        :return:
            fail_with - если не указаны настройки подключения к сервису.
            success - если всё ок. Передает дальше данные для инициализации класса SDK.

        """
        sdk_init_kwargs = {
            "url": settings.BOOKS_API_URL,
            "token": settings.BOOKS_API_TOKEN,
        }

        if not all(sdk_init_kwargs.values()):
            """ Если любой из настроек BOOKS_API_URL/BOOKS_API_TOKEN нет - возвращаем fail_with, чтобы завершить 
            выполнение всего сервиса. Логирование в этом случае не нужно. """
            return self.fail_with("Book api url and token required. Check settings!")

        """ Если настройки указаны - возвращаем success, там самым переходим к следующему методу """
        return self.success(sdk_init_kwargs=sdk_init_kwargs)

    def set_sdk(self, context):
        """
        Метод инициализирует класс SDK для подключения к сервису. Использует sdk_init_kwargs, переданные в
        предыдущем методе в метод success

        :param context: Контекст выполнения сервиса.
        :return:
            success - если всё ок. Передает дальше инициализированный класс SDK.

        """
        sdk = BookSDK(**context.sdk_init_kwargs)
        return self.success(sdk=sdk)

    def fetch_books(self, context):
        """
        Метод получения книг автора. Вызывает необходимый метод SDK.

        :param context: Контекст выполнения сервиса.
        :return:
            fail - Если в процессе получения книг вылетает ошибка SDKException - необходимо завершить сервис,
            т.к. дальнейшая обработка не имеет смысла. Здесь используется fail как пример, для логирования того,
            что прозошло.
            success - если всё ок. Передает дальше полученный от SDK список книг автора.
        """
        try:
            books = context.sdk.fetch_books(author_id=context.author.id)
        except SDKException as exc:
            return self.fail(exc)

        return self.success(books=books)

    def make_books(self, context):
        """
        Метод формирования списка объектов БД на основе полученного в предыдущем методе списка книг.

        :param context: Контекст выполнения сервиса.
        :return:
            success - если всё ок. Передает дальше список объектов книг автора.

        """
        books = []
        for book in context.books:
            books.append(
                Book(**book),
            )

        return self.success(book_objects=books)

    def create_books(self, context):
        """
        Метод сохранения в БД книг автора. Использует bulk_create для уменьшения количества запросов к БД,
        передавая в него список объектов книг, подготовленный предыдущим методом.

        :param context: Контекст выполнения сервиса.
        :return:
            success - если всё ок. Не передает дальше никаких данных.

        """
        Book.objects.bulk_create(context.book_objects)
        return self.success()

    def __call__(self, author: User):
        """
        Основной метод, который вызывается для работы сервиса. Передает все входящие данные в метод success для 
        формирования начального контекста, который будет передаваться и наполняться от метода к методу.
        
        :param author: Объект пользователя, чьи книги необходимо получить.
        :return: результат работы последнего выполненного метода. Если сервис отработал без ошибок - результат его 
            работы - это результат работы последнего вызванного метода (create_books). Если в процессе работы была 
            ошибка - эта ошибка и будет возвращена.
        """
        return self.success(author=author) | \
               self.prepare_sdk_init_kwargs | \
               self.set_sdk | \
               self.fetch_books | \
               self.make_books | \
               self.create_books

```

### Пример вызова:
```python
""" Инициализация класса сервиса """
service: UpdateBooksService = UpdateBooksService()

""" Вызов класса сервиса """
result: Union[Ok, Error] = service(
    author=some_user,
)

if result.is_error():
    """
    Результат Error возвращается, когда сервис завершился с ошибкой. Объект ошибки (то что передано в метод 
    fail/fail_with доступно через атрибут error результата.
    
    """
    
    print(result.error)
    
elif result.is_ok():
    """
    Результат Ok возвращается, когда сервис завершился без ошибок. Весь контекст работы сервиса, в этом случае, 
    доступен через атрибут value результата.

    """
    
    books = result.value.book_objects
    """ теперь в переменной books находится список объектов книг, который в процессе выполнения сервиса сформировал 
    метод make_books """
    print(books)
```