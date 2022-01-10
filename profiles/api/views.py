from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

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


class FavoStockLikeAPIView(generics.GenericAPIView):
    queryset = FavoStock.objects.all()
    serializer_class = FavoStockSerializer
    permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

    def post(self, request, symbol):
        return self.create(request)
    
    def delete(self, request, symbol):
        return self.delete(request)

# stocksのviewを作ってから。そこにuser_has_addedフィールドを入れる。
# class FavoStockAPIView(APIView):
#     serializer_class = FavoStockSerializer
#     permission_classes = [IsAuthenticated, IsOwnFavoStockOrReadOnly]

#     def post(self, request, ticker):

