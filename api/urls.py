from django import views
from django.urls import path
from . import views


app_name = 'appi'
urlpatterns = [
    path('', views.UserListCreateAPIView.as_view()),
    path('login', views.login_user),
]
