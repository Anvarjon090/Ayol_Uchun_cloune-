from django.db import models


class PaylovMethods(models.TextChoices):
    CHECK_TRANSACTION = "transaction.check", "Check Transaction"
    PERFORM_TRANSACTION = "transaction.perform", "Perform Transaction"


class HTTPMethods(models.TextChoices):
    GET = "GET", "GET"
    POST = "POST", "POST"
    DELETE = "DELETE", "DELETE"


SUBSCRIPTION_BASE_URL = "https://gw.paylov.uz/merchant/"
CHECKOUT_BASE_URL = "https://my.paylov.uz/checkout/create/"

API_ENDPOINTS = {
    "CREATE_CARD": ("userCard/createUserCard/", "POST"),
    "CONFIRM_CARD": ("userCard/confirmUserCardCreate/", "POST"),
    "GET_CARDS": ("userCard/getAllUserCards/", "GET"),
    "DELETE_CARD": ("userCard/deleteUserCard/", "DELETE"),
    "CREATE_RECEIPT": ("receipts/create/", "POST"),
    "PAY_RECEIPT": ("receipts/pay/", "POST"),
}

STATUS_CODES = {
    "ORDER_NOT_FOUND": "303",
    "ORDER_ALREADY_PAID": "201",
    "INVALID_AMOUNT": "5",
    "SERVER_ERROR": "3",
    "SUCCESS": "0",
}

STATUS_TEXT = {"SUCCESS": "OK", "ERROR": "ERROR"}