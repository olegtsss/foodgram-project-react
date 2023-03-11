# Cсылка на развернутый проект

https://yandex.olegtsss.ru

# Описание проекта Foodgram

Cайт Foodgram, «Продуктовый помощник» - это онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Используемые технологии

Python 3.7, Django 2.2, Django ORM, Django REST Framework, Postgresql

## Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/olegtsss/foodgram-project-react.git
cd foodgram-project-react
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
. venv/Scripts/activate
```

- Обновить менеджер пакетов:

```
python -m pip install --upgrade pip
```

- Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python backend/foodgram/manage.py migrate
```

- Загрузить ингридиенты в базу:

```
python backend/foodgram/manage.py import_into_db
```

- Запустить проект:

```
python backend/foodgram/manage.py runserver
```

## Как собрать и запустить проект в контейнерах:
- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/olegtsss/foodgram-project-react.git
cd foodgram-project-react/infra
```

- Запуск приложения в контейнерах:

```
docker-compose up -d
```

- Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

- Cоздать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

- Cобрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

- Загрузить ингридиенты в базу:

```
docker-compose exec web python manage.py import_into_db
```

## Как пересобрать frontend:
- Удаляем старый frontend:

```
rm -rf frontend/build
```

- Переходим в папку с кодом:

```
cd front_standalone/
```

- Сбор и запуск приложения в контейнерах:

```
docker-compose up -d
```

- Перенести новый frontend в проект:

```
mkdir ../frontend/build
cp -R frontend/build/ ../frontend/build/
```

- Остановка контейнеров:

```
docker-compose stop
```

## Настроены эндпоинты:

```
    api/users/ (GET, POST): список и регистрация пользователей
    api/users/{id}/ (GET): профиль пользователя
    api/users/me/ (GET): текущий пользователь
    api/users/set_password/ (POST): изменение пароля пользователя
    api/auth/token/login/ (POST): получение токена авторизации
    api/auth/token/logout/ (POST): удаление токена авторизации
    api/tags/ (GET): список тегов
    api/tags/{id}/ (GET): получение тега
    api/recipes/ (GET, POST): список или создание рецептов
    api/recipes/{id}/ (GET, PATCH, DELETE): получение, обновление или удаление рецепта
    api/recipes/download_shopping_cart/ (GET): список покупок
    api/recipes/{id}/shopping_cart/ (POST, DELETE): добавление или удаление рецепта из списка покупок
    api/recipes/{id}/favorite/ (POST, DELETE): добавление или удаление рецепта из избранного
    api/users/subscriptions/ (GET): мои подписки
    api/users/{id}/subscribe/ (POST, DELETE): подписаться или отписаться от пользователя
    api/ingredients/ (GET): список ингредиентов
    api/ingredients/{id}/ (GET): получение ингредиента
```

## Примеры запросов:

```
    GET http://127.0.0.1:8000/api/users/?limit=2

    POST http://127.0.0.1:8000/api/auth/token/login/
    Content-Type: application/json

    {
        "password": "secret",
        "email": "secret@secret.secret"
    }

    POST http://127.0.0.1:8000/api/users/set_password/
    Content-Type: application/json
    Authorization: Token secret

    {
        "new_password": "123",
        "current_password": "321"
    }

    GET http://127.0.0.1:8000/api/ingredients/?search=абрикосовый

    GET http://127.0.0.1:8000/api/recipes/?is_favorited=1
    Authorization: Token secret

    GET http://127.0.0.1:8000/api/recipes/?is_in_shopping_cart=1
    Authorization: Token secret

    POST http://127.0.0.1:8000/api/recipes/
    Content-Type: application/json
    Authorization: Token secret

    {
        "ingredients": [
            {
                "id": 1123,
                "amount": 14
            }
        ],
        "tags": [
            1,
            2
        ],
        "image": "data:image/png;base64,iVB...g==",
        "name": "string",
        "text": "string",
        "cooking_time": 1
    }

    DELETE http://127.0.0.1:8000/api/recipes/5/favorite/
    Authorization: Token secret

    GET http://127.0.0.1:8000/api/users/subscriptions/?recipes_limit=1&limit=1
    Authorization: Token secret
```

## Документация к API:

```
    https://yandex.olegtsss.ru/api/docs/
```

## Шаблон наполнения env-файла:

```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='secret'
DEBUG=False
ALLOWED_HOSTS='foodgram.olegtsss.ru'
NEED_SQLITE=False
```

# Разработчики

[olegtsss](https://github.com/olegtsss): backend

[yandex](https://ya.ru): frontend

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgresql](https://img.shields.io/badge/%D0%91%D0%B0%D0%B7%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-postgresql-brightgreen?style=for-the-badge)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=whte)
