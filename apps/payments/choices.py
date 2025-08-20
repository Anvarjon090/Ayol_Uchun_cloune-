from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProviderChoices(TextChoices):
    PAYLOV = ("paylov", _("Paylov"))
    PAYME = ("payme", _("Payme"))
    CLICK = ("click", _("Click"))


class OrderStatus(TextChoices):
    PENDING = ("pending", _("Pending"))
    COMPLETED = ("completed", _("Completed"))
    CANCELLED = ("cancelled", _("Cancelled"))
    REFUNDED = ("refunded", _("Refunded"))


class TransactionStatus(TextChoices):
    PENDING = ("pending", _("Pending"))
    PROCESSING = ("processing", _("Processing"))
    COMPLETED = ("completed", _("Completed"))
    FAILED = ("failed", _("Failed"))
    CANCELLED = ("cancelled", _("Cancelled"))
    REFUNDED = ("refunded", _("Refunded"))
