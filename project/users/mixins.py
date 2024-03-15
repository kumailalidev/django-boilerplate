from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.conf import settings

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL


class RedirectAuthenticatedUserMixin:
    """
    Redirects already authenticated user to redirect url defined in
    LOGIN_REDIRECT_URL (default to '/accounts/profile/') else redirected
    to url generated using redirect_url value.
    """

    # TODO: Add support for REDIRECT_FIELD_NAME (i.e. next field) for
    # redirection.

    redirect_to = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = self.get_redirect_url()
            if redirect_url == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_url)

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        """Return the default redirect URL."""
        if self.redirect_to:
            return resolve_url(self.redirect_to)
        else:
            return resolve_url(LOGIN_REDIRECT_URL)
