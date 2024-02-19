from .base import *

DEBUG = False


# You must set settings.ALLOWED_HOSTS if DEBUG is False.
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
