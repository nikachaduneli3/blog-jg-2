from django.contrib import admin
from .models import User
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserModelAdmin(UserAdmin):

    ...
    # list_display = ['username', 'email', 'age', 'is_active', 'is_staff', 'is_superuser']
#     search_fields = ['email', 'username']
#     list_filter = ['is_active', 'is_staff', 'is_superuser']
#     readonly_fields = ['profile_image_display']
#
#     def profile_image_display(self, obj):
#         if obj.profile_picture: return format_html(f'<img src="{obj.profile_picture.url}" width=400/>')