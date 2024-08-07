from django.db import models
from users.models import Profile
import os 
import datetime
# Create your models here.

def get_upload_to(*args, **kwargs):

    def func(*args, **kwargs):
        return 
    
    
    return func


@get_upload_to
def get_path(instance, filename):
        # Get the current year and month
    now = datetime.datetime.now()
    year = now.year
    month = now.strftime('%m')  # Zero-padded month
    
    # Define the upload path
    upload_to = os.path.join(base_folder, str(year), str(month), filename)
    return upload_to

class Post(models.Model):
    image = models.ImageField(upload_to=get_upload_to(base_folder='post_thumbnails'))
    title = models.CharField(max_length=512, blank=False, null=False)
    body = models.TextField(blank=False, null=False)  
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Picture(models.Model):
    post = models.ForeignKey(to=Post, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to(base_folder='post_pictures'))
    description = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.image.name


class Comment(models.Model):
    text = models.TextField(max_length=10000, null=False, blank=False)
    author = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)