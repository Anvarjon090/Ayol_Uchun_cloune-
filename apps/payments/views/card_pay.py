from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.models import Transaction, UserCard
from apps.payments.paylov.client import PaylovClient
from apps.payments.serializers import (
    UserCardReceiptConfirmSerializer,
    UserCardReceiptCreateSerializer,
)


class UserCardReceiptCreateAPIView(APIView):
    serializer_class = UserCardReceiptCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserCardReceiptCreateSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_token = serializer.validated_data["card_token"]
        product_id = serializer.validated_data["product_id"]
        product_type = serializer.validated_data["product_type"]

        _, response = PaylovClient().create_receipt(
            user=request.user,
            card_token=card_token,
            product_id=product_id,
            product_type=product_type,
        )

        return Response(data=response, status=status.HTTP_200_OK)


class UserCardReceiptConfirmAPIView(APIView):
    serializer_class = UserCardReceiptConfirmSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserCardReceiptConfirmSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_id = serializer.validated_data["transaction_id"]
        transaction = Transaction.objects.filter(remote_id=transaction_id).first()
        card_token = serializer.validated_data["card_token"]
        card = UserCard.objects.filter(card_token=card_token).first()

        if not card:
            return Response(
                data={"detail": "User card not found", "code": "card_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        _, response = PaylovClient().pay_receipt(
            user_id=request.user.id,
            transaction=transaction,
            card=card,
        )

        return Response(data=response, status=status.HTTP_200_OK)
