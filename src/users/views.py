from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy
from django.views.generic import FormView
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
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages

from .forms import (
    CustomUserCreationForm,
    CustomUserProfileForm,
    CustomUserAuthenticationForm,
    CustomUserPasswordChangeForm,
    CustomUserPasswordResetForm,
    CustomUserSetPasswordForm,
)
from .mixins import RedirectAuthenticatedUserMixin


# TODO: Write docstrings for views.


class CustomUserProfileView(FormView):
    """
    Displays basic user information, and handles process of
    updating.
    """

    template_name = "registration/profile.html"
    form_class = CustomUserProfileForm
    success_url = reverse_lazy("users:profile")

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Profile update unsuccessful. Please fix errors.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs


custom_user_profile_view = CustomUserProfileView.as_view()


class CustomUserSignupView(RedirectAuthenticatedUserMixin, FormView):
    """
    Display the sign up form and handles the
    user creation action.
    """

    # for authenticated users
    redirect_to = None

    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("users:login")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
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


class CustomUserPasswordResetView(RedirectAuthenticatedUserMixin, PasswordResetView):
    """
    Displays password reset form (email field only) and handles
    sending email for password reset.
    """

    # for authenticated users
    redirect_to = None

    email_template_name = "registration/password_reset_email.html"
    form_class = CustomUserPasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "registration/password_reset_form.html"


custom_user_password_reset_view = CustomUserPasswordResetView.as_view()


class CustomUserPasswordResetDoneView(
    RedirectAuthenticatedUserMixin, PasswordResetDoneView
):
    """
    Renders html template on successfully sending password reset email.
    """

    # for authenticated users
    redirect_to = None

    template_name = "registration/password_reset_done.html"


custom_user_password_reset_done_view = CustomUserPasswordResetDoneView.as_view()


class CustomUserPasswordResetConfirmView(
    RedirectAuthenticatedUserMixin, PasswordResetConfirmView
):
    """
    On providing valid password reset URL it displays form for password
    reset and handles the functionality for reset.
    """

    # for authenticated users
    redirect_to = None

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


class CustomUserPasswordResetCompleteView(
    RedirectAuthenticatedUserMixin, PasswordResetCompleteView
):
    """
    Renders template on successful password reset.
    """

    # for authenticated users
    redirect_to = None

    template_name = "registration/password_reset_complete.html"


custom_user_password_reset_complete_view = CustomUserPasswordResetCompleteView.as_view()
