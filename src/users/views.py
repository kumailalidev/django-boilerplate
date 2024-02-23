from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView

from .mixins import RedirectIfAuthenticatedMixin
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm


class CustomUserSignupView(RedirectIfAuthenticatedMixin, View):
    """
    Display the sign up form and handles the
    user creation action.
    """

    # TODO: Update view to generic FormView or any suitable
    # class based view.

    next_page = "users:home"
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()

        return render(
            request=request,
            template_name="registration/signup.html",
            context={"form": form},
        )

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(data=request.POST or None)

        if form.is_valid():
            form.save()
            return HttpResponse("User Created")
        else:
            return render(
                request=request,
                template_name="registration/signup.html",
                context={"form": form},
            )


custom_user_signup_view = CustomUserSignupView.as_view()


class CustomUserLoginView(LoginView):
    """
    Display the login form and handles the login action,
    inherits django.contrib.auth.views.LoginView

    On successful login user is redirected to url set inside
    LOGIN_REDIRECT_URL setting inside settings.py (by default
    it is '/accounts/profile/') else redirected to url
    generated using next_page value.
    """

    # TODO: use authentication_from property and see results

    next_page = "users:home"  # view name
    form_class = CustomUserAuthenticationForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True


custom_user_login_view = CustomUserLoginView.as_view()
