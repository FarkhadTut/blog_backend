from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'posts/search', PostsSearchViewSet, basename='PostSearch')
router.register(r'posts', PostsViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename="CommentByPostId")
router.register(r'category', CategoryViewSet, basename='Category')

urlpatterns = [
    path('', include(router.urls)),
]
