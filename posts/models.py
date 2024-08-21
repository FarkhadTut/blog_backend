from django.db import models
from users.models import User
import os 
import datetime
from django.utils.deconstruct import deconstructible
# Create your models here.
from django_quill.fields import QuillField

@deconstructible
class PathAndRename(object):
   def __init__(self, base_folder):
       self.base_folder = base_folder

   def __call__(self, instance, filename):
        now = datetime.datetime.now()
        year = now.year
        month = now.strftime('%m')  # Zero-padded month
        upload_to = os.path.join(self.base_folder, str(year), str(month), filename)
        return upload_to

class Tags(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not all([c == c.upper() for c in self.name]):
            self.name = self.name.lower()
        self.name = self.name.strip(" ").strip("#")

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return "#" + self.name

class Category(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not all([c == c.upper() for c in self.name]):
            self.name = self.name.lower()
            self.name = self.name.capitalize()
            self.name = self.name.strip(" ")

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(upload_to=PathAndRename(base_folder='post_thumbnails'))
    title = models.CharField(max_length=512, blank=False, null=False)
    body = QuillField(blank=False, null=False)  
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Picture(models.Model):
    post = models.ForeignKey(to=Post, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=PathAndRename(base_folder='post_pictures'))
    description = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.image.name


class Comment(models.Model):
    text = models.TextField(max_length=10000, null=False, blank=False)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)