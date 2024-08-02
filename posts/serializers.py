from rest_framework import serializers
from .models import Post, Picture



class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'post',  'image', 'description']
    
class PostSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'pictures', 'body', 'created_at', 'updated_at']
    
