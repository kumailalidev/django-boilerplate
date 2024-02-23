from django.urls import path
from django.views.generic import TemplateView

from .views import custom_user_login_view

app_name = "users"

urlpatterns = [
    path(
        route="",
        view=TemplateView.as_view(template_name="users/home.html"),
        name="home",
    ),
    path(route="login/", view=custom_user_login_view, name="login"),
]
