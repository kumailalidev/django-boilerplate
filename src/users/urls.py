from django.urls import path
from django.views.generic import TemplateView

from .views import (
    custom_user_login_view,
    custom_user_signup_view,
    custom_user_logout_view,
    custom_user_password_change_view,
    custom_user_password_change_done_view,
)

app_name = "users"

urlpatterns = [
    path(
        route="",
        view=TemplateView.as_view(template_name="users/home.html"),
        name="home",
    ),
    path(route="login/", view=custom_user_login_view, name="login"),
    path(route="signup/", view=custom_user_signup_view, name="signup"),
    path(route="logout/", view=custom_user_logout_view, name="logout"),
    path(
        route="password-change/",
        view=custom_user_password_change_view,
        name="password_change",
    ),
    path(
        route="password-change-done/",
        view=custom_user_password_change_done_view,
        name="password_change_done",
    ),
]
