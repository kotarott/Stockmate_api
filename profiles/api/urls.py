from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from profiles.api.views import ProfileViewSet, FavoStockListAPIView, FavoStockLikeAPIView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('profiles/<str:uuid>/favorites/', FavoStockListAPIView.as_view(), name='favostocks'),
    path('profiles/add_favorite', FavoStockLikeAPIView.as_view(), name="add-favorite")
]