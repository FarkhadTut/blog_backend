from django.db import models
from django.contrib.auth.models import User
import datetime
import os
# Create your models here.


def get_upload_to(instance, filename):
    # Get the current year and month
    now = datetime.datetime.now()
    year = now.year
    month = now.strftime('%m')  # Zero-padded month
    
    # Define the upload path
    upload_to = os.path.join('profile_pictures', str(year), str(month), filename)
    return upload_to




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=get_upload_to, blank=True, null=True)

    def __str__(self):
        return self.user.username