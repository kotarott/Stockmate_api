from django.urls import path, include
from stocks.api.v1.views import SearchFMPSymbolListAPIView, FMPSymbolDetailAPIView, fmp_get_historical_price

urlpatterns = [
    path('search/<str:kw>/', SearchFMPSymbolListAPIView.as_view(), name='search-symbol'),
    path('profile/<str:symbol>', FMPSymbolDetailAPIView.as_view(), name='profile'),
    path('historical_price/<str:symbol>', fmp_get_historical_price, name='histrical-price'),

]