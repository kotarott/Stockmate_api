from rest_framework import serializers
from profiles.models import Profile, FavoStock


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

    class Meta:
        model = Profile
        exclude = ('id', 'age', 'gender', )


# class FollowingSerializer(serializers.ModelSerializer):
#     following = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Profile
#         fields = ['following']


# class FollowersSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserFollowing
#         fields = ("id", "followers", "created_at")


# class UserFollowingSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     following_user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = UserFollowing
#         fields = '__all__'