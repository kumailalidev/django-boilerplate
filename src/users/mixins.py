from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.conf import settings

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL


class RedirectIfAuthenticatedMixin:
    """
    Redirects already authenticated user to redirect url defined in
    LOGIN_REDIRECT_URL (default to '/accounts/profile/') else redirected
    to url generated using next_page value.
    """

    # TODO: Add support for REDIRECT_FIELD_NAME (i.e. next field) for
    # redirection.

    next_page = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("User is already authenticated")
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            print("Redirecting to:", str(redirect_to))
            return HttpResponseRedirect(redirect_to)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.get_default_redirect_url()

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(LOGIN_REDIRECT_URL)
