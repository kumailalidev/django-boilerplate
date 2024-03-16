"""
Django production settings.
"""

from .base import *
from .base import env

# TODO: Update later.

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["project.com"])

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured Exception if DATABASE_URL Not in os.environ.
    # DATABASE_URL=postgres://user:password@hostname_or_ip:port/database_name
    "default": env.db("DATABASE_URL")
}
# https://docs.djangoproject.com/en/dev/ref/settings/#atomic-requests
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # Default: False
# https://docs.djangoproject.com/en/dev/ref/settings/#conn-max-age
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # Default: 0

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="webmaster@localhost",  # Default
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env(
    "DJANGO_SERVER_EMAIL",
    default="root@localhost",  # Default
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Django] ",  # Default
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")
