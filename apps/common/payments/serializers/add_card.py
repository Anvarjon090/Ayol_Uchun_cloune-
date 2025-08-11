from rest_framework import serializers


class AddUserCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, required=True)
    exp_month = serializers.CharField(max_length=2, required=True)
    exp_year = serializers.CharField(max_length=2, required=True)