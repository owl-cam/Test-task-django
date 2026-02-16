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
- openpyxl (импорт/экспорт XLSX)

## Архитектура

- **app_event** — CRUD мероприятий с поддержкой изображений, импорта/экспорта XLSX. Неавторизованные и обычные пользователи видят только опубликованные события. Суперпользователь — все операции.
- **app_event_place** — Площадки (название + координаты). Только суперпользователь.
- **app_weather** — Погода по площадкам. Обновляется через Celery каждый час (weatherapi.com).

### Слои архитектуры (app_event)

```
HTTP → schema.py (валидация) → service.py (бизнес-логика) → ORM models
                ↕
         domain.py (Pydantic модели)
```

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

### Авторизация

| Метод | Путь | Описание |
|---|---|---|
| POST | `/api/v1/auth/token/pair` | Получить access + refresh токены |
| POST | `/api/v1/auth/token/verify` | Проверить access токен |
| POST | `/api/v1/auth/token/refresh` | Обновить access токен |

### Мероприятия

| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| GET | `/api/v1/event/` | Список (фильтры, пагинация, сортировка) | все |
| POST | `/api/v1/event/` | Создать | superuser |
| GET | `/api/v1/event/{id}` | Получить | все (published) |
| PATCH | `/api/v1/event/{id}` | Обновить | superuser |
| DELETE | `/api/v1/event/{id}` | Удалить | superuser |
| GET | `/api/v1/event/export` | Экспорт в XLSX | superuser |
| POST | `/api/v1/event/import` | Импорт из XLSX | superuser |
| POST | `/api/v1/event/image` | Загрузить фото | superuser |
| DELETE | `/api/v1/event/image/{id}` | Удалить фото | superuser |

### Площадки

| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| GET | `/api/v1/event_place/` | Список | superuser |
| POST | `/api/v1/event_place/` | Создать | superuser |
| GET | `/api/v1/event_place/{id}` | Получить | superuser |
| PATCH | `/api/v1/event_place/{id}` | Обновить | superuser |
| DELETE | `/api/v1/event_place/{id}` | Удалить | superuser |

### Фильтрация и сортировка (GET /api/v1/event/)

**Фильтры:**
- `start_date_from`, `start_date_to` — диапазон даты начала
- `end_date_from`, `end_date_to` — диапазон даты окончания
- `place_id` — множественный выбор площадок
- `rate_from`, `rate_to` — диапазон рейтинга (0-25)
- `search` — поиск по названию мероприятия или площадки

**Сортировка:**
- `name` — по названию
- `start_date` — по дате начала
- `end_date` — по дате окончания

## Импорт/Экспорт XLSX

### Экспорт

`GET /api/v1/event/export` — скачать XLSX файл с мероприятиями.

Фильтры:
- `publish_date_from`, `publish_date_to`
- `start_date_from`, `start_date_to`
- `end_date_from`, `end_date_to`
- `place_id` (множественный)
- `rate_from`, `rate_to`

### Импорт

`POST /api/v1/event/import` — загрузить XLSX файл.

Обязательные колонки: Название, Описание, Дата начала, Дата окончания, Рейтинг.

Особенности:
- Автоматически создаёт площадки, если указаны координаты
- Валидация каждой строки с детальными ошибками
- Транзакционное сохранение (все или ничего)

## Тесты

85 тестов покрывают основной функционал:

```bash
# Запуск всех тестов
cd src && uv run pytest

# С покрытием
uv run pytest --cov=. --cov-report=html
```

| Модуль | Тестов | Описание |
|---|---|---|
| test_auth | 6 | JWT токены: получение, верификация, обновление |
| test_event | 54 | CRUD, фильтрация, пагинация, изображения, импорт/экспорт |
| test_event_place | 24 | CRUD площадок, права доступа |
| test_healthcheck | 1 | Проверка работоспособности |
