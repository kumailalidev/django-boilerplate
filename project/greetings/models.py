from django.db import models


class Greeting(models.Model):
    message = models.TextField(verbose_name="Greeting message", max_length=255)

    def __str__(self):
        return str(self.message[0:50] + "...")


class Image(models.Model):
    def upload_to(self, filename):
        return f"images/{filename}"

    image = models.ImageField(upload_to=upload_to)
