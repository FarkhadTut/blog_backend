from django.contrib import admin
from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  
    list_display = ['title', 'id', 'created_at', 'updated_at']
    filter_horizontal = ("tags", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):  
    list_display = ['text', 'author', 'post', 'updated_at', 'id']
    
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):  
    list_display = ['name', 'created_at', 'updated_at', 'id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  
    list_display = ['name', 'created_at', 'updated_at', 'id']
    
