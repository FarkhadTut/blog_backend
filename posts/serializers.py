from rest_framework import serializers
from .models import Post, Picture, Comment



class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'post',  'image', 'description']
    

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField('get_author_username')
    author_email = serializers.SerializerMethodField('get_author_email')
    class Meta:
        model = Comment
        fields = "__all__"
        # fields = ['id', 'text', 'author', 'post', 'created_at', 'updated_at']
    

    def get_author_username(self, obj):
        return obj.author.username
    
    def get_author_email(self, obj):
        return obj.author.email


class PostSerializer(serializers.ModelSerializer):

    body = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    pictures = PictureSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def get_body(self, instance):
        return instance.body.html
    
    def get_author_username(self, instance):
        return instance.author.username

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'author', 'title', 'pictures', 'comments', 'body', 'created_at', 'updated_at']
    
