from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from profiles.api.views import ProfileViewSet

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]