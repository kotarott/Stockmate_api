from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from stockmate.lib import fmp_api
from stocks.api.v1.serializers import (FMPSearchSymbolSerializer, FMPSymbolProfileSerializer,
    SymbolSerializer, FavoriteSymbolSerializer)
from stocks.models import Symbol, FavoriteSymbol


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

    def get(self, request, uuid):
        return self.list(request)


class SymbolListCreateAPIView(generics.ListCreateAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save()


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
