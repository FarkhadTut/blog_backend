from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PictureViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'pictures', PictureViewSet)

urlpatterns = [
    path('posts', include(router.urls)),
]
