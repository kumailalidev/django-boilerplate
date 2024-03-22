from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0


@deconstructible
class NameValidator(validators.RegexValidator):
    regex = f"^[A-Za-z]+$"
    message = _(
        "Enter a valid name. This value may contain only unaccented lowercase a-z "
        "and uppercase A-Z letters."
    )
    flags = 0
