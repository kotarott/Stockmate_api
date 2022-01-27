from rest_framework import serializers

# from profiles.models import FavoStock
from stocks.models import Symbol


class SymbolSerializer(serializers.ModelSerializer):
    user_has_liked_symbol = serializers.SerializerMethodField()

    class Meta:
        model = Symbol

    def create(self, validated_data):
        request_profile = self.context.request.user.profile
        stock = Symbol.objects.create(**validated_data)
        Symbol.voters.add(request_profile)
        return stock

    def get_user_has_liked_symbol(self, request):
        request_profile = self.context.request.user.profile


class FMPSearchSymbolSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    currency = serializers.CharField(max_length=3)
    stockExchange = serializers.CharField(max_length=100)
    exchangeShortName = serializers.CharField(max_length=15)
    user_has_liked_symbol = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    vender = serializers.SerializerMethodField()
    is_record = serializers.SerializerMethodField()

    def get_user_has_liked_symbol(self, instance):
        request = self.context.get('request')
        return Symbol.objects.filter(profile=request.user.profile, symbol=instance['symbol']).voters.exists()

    def get_like_count(self, instance):
        return Symbol.objects.filter(symbol=instance['symbol']).voters.count()

    def is_record(self, instance):
        return Symbol.objects.filter(symbol=instance['symbol']).exists()

    def get_vender(self, instance):
        return 'FMP'


class FMPSymbolProfileSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=20)
    price = serializers.FloatField()
    beta = serializers.FloatField()
    volAvg = serializers.IntegerField()
    lastDiv = serializers.FloatField()
    changes = serializers.FloatField()
    companyName = serializers.CharField(max_length=100)
    currency = serializers.CharField(max_length=3)
    isin = serializers.CharField(max_length=12)
    exchange = serializers.CharField(max_length=50)
    sector = serializers.CharField(max_length=20)
    industry = serializers.CharField(max_length=20)
    website = serializers.URLField(max_length=200)
    description = serializers.CharField()
    image = serializers.URLField(max_length=200)
    address = serializers.CharField(max_length=100)
    ipoDate = serializers.DateField()
    user_has_liked_symbol = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_user_has_liked_symbol(self, instance):
        request = self.context.get('request')
        return Symbol.objects.filter(profile=request.user.profile, symbol=instance['symbol']).voters.exists()

    def get_like_count(self, instance):
        return Symbol.objects.filter(symbol=instance['symbol']).voters.count()

