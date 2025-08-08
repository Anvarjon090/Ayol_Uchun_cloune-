from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.actions import deactivate_users
from apps.users.models import Interest, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "phone_number",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
    )
    list_display_links = ("id", "phone_number")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = (
        "id",
        "phone_number",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("phone_number",)
    actions = [deactivate_users]

    fieldsets = (
        (None, {"fields": ("phone_number", "username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                    "bio",
                    "reason_delete_choices",
                    "reason_delete_str",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_confirmed",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "username", "password1", "password2"),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("id", "name")
