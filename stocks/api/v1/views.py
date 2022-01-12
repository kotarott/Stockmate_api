from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stockmate.lib import fmp_api
from stocks.api.v1.serializers import FMPSearchSymbolSerializer, FMPSymbolProfileSerializer


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
