# praktikum_new_diplom

http://127.0.0.1:8000/api/users/  Post-запрос (email, username, password) создать юзера

http://127.0.0.1:8000/api/auth/token/login  Post-запрос (username, password) получить токен



cd foodgram-project-react
создать файл .env c переменными окружения.

Запуск контейнера:

docker-compose up -d

Заполнение базы данными:

sudo docker-compose exec backend python manage.py collectstatic --no-input

sudo docker-compose exec backend python manage.py makemigrations --noinput

sudo docker-compose exec backend python manage.py migrate --noinput

sudo docker-compose exec backend python manage.py createsuperuser

sudo docker-compose exec backend python manage.py loader