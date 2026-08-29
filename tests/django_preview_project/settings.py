from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "test-only-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

CODEX_PREVIEW_ENABLED = True
CODEX_PREVIEW_TEMPLATE_ROOTS = [BASE_DIR / "templates"]

ROOT_URLCONF = "tests.django_preview_project.urls"
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "tests.django_preview_project.middleware.SampleMiddleware",
]
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_codex_preview",
]
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "tests.django_preview_project.context_processors.sample_context",
            ],
        },
    }
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
