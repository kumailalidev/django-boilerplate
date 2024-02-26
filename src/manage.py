#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import environ
import os
import sys
from pathlib import Path


env = environ.Env(
    ENVIRONMENT=(str, "development"),
)

# '.env' directory path
ENV_DIR = Path(__file__).resolve(strict=True).parent.parent

# '.env' file
ENV_FILE = ENV_DIR / ".env"
if Path(ENV_FILE).exists():
    # Take environment variables form .env file
    env.read_env(env_file=str(ENV_FILE), overwrite=True)

ENVIRONMENT = env("ENVIRONMENT")


def main():
    # Set DJANGO_SETTINGS_MODULE environment variable.
    if ENVIRONMENT == "development":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.development")
    elif ENVIRONMENT == "production":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.production")

    # Run administrative tasks
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
