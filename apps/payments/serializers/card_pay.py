from rest_framework import serializers

from apps.courses.choices import ProductTypeChoices


class UserCardReceiptCreateSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(
        choices=ProductTypeChoices.choices, required=True
    )
    product_id = serializers.IntegerField(required=True)
    cart_tokin = serializers.CharField(required=True)


class UserCardReceiptConfirmSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(required=True)
    card_tokin = serializers.CharField(required=True)
