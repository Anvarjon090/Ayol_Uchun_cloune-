from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone

from apps.users.models import User


@admin.action(description="Delete (soft) selected users")
def deactivate_users(modeladmin, request, queryset):
    """Custom admin action to soft delete users"""
    deactivated_count = 0

    with transaction.atomic():
        for user in queryset:
            if not user.is_deleted:  # Only deactivate active users
                timestamp = int(timezone.now().timestamp())

                # Update using queryset to bypass validation
                User.objects.filter(pk=user.pk).update(
                    phone_number=f"{user.phone_number}_deleted_{timestamp}",
                    is_deleted=True,
                    is_active=False,  # Also deactivate
                )
                deactivated_count += 1

    messages.success(request, f"Successfully deactivated {deactivated_count} user(s).")
