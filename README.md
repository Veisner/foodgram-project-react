# praktikum_new_diplom

Данный проект выполняется для курса Python-разработчик от Яндекс.Практикума

![Foodgram_workflow](https://github.com/Veisner/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

# Продуктовый помощник Foodgram.

Проект развернут по адресу: http://130.193.41.109/

## Описание сервиса

Проект Продуктовый помощник - это сайт, который позволяет пользователям публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов, а также создавать и скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.


## После каждого обновления репозитория запускается:

 * Проверка кода на соответствие стандарту PEP8 (flake8)
 * Сборка и доставка образа на Docker Hub
 * Деплой образов на ВМ
 * Запуск контейнеров
 * Отправка уведомления в Telegram

## Данные для входа:

### Суперпользователь:

* ### Email: admin@mail.ru
* ### Password: admin

Документация:

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


