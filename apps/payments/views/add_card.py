from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.paylov.client import PaylovClient
from apps.payments.serializers import AddUserCardSerializer


class AddUserCardAPIView(APIView):
    serializer_class = AddUserCardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AddUserCardSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, response = PaylovClient().create_user_card(
            user=request.user,
            card_number=serializer.validated_data["card_number"],
            expire_month=serializer.validated_data["exp_month"],
            expire_year=serializer.validated_data["exp_year"],
        )

        return Response(data=response, status=status.HTTP_200_OK)
