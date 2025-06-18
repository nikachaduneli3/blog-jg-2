from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(default=18)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(default='not-found.jpg')
    gender = models.CharField(max_length=1, choices={'m': 'male',
                                                      'f': 'female'})
    following = models.ManyToManyField('self', symmetrical=False,
                                       related_name='followers')


class Request(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='received_requests')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='sent_requests')

    def accept(self):
        self.to_user.followers.add(self.from_user)
        self.delete()

    def follow_back(self):
        self.to_user.followers.add(self.from_user)
        self.to_user.following.add(self.from_user)
        self.delete()

    def reject(self):
        self.delete()
