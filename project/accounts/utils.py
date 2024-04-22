import unicodedata

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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

    email_message.send(fail_silently=False)


def get_users(email):
    """Given an email, return matching user(s) who should receive a reset.

    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    email_field_name = UserModel.get_email_field_name()
    active_users = UserModel._default_manager.filter(
        **{
            "%s__iexact" % email_field_name: email,
            "is_active": True,
        }
    )
    return (
        user
        for user in active_users
        if user.has_usable_password()
        and _unicode_ci_compare(email, getattr(user, email_field_name))
    )


def generate_and_mail_link(
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
            "token": token_generator.make_token(user=user),
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


def get_user_via_uidb64(uidb64):
    """Return user object using provided base 64 encoded user id value."""
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        UserModel.DoesNotExist,
        ValidationError,
    ):
        user = None
    return user
