`backend.project.utils.handler_validation_mixin.ValidationMixin`

Класс-примесь для добавления возможности валидации и очистки данных.

### Атрибуты:

* `validated_data` - объект, который содержит провалидированные данные. До запуска валидации имеет тип `None`, после 
`Dict`.

### Методы:

* `validate` - основной метод, который необходимо вызвать в классе, для запуска валидации. Принимает любое количество 
именованных аргументов для валидации.



Пример использования:



```python
class Foo(ValidationMixin):
    def __init__(self, name: str, age: int):
        self.validate(name=name, age=age)

    def _clean_name(self, name: str) -> str:
        return "Cleaned name: %s" % name

    def _clean_age(self, age: int) -> int:
        if age < 18:
            raise SomeException('Denied')
        return age

foo = Foo(name="Vasya", age=20)
print(foo.validated_data)
# { "name": "Cleaned name: Vasya", "age": 20 }
```

Как видно, миксин не реализует логику валидации и очистки самостоятельно, он лишь предоставляет интерфейс для её реализации. Каждый метод должен вернуть очищенное значение, либо породить ошибку, которую необходимо обработать самостоятельно.



В нашей архитектуре данный миксин используется (в основном) для обработчиков (`Handler`). В этом случае, внутри методов очистки удобно порождать исключение самого обработчика (есть у каждого из них), которое автоматически отваливается на уровне `View`.

<div align="center">
    
  [⇜ Базовые классы: EagerLoadingMixin](eager-loading.md)
  •
  [Базовые классы: SignalMixin ⇝](signal-mixin.md)
</div>
