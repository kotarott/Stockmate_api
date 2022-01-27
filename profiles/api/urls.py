from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from profiles.api.views import (ProfileViewSet, 
    FavoStockListAPIView, FavoStockCreateAPIView, FolloweeListAPIView, #FavoStockDestroyAPIView, 
    FollowerListAPIView, FollowAPIView)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename='profiles')
# router.register(r"followers", UserFollowingViewSet, basename='followers')

urlpatterns = [
    path('', include(router.urls)),
    # path('profiles/<str:uuid>/favorites/', FavoStockListAPIView.as_view(), name='favorites'),
    path('profiles/<str:uuid>/followees/', FolloweeListAPIView.as_view(), name='followees'),
    path('profiles/<str:uuid>/followers/', FollowerListAPIView.as_view(), name='followers'),
    path('follow/<str:uuid>/', FollowAPIView.as_view(), name='follow'),

    # path('addfavorite/', FavoStockCreateAPIView.as_view(), name="add-favorite"),
    # path('removefavorite/<str:symbol>/', FavoStockDestroyAPIView.as_view(), name='remove-favorite'),
]