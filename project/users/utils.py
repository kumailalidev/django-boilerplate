from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.conf import settings
from django.template import loader
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.template import loader
from django.core.mail import EmailMultiAlternatives

from urllib.parse import urlparse

from .views import UserLogoutView

UserModel = get_user_model()


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


def send_mail(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
):
    """
    Email message which can be sent to multiple users.
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()
