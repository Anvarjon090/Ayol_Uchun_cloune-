from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.paylov.client import PaylovClient
from apps.payments.serializers import DeleteUserCardSerializer


class DeleteUserCardAPIView(APIView):
    serializer_class = DeleteUserCardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DeleteUserCardSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, response = PaylovClient().delete_user_card(
            card_id=serializer.validated_data("card_id")
        )

        return Response(data=response, status=status.HTTP_200_OK)
