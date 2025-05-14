from .models import Post, Tag
from django import forms
from django.utils.html import format_html

class PostForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = Post
        fields = ('title', 'content', 'likes', 'dislike', 'publish_date',
                  'author', 'published', 'image', 'tags')


