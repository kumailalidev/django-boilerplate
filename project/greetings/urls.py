from django.urls import path

from . import views

app_name = "greetings"

urlpatterns = [
    path(route="", view=views.home, name="home"),
    path(route="images/", view=views.images, name="images"),
]
