from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_age(value):
    """
    Validator function to ensure the user's age is greater than 18.
    """
    if (timezone.now().date() - value).days < 365 * 18:
        raise ValidationError(message=_("You must be at least 18 years old."))
