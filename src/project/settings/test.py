"""
Test settings
"""

from .base import *

# GENERAL
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
