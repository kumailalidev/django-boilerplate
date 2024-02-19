from .base import *

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "debug_toolbar",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Media files (Uploaded by users) (Development environment only)

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"  # media folder location

# EMAIL

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Django Debug Toolbar

INTERNAL_IPS = [
    "127.0.0.1",
]
