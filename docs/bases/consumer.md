`backend.project.ws_v1.consumer.Consumer`

Класс, который обслуживает каждое `Web Socket` подключение. Для каждого нового подключения создается новый экземпляр класса `Consumer`, который обрабатывает как входящие сообщения, так и сообщения, которые необходимо отправить в канал.

Все классы-консьюмеры в процессе работы раскидываются по группам, и для отправки сообщения в сокет необходимо отравить сообщение в группу. Таким образом все обработчики, подключенные к этой группе получат сообщение, и, при необходимости, отправят это сообщение в канал.

### Группы подключений и отправка сообщений в них

![Screenshot from 2023-03-07 10-53-24](https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/f0352116-aaa3-4817-92f7-27d559915c22)

На данной схеме изображен процесс подключения пользователей к `WS`. Здесь 2 пользователя (Вася и Петя) подключаются к сокету, причем Вася создает сразу несколько подключений.
При подключении каждый авторизованный пользователь сразу же добавляется в группу конкретного пользователя (на схеме для понимания эти группы называются `ws_group_vasya` и `ws_group_petya`, на практике же такие группы должны называться по неким уникальным и неизменным параметрам, например идентификатор пользователя в БД: `user_1`, `user_213`).

![Screenshot from 2023-03-07 11-02-40](https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/68fc6f12-3313-4545-a11e-dee4ab927905)

Каждое подключение по каналу `ws` может быть добавлено одновременно в несколько групп. На данной схеме представлена ситуация, когда 2 подключения разных пользователей добавлены в общую группу по некому признаку - для примера, на схеме изображена группа `ws_project_main`. Количество и типы групп сокет подключений зависят от проекта, и в основном завязаны на основные сущности проекта.

![Screenshot from 2023-03-07 11-12-31](https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/dded38ff-af74-4cfd-9b64-5c0c6d527bdb)

На этой схеме изображена ситуация с группировкой подключений в [реальном проекте]().
В этом проекте используется 3 вида групп:
* `all` - общая группа, в которую попадает каждое подключение в момент создания. Нужна для отправки сообщение всем 
(например массовое уведомление; новая/измененная/удаленная сущность, с которой работает каждый).
* `user_<user_id>` - группа пользователя. В эту группу подключение попадает так же при создании. Группа нужна для 
  отправки сообщения в канал конкретного пользователя.
* `note_<note_id>` - группа записи. В эту группу подключение попадает по запросу от клиента. Специфика проекта такая, 
  что клиентская часть при работе с сущностью "запись" отправляет в сокет запрос на открытие этой "записи", и `consumer`, обрабатывающий это подключение, добавляет себя в группу `note_<note_id>`. Таким образом все, кто на данный момент работает с это "записью" получат все сообщения, отправленные в эту группу. **Важно - когда пользователь завершает работу с "записью", так же необходимо, чтобы клиентская часть сообщила об этом классу-консьюмеру, чтобы он перестал получать и обрабатывать сообщения, связанные с этой записью.**


### Отправка сообщение в группу сокет-подключений:
```python
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

CHANNEL_LAYER = get_channel_layer()

async_to_sync(CHANNEL_LAYER.group_send)(
    group="user_1",
    message={
        "type": "send_notify",
        "data": {
            "message": "Test message",
            "status": "info",
        },
    },
)
```
Что происходит при выполнении этого кода?
1. Вычисляется список всех экземпляров класса `Consumer`, которые подключены к группе `user_1`.
2. У каждого из них вызывается метод `dispatch`, который принимает словарь `message`.
3. Вычисляется название метода обработчика сообщения на основе значения ключа `type`.
4. Вызывается метод класса `Consumer`, название которого было вычислено на предыдущем шаге - это метод `Consumer.send_notify`. Этому методу передается распакованный словарь `message`.
5. Метод выполняет необходимую логику формирования и отправки сообщения в сокет.

Для упрощения отправки сообщения в сокет был добавлен метод `send_to_socket_group`, благодаря которому то же сообщение можно отправить куда проще:
```python
send_to_socket_group(
    group_name="user_1",
    event="send_notify",
    message="Test message",
    status="info",
)
```

### Базовые атрибуты:
* `__user` - объект пользователя, подключение которого обрабатывается

### Базовые методы:
* `__add_group` - добавить себя в группу с названием `name`.
* `__discard_group` - удалить себя из группы с названием `name`.
*`connect` - метод, который обрабатывает сообщение о подключении к сокету. Внутри этого метода необходимо принять 
  подключение пользователя (`self.accept()`) или отклонить его (`self.close()`)
* `disconnect` - метод, который вызывается при отключении от сокета.
* `receive_json` -  диспетчер, обрабатывающий входящий `json`, содержащий `event` (по которому определяется какой 
  метод надо запустить для обработки этого сообщения) и словарь `data` (содержит данные для обработки сообщения).
* `process_message` - метод обработки события `event`.  Ищет среди методов класса метод с названием `event`, вызывает 
  его, передавая внутрь данные `data`. Если метод обработки завершился с ошибкой - отправляет в сокет сообщение `Request error`. Если метод обработки завершился без ошибок, но вернул текст - отправляет этот текст в сокет.
* `dispatch` - метод обработки сообщения, которое необходимо отправить в сокет. Находит нужный метод класса 
  `consumer`, вызывает этот метод, передавая ему данные из сообщения.
* `send_data` - метод отправки данных в подключение.
* `send_notify` - метод отправки в сокет уведомления.

<div align="center">
  
  [⇜ Базовые классы: ServiceObject](service-object.md)
</div>
