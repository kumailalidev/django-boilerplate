from django.urls import path

from .views import (
    signup_view,
    login_view,
    logout_view,
    password_reset_view,
    password_reset_done_view,
    password_reset_confirm_view,
    password_reset_complete_view,
    password_change_view,
    password_change_done_view,
)

app_name = "accounts"

urlpatterns = [
    path(route="signup/", view=signup_view, name="signup"),
    path(route="login/", view=login_view, name="login"),
    path(route="logout/", view=logout_view, name="logout"),
    path(route="password/reset/", view=password_reset_view, name="password_reset"),
    path(
        route="password/reset/done/",
        view=password_reset_done_view,
        name="password_reset_done",
    ),
    path(
        route="password/reset/confirm/<uidb64>/<token>/",
        view=password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    path(
        route="password/reset/complete/",
        view=password_reset_complete_view,
        name="password_reset_complete",
    ),
    path(route="password/change/", view=password_change_view, name="password_change"),
    path(
        route="password/change/done/",
        view=password_change_done_view,
        name="password_change_done",
    ),
]
