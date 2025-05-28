from django.urls import path
from . import views


urlpatterns = [
     path('posts/', views.PostListApiView.as_view()),
     path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyApiView.as_view()),
     path('posts/<int:pk>/like', views.like_post),
     path('posts/<int:pk>/dislike', views.dislike_post),
]
