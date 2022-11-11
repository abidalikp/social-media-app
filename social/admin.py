from django.contrib import admin

from social import models

# Register your models here.

admin.site.register([
    models.Friend,
    models.Post,
    models.Like,
    models.Comment,
    models.FriendRequest,
])