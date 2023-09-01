`backend.project.utils.eager_loading_mixin.EagerLoadingMixin`

Класс-примесь для использования в сериализаторах `DRF`.

### Атрибуты:

* `select_related` - список объектов, используемых для вызова метода `select_related` при построении запроса на 
выборку объектов из БД.
* `prefetch_related` - список объектов, используемых для вызова метода `prefetch_related` при построении запроса на 
  выборку объектов из БД.
* `annotate` - словарь объектов, используемых для вызова метода `annotate` при построении запроса на выборку объектов 
  из БД.
* `aggregate` - словарь объектов, используемых для вызова метода `aggregate` при построении запроса на выборку 
  объектов из БД.

### Методы:

* `many_init` - переопределенный метод класса сериализатора. Вызывается внутри сериализатора для обработки множества 
объектов. Данный метод переопределен для добавления связей в запрос к БД.
* `setup_eager_loading` - основной метод переопределения запроса для выборки.