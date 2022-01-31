from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from profiles.models import Profile, FriendShip 
from profiles.api.serializers import ProfileSerializer, FolloweeSerializer, FollowerSerializer, ProfileCharacteristicSerializer
from profiles.api.permissions import IsOwnProfileOrReadOnly, IsOwnProfile


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    lookup_field ='uuid'
    filter_backends = [SearchFilter]
    search_fields = ['description', 'user__username']


class MyProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]

    def get_object(self):
        request_user = self.request.user.profile
        return request_user


class FolloweeListAPIView(mixins.ListModelMixin,
                           generics.GenericAPIView):
    serializer_class = FolloweeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FriendShip.objects.all()
        request_uuid = self.kwargs.get('uuid')
        return queryset.filter(follower__uuid=request_uuid)

    def get(self, request, uuid):
        return self.list(request)


class FollowerListAPIView(mixins.ListModelMixin,
                           generics.GenericAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FriendShip.objects.all()
        request_uuid = self.kwargs.get('uuid')
        return queryset.filter(followee__uuid=request_uuid)

    def get(self, request, uuid):
        return self.list(request)


class FollowAPIView(APIView):
    serializer_class = ProfileSerializer
    permmission_classes = [IsAuthenticated, IsOwnProfile]

    def post(self, request, uuid):
        follow_user = Profile.objects.filter(uuid=uuid).get()

        try:
            follow = request.user.profile.followee_friendships.create(followee=follow_user)
        except:
            raise ValidationError('already added.')

        return Response(
            {
                "request": 'add',
                'completed': True
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, uuid):
        follow_user = Profile.objects.filter(uuid=uuid).get()

        try:
            follow = request.user.profile.followee_friendships.get(followee=follow_user)
            follow.delete()
        except:
            raise ValidationError('not exist.')
        
        return Response(
            {
                "request": 'remove',
                'completed': True
            },
            status=status.HTTP_200_OK
        )


class CharacteristicUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileCharacteristicSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]

    def get_object(self):
        profile_object = self.request.user.profile
        print(profile_object)
        return profile_object