`backend.project.utils.signal_mixin.SignalMixin`

Класс-примесь для добавления возможности отправки сигнала о совершении действия.

### Атрибуты:

* `signal` - сигнал для отправки.
* `signal_sender` - отправитель сигнала.
* `_signal_prevented` - флаг, устанавливается для предотвращения отправки сигнала.

### Методы:

* `prevent_signal_send` - метод, необходимый для установки флага о том, что класс не должен отправлять сигнал.
* `_send_signal` - основной метод, который нужно вызвать когда необходимо отправить сигнал.
* `_inner_send_signal` - внутренний метод, через который происходит формирование данных для сигнала и его отправка. 
  Может быть вызван у объекта класса, а не у его экземпляра.
* `_get_signal_kwargs` - метод, который необходим для изменения аргументов для передачи в сигнал. Может быть 
  использован как для простого изменения ключей/значений аргументов, так и для реализации возможности отправки множества сигналов с разными аргументами. Для множества сигналов должен вернуть генератор, который возвращает словарь данных для отправки сигнала.
* `send_signal` - метод отправки сигнала. Устанавливает задачу как callback применения транзакции. Может быть вызван 
  у объекта класса, а не у его экземпляра.

Пример использования:

В этом примере происходит простая отправка сигнала с 2-мя аргументами.

```python
class Foo(SignalMixin):
    signal = some_signal
    signal_sender = SomeSender
    
    def main(self):
        ... some logic
        self._send_signal(name="Vasya", age=40)    
```

В результате будет отправлен 1 сигнал:

```python
some_signal.send(sender=SomeSender, name="Vasya", age=40)
```

Другой пример:

В этом примере используется всё тот же сигнал, но другие начальные данные. Как видно атрибут `age` - это список чисел, для каждого из которых необходимо отправить сигнал.

```python
class Foo(SignalMixin):
    signal = some_signal
    signal_sender = SomeSender

    def main(self):
        ... another some logic
        self._send_signal(name="Vasya", ages=[10, 20, 30])
    
    def _get_signal_kwargs(**kwargs):
        name = kwargs.get("name")
        ages = kwargs.get("ages")
        for age in ages:
            yield { "name": name, "age": age }
```

В результате будет отправлено 3 сигнала:

```python
some_signal.send(sender=SomeSender, name="Vasya", age=10)
some_signal.send(sender=SomeSender, name="Vasya", age=20)
some_signal.send(sender=SomeSender, name="Vasya", age=30)
```

<div align="center">
  
  [⇜ Базовые классы: ValidationMixin](validation-mixin.md)
  •
  [Базовые классы: BaseDataHandler ⇝](data-handler.md)
</div>
