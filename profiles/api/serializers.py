from rest_framework import serializers
from profiles.models import Profile, FavoStock


class FavoStockSerializer(serializers.ModelSerializer):
    profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FavoStock
        # fields = '__all__'
        exclude = ('updated_at', )


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        exclude = ('id', 'age', 'gender')

