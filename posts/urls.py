from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'posts', PostsViewSet)
router.register(r'search', PostsSearchViewSet, basename='PostSearch')

urlpatterns = [
    path('', include(router.urls)),
]
