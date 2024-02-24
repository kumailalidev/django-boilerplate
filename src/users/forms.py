from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import (
    UsernameField,
    ReadOnlyPasswordHashField,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

CustomUserModel = get_user_model()


class CustomUserProfileForm(forms.ModelForm):
    """
    A from for displaying and changing users basic information.
    NOTE: default UserChangeForm can also be used instead.
    """

    class Meta:
        model = CustomUserModel
        fields = (
            "email",
            "username",
            "date_of_birth",
            "first_name",
            "middle_name",
            "last_name",
        )


class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username,
    email, date of birth and password.
    """

    error_messages = {"password_mismatch": _("The two password field's didn't match.")}

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
            }
        ),
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CustomUserModel
        fields = (
            "email",
            "username",
            "date_of_birth",
            "first_name",
            "middle_name",
            "last_name",
            "password1",
            "password2",
        )
        fields_classes = {"username": UsernameField}
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # auto focus USERNAME_FIELD i.e. 'email'
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """A from for displaying and changing users information"""

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = CustomUserModel
        fields = (
            "username",
            "email",
            "date_of_birth",
            "first_name",
            "middle_name",
            "last_name",
        )
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )


class CustomUserAuthenticationForm(AuthenticationForm):
    """Authentication from"""

    pass


class CustomUserPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """

    pass


class CustomUserPasswordResetForm(PasswordResetForm):
    """
    A form that lets a user reset their password by entering their email
    address.
    """

    pass


class CustomUserSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user set their password without entering the old
    password
    """

    pass
