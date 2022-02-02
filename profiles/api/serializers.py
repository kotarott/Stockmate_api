from rest_framework import serializers
from profiles.models import Profile, FriendShip #FavoStock, 
from rest_framework.reverse import reverse

from profiles.lib.birth import get_age


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    description = serializers.CharField(read_only=True)
    # generation = serializers.SerializerMethodField()
    # favorites = serializers.HyperlinkedIdentityField(
    #     view_name='favorites',
    #     lookup_field='uuid'
    # )
    # comments = serializers.HyperlinkedIdentityField(
    #     view_name='comments',
    #     lookup_field='uuid'
    # )
    # followees = serializers.HyperlinkedIdentityField(
    #     view_name='followees',
    #     lookup_field='uuid'
    # )
    # followers = serializers.HyperlinkedIdentityField(
    #     view_name='followers',
    #     lookup_field='uuid'
    # )
    followee_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_user_followee = serializers.SerializerMethodField()
    is_user_follower = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ('id', 'gender', 'birth', 'followees', 'followers')
    
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

    # def get_generation(self, instance):
    #     birthday = instance.birth
    #     if (birthday):
    #         age = get_age(birthday.year, birthday.month, birthday.day)
    #         return age
    #     return False
    
    def get_is_user(self, instance):
        request = self.context.get('request')
        return instance.user == request.user


class ProfileCharacteristicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('birth', 'gender', 'description')


class FolloweeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    uuid = serializers.SerializerMethodField()
    followee_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_user_followee = serializers.SerializerMethodField()
    is_user_follower = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendShip
        exclude = ('follower', 'id')

    def get_user(self, instance):
        return instance.followee.user.username

    def get_description(self, instance):
        return instance.followee.description

    def get_uuid(self, instance):
        return instance.followee.uuid
    
    def get_followee_count(self, instance):
        return instance.followee.followees.count()
    
    def get_follower_count(self, instance):
        return instance.followee.followers.count()
    
    def get_is_user_followee(self, instance):
        request = self.context.get('request')
        return instance.followee.followers.filter(user=request.user).exists()
    
    def get_is_user_follower(self, instance):
        request = self.context.get('request')
        return instance.followee.followees.filter(user=request.user).exists()
    
    def get_is_user(self, instance):
        request = self.context.get('request')
        return instance.followee.user == request.user


class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    uuid = serializers.SerializerMethodField()
    followee_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    is_user_followee = serializers.SerializerMethodField()
    is_user_follower = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendShip
        exclude = ('followee','follower', 'id', 'created_at')

    def get_user(self, instance):
        return instance.follower.user.username
    
    def get_description(self, instance):
        return instance.follower.description

    def get_uuid(self, instance):
        return instance.follower.uuid

    def get_followee_count(self, instance):
        return instance.follower.followees.count()

    def get_follower_count(self, instance):
        return instance.follower.followers.count()

    def get_is_user_followee(self, instance):
        request = self.context.get('request')
        return instance.follower.followers.filter(user=request.user).exists()
    
    def get_is_user_follower(self, instance):
        request = self.context.get('request')
        return instance.follower.followees.filter(user=request.user).exists()
    
    def get_is_user(self, instance):
        request = self.context.get('request')
        return instance.follower.user == request.user