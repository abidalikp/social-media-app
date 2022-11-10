from django.urls import path

from social import views

urlpatterns = [
    path('profile', views.Profile.as_view(), name='profile'),
    path('postlike/<pk>', views.PostLike.as_view(), name='postlike'),
    path('postcreate', views.PostCreate.as_view(), name='postcreate'),
    path('postdelete/<pk>', views.PostDelete.as_view(), name='postdelete'),
    path('addfriend/<pk>', views.AddFriend.as_view(), name='addfriend'),
    path('removefriend/<pk>', views.RemoveFriend.as_view(), name='removefriend'),
    path('users', views.Users.as_view(), name='users'),
    path('', views.Wall.as_view(), name='wall'),
]