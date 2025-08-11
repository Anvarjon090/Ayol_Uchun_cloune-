import datetime

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.payments.choices import OrderStatus, ProviderChoices, TransactionStatus


class Order(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name=_("User"),
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name=_("Course"),
        null=True,
        blank=True,
    )
    webinar = models.ForeignKey(
        "courses.Webinar",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name=_("Webinar"),
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount")
    )
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name=_("Status"),
    )
    is_paid = models.BooleanField(default=False, verbose_name=_("Is paid"))

    def __str__(self):
        return f"Order: {self.id}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Transaction(BaseModel):
    order = models.ForeignKey(
        "payments.Order", on_delete=models.CASCADE, verbose_name=_("order")
    )
    provider = models.ForeignKey(
        "payments.Providers",
        on_delete=models.CASCADE,
        verbose_name=_("Provider"),
    )
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        verbose_name=_("Status"),
    )
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Paid at"))
    cancelled_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Cancelled at")
    )
    remote_id = models.CharField(
        max_length=512, null=True, blank=True, verbose_name=_("Remote Transaction ID")
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name=_("Amount")
    )
    extra = models.JSONField(null=True, blank=True, verbose_name=_("Extra Data"))

    def __str__(self):
        return f"Transaction: {self.id}"

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    @property
    def get_payment_url(self):
        payment_link = None
        if self.provider.name == ProviderChoices.PAYLOV:
            from apps.payments.paylov.client import PaylovClient

            payment_link = PaylovClient.create_payment_link(self)

        return payment_link

    def apply_transaction(
        self,
        provider=None,
        transaction_id: str | None = None,
    ):
        if not self.remote_id and transaction_id:
            self.remote_id = str(transaction_id)
        self.provider = provider
        self.paid_at = datetime.datetime.now()
        self.status = TransactionStatus.COMPLETED

        try:
            with transaction.atomic():
                self.save(
                    update_fields=[
                        "paid_at",
                        "status",
                        "remote_id",
                        "provider",
                    ]
                )
                self.order.status = OrderStatus.COMPLETED
                self.order.is_paid = True if self.paid_at else False
                self.order.save(update_fields=["is_paid", "status"])
        except Exception:
            raise

        return self

    def cancel_transaction(self, reason):
        self.cancelled_at = datetime.datetime.now()
        self.status = TransactionStatus.CANCELLED
        self.extra = {"payme_cancel_reason": reason}
        self.save(
            update_fields=[
                "cancelled_at",
                "status",
            ]
        )

        self.order.paid_at = None
        self.order.save(update_fields=["is_paid"])

        return self
    

class UserCard(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_cards", verbose_name=_("User")
    )
    card_token = models.CharField(max_length=255, verbose_name=_("Card Token"))
    provider = models.ForeignKey(
        "payments.Providers", on_delete=models.CASCADE, verbose_name=_("Provider")
    )
    cardholder_name = models.CharField(max_length=255, verbose_name=_("Cardholder Name"), null=True, blank=True)
    last_four_digits = models.CharField(max_length=4, verbose_name=_("Last Four Digits"), null=True, blank=True)
    brand = models.CharField(max_length=255, verbose_name=_("Brand"), null=True, blank=True)
    expire_month = models.CharField(max_length=2, verbose_name=_("Expire Month"))
    expire_year = models.CharField(max_length=4, verbose_name=_("Expire Year"))
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is confirmed"))

    class Meta:
        verbose_name = _("User Card")
        verbose_name_plural = _("User Cards")

    def __str__(self):
        return f"User Card: {self.id}"


class Providers(BaseModel):
    name = models.CharField(
        max_length=255, verbose_name=_("Name"), choices=ProviderChoices.choices
    )
    key = models.CharField(max_length=255, verbose_name=_("Key"))

    def __str__(self):
        return f"Provider: {self.name}"

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")


class ProviderCredentials(BaseModel):
    provider = models.ForeignKey("payments.Providers", on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    key_description = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "provider",
            "key",
        )
        verbose_name = "Provider Credential"
        verbose_name_plural = "Provider Credentials"

    def __str__(self):
        return f"{self.provider} - {self.key}"