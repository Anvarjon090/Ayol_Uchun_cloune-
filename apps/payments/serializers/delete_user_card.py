from rest_framework import serializers


class DeleteUserCardSerializer(serializers.Serializer):
    card_id = serializers.CharField(required=True)
