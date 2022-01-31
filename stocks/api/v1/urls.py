from django.urls import path, include
from stocks.api.v1.views import (SearchFMPSymbolListAPIView, FMPSymbolDetailAPIView, fmp_get_historical_price,
    SymbolListViewSet, SymbolLikeAPIView, SymbolCommentListCreateAPIView, CommentViewSet, TagViewSet, SymbolTagsRUDAPIView,
    TagToSymbolListAPIView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename='comments')
router.register(r"symbols", SymbolListViewSet, basename='symbols')
router.register(r"tags", TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
    path('symbols/<slug:slug>/like/', SymbolLikeAPIView.as_view(), name='symbol-like'),
    path('symbols/<slug:slug>/comments/', SymbolCommentListCreateAPIView.as_view(), name='symbol-comment'),
    path('symbols/<slug:slug>/tags/', SymbolTagsRUDAPIView.as_view(), name='symbol-tag'),

    path('tags/<str:name>/symbols/', TagToSymbolListAPIView.as_view(), name='tag-symbol'),

    path('stocks/v1/search/<str:kw>/', SearchFMPSymbolListAPIView.as_view(), name='search-symbol'),
    path('stocks/v1/profile/<str:symbol>/', FMPSymbolDetailAPIView.as_view(), name='profile'),
    path('stocks/v1/historical_price/<str:symbol>/', fmp_get_historical_price, name='histrical-price'),
]