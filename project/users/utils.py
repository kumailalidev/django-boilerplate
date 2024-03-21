from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

from urllib.parse import urlparse

from .views import UserLogoutView


def logout_the_login(request, login_url=None):
    """
    Log out the user if they are logged in. Then redirect the login page.
    """
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return UserLogoutView.as_view(next_page=login_url)(request)


def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolve_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe="/")

    return HttpResponseRedirect(urlparse(login_url_parts))
