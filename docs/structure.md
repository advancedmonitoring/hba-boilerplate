### Базовая структура

```
🗂 { project root }
    🗂 { project }
        🗂 interface_v{ version }
            🗂 { app }
                📄 urls.py
                📄 serializers.py
                📄 views.py
        🗂 { app }
            🗂 handlers
                🗂 { entity }
                    📄 create.py
                    📄 get.py
                    📄 update.py
                    📄 delete.py
            🗂 services
                🗂 { entity }
                    📄 create.py
                    📄 update.py
                    📄 delete.py
            🗂 signals
                📄 signals.py
                📄 handlers.py
            📄 models.py
        🗂 permissions
            📄 permissions.py
    🗂 config
        🗂 settings
            📄 base.py
            📄 local.py
            📄 production.py
        📄 urls.py
    🗂 requirements
        📄 base.txt
        📄 dev.txt
        📄 production.txt
    📄 manage.py
```

### 🗂 { project root }

Корень проекта. Тут содержаться общие для всего проекта файлы: запуск, настройка редактора, настройки гита и дополнительных библиотек. Так же в корне содержаться папки/пакеты, содержащие настройки проекта, приложения проекта, настройки CI/CD.



### 🗂 { project }

Основная пакет, содержащий приложения. Название обычно совпадает с названием проекта. Вся логика проекта содержится в этом пакете.



### 🗂 interface_v{ version }

Приложение, реализующее интерфейс взаимодействия с проектом. Должно содержать только логику обработки запроса/формирования ответа согласно протоколу интерфейса. Не должно содержать бизнес-логику проекта.



Обязательный интерфейс (представлен в структуре папок сверху) - `REST Api`. Внутри этого интерфейса логику удобно разделять по сущностям/приложениям.



### 🗂 { app }

Стандартное приложение `django` проекта. Обычно содержит логически связанные сущности проекта. Кроме стандартных модулей, созданных `django`, содержит пакеты и модули работы с сущностями приложения.



### 🗂 handlers

Каждое приложение (содержащее сущности с которыми можно взаимодействовать пользователю), содержит набор обработчиков для CRUD операций с сущностями. Если приложение содержит много сущностей - обработчики тоже удобно делить по разным пакетам.



В структуре папок сверху пакет `handlers` содержит 4-е обработчика для сущности `{ entity }` - по одному для каждой `CRUD` операции.



### 🗂 services

Для каждого обработчика `CUD` операций сущности должен быть создан сервис создания, изменения, удаления сущности. Для получения сущности/списка сущностей сервис обычно не требуется, т.к. нет изменения данных БД.



### 🗂 signals

Данная архитектура предполагает выполнение дополнительных операций внутри обработчиков сигнала после работы с сущностями. Все нестандартные сигналы и обработчики этих сигналов должны быть расположены в пакете `signals` приложения.



### 🗂 permissions

Приложение, содержащее модули, в котором происходят все проверки возможности выполнения запроса пользователем. Все проверки ролевой системы должны быть в этом приложении.



### 🗂 config

Вместо использования стандартно созданного модуля настроек `django` (`settings.py`) настройки проекта разделены на несколько модулей - базовые/настройки для боевого режима запуска/настройки для локальной разработки. Такой подход позволяет проще следить за настройками в разных режимах и вести локальную разработку, просто настроив настройки "под себя" в файле `local.py`, которые не будут мешать другим разработчикам.



### 🗂 requirements

Папка с зависимостями проекта. Все зависимости, как и настройки, лучше разделять на несколько файлов на основе режима запуска. Такой подход позволяет избавиться от dev-пакетов на боевом сервере.