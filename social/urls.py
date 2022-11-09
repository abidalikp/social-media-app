from django.urls import path

from social import views

urlpatterns = [
    path('profile', views.Profile.as_view(), name='profile'),
    path('users', views.Users.as_view(), name='users'),
    path('post', views.Post.as_view(), name='post'),
    path('', views.Wall.as_view(), name='wall'),
]