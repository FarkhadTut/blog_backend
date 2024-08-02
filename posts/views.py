from rest_framework import viewsets
from .models import Post, Picture
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PictureSerializer, PostSerializer
from django.shortcuts import get_object_or_404

class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer