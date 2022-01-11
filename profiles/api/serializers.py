from rest_framework import serializers
from profiles.models import Profile, FavoStock, FriendShip
from rest_framework.reverse import reverse


class FavoStockSerializer(serializers.ModelSerializer):
    profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FavoStock
        exclude = ('updated_at', )


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    favorites = serializers.HyperlinkedIdentityField(
        view_name='favorites',
        lookup_field='uuid'
    )
    followees = serializers.HyperlinkedIdentityField(
        view_name='followees',
        lookup_field='uuid'
    )
    followers = serializers.HyperlinkedIdentityField(
        view_name='followers',
        lookup_field='uuid'
    )
    followee_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_user_followee = serializers.SerializerMethodField()
    is_user_follower = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ('id', 'age', 'gender', )
    
    def get_followee_count(self, instance):
        return instance.followees.count()

    def get_follower_count(self, instance):
        return instance.followers.count()
    
    def get_is_user_followee(self, instance):
        request = self.context.get('request')
        return instance.followers.filter(user=request.user).exists()
    
    def get_is_user_follower(self, instance):
        request = self.context.get('request')
        return instance.followees.filter(user=request.user).exists()


class FolloweeSerializer(serializers.ModelSerializer):
    followee = serializers.StringRelatedField(read_only=True)
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = FriendShip
        exclude = ('follower', 'id')

    def get_uuid(self, instance):
        return instance.followee.uuid


class FollowerSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = FriendShip
        exclude = ('followee', 'id')

    def get_uuid(self, instance):
        return instance.followee.uuid
