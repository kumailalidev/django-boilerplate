from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import UsernameValidator, NameValidator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model. Username, email, and password are required,
    Other fields are optional.
    """

    username_validator = UsernameValidator()
    name_validator = NameValidator()

    username = models.CharField(
        verbose_name=_("username"),
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
        verbose_name=_("email address"),
        unique=True,
        error_messages={
            "unique": _("Email address is already registered."),
        },
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=150,
        help_text=_(
            "Contains unaccented lowercase a-z and uppercase A-Z letters only."
        ),
        blank=True,
        validators=[name_validator],
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=150,
        blank=True,
        help_text=_(
            "Contains unaccented lowercase a-z and uppercase A-Z letters only."
        ),
        validators=[name_validator],
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
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        """Normalize email address."""
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
