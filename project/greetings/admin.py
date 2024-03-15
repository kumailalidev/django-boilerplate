from django.contrib import admin

from .models import Greeting, Image

admin.site.register(Greeting)
admin.site.register(Image)
