from rest_framework import serializers
from profiles.models import Profile, FavoStock


class FavoStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoStock
        # fields = '__all__'
        exclude = ('id', 'profile', 'updated_at')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    favorites = FavoStockSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

