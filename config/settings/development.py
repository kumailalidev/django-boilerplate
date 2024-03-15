from .base import *

# GENERAL
DEBUG = True
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="django-insecure-^uz2g$=t%t)i=3aas2@_ia94q*(&d2m4z7xczlq&@*fn)y*hv6",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# APPS
INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]

# MIDDLEWARES
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# EMAIL
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
