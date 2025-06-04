from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from django.db.models import F
from .models import Post, Comment, Tag
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    TagSerializer,
)
from .filters import  PostFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .pagination import PostPagination
from .perrmissions import IsAuthorOrReadOnly


class PostListApiView(ListCreateAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    pagination_class = PostPagination

class PostRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthorOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = F('views')+1
        post.save()
        return super().get(request, *args, **kwargs)
        
@api_view(['POST'])
def like_post(request, pk, *args, **kwargs):
    undo = request.data.get('undo')

    post = Post.objects.get(id=pk)
    if undo:
        post.likes = F('likes') - 1
    else:
        post.likes = F('likes') + 1

    post.save()
    return Response({'message': 'success'}, status=200)

@api_view(['POST'])
def dislike_post(request, pk, *args, **kwargs):
    undo = request.data.get('undo')

    post = Post.objects.get(id=pk)
    if undo:
        post.dislike = F('dislike') + 1
    else:
        post.dislike = F('dislike') - 1

    post.save()
    return Response({'message': 'success'}, status=200)


class PostCommentsApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        return res.filter(post_id=post_id, parent_comment=None)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        publish_date = timezone.now().date()
        serializer.save(post_id=post_id, publish_date=publish_date)

class TagListCreateApiView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagPostListView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        tag = Tag.objects.get(id=tag_id)
        return tag.posts.all()
