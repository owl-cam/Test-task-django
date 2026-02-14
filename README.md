# Тестовое задание

Django-приложение для управления мероприятиями.

## Стек

- Python 3.14
- Django 5.2
- PostgreSQL 17
- django-ninja (API)
- django-jazzmin (админка)
- django-imagekit (обработка изображений)

## Запуск в Docker

1. Создайте файл `src/.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_HOST=db_test
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
DATABASE_URL=postgresql://postgres:your-password@db_test:5432/postgres
```

2. Запустите контейнеры:

```bash
docker compose up --build -d
```

3. Примените миграции и создайте суперпользователя:

```bash
docker exec -it test-server python manage.py migrate
docker exec -it test-server python manage.py createsuperuser
```

Приложение будет доступно по адресу http://localhost:8000

## Локальный запуск

### Требования

- [uv](https://docs.astral.sh/uv/) — менеджер пакетов
- PostgreSQL 17

### Установка

1. Клонируйте репозиторий:

```bash
git clone <url>
cd testovoe
```

2. Создайте файл `src/.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_HOST=localhost
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
DATABASE_URL=postgresql://postgres:your-password@localhost:5432/postgres
```

3. Установите зависимости:

```bash
cd src
uv sync
```

4. Примените миграции и создайте суперпользователя:

```bash
uv run manage.py migrate
uv run manage.py createsuperuser
```

5. Запустите сервер:

```bash
uv run manage.py runserver
```

Приложение будет доступно по адресу http://localhost:8000
