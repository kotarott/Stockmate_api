from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from profiles.models import Profile, FriendShip #FavoStock,
from profiles.api.serializers import ProfileSerializer, FolloweeSerializer, FollowerSerializer #FavoStockSerializer, 
from profiles.api.permissions import IsOwnProfileOrReadOnly #, IsOwnFavoStockOrReadOnly


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    lookup_field ='uuid'
    filter_backends = [SearchFilter]
    search_fields = ['description', 'user__username']


# class FavoStockListAPIView(mixins.ListModelMixin,
#                            generics.GenericAPIView):
#     serializer_class = FavoStockSerializer
#     permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

#     def get_queryset(self):
#         queryset = FavoStock.objects.all()
#         request_uuid = self.kwargs.get('uuid')
#         return queryset.filter(profile__uuid=request_uuid).order_by('-created_at')

#     def get(self, request, uuid):
#         return self.list(request)


# class FavoStockCreateAPIView(generics.CreateAPIView):
#     queryset = FavoStock.objects.all()
#     serializer_class = FavoStockSerializer
#     permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

#     def perform_create(self, serializer):
#         symbol = self.request.data.get('symbol')
#         user_profile = self.request.user.profile
#         queryset = self.get_queryset()

#         has_user_added = self.queryset.filter(symbol=symbol, profile=user_profile).exists()

#         if has_user_added:
#             raise ValidationError('already added.')
        
#         serializer.save(profile=user_profile)


# class FavoStockDestroyAPIView(generics.DestroyAPIView):
#     queryset = FavoStock.objects.all()
#     serializer_class = FavoStockSerializer
#     permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]
#     lookup_field ='symbol'

#     def perform_destroy(self, instance):
#         symbol = self.kwargs.get('symbol')
#         user_profile = self.request.user.profile
#         queryset = self.get_queryset()

#         has_user_added = self.queryset.filter(symbol=symbol, profile=user_profile).exists()

#         if not has_user_added:
#             raise ValidationError('not exists.')

#         instance.delete()


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
    permmission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]

    def post(self, request, uuid):
        follow_user = Profile.objects.filter(uuid=uuid).get()

        try:
            follow = request.user.profile.followee_friendships.create(followee=follow_user)
        except:
            raise ValidationError('already added.')
        
        # serializer_context = {'request': request}
        # serializer = self.serializer_class(follow, context=serializer_context)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        follow_user = Profile.objects.filter(uuid=uuid).get()

        try:
            follow = request.user.profile.followee_friendships.get(followee=follow_user)
            follow.delete()
        except:
            raise ValidationError('not exist.')
        
        return Response(status=status.HTTP_200_OK)


# class UserFollowingViewSet(viewsets.ModelViewSet):

#     permission_classes = [IsAuthenticated, ]
#     serializer_class = UserFollowingSerializer
#     queryset = UserFollowing.objects.all()