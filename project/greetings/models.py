from django.db import models


class Greeting(models.Model):
    message = models.TextField(verbose_name="Greeting message", max_length=255)

    def __str__(self):
        return str(self.message[0:50] + "...")
