from .base import *

# GENERAL
DEBUG = True

# APPS
INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARES
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

# Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# MESSAGES
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# EMAIL
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
