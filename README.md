# Продуктовый помощник Foodgram.

Данный проект выполняется для курса Python-разработчик от Яндекс.Практикума

## Статус
![Foodgram_workflow](https://github.com/Veisner/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)



Проект развернут по адресу: http://130.193.41.109/

## Описание сервиса

Онлайн-сервис и API для него. Проект Продуктовый помощник - это сайт, который позволяет пользователям публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов, а также создавать и скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.


## После каждого обновления репозитория запускается:

 * Проверка кода на соответствие стандарту PEP8 (flake8)
 * Сборка и доставка образа на Docker Hub
 * Деплой образов на ВМ
 * Запуск контейнеров
 * Отправка уведомления в Telegram


## Регистрация и авторизация
В сервисе предусмотрена система регистрации и авторизации пользователей.
Обязательные поля для пользователя:
<li> Логин
<li> Пароль
<li> Email
<li> Имя
<li> Фамилия

## Права доступа к ресурсам сервиса

### неавторизованные пользователи могут:

    - создать аккаунт;
    - просматривать рецепты на главной;
    - просматривать отдельные страницы рецептов;
    - фильтровать рецепты по тегам;

### авторизованные пользователи могут:

    - входить в систему под своим логином и паролем;
    - выходить из системы (разлогиниваться);
    - менять свой пароль;
    - создавать/редактировать/удалять собственные рецепты;
    - просматривать рецепты на главной;
    - просматривать страницы пользователей;
    - просматривать отдельные страницы рецептов;
    - фильтровать рецепты по тегам;
    - работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов;
    - работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок;
    - подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок;

### администратор
Администратор обладает всеми правами авторизованного пользователя.
<br> Плюс к этому он может:

    - изменять пароль любого пользователя;
    - создавать/блокировать/удалять аккаунты пользователей;
    - редактировать/удалять любые рецепты;
    - добавлять/удалять/редактировать ингредиенты;
    - добавлять/удалять/редактировать теги.


### Суперпользователь:

* ### Email: admin@mail.ru
* ### Password: admin


### Документация к API:

http://130.193.41.109/api/docs/







создать файл .env c переменными окружения.


Запуск контейнера:

sudo docker compose up -d

Миграции:

sudo docker compose exec backend python manage.py makemigrations users --noinput

sudo docker compose exec backend python manage.py makemigrations recipes --noinput

sudo docker compose exec backend python manage.py migrate --noinput

Сбор статики:

sudo docker compose exec backend python manage.py collectstatic --no-input

Заполнение базы данными:

sudo docker compose exec backend python manage.py loader

Суперюзер:

sudo docker compose exec backend python manage.py createsuperuser


