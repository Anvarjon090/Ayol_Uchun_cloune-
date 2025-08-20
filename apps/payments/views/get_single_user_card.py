from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.paylov.client import PaylovClient


class GetSingleUserCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        _, response = PaylovClient().get_single_card(user_id=kwargs.get("card_id"))

        return Response(data=response, status=status.HTTP_200_OK)
