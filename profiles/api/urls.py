from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from profiles.api.views import (ProfileViewSet, FolloweeListAPIView,
    FollowerListAPIView, FollowAPIView, CharacteristicUpdateAPIView)
from stocks.api.v1.views import SymbolLikeListAPIView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('characteristic/', CharacteristicUpdateAPIView.as_view(), name="characteristic"),
    path('profiles/<str:uuid>/favorites/', SymbolLikeListAPIView.as_view(), name='favorites'),
    path('profiles/<str:uuid>/followees/', FolloweeListAPIView.as_view(), name='followees'),
    path('profiles/<str:uuid>/followers/', FollowerListAPIView.as_view(), name='followers'),
    path('follow/<str:uuid>/', FollowAPIView.as_view(), name='follow'),
]