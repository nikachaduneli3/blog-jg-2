from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import User
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .forms import UserForm

class FollowersInline(TabularInline):
    verbose_name = 'follower'
    verbose_name_plural = 'followers'
    model = User.followers.through
    fk_name = 'to_user'
    extra = 0
    readonly_fields = ['from_user', 'to_user']
    can_delete = False



@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'age', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['profile_image_display']
    form = UserForm
    inlines = [FollowersInline]

    def profile_image_display(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width=400/>')