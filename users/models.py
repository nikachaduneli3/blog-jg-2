from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(default=18)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField()
    gender = models.CharField(max_length=1, choices={'m': 'male',
                                                      'f': 'female'})
