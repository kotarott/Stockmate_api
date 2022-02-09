from django.urls import path, include
from stocks.api.v1.views import (SearchFMPSymbolListAPIView, FMPSymbolDetailAPIView, fmp_get_historical_price,
    SymbolListViewSet, SymbolLikeAPIView, CommentViewSet, TagListAPIView, SymbolTagsRUAPIView, SymbolCommentListAPIView,
    TagToSymbolListAPIView, ImageViewSet, SymbolRUDAPIView, TagViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename='comments')
router.register(r"symbols", SymbolListViewSet, basename='symbols')
router.register(r"tags", TagViewSet, basename='tags')
router.register(r"images", ImageViewSet, basename='images')


urlpatterns = [
    path('', include(router.urls)),
    path('symbols/<slug:slug>/like/', SymbolLikeAPIView.as_view(), name='symbol-like'),
    path('symbols/<slug:slug>/comments/', SymbolCommentListAPIView.as_view(), name='symbol-comment'),
    path('symbols/<slug:slug>/tags/', SymbolTagsRUAPIView.as_view(), name='symbol-tag'),
    path('symbols/<slug:slug>/update/', SymbolRUDAPIView.as_view(), name='symbol-update'),

    path('taglist/', TagListAPIView.as_view(), name='taglist'),

    path('tags/<slug:slug>/symbols/', TagToSymbolListAPIView.as_view(), name='tag-symbol'),

    path('stocks/v1/search/<str:kw>/', SearchFMPSymbolListAPIView.as_view(), name='search-symbol'),
    path('stocks/v1/profile/<str:symbol>/', FMPSymbolDetailAPIView.as_view(), name='profile'),
    path('stocks/v1/line-chart/<str:symbol>/', fmp_get_historical_price, name='histrical-price'),
]