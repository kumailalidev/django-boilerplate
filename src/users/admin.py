from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin class for CustomUser model
    """

    fieldsets = (
        (
            "User Information",
            {"fields": ("username", "email", "password", "date_of_birth")},
        ),
        (
            _("Personal Information"),
            {"fields": ("first_name", "middle_name", "last_name")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "Required Information",
            {
                "fields": (
                    "username",
                    "email",
                    "date_of_birth",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Optional Information",
            {
                "fields": ("first_name", "middle_name", "last_name"),
            },
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        "username",
        "email",
        "date_of_birth",
        "is_staff",
        "first_name",
        "middle_name",
        "last_name",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email", "first_name", "middle_name", "last_name")
    ordering = ("username", "email")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
