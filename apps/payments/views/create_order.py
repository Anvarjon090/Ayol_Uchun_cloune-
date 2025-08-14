from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payments.models import Order
from apps.payments.serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]