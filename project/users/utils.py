import unicodedata

from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.conf import settings
from django.template import loader
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from urllib.parse import urlparse

from .views import UserLogoutView
from .utils import send_mail

UserModel = get_user_model()


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )


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


def get_users(email):
    """Given an email, return matching user(s) who should receive a reset.

    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    email_field_name = UserModel.get_email_field_name()
    active_users = UserModel._default_manager.filter(
        **{
            "%s_iexact" % email_field_name: email,
            "is_active": True,
        }
    )
    return (
        user
        for user in active_users
        if user.has_usable_password()
        and _unicode_ci_compare(email, getattr(user, email_field_name))
    )


def generate_and_mail_reset_link(
    email,
    domain_override,
    subject_template_name,
    email_template_name,
    use_https,
    token_generator,
    from_email,
    request,
    html_email_template_name,
    extra_email_context,
):
    """
    Generate a one-use only link and send it to the user(s) via email, generally used for
    password reset or email confirmation.
    """
    if not domain_override:
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
    else:
        site_name = domain = domain_override
    email_field_name = UserModel.get_email_field_name()
    for user in get_users(email):
        user_email = getattr(user, email_field_name)
        context = {
            "email": user_email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
            **(extra_email_context or {}),
        }
        send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            user_email,
            html_email_template_name=html_email_template_name,
        )
