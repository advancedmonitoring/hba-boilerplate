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

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Advanced Monitoring HBA](https://img.shields.io/badge/AM-HBA-orange)](https://amonitoring.ru/)

[Введение](#введение) •
[Особенности](#особенности) •
[Настройка установки](#настройка-установки) •
[Установка](#установка) •
[Что дальше](#что-дальше)
</div>

## Введение

![render1693392090674-min](https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/c8b055ed-4ab3-4ad5-90cd-925f7cd9f7f5)

`HBA` архитектура создана, чтобы помочь разработчикам сосредоточится на бизнес-логике. Каждое приложение 
на основе данной архитектуры имеет простой и понятный процесс валидации, проверки, и обработки запроса из любого 
интерфейса.

Архитектура использует метод доставки данных конечному пользователю с помощью сокет соединения, поэтому каждое
приложение получается полностью интерактивным порталом, достаточно лишь придерживаться простых правил при написании
кода.

В последствии, если Вы будете придерживаться единообразия в написании кода, у Вас будет легко расширяемое приложение
с прозрачной логикой, где каждый модуль занимается своей задачей: валидация, проверка прав, проверка логики,
реализация логики, отображение.

## Особенности

<p align="center">
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/e912289a-cb18-405a-93fb-a13a824ebd14" alt="api-ws"/>
&nbsp;
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/73e231b0-8850-45a8-9a36-6b7ef20478d5" alt="low-fw-rel"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/69b7dbc8-c9d0-486b-ae53-2e6b269052f6" alt="result"/>
&nbsp;
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/786b13a8-9c6c-4603-b1ad-b5dfc47c1580" alt="done"/>
</p>

<p align="center">
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/21898bf1-caff-4bd5-ae70-b05ffffe5f0f" alt="docs"/>
&nbsp;
    <img width="49%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/67782d02-9f5e-4b21-af8c-cfccd73229a5" alt="ws-docs"/>
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
самостоятельно — этот шаг лучше так же закомментировать.

* `install_dependencies`

Установка зависимостей для локальной разработки `requirements/local.txt`. Этот шаг так же можно отключить, если Вы
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
