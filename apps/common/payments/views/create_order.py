from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from apps.payments.models import Order, Transaction, Providers
from apps.payments.choices import OrderStatus, TransactionStatus
from apps.common.payments.serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]