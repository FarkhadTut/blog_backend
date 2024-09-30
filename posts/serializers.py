from rest_framework import serializers
from .models import *
from django.forms.models import model_to_dict


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'post',  'image', 'description']
    

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField('get_author_username')
    author_email = serializers.SerializerMethodField('get_author_email')
    children = serializers.SerializerMethodField('get_children')
    class Meta:
        model = Comment
        # fields = "__all__"
        fields = ['id', 'text', 'author_username', 'author_email', 'post', 'parent', 'children','created_at', 'updated_at']
    

    def get_author_username(self, instance):
        return instance.author.username
    
    def get_author_email(self, instance):
        return instance.author.email
    
    def get_children(self, instance):
        children = []
        for comment_child in instance.children:
            children.append(model_to_dict(comment_child))
        return children    


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    category = CategorySerializer()
    body = serializers.SerializerMethodField()
    pictures = PictureSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_author_username(self, instance):
        return instance.author.username

    def get_body(self, instance):
        return instance.body.html
    
    # def get_category(self, instance):
    #     return instance.category

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'author', 'title', "category", "tags", 'pictures', 'comments', 'body', 'created_at', 'updated_at']
    
