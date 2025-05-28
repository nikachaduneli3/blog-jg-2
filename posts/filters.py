import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains', field_name='author__username')
    likes_gte = django_filters.NumberFilter(field_name='likes', lookup_expr='gte')
    dislikes_gte = django_filters.NumberFilter(field_name='dislike', lookup_expr='lte')
    published = django_filters.DateFilter()
    published_before = django_filters.DateFilter(field_name='published', lookup_expr='lte')
    published_after = django_filters.DateFilter(field_name='published', lookup_expr='gte')

    class Meta:
        model = Post
        fields = ['title', 'author', 'likes_gte', 'dislikes_gte',
                  'published', 'published_before', 'published_after']

