from django.contrib import admin

from apps.payments.models import (
    Order,
    ProviderCredentials,
    Providers,
    Transaction,
    UserCard,
)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user__username", "status", "amount", "created_at")
    list_display_links = ("id", "user__username")
    search_fields = ("user__username",)
    ordering = ("-created_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "status", "amount", "created_at")
    list_display_links = ("id", "order")
    search_fields = ("order__user__username",)
    ordering = ("-created_at",)


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user__username",
        "provider__name",
        "card_number",
        "expire_date",
        "is_confirmed",
    )
    list_display_links = ("id", "user__username")
    list_filter = ("provider", "is_confirmed")
    search_fields = ("user__username", "card_number")
    ordering = ("-created_at",)

    def card_number(self, obj):
        return f"**** **** **** {obj.last_four_digits}"

    card_number.short_description = "Card Number"

    def expire_date(self, obj):
        return f"{obj.expire_month}/{obj.expire_year}"

    expire_date.short_description = "Expire Date"


@admin.register(Providers)
class ProvidersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "key")
    list_display_links = ("id", "name")
    search_fields = ("name", "key")
    ordering = ("-created_at",)


@admin.register(ProviderCredentials)
class ProviderCredentialsAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "key")
    list_display_links = ("id", "provider")
    search_fields = ("provider__name", "key")
    ordering = ("-created_at",)