from django.urls import path

from social import views

urlpatterns = [
    path('profile', views.Profile.as_view(), name='profile'),
    path('postlike/<pk>', views.PostLike.as_view(), name='postlike'),
    path('addfriend/<pk>', views.AddFriend.as_view(), name='addfriend'),
    path('users', views.Users.as_view(), name='users'),
    path('post', views.Post.as_view(), name='post'),
    path('', views.Wall.as_view(), name='wall'),
]