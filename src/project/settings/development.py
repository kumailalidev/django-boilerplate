from .base import *


# GENERAL SETTINGS
DEBUG = True
SECRET_KEY = env(
    "SECRET_KEY", default="s(v&re7l8e%tvknfc3lpvzzjm(=cv$6g68@%h^$epvd-fu#^88"
)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# APPS
INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARES
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

# Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
