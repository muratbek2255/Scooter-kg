Scooter-KG Django
Каршеринг скутеров и велосипедов на Django Rest Framework.

Стек:

Python >= 3.9
Django Rest Framework
Postgres

Старт
1) Создать образ
docker-compose build
2) Запустить контейнер
docker-compose up
3) Перейти по адресу
http://127.0.0.1:8000/api/v1/swagger/
Разработка с Docker
4) Сделать форк репозитория
5) Клонировать репозиторий
git clone ссылка_сгенерированная_в_вашем_репозитории
6) В корне проекта создать .env
DEBUG=1
SECRET_KEY=secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Data Base
POSTGRES_DB=example(postgres)
POSTGRES_ENGINE=example(django.db.backends.postgresql)
POSTGRES_DATABASE=example(postgres)
POSTGRES_USER=example(postgres)
POSTGRES_PASSWORD=example(postgres)
POSTGRES_HOST=example(db)
POSTGRES_PORT=example(db)
DATABASE=postgres

# Email
DEFAULT_FROM_EMAIL=your@your.com
EMAIL_USE_TLS=True
EMAIL_HOST=your_smtp
EMAIL_HOST_USER=your@your.com
EMAIL_HOST_PASSWORD=pass
EMAIL_PORT=587

7) Создать образ
docker-compose build
8) Запустить контейнер
docker-compose up
9) Создать суперюзера
docker exec -it your project python manage.py createsuperuser
10) Если нужно очистить БД
docker-compose down -v
