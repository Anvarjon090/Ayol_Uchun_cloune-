import base64
import urllib

import httpx

from apps.payments.choices import TransactionStatus
from apps.payments.models import Transaction
from apps.payments.paylov.constants import (
    API_ENDPOINTS,
    CHECKOUT_BASE_URL,
    STATUS_CODES,
    SUBSCRIPTION_BASE_URL,
    HTTPMethods,
)
from apps.payments.paylov.credentials import get_credentials
from apps.payments.paylov.errors import error_codes


class PaylovClient:
    """
    This class serves as a client for Paylov API.
    The client wraps API endpoints and provides methods
    to interact with the API.
    """

    def __init__(self, params: dict | None = None) -> None:
        """
        Initialize the client with credentials and parameters.
        """
        credentials = get_credentials()
        self.MERCHANT_KEY = credentials["PAYLOV_API_KEY"]
        self.USERNAME = credentials["PAYLOV_USERNAME"]
        self.PASSWORD = credentials["PAYLOV_PASSWORD"]
        self.SUBSCRIPTION_KEY = credentials["PAYLOV_SUBSCRIPTION_KEY"]

        # Provider attrs
        self.merchant_headers = {"api-key": self.MERCHANT_KEY}
        self.subscription_headers = {"api-key": self.SUBSCRIPTION_KEY}
        self.params = params
        self.error = False
        self.code = STATUS_CODES["SUCCESS"]
        self.transaction = self.get_transaction()

    # Main Functional methods
    # ----------------

    def send_request(
        self, to_endpoint: str, payload: dict | None = None, params: dict | None = None
    ) -> tuple[bool, dict]:
        endpoint, method = API_ENDPOINTS[to_endpoint]
        url = SUBSCRIPTION_BASE_URL + str(endpoint)
        headers = self.subscription_headers

        if method not in HTTPMethods.choices:
            raise ValueError("Unsupported HTTP method")

        try:
            if method == "GET":
                response = httpx.get(url, json=payload, headers=headers, params=params)
            elif method == "POST":
                response = httpx.post(url, json=payload, headers=headers, params=params)
            elif method == "DELETE":
                response = httpx.delete(
                    url, json=payload, headers=headers, params=params
                )

            response.raise_for_status()
            response_data = response.json()

            return response.ok, response_data

        except httpx.HTTPStatusError as e:
            try:
                response_data = e.response.json()
                return False, {
                    "error": {
                        "code": "api_error",
                        "message": str(e),
                        "details": response_data,
                    }
                }
            except ValueError:
                return False, {
                    "error": {
                        "code": "api_error",
                        "message": str(e),
                        "details": "Non-JSON response",
                    }
                }
        except httpx.RequestError as e:
            return False, {"error": {"code": "api_error", "message": str(e)}}
        except ValueError as e:
            return False, {"error": {"code": "invalid_response", "message": str(e)}}

    @classmethod
    def create_payment_link(cls, transaction: Transaction) -> str:
        credentials = get_credentials()
        merchant_key = credentials["PAYLOV_API_KEY"]
        return_url = urllib.parse.quote(
            credentials["PAYLOV_REDIRECT_URL"] + f"?transaction_id={transaction.id}",
            safe="",
        )

        if merchant_key is None:
            raise ValueError("Credentials not found")

        amount = int(transaction.amount)
        query = f"merchant_id={merchant_key}&amount={amount}&account.order_id={transaction.id}&return_url={return_url}"
        encode_params = base64.b64encode(query.encode("utf-8"))
        encode_params = str(encode_params, "utf-8")
        return f"{CHECKOUT_BASE_URL}{encode_params}"

    # Utility methods
    # ----------------

    def get_transaction(self) -> Transaction | None:
        """
        Get the transaction from the database based on the provided params.
        """
        if not self.params or not self.params.get("account"):
            return None
        try:
            return Transaction.objects.get(id=self.params["account"]["order_id"])
        except Transaction.DoesNotExist:
            return None

    @staticmethod
    def send_error_response(error_code: str) -> tuple[bool, dict]:
        error_details = error_codes.get(
            str(error_code).upper(), ["unknown_error", "Unknown error"]
        )

        error_response = {"detail": error_details[1], "code": error_details[0]}
        return False, error_response

    def check_transaction(self) -> tuple[bool, str]:
        if not self.transaction:
            return True, STATUS_CODES["ORDER_NOT_FOUND"]

        self.is_transaction_already_completed()
        self.is_transaction_amount_correct(self.params["amount"])
        return self.error, self.code

    def perform_transaction(self) -> tuple[bool, str]:
        if not self.transaction:
            return True, STATUS_CODES["ORDER_ALREADY_PAID"]

        if self.transaction.status == TransactionStatus.FAILED:
            return True, STATUS_CODES["SERVER_ERROR"]

        self.is_transaction_already_completed()
        self.is_transaction_amount_correct(self.params["amount"])
        return self.error, self.code

    def is_transaction_already_completed(self):
        if self.transaction.status == TransactionStatus.COMPLETED:
            self.error = True
            self.code = STATUS_CODES["ORDER_ALREADY_PAID"]

    def is_transaction_amount_correct(self, amount: int):
        if int(self.transaction.amount) != int(amount):
            self.error = True
            self.code = STATUS_CODES["INVALID_AMOUNT"]