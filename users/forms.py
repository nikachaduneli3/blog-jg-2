from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin import widgets
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.forms import UserChangeForm
from .models import User


class UserForm(UserChangeForm):

    user_permissions = ModelMultipleChoiceField(
        required=False,
        widget=widgets.FilteredSelectMultiple('Permission', is_stacked=False),
        queryset= Permission.objects.all(),
    )
    groups = ModelMultipleChoiceField(
        required=False,
        widget=widgets.FilteredSelectMultiple('Group', is_stacked=False),
        queryset=Group.objects.all(),
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'age',
                  'address', 'gender', 'profile_picture',
                  'is_staff', 'is_active', 'is_superuser',
                  'groups', 'user_permissions']