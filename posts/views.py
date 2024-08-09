from rest_framework import viewsets
from .models import Post, Picture
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PictureSerializer, PostSerializer
from rest_framework import status
from blog.drf_defaults import MyPaginator

class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class PostsSearchViewSet(ModelViewSet):
    pagination_class = MyPaginator

    def list(self, request, *args, **kwargs):
        search_query = request.query_params['q']
        posts = Post.objects.filter(body__contains=search_query)
        if len(posts) != 0:
            results = self.paginate_queryset(posts)
            serializer = PostSerializer(instance=results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response("Posts not found.", status=status.HTTP_404_NOT_FOUND)

