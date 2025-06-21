from lib2to3.btm_utils import rec_test

from rest_framework.permissions import BasePermission


class PostViewPermission(BasePermission):

    def has_permission(self, request, view):
        current_user = request.user
        author_id = view.kwargs.get('pk')
        followings_ids = current_user.following.all().values_list('id', flat=True)
        print(current_user)
        print(author_id)
        print(followings_ids)
        return author_id in followings_ids
    # def has_object_permission(self, request, view, obj):


