from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from django.contrib import messages

from .mixins import RedirectURLMixin
from .forms import UserCreationForm

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL


class UserSignUpView(RedirectURLMixin, FormView):
    """
    Display the sign up form and handle the sign up action.
    """

    # TODO: After creating UserLoginView create SIGNUP_REDIRECT_URL constant
    # in settings and set value to UserLoginView route and update get_default_redirect_url
    # method.

    form_class = UserCreationForm
    authentication_form = None
    template_name = "registration/signup.html"
    redirect_authenticated_user = True
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a signup page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(LOGIN_REDIRECT_URL)

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def form_valid(self, form):
        """Create a new user, send success message and redirect to URL."""
        user = form.save()
        messages.success(
            request=self.request,
            message=_("Your account had been created successfully."),
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context


user_signup_view = UserSignUpView.as_view()
