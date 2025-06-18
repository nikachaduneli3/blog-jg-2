from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('activate/<str:uid>/<str:token>', views.activate),
    path('', views.UsersListApiView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('<int:pk>/posts/', views.UserPostsListApiView.as_view()),
    path('<int:pk>/request/', views.send_follow_request),
    path('request/<int:request_pk>/', views.RequestsDetailApiView.as_view()),

]
