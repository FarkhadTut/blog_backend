from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
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



class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(blank=True, max_length=30, null=True)
    last_name = models.CharField(blank=True, max_length=100, null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=get_upload_to, blank=True, null=True)


    def __str__(self):
        return self.username