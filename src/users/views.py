from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib import messages

from .mixins import RedirectIfAuthenticatedMixin
from .forms import (
    CustomUserCreationForm,
    CustomUserAuthenticationForm,
    CustomUserPasswordChangeForm,
)


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


class CustomUserLogoutView(LogoutView):
    """
    Log out the user and display the 'You are logged out message'
    inherited from django.contrib.auth.views.LogoutView

    User will be redirected to url set in LOGOUT_REDIRECT_URL (by default value
    is None) or to url generated using next_page value.

    NOTE: Log out via GET requests is deprecated and will be removed
    in Django 5.
    """

    next_page = None
    template_name = "registration/logged_out.html"

    # adding custom message
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "You have been logged out successfully.")

        return response


custom_user_logout_view = CustomUserLogoutView.as_view()


class CustomUserPasswordChangeView(PasswordChangeView):
    """
    Displays password change form and handles the password
    change action and sends a message.
    """

    form_class = CustomUserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "registration/password_change_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            request=self.request,
            message="Password was changed successfully. Please login with your new credentials.",
        )

        return response


custom_user_password_change_view = CustomUserPasswordChangeView.as_view()


class CustomUserPasswordChangeDoneView(PasswordChangeDoneView):
    """
    Renders template on successfully changing password.
    """

    template_name = "registration/password_change_done.html"


custom_user_password_change_done_view = CustomUserPasswordChangeDoneView.as_view()
