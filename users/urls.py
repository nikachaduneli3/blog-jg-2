from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('activate/<str:uid>/<str:token>', views.activate)
]
