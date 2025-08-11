from collections.abc import Callable
from typing import Any, ClassVar

from django.db import transaction as db_transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.choices import TransactionStatus
from apps.payments.models import Providers, Transaction
from apps.payments.paylov.auth import authentication as paylov_auth
from apps.payments.paylov.client import PaylovClient
from apps.payments.paylov.constants import STATUS_CODES, STATUS_TEXT, PaylovMethods
from apps.payments.paylov.serializers import PaylovSerializer


class PaylovAPIView(APIView):
    """
    API view for handling Paylov transactions.

    This view manages the processing of Paylov transactions
    using the specified methods for checking and performing transactions.
    It handles authentication, serialization, and execution of transaction
    methods atomically.
    """

    permission_classes = (AllowAny,)
    http_method_names = ("post",)
    authentication_classes: ClassVar[list] = []

    def __init__(self):
        self.METHODS: dict[str, Callable[[], dict[str, Any]]] = {
            PaylovMethods.CHECK_TRANSACTION: self.check_transaction,
            PaylovMethods.PERFORM_TRANSACTION: self.perform_transaction,
        }
        self.params: dict[str, Any] | None = None
        super().__init__()

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests for processing transactions.

        Authenticates the request, validates input data, and executes
        the specified transaction method in an atomic database transaction.

        Returns a JSON response with the transaction result.
        """
        is_authenticated = paylov_auth(request)
        if not is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        print(">>> Request data: ", request.data)

        serializer = PaylovSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        method = serializer.validated_data["method"]
        self.params = serializer.validated_data["params"]

        with db_transaction.atomic():
            response_data = self.METHODS[method]()

        if isinstance(response_data, dict):
            response_data.update({"jsonrpc": "2.0", "id": request.data.get("id", None)})

        return Response(response_data)

    def check_transaction(self) -> dict[str, Any]:
        """
        Check the status of a Paylov transaction.

        Returns a dictionary with the result indicating whether the transaction
        was found and its current status.
        """
        error, code = PaylovClient(self.params).check_transaction()

        if error:
            if code == STATUS_CODES["ORDER_NOT_FOUND"]:
                return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))
            elif code == STATUS_CODES["INVALID_AMOUNT"]:
                return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))
        return dict(result=dict(status=code, statusText=STATUS_TEXT["SUCCESS"]))

    def perform_transaction(self) -> dict[str, Any]:
        """
        Perform a Paylov transaction.

        Updates the transaction status based on the result of the transaction
        execution and returns a dictionary with the transaction outcome.
        """
        error, code = PaylovClient(self.params).perform_transaction()

        if error and code == STATUS_CODES["ORDER_NOT_FOUND"]:
            return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))

        provider = Providers.objects.filter(key="paylov").last()
        transaction = Transaction.objects.get(
            id=self.params["account"]["order_id"],
            provider=provider,
        )

        if error:
            transaction.status = TransactionStatus.FAILED
            transaction.save(update_fields=["status"])
            return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))

        transaction.apply_transaction(provider=provider)
        return dict(result=dict(status=code, statusText=STATUS_TEXT["SUCCESS"]))