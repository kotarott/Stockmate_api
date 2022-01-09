from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from stockmate.lib import fmp_api


class SearchFMPSymbolAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,kw):
        data = fmp_api.search_symbol(kw)
        if data:
            return Response(data, status=status.HTTP_200_OK)
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