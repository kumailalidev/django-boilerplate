"""
Django development settings
"""

from .base import *
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="django-insecure-^uz2g$=t%t)i=3aas2@_ia94q*(&d2m4z7xczlq&@*fn)y*hv6",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",  # Default
        "LOCATION": "",  # Default
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Django] ",  # Default
)

# INSTALLED APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    # https://django-extensions.readthedocs.io/en/latest/
    "django_extensions",
    # https://django-debug-toolbar.readthedocs.io/en/latest/
    "debug_toolbar",
]
# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]

# MIDDLEWARES
# ------------------------------------------------------------------------------
MIDDLEWARE += [
    # https://django-debug-toolbar.readthedocs.io/en/latest/
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
