from django.contrib import admin
from django.urls import reverse

from .models import Post, Tag, Comment, Category
from django.utils.html import format_html
from .forms import PostForm


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['content', 'author', 'publish_date']
    can_delete = False
    readonly_fields = ['content', 'author', 'publish_date']


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_link', 'tags_rel', 'categories_rel', 'publish_date', 'published']
    search_fields = ['title', 'author__username']
    list_filter = ['published', 'publish_date']
    readonly_fields = ['display_image']
    inlines = [CommentInline]
    form = PostForm

    def author_link(self, obj):
        link = reverse('admin:users_user_change', args=[obj.author.id])
        return format_html(f'<a href={link}>{obj.author.username}</a>')

    def display_image(self, obj):
        if obj.image: return format_html(f'<img src={obj.image.url} width=400/>')
        return ''

    def tags_rel(self, obj):
        res = ''
        for t in obj.tags.all():
            res += f'<span style="border-radius: 50px; background-color: {t.color}; margin: 5px; padding:5px;">{t.name}</span>'
        return format_html(res)

    def categories_rel(self, obj):
        res = ''
        for c in obj.categories.all():
            res += f'<span style="border-radius: 50px; background-color: grey; margin: 5px; padding:5px;">{c.name}</span>'
        return format_html(res)

    categories_rel.short_description = 'categories'
    tags_rel.short_description = 'tags'

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'publish_date', 'parent_comment','likes', 'dislike']

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']


