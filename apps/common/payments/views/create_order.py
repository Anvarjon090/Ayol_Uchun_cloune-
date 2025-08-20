from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.payments.serializers import OrderCreateSerializer
from apps.payments.models import Order


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
