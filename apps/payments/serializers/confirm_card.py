from rest_framework import serializers

class ConfirmUserCardSerializer(serializers.Serializer):
    card_id = serializers.IntegerField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    card_name = serializers.CharField(max_length=255, required=True)