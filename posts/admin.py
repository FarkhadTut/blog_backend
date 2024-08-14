from django.contrib import admin
from .models import *
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  
    list_display = ['id', 'title', 'body', 'created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):  
    list_display = ['id', 'text', 'author', 'post', 'updated_at']
    