from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError

from profiles.models import Profile, FavoStock
from profiles.api.serializers import ProfileSerializer, FavoStockSerializer
from profiles.api.permissions import IsOwnProfileOrReadOnly, IsOwnFavoStockOrReadOnly


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    lookup_field ='uuid'
    filter_backends = [SearchFilter]
    search_fields = ['description']


class FavoStockListAPIView(mixins.ListModelMixin,
                           generics.GenericAPIView):
    serializer_class = FavoStockSerializer
    permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

    def get_queryset(self):
        queryset = FavoStock.objects.all()
        request_uuid = self.kwargs.get('uuid')
        return queryset.filter(profile__uuid=request_uuid).order_by('-created_at')

    def get(self, request, uuid):
        return self.list(request)


class FavoStockCreateAPIView(generics.CreateAPIView):
    queryset = FavoStock.objects.all()
    serializer_class = FavoStockSerializer
    permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

    def perform_create(self, serializer):
        symbol = self.request.data.get('symbol')
        user_profile = self.request.user.profile
        queryset = self.get_queryset()

        has_user_added = self.queryset.filter(symbol=symbol, profile=user_profile).exists()

        if has_user_added:
            raise ValidationError('already added.')
        
        serializer.save(profile=user_profile)


class FavoStockDestroyAPIView(generics.DestroyAPIView):
    queryset = FavoStock.objects.all()
    serializer_class = FavoStockSerializer
    permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]
    lookup_field ='symbol'

    def perform_destroy(self, instance):
        symbol = self.kwargs.get('symbol')
        user_profile = self.request.user.profile
        queryset = self.get_queryset()

        has_user_added = self.queryset.filter(symbol=symbol, profile=user_profile).exists()

        if not has_user_added:
            raise ValidationError('not exists.')

        instance.delete()


# class FollowingListAPIView(mixins.ListModelMixin,
#                            generics.GenericAPIView):
#     serializer_class = FollowingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = Profile.objects.all()
#         request_uuid = self.kwargs.get('uuid')
#         return queryset.filter(uuid=request_uuid)

#     def get(self, request, uuid):
#         return self.list(request)

# class UserFollowingViewSet(viewsets.ModelViewSet):

#     permission_classes = [IsAuthenticated, ]
#     serializer_class = UserFollowingSerializer
#     queryset = UserFollowing.objects.all()