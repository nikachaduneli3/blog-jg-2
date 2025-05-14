from django.contrib import admin
from .models import Post, Tag, Comment
from .forms import PostForm
from django.utils.html import format_html

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['content', 'author', 'publish_date']
    readonly_fields = ['content', 'author', 'publish_date']

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'tags_rel', 'publish_date', 'published']
    search_fields = ['title', 'author__username']
    list_filter = ['published', 'publish_date']
    form = PostForm
    readonly_fields = ['display_image']
    inlines = [CommentInline]

    def display_image(self, obj):
        if obj.image: return format_html(f'<img src={obj.image.url} width=400/>')
        return ''

    def tags_rel(self, obj):
        return ', '.join([t.name for t in obj.tags.all()])

    tags_rel.short_description = 'tags'

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'publish_date', 'likes', 'dislike']
