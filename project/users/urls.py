from django.urls import path
from django.views.generic import TemplateView

from .views import (
    custom_user_profile_view,
    custom_user_login_view,
    custom_user_signup_view,
    send_email_verification_mail_view,
    custom_user_email_verification_confirm_view,
    custom_user_logout_view,
    custom_user_password_change_view,
    custom_user_password_change_done_view,
    custom_user_password_reset_view,
    custom_user_password_reset_done_view,
    custom_user_password_reset_confirm_view,
    custom_user_password_reset_complete_view,
)

app_name = "users"

urlpatterns = [
    path(
        route="",
        view=TemplateView.as_view(template_name="users/home.html"),
        name="home",
    ),
    path(
        route="send-email-verification-mail/",
        view=send_email_verification_mail_view,
        name="send-email-verification-mail",
    ),
    path(route="profile/", view=custom_user_profile_view, name="profile"),
    path(route="login/", view=custom_user_login_view, name="login"),
    path(route="signup/", view=custom_user_signup_view, name="signup"),
    path(
        route="verify/<str:uidb64>/<str:token>/",
        view=custom_user_email_verification_confirm_view,
        name="custom_user_email_verification_confirm",
    ),
    path(route="logout/", view=custom_user_logout_view, name="logout"),
    path(
        route="password-change/",
        view=custom_user_password_change_view,
        name="password_change",
    ),
    path(
        route="password-change/done/",
        view=custom_user_password_change_done_view,
        name="password_change_done",
    ),
    path(
        route="password-reset/",
        view=custom_user_password_reset_view,
        name="password_reset",
    ),
    path(
        route="password-reset/done/",
        view=custom_user_password_reset_done_view,
        name="password_reset_done",
    ),
    path(
        route="password-reset/confirm/<uidb64>/<token>/",
        view=custom_user_password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    path(
        route="password-reset/complete/",
        view=custom_user_password_reset_complete_view,
        name="password_reset_complete",
    ),
]
