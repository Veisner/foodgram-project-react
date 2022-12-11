# praktikum_new_diplom

![Foodgram_workflow](https://github.com/Veisner/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

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
