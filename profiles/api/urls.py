from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from profiles.api.views import (ProfileViewSet, 
    FavoStockListAPIView, FavoStockCreateAPIView, FavoStockDestroyAPIView)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename='profiles')
# router.register(r"followers", UserFollowingViewSet, basename='followers')

urlpatterns = [
    path('', include(router.urls)),
    path('profiles/<str:uuid>/favorites/', FavoStockListAPIView.as_view(), name='favorites'),

    path('addfavorite/', FavoStockCreateAPIView.as_view(), name="add-favorite"),
    path('removefavorite/<str:symbol>/', FavoStockDestroyAPIView.as_view(), name='remove-favorite'),
]