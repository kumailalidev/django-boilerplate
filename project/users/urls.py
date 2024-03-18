from django.urls import path

from .views import user_signup_view, user_login_view

app_name = "users"

urlpatterns = [
    path(route="signup/", view=user_signup_view, name="signup"),
    path(route="login/", view=user_login_view, name="login"),
]
