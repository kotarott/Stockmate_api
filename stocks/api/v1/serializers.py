from rest_framework import serializers

# from profiles.models import FavoStock
from stocks.models import Symbol, FavoriteSymbol, Comment, Tag


class SymbolSerializer(serializers.ModelSerializer):
    user_has_liked_symbol = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Symbol
        exclude = ['created_at', 'updated_at', 'voters', 'id']

    def get_user_has_liked_symbol(self, instance):
        request = self.context.get('request')
        return instance.voters.filter(pk=request.user.profile.id).exists()

    def get_likes_count(self, instance):
        return instance.voters.count()
    
    def get_comments_count(self, instance):
        return instance.comments.count()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class SymbolTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symbol
        fields = ('tags', )


class FavoriteSymbolSerializer(serializers.ModelSerializer):
    symbol = SymbolSerializer()

    class Meta:
        model = FavoriteSymbol
        exclude = ('id', 'profile',)


class SymbolCommentSerializer(serializers.ModelSerializer):
    symbol = serializers.StringRelatedField(read_only=True)
    symbol_des = serializers.SerializerMethodField()
    symbol_slug = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
    author_uuid = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('updated_at', )

    def get_author_uuid(self, instance):
        return instance.author.uuid

    def get_created_at(self, instance):
        return instance.created_at.strftime('%B %d, %T')

    def get_symbol_des(self, instance):
        return instance.symbol.description

    def get_symbol_slug(self, instance):
        return instance.symbol.slug


# StockAPI
class FMPSearchSymbolSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    currency = serializers.CharField(max_length=3)
    stockExchange = serializers.CharField(max_length=100)
    exchangeShortName = serializers.CharField(max_length=15)
    user_has_liked_symbol = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    vender = serializers.SerializerMethodField()
    symbol_slug = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_user_has_liked_symbol(self, instance):
        request = self.context.get('request')
        is_symbol = Symbol.objects.filter(symbol=instance['symbol']).exists()
        if is_symbol:
            return Symbol.objects.get(symbol=instance['symbol']).voters.filter(pk=request.user.profile.id).exists()
        return False

    def get_likes_count(self, instance):
        is_symbol = Symbol.objects.filter(symbol=instance['symbol']).exists()
        if is_symbol:
            return Symbol.objects.get(symbol=instance['symbol']).voters.count()
        return 0
    
    def get_comments_count(self, instance):
        is_symbol = Symbol.objects.filter(symbol=instance['symbol']).exists()
        if is_symbol:
            return Symbol.objects.get(symbol=instance['symbol']).comments.count()
        return 0

    def get_symbol_slug(self, instance):
        symbol = Symbol.objects.filter(symbol=instance['symbol'])
        if symbol.exists():
            return symbol.get().slug
        return False

    def get_vender(self, instance):
        return 'FMP'

    def get_tags(self, instance):
        symbol = Symbol.objects.filter(symbol=instance['symbol'])
        if symbol.exists():
            return symbol.get().tags.values('id', 'name')
        return False


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
    vender = serializers.SerializerMethodField()
    symbol_slug = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_user_has_liked_symbol(self, instance):
        request = self.context.get('request')
        is_symbol = Symbol.objects.filter(symbol=instance['symbol']).exists()
        if is_symbol:
            return Symbol.objects.get(symbol=instance['symbol']).voters.filter(pk=request.user.profile.id).exists()
        return False

    def get_like_count(self, instance):
        request = self.context.get('request')
        is_symbol = Symbol.objects.filter(symbol=instance['symbol']).exists()
        if is_symbol:
            return Symbol.objects.get(symbol=instance['symbol']).voters.count()
        return 0
    
    def get_vender(self, instance):
        return 'FMP'
    
    def get_symbol_slug(self, instance):
        symbol = Symbol.objects.filter(symbol=instance['symbol'])
        if symbol.exists():
            return symbol.get().slug
        return False

    def get_tags(self, instance):
        symbol = Symbol.objects.filter(symbol=instance['symbol'])
        if symbol.exists():
            return symbol.get().tags.values()
        return False

