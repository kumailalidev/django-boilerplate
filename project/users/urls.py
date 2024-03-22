from django.urls import path

from .views import (
    user_signup_view,
    user_login_view,
    user_logout_view,
    password_reset_view,
    password_reset_done_view,
)

app_name = "users"

urlpatterns = [
    path(route="signup/", view=user_signup_view, name="signup"),
    path(route="login/", view=user_login_view, name="login"),
    path(route="logout/", view=user_logout_view, name="logout"),
    path(
        route="password-reset/",
        view=password_reset_view,
        name="password_reset",
    ),
    path(
        route="password-reset/done/",
        view=password_reset_done_view,
        name="password_reset_done",
    ),
]
