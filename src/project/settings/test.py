"""
Test settings
"""

from .base import *
from .base import env

# GENERAL
SECRET_KEY = env(
    "SECRET_KEY",
    default="s(v&re7l8e%tvknfc3lpvzzjm(=cv$6g68@%h^$epvd-fu#^88",
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
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
