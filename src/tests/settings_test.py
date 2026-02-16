from pathlib import Path
from typing import OrderedDict

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key-for-testing-only"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app_event_place",
    "app_event",
    "app_weather",
    "imagekit",
    "ninja_jwt",
    "post_office",
    "constance",
    "constance.backends.database",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "proj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WEATHER_API_KEY = "test-weather-api-key"

CELERY_BROKER_URL = "memory://"

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_ADDITIONAL_FIELDS = {
    "tinymce_field": [
        "django.forms.CharField",
        {},
    ],
}
CONSTANCE_CONFIG = OrderedDict(
    [
        ("EMAIL_TO", ("test@example.com", "Список адресатов")),
        ("EMAIL_SUBJECT", ("Новое мероприятие!", "Тема письма")),
        ("EMAIL_TEXT", ("Текст письма", "Текст письма", "tinymce_field")),
    ]
)
CONSTANCE_CONFIG_FIELDSETS = {
    "Настройки рассылки": (
        "EMAIL_TO",
        "EMAIL_SUBJECT",
        "EMAIL_TEXT",
    ),
}

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
