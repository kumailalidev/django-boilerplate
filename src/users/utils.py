from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError

from .tokens import default_email_verification_token_generator

CustomUserModel = get_user_model()


def get_user(uidb64):
    """
    Returns user object by providing base 64 encoded id.
    """
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUserModel._default_manager.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        CustomUserModel.DoesNotExist,
        ValidationError,
    ):
        user = None

    return user


def send_html_mail(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
):
    """
    A version of EmailMessage that makes it easy to send multipart/alternative messages.
    For example, including text and HTML versions of the text is made easier.
    """
    subject = loader.render_to_string(
        template_name=subject_template_name, context=context
    )
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(template_name=email_template_name, context=context)

    # generate email message
    email_message = EmailMultiAlternatives(
        subject=subject, body=body, from_email=from_email, to=[to_email]
    )

    # attach html email template
    if html_email_template_name is not None:
        html_email = loader.render_to_string(
            template_name=html_email_template_name, context=context
        )
        email_message.attach_alternative(content=html_email, mimetype="text/html")

    # send email
    email_message.send(fail_silently=False)


def send_email_verification_mail_to_user(
    request,
    user,
    use_https=False,
    domain_override=None,
    from_email=None,
    subject_template_name="registration/email_verification_mail_subject.txt",
    email_template_name="registration/email_verification_mail.html",
    html_email_template_name=None,
    extra_email_context=None,
    token_generator=default_email_verification_token_generator,
):
    """
    Generate a one-use only link for resetting password and send it to the
    user and sends mail for email verification
    """
    # get the domain name
    if not domain_override:
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
    else:
        site_name = domain = domain_override

    # get the user email
    email_field_name = CustomUserModel.get_email_field_name()
    user_email = getattr(user, email_field_name)

    # email context
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

    send_html_mail(
        subject_template_name=subject_template_name,
        email_template_name=email_template_name,
        context=context,
        from_email=from_email,
        to_email=user_email,
        html_email_template_name=html_email_template_name,
    )
