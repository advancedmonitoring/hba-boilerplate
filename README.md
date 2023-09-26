<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

<div align="center">
  <h6 align="center">
    <a href="https://amonitoring.ru/#gh-light-mode-only">
    <img width="20%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/9522302b-bd18-47c8-961d-e1da3cfddd80">
    </a>
    <a href="https://amonitoring.ru/#gh-dark-mode-only">
    <img width="20%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/0aad4d95-9a59-45e9-ab92-29cd8708e7a5">
    </a>
  </h6>

# Handler Based Arch Boilerplate

Шаблон позволяет быстро запустить новый проект на основе **HBA** архитектуры

Данная архитектура дает возможность быстрой разработки высоко-интерактивного <br/>`клиент - серверного` приложения

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3110/)
[![Advanced Monitoring HBA](https://img.shields.io/badge/AM-HBA-orange?style=flat-square)](https://amonitoring.ru/)
[![GitHub Demo App](https://img.shields.io/badge/GitHub-Demo-orange?style=flat-square)](https://github.com/advancedmonitoring/hba-demo-todo-app)
[![Telegram channel](https://img.shields.io/badge/Telegram%20Channel-2ba4df?style=flat-square&logo=telegram)](https://t.me/+ykplVtIK-0tmZGUy)

[Введение](#введение) •
[Особенности](#особенности) •
[Настройка установки](#настройка-установки) •
[Установка](#установка) •
[Что дальше](#что-дальше)
</div>

## Введение

![setupGif](https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/c8b055ed-4ab3-4ad5-90cd-925f7cd9f7f5)

`HBA` архитектура создана, чтобы помочь разработчикам сосредоточится на бизнес-логике. Каждое приложение 
на основе данной архитектуры имеет простой и понятный процесс валидации, проверки и обработки запроса из любого 
интерфейса.

Архитектура использует метод доставки данных конечному пользователю с помощью сокет соединения, поэтому каждое
приложение получается полностью интерактивным порталом, достаточно лишь придерживаться простых правил при написании
кода.

В последствии, если Вы будете придерживаться единообразия в написании кода, у Вас будет легко расширяемое приложение
с прозрачной логикой, где каждый модуль занимается своей задачей: валидация, проверка прав, проверка логики,
реализация логики, отображение.

## Особенности

<p align="center">
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/aaf79e3b-ba3b-4326-ac7d-afb562132c1b" alt="api-ws"/>
&nbsp;
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/7967f48f-0b06-4c4b-af53-a2cb5b8df429" alt="low-fw-rel"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/b383e02f-062e-4f6e-a12a-3a511074f196" alt="result"/>
&nbsp;
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/9a1a5997-df27-4b72-b03e-5dc33191350c" alt="done"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/5597357e-bca9-41bb-943f-fbe58deae0f0" alt="docs"/>
&nbsp;
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/ed176a00-f65f-43c5-9191-dd929bf1061e" alt="ws-docs"/>
</p>

## Настройка установки

Скрипт `setup.sh` содержит ряд команд, которые выполняются последовательно:

* `update_project_files`

На данном шаге происходит обновление файлов проекта: изменение название папки с приложениями, изменение путей импорта
внутри файлов, создание локального файла настроек. Данный шаг является __обязательным__, отключать его не рекомендуется.

* `create_virtualenv`

Шаг создания виртуального окружения. В скрипте используется команда `python3.10 -m venv ENV`. Вы можете изменить
версию `python`, изменить название виртуального окружения, или отменить создание окружения и сделать это
самостоятельно после настройки проекта.

* `activate_virtualenv`

Этот шаг лишь активирует созданное ранее виртуальное окружение. Если Вы решите создать виртуальное окружение
самостоятельно — этот шаг лучше также закомментировать.

* `install_dependencies`

Установка зависимостей для локальной разработки `requirements/local.txt`. Этот шаг также можно отключить, если Вы
устанавливаете и настраиваете виртуальное окружение самостоятельно.

* `print_tutorial`

Просто показывает дальнейшие шаги.

* `remove_extra_data`

Данный шаг удаляет временные файлы (файл установки проекта, папку .git)

Если на любом из шагов возникли проблемы — Вы всегда можете начать сначала 🙂

## Установка

```bash
git clone https://github.com/advancedmonitoring/hba-boilerplate.git ./название_проекта
cd ./название_проекта
./setup.sh my_awesome_project
```

После выполнения команды в текущей директории будет находиться готовый к использованию проект.

## Что дальше?

### Backend

Первое, что нужно сделать дальше — активировать виртуальное окружение. Если в процессе установки Вы отключили
автоматическое создание окружения — создайте его самостоятельно, активируйте и установите необходимые зависимости.

Следующий шаг — применение миграций БД (`python manage.py migrate`). По умолчанию проект использует SQLite в качестве
базы данных, которого должно быть достаточно для начала разработки.

> Рекомендуется как можно раньше заменить БД на ту, которую Вы будете использовать в боевом режиме. В шаблоне же
> используется БД, которая не требует дополнительных системных зависимостей.

После применения миграций - создайте первого пользователя-администратора с помощью `python manage.py createsuperuser`.

На этом всё, сервер можно запустить `python manage.py runserver`.

### Frontend

Откройте новую вкладку терминала и перейдите в директорию `frontend`.

> По умолчанию в проекте настроено Vue-приложение, но никаких ограничений на frontend фреймворки
> нет - Вы можете перенести логику работы с данными на любой стек.

Если Вы решите оставить текущий фреймворк - достаточно установить зависимости (`npm install`) и запустить
frontend сервер (`npm run serve`).

## Документация
* [Введение](docs/about.md)
* [Глоссарий](docs/glossary.md)
* [Порядок обработки запроса](docs/request-pipeline.md)
* [Структура проекта](docs/structure.md)
* Базовые классы
  * [EagerLoadingMixin](docs/bases/eager-loading.md)
  * [ValidationMixin](docs/bases/validation-mixin.md)
  * [SignalMixin](docs/bases/signal-mixin.md)
  * [BaseDataHandler](docs/bases/data-handler.md)
  * [BaseHandler](docs/bases/handler.md)
  * [EventPermissions](docs/bases/event-permissions.md)
  * [HandlerView](docs/bases/base-handler-view.md)
  * [ServiceObject](docs/bases/service-object.md)
  * [Consumer](docs/bases/consumer.md)


## Участники

<a href="https://github.com/kiselas"><img src="https://avatars.githubusercontent.com/u/70576848?v=4" title="kiselas" width="50" height="50"></a>
<a href="https://github.com/hpawa"><img src="https://avatars.githubusercontent.com/u/45428746?v=4" title="hpawa" width="50" height="50"></a>
<a href="https://github.com/Codek32"><img src="https://avatars.githubusercontent.com/u/9204414?v=4" title="codek32" width="50" height="50"></a>
<a href="https://github.com/Aleksey170999"><img src="https://avatars.githubusercontent.com/u/91157178?v=4" title="Aleksey170999" width="50" height="50"></a>
<a href="https://github.com/achievement008"><img src="https://avatars.githubusercontent.com/u/15703713?v=4" title="achievement008" width="50" height="50"></a>
<a href="https://github.com/sheremeev"><img src="https://avatars.githubusercontent.com/u/45734624?v=4" title="sheremeev" width="50" height="50"></a>
<a href="https://github.com/salykin"><img src="https://avatars.githubusercontent.com/u/2499169?v=4" title="salykin" width="50" height="50"></a>
<a href="https://github.com/Donnicool"><img src="https://avatars.githubusercontent.com/u/114762347?v=4" title="Donnicool" width="50" height="50"></a>
<a href="https://github.com/Vad1q"><img src="https://avatars.githubusercontent.com/u/66086848?v=4" title="Vad1q" width="50" height="50"></a>
<a href="https://github.com/IMegaMaan"><img src="https://avatars.githubusercontent.com/u/69349808?v=4" title="IMegaMaan" width="50" height="50"></a>
