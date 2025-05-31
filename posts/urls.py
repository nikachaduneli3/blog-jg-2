from django.urls import path
from . import views


urlpatterns = [
     path('posts/', views.PostListApiView.as_view()),
     path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyApiView.as_view()),
     path('posts/<int:pk>/like', views.like_post),
     path('posts/<int:pk>/dislike', views.dislike_post),
     path('posts/<int:post_id>/comments', views.PostCommentsApiView.as_view()),
     path('tags/', views.TagListCreateApiView.as_view()),
     path('tags/<int:tag_id>/posts/', views.TagPostListView.as_view())
]
