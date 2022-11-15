from django import forms

from social import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['user']

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['content', 'image']

class FriendForm(forms.ModelForm):
    class Meta:
        model = models.Friend
        exclude = []

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']