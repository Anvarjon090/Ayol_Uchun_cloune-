from rest_framework import serializers


class AddUserCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=19, min_length=19)
    expire_month = serializers.IntegerField(min_value=1, max_value=12)
    expire_year = serializers.IntegerField(min_value=2000)