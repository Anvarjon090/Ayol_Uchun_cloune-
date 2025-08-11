from rest_framework import serializers
from django.db import transaction

from apps.payments.models import Order, Transaction, Providers
from apps.payments.choices import TransactionStatus

from apps.payments.models import Order, Transaction
from apps.courses.models import Course, Webinar
from apps.courses.choices import ProductTypeChoices
from apps.payments.paylov.client import PaylovClient


class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    product_type = serializers.ChoiceField(
        choices=ProductTypeChoices.choices, required=True
    )

    def create(self, validated_data):
        user = self.context["request"].user
        product_id = validated_data["product_id"]
        product_type = validated_data["product_type"]

        if product_type == ProductTypeChoices.COURSE:
            product = Course.objects.filter(id=product_id).first()
        elif product_type == ProductTypeChoices.WEBINAR:
            product = Webinar.objects.filter(id=product_id).first()
        else:
            raise serializers.ValidationError("Invalid product type")

        if not product:
            raise serializers.ValidationError("Product not found")

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                course=product if product_type == ProductTypeChoices.COURSE else None,
                webinar=product if product_type == ProductTypeChoices.WEBINAR else None,
                amount=product.price,
            )

            provider = Providers.objects.filter(key="paylov").last()
            transaction_obj = Transaction.objects.create(
                order=order,
                provider=provider,
                status=TransactionStatus.PENDING,
                amount=order.amount,
            )

        # Attach transaction for to_representation
        order._transaction = transaction_obj

        return order

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "amount": instance.amount,
            "payment_url": instance._transaction.get_payment_url,
        }