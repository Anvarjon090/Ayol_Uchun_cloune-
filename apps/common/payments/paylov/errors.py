from django.utils.translation import gettext_lazy as _

error_codes = {
    "OTP_CODE_ALREADY_SENT": (
        "otp_code_already_sent",
        _("The OTP code has already been sent."),
    ),
    "UNKNOWN_ERROR": ("unknown_error", _("An unknown error has occurred.")),
    "INVALID_OTP": ("invalid_otp", _("The provided OTP is invalid.")),
    "CARD_IS_BLOCKED": ("card_is_blocked", _("The card is blocked.")),
    "CARD_EXISTS": ("card_exists", _("The card already exists.")),
    "CARD_NOT_FOUND": ("card_not_found", _("The card not found.")),
    "CARD_EXPIRED": ("card_expired", _("The card has expired.")),
    "FIELD_REQUIRED": ("field_required", _("A required field is missing.")),
    "INSUFFICIENT_FUNDS": (
        "insufficient_funds",
        _("There are insufficient funds available."),
    ),
    "VALIDATION_ERROR": ("validation_error", _("There is a validation error.")),
    "SERVER_ERROR": ("server_error", _("A provider's server error.")),
    "TRANSACTION_NOT_FOUND": ("transaction_not_found", _("The transaction not found.")),
    "GATEWAY_NOT_WORKING": (
        "gateway_not_working",
        _("The payment gateway is not working."),
    ),
    "TRANSACTION_ALREADY_PAYED": (
        "transaction_already_payed",
        _("The transaction has already been paid."),
    ),
    "CARD_IS_NOT_SUPPORTED": ("card_is_not_supported", _("The card is not supported.")),
    "PROCESSING_ERROR": ("processing_error", _("There was a processing error.")),
    "INVALID_CARD_TOKEN": ("invalid_card_token", _("The card token is invalid.")),
    "TOO_MANY_ATTEMPTS": ("too_many_attempts", _("There have been too many attempts.")),
    "TERMINAL_DOES_NOT_EXIST": (
        "terminal_does_not_exist",
        _("The terminal does not exist."),
    ),
    "CARD_IS_ALREADY_ACTIVATED": (
        "card_is_already_activated",
        _("The card is already activated."),
    ),
    "FIELD_NOT_VALID": ("field_not_valid", _("The field is not valid.")),
    "BANK_NOT_FOUND": ("bank_not_found", _("The bank could not be found.")),
    "MERCHANT_NOT_AVAILABLE": (
        "merchant_not_available",
        _("The merchant is not available."),
    ),
    "INVALID_AMOUNT": ("invalid_amount", _("The amount is invalid.")),
    "TRANSACTION_NOT_AVAILABLE_FOR_PAYMENT": (
        "transaction_not_available_for_payment",
        _("The transaction is not available for payment."),
    ),
    "ALREADY_CONFIRMED": (
        "already_confirmed",
        _("The transaction has already been confirmed."),
    ),
    "HOLD_NOT_FOUND": ("hold_not_found", _("The hold could not be found.")),
    "INVALID_CARD": ("invalid_card", _("The card is invalid.")),
    "ERROR_AT_PAY": ("error_at_pay", _("There was an error during payment.")),
    "PAN_NOT_VALID": (
        "pan_not_valid",
        _("The PAN (Primary Account Number) is not valid."),
    ),
    "ERROR_CARD_CREATE": (
        "error_create_card",
        _("There was an error creating the card."),
    ),
    "CARD_IS_NOT_FOR_THIS_CHECK": (
        "card_is_not_for_this_check",
        _("The card is not for this check."),
    ),
    "CARD_IS_NOT_ACTIVATED": ("card_is_not_activated", _("The card is not activated.")),
}