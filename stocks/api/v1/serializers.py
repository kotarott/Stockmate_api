from rest_framework import serializers

from profiles.models import FavoStock


class FMPSearchSymbolSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    currency = serializers.CharField(max_length=3)
    stockExchange = serializers.CharField(max_length=100)
    exchangeShortName = serializers.CharField(max_length=15)
    user_has_liked_symbol = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_user_has_liked_symbol(self, instance):
        request = self.context.get('request')
        return FavoStock.objects.filter(profile=request.user.profile, symbol=instance['symbol']).exists()

    def get_like_count(self, instance):
        return FavoStock.objects.filter(symbol=instance['symbol']).count()