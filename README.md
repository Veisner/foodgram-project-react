# praktikum_new_diplom

![Foodgram_workflow](https://github.com/Veisner/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

http://127.0.0.1:8000/api/users/  Post-запрос (email, username, password) создать юзера

http://127.0.0.1:8000/api/auth/token/login  Post-запрос (username, password) получить токен


создать файл .env c переменными окружения.

Запуск контейнера:

docker-compose up -d

Миграции:

sudo docker compose exec web python manage.py makemigrations users --noinput

sudo docker compose exec web python manage.py makemigrations recipes --noinput

sudo docker compose exec web python manage.py migrate --noinput

Сбор статики:

sudo docker compose exec web python manage.py collectstatic --no-input

Заполнение базы данными:

sudo docker compose exec web python manage.py loader

Суперюзер:

sudo docker compose exec web python manage.py createsuperuser
