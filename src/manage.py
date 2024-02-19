#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import environ
import os
import sys

env = environ.Env(
    # set casting, default value
    ENVIRONMENT=(str, "development")
)

# Set the project base directory
ENV_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # / root directory

# Take environment variables form .env file
environ.Env.read_env(os.path.join(ENV_DIR, ".env"))


def main():
    """Run administrative tasks."""

    if env("ENVIRONMENT") == "development":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.development")
    elif env("ENVIRONMENT") == "production":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.production")

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
