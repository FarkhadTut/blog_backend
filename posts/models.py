from django.db import models
import os 
import datetime
# Create your models here.

def get_upload_to(instance, filename):
    # Get the current year and month
    now = datetime.datetime.now()
    year = now.year
    month = now.strftime('%m')  # Zero-padded month
    
    # Define the upload path
    upload_to = os.path.join('post_pictures', str(year), str(month), filename)
    return upload_to





class Post(models.Model):
    title = models.CharField(max_length=512, blank=False, null=False)
    body = models.TextField(blank=False, null=False)    
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)



class Picture(models.Model):
    post = models.ForeignKey(to=Post, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to)
    description = models.CharField(max_length=512, blank=True, null=True)


    def __str__(self):
        return self.image.name
