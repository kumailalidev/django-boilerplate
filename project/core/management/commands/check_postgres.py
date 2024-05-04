from django.core.management.base import BaseCommand
from django.conf import settings

import psycopg2


class Command(BaseCommand):
    help = "Check if Postgres server is up and running."

    def handle(self, *args, **kwargs):
        try:
            database = settings.DATABASES["default"]
            database_engine = database["ENGINE"]

            if database_engine == "django.db.backends.postgresql":
                postgres_dbname = database["NAME"]
                postgres_user = database["USER"]
                postgres_password = database["PASSWORD"]
                postgres_host = database["HOST"]
                postgres_port = database["PORT"]
            else:
                self.stdout.write(
                    self.style.ERROR("Your default database is NOT PostgreSQL.")
                )
                # Stop executing further
                return None
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    "Please make sure DATABASES settings are setup correctly in Django settings."
                )
            )
            self.stdout.write(self.style.WARNING(f"EXCEPTION: {e}"))
            # Stop executing further
            return None

        try:
            psycopg2.connect(
                dbname=postgres_dbname,
                user=postgres_user,
                password=postgres_password,
                host=postgres_host,
                port=postgres_port,
            )
            self.stdout.write(self.style.SUCCESS("Postgres server is up and running."))
        except psycopg2.OperationalError:
            self.stdout.write(self.style.ERROR("Failed to connect to Postgres server."))
