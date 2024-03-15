import environ
from pathlib import Path

# '/src', '/app', or '/[repository name]' directory
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
PROJECT_DIR = BASE_DIR / "project"

# load '.env' file
env = environ.Env()

ENV_FILE = BASE_DIR / ".env"
if Path(ENV_FILE).exists():
    # Take environment variables form .env file
    env.read_env(str(ENV_FILE), overwrite=True)

# DEBUG SETTING
DEBUG = env.bool("DJANGO_DEBUG", False)

# APPS
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = []
LOCAL_APPS = [
    "project.users.apps.UsersConfig",
    "project.greetings.apps.GreetingsConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARES
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# DATABASE
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3",
    )
}

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# USER MODEL
AUTH_USER_MODEL = "users.CustomUser"

# Static files (CSS, JavaScript, Images)
# In addition to using a static/ directory inside your apps,
# you can define a list of directories (STATICFILES_DIRS) in
# your settings file where Django will also look for static
# files
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")  # used by collectstatic command
STATICFILES_DIRS = [str(PROJECT_DIR / "static")]

# MEDIA FILES (Uploaded by users)
MEDIA_URL = "/media/"
MEDIA_ROOT = str(PROJECT_DIR / "media")  # media folder location

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
