# Тестовое задание

Django-приложение для управления мероприятиями.

## Стек

- Python 3.12
- Django 5.2
- PostgreSQL 17
- Redis 7
- django-ninja (REST API, JWT)
- Celery + Celery Beat (фоновые задачи)
- django-post-office (очередь email)
- django-constance (динамические настройки через admin)
- django-imagekit (обработка изображений)

## Архитектура

- **app_event** — CRUD мероприятий. Неавторизованные и обычные пользователи видят только опубликованные события.
- **app_event_place** — Площадки (название + координаты). Только суперпользователь.
- **app_weather** — Погода по площадкам. Обновляется через Celery каждый час.

### Фоновые задачи (Celery Beat)

| Задача | Расписание | Описание |
|---|---|---|
| `app_event.task.publish_scheduled_events` | каждые 5 минут | Публикует события, у которых `publish_date` наступил |
| `app_weather.task.update_weather` | каждый час | Обновляет погоду по всем площадкам |
| `proj.celery.send_queued_emails` | каждые 5 минут | Отправляет письма из очереди django-post-office |

При публикации события (переход `published=False → True`) автоматически уходит email-уведомление (настраивается через admin → Constance: `EMAIL_TO`, `EMAIL_SUBJECT`, `EMAIL_TEXT`).

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
WEATHER_API_KEY=your-weatherapi-key
EMAIL_BACKEND=post_office.EmailBackend
CELERY_BROKER_URL=redis://redis:6379/0
```

2. Запустите контейнеры:

```bash
docker compose up --build -d
```

3. Примените миграции и создайте суперпользователя:

```bash
docker exec -it test-server uv run manage.py migrate
docker exec -it test-server uv run manage.py createsuperuser
```

Приложение будет доступно по адресу http://localhost:8000

Docker запускает: сервер Django, PostgreSQL, Redis, Celery worker и Celery beat.

## Локальный запуск

### Требования

- [uv](https://docs.astral.sh/uv/) — менеджер пакетов
- PostgreSQL 17
- Redis

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
WEATHER_API_KEY=your-weatherapi-key
EMAIL_BACKEND=post_office.EmailBackend
CELERY_BROKER_URL=redis://localhost:6379/0
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

6. В отдельных терминалах запустите Celery:

```bash
uv run celery -A proj worker -l info
uv run celery -A proj beat -l info
```

Приложение будет доступно по адресу http://localhost:8000

## API

Документация: http://localhost:8000/api/v1/docs

- `POST /api/v1/auth/token/` — получить JWT токен
- `GET/POST /api/v1/event/` — список и создание мероприятий
- `GET/PUT/DELETE /api/v1/event/{id}/` — детали, редактирование, удаление
- `GET/POST /api/v1/event_place/` — площадки (только суперпользователь)
