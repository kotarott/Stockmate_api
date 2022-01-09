from django.urls import path, include
from stocks.api.v1.views import SearchFMPSymbolAPIView

urlpatterns = [
    path('search/<str:kw>/', SearchFMPSymbolAPIView.as_view(), name='search-symbol'),
]