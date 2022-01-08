from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins

from profiles.models import Profile
from profiles.api.serializers import ProfileSerializer, FavoStockSerializer
from profiles.api.permissions import IsOwnProfileOrReadOnly


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    lookup_field ='uuid'


