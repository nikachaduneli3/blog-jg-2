from django.db import models
from django.utils import timezone
from django.conf import settings
from .validators import (
    validate_for_restricted_symbols,
    validate_for_restricted_words,
    validate_future_date
)

class Post(models.Model):
    title = models.CharField(max_length=255, validators=[validate_for_restricted_symbols,
                                                         validate_for_restricted_words])
    content = models.TextField(validators=[validate_for_restricted_words])
    likes = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    publish_date = models.DateField(default=timezone.now, validators=[validate_future_date])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='posts/')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    categories = models.ManyToManyField('Category', related_name='posts')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self): return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, validators=[validate_for_restricted_words])
    color = models.CharField(max_length=20,
                             choices={'gray':'gray', 'orange':'orange',
                                      'yellow': 'yellow', 'blue':'blue',
                                      'cyan':'cyan', 'red': 'red',
                                      'purple': 'purple'},
                             default='gray'
                             )

    def __str__(self): return self.name

class Comment(models.Model):
    content = models.TextField(validators=[validate_for_restricted_words])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    publish_date = models.DateField(default=timezone.now, validators=[validate_future_date])
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies',
                                       null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self): return self.content[:15]


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories',
                                       null=True, blank=True)
    def __str__(self): return self.name

    class Meta:
        verbose_name_plural  = 'categories'


