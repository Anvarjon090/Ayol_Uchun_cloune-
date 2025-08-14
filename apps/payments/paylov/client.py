import base64
import urllib
import requests

from django.db import transaction as db_transaction
from rest_framework.exceptions import NotFound, APIException

from apps.payments.choices import TransactionStatus, ProviderChoices
from apps.courses.choices import ProductTypeChoices
from apps.payments.models import Providers, Transaction, UserCard, Order
from apps.courses.models import Course, Webinar
from apps.payments.paylov.constants import (
    API_ENDPOINTS,
    CHECKOUT_BASE_URL,
    STATUS_CODES,
    SUBSCRIPTION_BASE_URL,
)
from apps.payments.paylov.credentials import get_credentials
from apps.payments.paylov.errors import error_codes
from apps.users.models import User


class PaylovClient:
    """
    This class serves as a client for Paylov API.
    The client wraps API endpoints and provides methods
    to interact with the API.

    The Client consists of 2 parts:
    - Merchant API code
    - Subscribe API code
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
        self.provider = Providers.objects.filter(key="paylov").last()

    """
        Merchant API code
    """

    def send_request(
        self, to_endpoint: str, payload: dict | None = None, params: dict | None = None
    ) -> tuple[bool, dict]:
        endpoint, method = API_ENDPOINTS[to_endpoint]
        url = SUBSCRIPTION_BASE_URL + str(endpoint)
        headers = self.subscription_headers

        method_map = {
            "POST": requests.post,
            "GET": requests.get,
            "DELETE": requests.delete,
        }

        try:
            response = method_map[method](
                url, json=payload, headers=headers, params=params
            )

            response.raise_for_status()
            response_data = response.json()

            return response.ok, response_data

        except requests.exceptions.HTTPError as e:
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
        except requests.exceptions.RequestException as e:
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

    """
        Subscribe API code
    """

    def create_user_card(
        self, user, card_number: str, expire_month: str, expire_year: str
    ) -> tuple[bool, dict]:
        expire_date_str = expire_year + expire_month  # MM/YY -> YYMM | 06/29 2906

        payload = {
            "userId": str(user.id),
            "cardNumber": str(card_number),
            "expireDate": str(expire_date_str),
        }

        # user_card = UserCard.objects.filter(user=user, card_number=card_number).first()

        # if user_card and user_card.confirmed:
        #     return self.get_error_response("card_exists")

        success, response_data = self.send_request("CREATE_CARD", payload=payload)

        print(">>>", success, response_data)

        if success:
            otp_sent_phone = response_data["result"]["otpSentPhone"]
            card_id = response_data["result"]["cid"]

            is_already_exists = UserCard.objects.filter(
                user=user, card_token=card_id
            ).exists()

            if is_already_exists:
                return self.get_error_response("card_exists")

            user_card = UserCard.objects.create(
                user=user,
                card_token=card_id,
                provider=self.provider,
                expire_month=expire_month,
                expire_year=expire_year,
                is_confirmed=False,
            )

            return True, {"otp_sent_phone": otp_sent_phone, "card_id": user_card.id}

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def confirm_user_card(
        self, user: User, card_id: int, otp: str, card_name: str | None
    ) -> tuple[bool, dict]:
        try:
            print(user, card_id, otp, card_name)
            card = UserCard.objects.get(user=user, id=card_id)
        except UserCard.DoesNotExist:
            return self.get_error_response("card_not_found")

        if card.is_confirmed:
            return self.get_error_response("card_is_already_activated")

        payload = {
            "cardId": card.card_token,
            "otp": otp,
            "card_name": card_name or "User",
        }

        success, response_data = self.send_request("CONFIRM_CARD", payload=payload)

        if (
            success
            or response_data.get("error", {}).get("code") == "card_is_already_activated"
        ):
            card_data = response_data.get("result", {}).get("card", {})

            if card_data:
                card.is_confirmed = True
                card.cardholder_name = card_data.get("owner", "")
                card.last_four_digits = card_data.get("number")[-4:]
                card.save(update_fields=["is_confirmed"])
                return True, {"card_token": card.card_token, "is_confirmed": True}

        error_code = (
            response_data.get("error", {"code": "unknown_error"})
            .get("details", {"code": "unknown_error"})
            .get("error", {"code": "unknown_error"})["code"]
        )
        print(">>>", error_code)
        return self.get_error_response(error_code)

    def get_user_cards(self, user_id: str) -> tuple[bool, dict]:
        query_params = {"userId": str(user_id)}
        success, response_data = self.send_request("GET_CARDS", params=query_params)

        if success:
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def get_single_card(self, card_id: str) -> tuple[bool, dict]:
        query_params = {"cardId": str(card_id)}
        success, response_data = self.send_request(
            "GET_SINGLE_CARD", params=query_params
        )

        if success:
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def delete_user_card(self, user: User, card_id: str) -> tuple[bool, dict]:
        card = UserCard.objects.filter(id=int(card_id)).first()

        if not card:
            raise NotFound("User card not found", code="card_not_found")

        query_param = {"userCardId": card.card_id}
        success, response_data = self.send_request("DELETE_CARD", params=query_param)

        if success:
            card.soft_delete()
            response_data = {"detail": "User card is deleted successfully", "code": 204}
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def create_receipt(
            self, 
            user: User, 
            card_token: str, 
            product_id: int, 
            product_type: str
        ) -> tuple[bool, dict]:
        try:
            user_card = UserCard.objects.get(user=user, card_token=card_token)
        except UserCard.DoesNotExist:
            return self.get_error_response("card_not_found")

        if not user_card.is_confirmed:
            return self.get_error_response("card_is_not_activated")

        with db_transaction.atomic():
            if product_type == ProductTypeChoices.COURSE:
                course = Course.objects.filter(id=product_id).first()
                order = Order.objects.create(
                    user=user,
                    amount=course.price,
                    course=course,
                    is_paid=False
                )
            elif product_type == ProductTypeChoices.WEBINAR:
                webinar = Webinar.objects.filter(id=product_id).first()
                order = Order.objects.create(
                    user=user,
                    amount=webinar.price,
                    webinar=webinar,
                    is_paid=False
                )
            else:
                raise APIException("Invalid product type")
            

            transaction = Transaction.objects.create(
                order=order,
                provider=self.provider,
                amount=order.amount,
                status=TransactionStatus.PENDING
            )

        payload = {
            "userId": str(user.id),
            "amount": int(order.amount),
            "account": {
                "order_id": transaction.order.id,
                "card_token": card_token,
                "product_type": product_type,
                "product_id": product_id
            }
        }

        success, response_data = self.send_request("CREATE_RECEIPT", payload=payload)
        print(">>>", success, response_data)

        if success:
            transaction.remote_id = response_data["result"]["transactionId"]
            transaction.provider = self.provider
            transaction.save(update_fields=["remote_id", "provider"])
            response_data["transaction"] = transaction.id
            response_data["user_card"] = user_card.card_token
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def pay_receipt(self, transaction: Transaction, card: UserCard, user_id: int) -> tuple[bool, dict]:
        payload = {
            "transactionId": transaction.remote_id,
            "cardId": card.card_token,
            "userId": user_id,
        }

        success, response_data = self.send_request("PAY_RECEIPT", payload=payload)

        if success:
            transaction_id = response_data.get("result", {}).get("transactionId")
            if not transaction_id:
                return False, {"error": {"code": "invalid_response", "message": "No transactionId in response"}}

            try:
                transaction_from_db = Transaction.objects.get(id=transaction.id)

                with db_transaction.atomic():
                    transaction_from_db.apply_transaction(
                        provider=self.provider,
                        transaction_id=transaction_id,
                        card=card
                    )

                    transaction_from_db.refresh_from_db()
                    if transaction_from_db.status != TransactionStatus.COMPLETED:
                        raise ValueError(f"Transaction status failed to update to SUCCESS, "
                                         f"current status: {transaction_from_db.status}")

                transaction.refresh_from_db()

                response_data = {
                    "detail": "Payment is applied successfully",
                    "code": "payment_success",
                    "status": 200
                }
                return success, response_data

            except Exception as e:
                return False, {"error": {"code": "transaction_error", "message": str(e)}}

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    """
        Utility methods
    """

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

    @staticmethod
    def get_error_response(error_code: str) -> tuple[bool, dict]:
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