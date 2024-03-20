# ПРОЕКТ YATUBE

## ОПИСАНИЕ
Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять и удалять комментари к постам, оставлять новые посты на главной странице и в тематических группах.

## ЗАПУСК ПРОЕКТА ЛОКАЛЬНО
1. клонировать репозиторий
```sh
git clone git@github.com:monteg179/yatube.git
cd yatube
```

2. создать файл .env, например, с таким содержанием
```
DJANGO_SUPERUSER_USERNAME=admin1
DJANGO_SUPERUSER_EMAIL=admin1@example.com
DJANGO_SUPERUSER_PASSWORD=12345
DJANGO_SECRET_KEY=secretkey
POSTGRES_DB=yatube
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

3. создать и запустить контейнеры docker
```sh
sudo bash setup.sh install
```

После запуска проект будет доступен по адресу:
`http://localhost:8000/`

Удалить установленные контейнеры doker можно командой:
```sh
sudo bash setup.sh uninstall
```

## ДЛЯ РАЗРАБОТКИ
1. клонировать репозиторий
```sh
git clone git@github.com:monteg179/yatube.git
cd yatube_project
```

2. создать файл .env, например, с таким содержанием
```
DJANGO_SUPERUSER_USERNAME=admin1
DJANGO_SUPERUSER_EMAIL=admin1@example.com
DJANGO_SUPERUSER_PASSWORD=12345
DJANGO_SECRET_KEY=secretkey
DJANGO_DEBUG=True
POSTGRES_DB=yatube
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
```

3. запустить контейнер docker СУБД
```sh
sudo service docker start
sudo docker image build -t yatube_database database
sudo docker container create --name database --env-file .env -p 5432:5432 yatube_database
sudo docker container start database
```
3. инициализация
```sh
poetry install
poetry shell
python django/manage.py migrate
python django/manage.py superuser
python django/manage.py import_db django/data/leo
```
4. запуск
```sh
uvicorn --app-dir django yatube.asgi:application --reload
```

## ИСПОЛЬЗОВАНИЕ

### эндпоинты

- админка:
`http://localhost:8000/admin/`

- регистрация пользователя:
`http://localhost:8000/users/signup/`

- вход пользователя:
`http://localhost:8000/users/signin/`

- выход пользователя: 
`http://localhost:8000/users/signout/`

- список постов автора:
`http://localhost:8000/users/profile/<username>/`

- подписаться на автора:
`http://localhost:8000/users/profile/<username>/follow/`

- отменить подписку на автора:
`http://localhost:8000/users/profile/<username>/unfollow/`

- список всех постов:
`http://localhost:8000/`

- список постов, относящихся к группе:
`http://localhost:8000/group/<slug>/`

- список постов авторов, на которых подписан текущий пользователь:
`http://localhost:8000/posts/follow/`

- детальная информация о посте:
`http://localhost:8000/posts/<post_id>/`

- создание поста:
`http://localhost:8000/posts/create/`

- обновление поста:
`http://localhost:8000/posts/<post_id>/edit/`

- создание комментария к посту:
`http://localhost:8000/posts/<post_id>/comment/`

## ИСПОЛЬЗОВАННЫЕ ТЕХНОЛОГИИ

- Python
- Django
- Postgres
- Nginx
- Docker

## АВТОРЫ
* Сергей Кузнецов - monteg179@yandex.ru
