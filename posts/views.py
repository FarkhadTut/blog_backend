from rest_framework import viewsets
from .models import Post, Picture, Comment
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.viewsets import ModelViewSet
from .serializers import PictureSerializer, PostSerializer, CommentSerializer
from rest_framework import status
from blog.drf_defaults import MyPaginator
from users.models import User
from time import sleep 
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    ordering = ['-created_at']


class PostsSearchViewSet(ModelViewSet):
    pagination_class = MyPaginator

    def list(self, request, *args, **kwargs):
        search_query = request.query_params['q']
        posts = Post.objects.filter(body__contains=search_query)

        sleep(2)
        if len(posts) != 0:
            results = self.paginate_queryset(posts)
            serializer = PostSerializer(instance=results, many=True)
            return self.get_paginated_response(serializer.data)
        
        return Response("Posts not found.", status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    ordering = ['-created_at']
    

    def list(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        comments = Comment.objects.filter(post__id=post_id).order_by(*self.ordering)
        if len(comments) != 0:
            results = self.paginate_queryset(comments)
            serializer = CommentSerializer(instance=results, many=True)
            return self.get_paginated_response(serializer.data)

        return Response("Posts not found.", status=status.HTTP_404_NOT_FOUND)
 

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)