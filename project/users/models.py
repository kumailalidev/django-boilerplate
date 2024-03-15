from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import validate_age
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    Username, email, date of birth and password are required.
    Other fields are optional
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Username contains 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email address is already registered.")
        },
    )
    date_of_birth = models.DateField(
        _("Date of Birth"),
        validators=[validate_age],
        help_text=_("You must be 18 years old."),
    )
    first_name = models.CharField(
        verbose_name=_("First Name"), max_length=150, blank=True
    )
    middle_name = models.CharField(
        verbose_name=_("Middle Name"), max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"), max_length=150, blank=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    # TODO Update helptext, make more descriptive.
    is_verified = models.BooleanField(
        verbose_name=_("Is Verified"),
        default=False,
        help_text=_(
            "Designates whether the user has verified their email or not. "
            "If email is not verified, the user can not log into site but still can authenticate."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # required=True
    REQUIRED_FIELDS = ["username", "date_of_birth"]  # required=True

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
