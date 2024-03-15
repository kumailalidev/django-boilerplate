"""
Test settings
"""

from .base import *

# GENERAL
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="django-insecure-^uz2g$=t%t)i=3aas2@_ia94q*(&d2m4z7xczlq&@*fn)y*hv6",
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"


# CACHES
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
