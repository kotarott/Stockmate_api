from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter

from stockmate.lib import fmp_api
from stocks.api.v1.permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from stocks.api.v1.serializers import (FMPSearchSymbolSerializer, FMPSymbolProfileSerializer,
    SymbolSerializer, FavoriteSymbolSerializer, SymbolCommentSerializer, TagSerializer, SymbolTagsSerializer,
    ImageSerializer, UnitTagSerializer, UnitSymbolSerializer)
from stocks.models import Symbol, FavoriteSymbol, Comment, Tag, Image


class SymbolLikeAPIView(APIView):
    serializer_class = SymbolSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, slug):
        symbol = get_object_or_404(Symbol, slug=slug)
        symbol.voters.add(request.user.profile)
        symbol.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(symbol, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, slug):
        symbol = get_object_or_404(Symbol, slug=slug)
        symbol.voters.remove(request.user.profile)
        symbol.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(symbol, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SymbolLikeListAPIView(generics.ListAPIView):
    serializer_class = FavoriteSymbolSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = FavoriteSymbol.objects.all()
        request_uuid = self.kwargs.get('uuid')
        return queryset.filter(profile__uuid=request_uuid)


class SymbolListViewSet(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    queryset = Symbol.objects.all()
    serializer_class = UnitSymbolSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'


class SymbolRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SymbolSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Symbol.objects.all()
        request_slug = self.kwargs.get('slug')
        return queryset.filter(slug=request_slug)


# class SymbolCommentListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = SymbolCommentSerializer
#     permission_classes = [IsAuthenticated, IsOwnCommentOrReadOnly]

#     def get_queryset(self):
#         request_slug = self.kwargs.get('slug')
#         queryset = Symbol.objects.filter(slug=request_slug).comments.order_by('-created_at')
#         return queryset
 
    # def perform_create(self, serializer):
    #     symbol = Symbol.objects.get(slug=self.kwargs.get('slug'))
    #     profile = self.request.user.profile
    #     serializer.save(symbol=symbol, author=profile)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = SymbolCommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [SearchFilter]
    lookup_field = 'uuid'
    search_fields = ['body', 'symbol__symbol', 'symbol__description']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)


class ProfileCommentListAPIView(generics.ListAPIView):
    serializer_class = SymbolCommentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        request_uuid = self.kwargs.get('uuid')
        queryset = Comment.objects.filter(author__uuid=request_uuid).order_by('-created_at')
        return queryset


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = UnitTagSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


class SymbolTagsRUAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = SymbolTagsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Symbol.objects.all()
        request_slug = self.kwargs.get('slug')
        return queryset.filter(slug=request_slug)


class TagToSymbolListAPIView(generics.ListAPIView):
    serializer_class = SymbolSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        request_tag = self.kwargs.get('name')
        queryset = Tag.objects.get(name=request_tag).symbol_set.all()
        print(queryset)
        return queryset


# stockAPI
class SearchFMPSymbolListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FMPSearchSymbolSerializer

    def get(self, request, kw):
        data = fmp_api.search_symbol(kw)
        if data:
            results = FMPSearchSymbolSerializer(data, many=True, context={"request": request})
            return Response(results.data)
        else:
            return Response(
                {
                    "error": {
                        "code": 404,
                        "message": "not found"
                    }
                },
                status = status.HTTP_404_NOT_FOUND
            )


class FMPSymbolDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FMPSymbolProfileSerializer
    
    def get(self, request, symbol):
        data = fmp_api.get_profile(symbol)
        if data:
            results = FMPSymbolProfileSerializer(data, many=True, context={"request": request})
            return Response(results.data[0]) #配列ではなくオブジェクトで返す。
        else:
            return Response(
                {
                    "error": {
                        "code": 404,
                        "message": "not found"
                    }
                },
                status = status.HTTP_404_NOT_FOUND
            )

# APIのJsonの形が変わった時に備え、Serializerを通した方がいいかもしれない…
@api_view(['GET'])
def fmp_get_historical_price(request, symbol):
    data = fmp_api.get_historical_price(symbol)
    if data:
        return Response(data)
    else:
        return Response(
            {
                "error": {
                    "code": 404,
                    "message": "not found"
                }
            },
            status = status.HTTP_404_NOT_FOUND
        )
