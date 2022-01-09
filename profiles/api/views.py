from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.api.serializers import ProfileSerializer, FavoStockSerializer
from profiles.api.permissions import IsOwnProfileOrReadOnly, IsOwnFavoStockOrReadOnly


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    lookup_field ='uuid'

# stocksのviewを作ってから。そこにuser_has_addedフィールドを入れる。
# class FavoStockAPIView(APIView):
#     serializer_class = FavoStockSerializer
#     permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

#     def post(self, request, ticker):

