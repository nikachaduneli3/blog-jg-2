from rest_framework import serializers
from .models import Post, Comment, Tag

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


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()
    publish_date = serializers.DateField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    dislike = serializers.IntegerField(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(),
                                                        write_only=True, allow_null=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'author', 'publish_date',
                  'likes', 'dislike', 'replies', 'parent_comment']
        depth = 1

    def get_replies(self, obj):
        return CommentSerializer(instance=obj.replies, many=True).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'