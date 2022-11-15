from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Functions for models.

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return '%s/%s.%s' % (instance.user.username, uuid4().hex, ext)

# Create your models here.

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)
    content = models.TextField()
    image = models.ImageField(blank = True, upload_to=upload_to)

    def __str__(self):
        return '{} - {}'.format(self.user.first_name, self.content[:50])

    def delete(self):
        self.image.delete()
        super().delete()

class Like(models.Model):

    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete = models.CASCADE)

class Comment(models.Model):

    content = models.CharField(max_length = 1024)
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE)

class Friend(models.Model):

    person1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person1')
    person2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person2')

    def __str__(self):
        return "{} - {}".format(self.person1.first_name, self.person2.first_name)

class FriendRequest(models.Model):

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    requestee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requestee')

    def __str__(self):
        return "{} - {}".format(self.requester.first_name, self.requestee.first_name)
    