from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apps.payments.paylov.client import PaylovClient
from apps.common.payments.serializers import ConfirmUserCardSerializer


class ConfirmUserCardAPIView(APIView):
    serializer_class = ConfirmUserCardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ConfirmUserCardSerializer,
        responses={200: "Success", 400: "Validation Error"}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, response = PaylovClient().confirm_user_card(
            user=request.user,
            card_id=serializer.validated_data["card_id"],
            otp=serializer.validated_data["otp"],
            card_name=serializer.validated_data["card_name"]
        )

        return Response(
            data=response,
            status=status.HTTP_200_OK
        )