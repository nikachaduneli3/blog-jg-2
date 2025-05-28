from rest_framework import serializers
from .models import Post, Comment

class PostListSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'likes', 'dislike', 'content','author', 'publish_date', 'image']

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        depth = 1
        fields = ['id', 'title', 'content',
                  'likes', 'dislike',
                  'author', 'publish_date', 'views',
                  'image', 'categories', 'tags']

class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'publish_date',
                          'likes', 'dislike', 'replies']



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'publish_date',
                  'likes', 'dislike', 'replies']
        depth = 1