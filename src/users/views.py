from django.conf import settings
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages

from .forms import (
    CustomUserCreationForm,
    CustomUserAuthenticationForm,
    CustomUserPasswordChangeForm,
    CustomUserPasswordResetForm,
    CustomUserSetPasswordForm,
)

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL

# TODO: Implement CustomUserProfileView
# TODO: Instead of overriding dispatch method in CustomUserSignupView and
# CustomUserPasswordResetView create a mixin called RedirectAuthenticatedUserMixin
# to redirect the authenticated user.


class CustomUserSignupView(FormView):
    """
    Display the sign up form and handles the
    user creation action.
    """

    redirect_to = "users:home"
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("users:login")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Restrict view for already logged in users.
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.redirect_to))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid create user and redirect to supplied URL."""
        form.save()
        messages.success(
            request=self.request, message="Registration successful. Please login"
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form and pass error messages"""
        messages.error(
            request=self.request,
            message="Registration Unsuccessful. Please fix the errors.",
        )

        return super().form_invalid(form)


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


class CustomUserPasswordResetView(PasswordResetView):
    """
    Displays password reset form (email field only) and handles
    sending email for password reset.
    """

    redirect_to = "users:home"
    email_template_name = "registration/password_reset_email.html"
    form_class = CustomUserPasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "registration/password_reset_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Restrict view for already logged in users.
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.redirect_to))
        return super().dispatch(request, *args, **kwargs)


custom_user_password_reset_view = CustomUserPasswordResetView.as_view()


class CustomUserPasswordResetDoneView(PasswordResetDoneView):
    """
    Renders html template on successfully sending password reset email.
    """

    template_name = "registration/password_reset_done.html"


custom_user_password_reset_done_view = CustomUserPasswordResetDoneView.as_view()


class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    On providing valid password reset URL it displays form for password
    reset and handles the functionality for reset.
    """

    form_class = CustomUserSetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "registration/password_reset_confirm.html"

    # On successful password reset, send the success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            request=self.request,
            message="Password rest successfully. Please login using new credentials.",
        )

        return response


custom_user_password_reset_confirm_view = CustomUserPasswordResetConfirmView.as_view()


class CustomUserPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Renders template on successful password reset.
    """

    template_name = "registration/password_reset_complete.html"


custom_user_password_reset_complete_view = CustomUserPasswordResetCompleteView.as_view()
