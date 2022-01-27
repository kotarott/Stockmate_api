from django.urls import path, include
from stocks.api.v1.views import (SearchFMPSymbolListAPIView, FMPSymbolDetailAPIView, fmp_get_historical_price,
    SymbolCreateAPIView, SymbolLikeAPIView)

urlpatterns = [
    path('search/<str:kw>/', SearchFMPSymbolListAPIView.as_view(), name='search-symbol'),
    path('profile/<str:symbol>', FMPSymbolDetailAPIView.as_view(), name='profile'),
    path('historical_price/<str:symbol>', fmp_get_historical_price, name='histrical-price'),

    path('symbols/', SymbolCreateAPIView.as_view(), name='symbols'),
    path('symbols/<slug:slug>/like/', SymbolLikeAPIView.as_view(), name='symbol-like'),
]